#!/usr/bin/env python3
"""Append-only scientific build snapshots. No sandbox or scientific validity claim."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import signal
import subprocess
import sys
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_new(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def inventory(root):
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('Symlink cannot be archived as regular evidence: ' + str(p))
        if p.is_file():
            result[p.relative_to(root).as_posix()] = {'sha256': digest(p), 'bytes': p.stat().st_size}
    return result


def relative(raw):
    p = PurePosixPath(raw)
    if not raw or p.is_absolute() or '..' in p.parts or str(p) == '.' or '\\' in raw:
        raise ValueError('Artifact must be a nonempty relative POSIX path without ..')
    return str(p)


def verified(attempt, expected_manifest_sha256=None):
    manifest_sha256 = digest(attempt / 'FREEZE.json')
    manifest = json.loads((attempt / 'FREEZE.json').read_text())
    current = inventory(attempt)
    current.pop('FREEZE.json', None)
    expected = manifest['files']
    return {'valid': current == expected and (expected_manifest_sha256 is None or expected_manifest_sha256 == manifest_sha256),
            'external_manifest_binding_checked': expected_manifest_sha256 is not None,
            'missing': sorted(set(expected) - set(current)),
            'extra': sorted(set(current) - set(expected)),
            'changed': sorted(k for k in set(current) & set(expected) if current[k] != expected[k]),
            'manifest_sha256': manifest_sha256}


def run_build(source, attempt, artifacts, command, timeout=None):
    source, attempt = source.resolve(), attempt.resolve()
    if not source.is_dir() or source == attempt or source in attempt.parents or attempt in source.parents:
        raise ValueError('Source and new attempt must be disjoint directories')
    if not command or (timeout is not None and timeout <= 0):
        raise ValueError('Nonempty command and positive timeout required')
    artifacts = [relative(p) for p in artifacts]
    if len(set(artifacts)) != len(artifacts):
        raise ValueError('Duplicate artifact path')
    before = inventory(source)
    stale = [name for name in artifacts if (source / name).exists()]
    if stale:
        raise ValueError('Requested build artifacts already exist in source; stage source-only inputs and keep prior products in their own archives: ' + ', '.join(stale))
    # mkdir without exist_ok intentionally rejects reuse, including failed builds.
    attempt.mkdir(parents=True, exist_ok=False)
    started = utc()
    tick = time.monotonic()
    write_new(attempt / 'request.json', {
        'utc': started, 'source': str(source), 'source_files': before,
        'command': command, 'cwd': 'workspace', 'timeout_seconds': timeout,
        'expected_artifacts': artifacts, 'runner_sha256': digest(Path(__file__)),
        'scope': 'Copies source then runs command in a separate workspace. This is not an OS sandbox. Absolute command paths, network and external writes are not confined by this tool.'})
    # Keep immutable pre-execution sources even if the command changes its own copy.
    shutil.copytree(source, attempt / 'source')
    if inventory(attempt / 'source') != before or inventory(source) != before:
        raise ValueError('Source changed during snapshot; partial attempt retained, not frozen')
    shutil.copytree(attempt / 'source', attempt / 'workspace')
    returncode, error, timedout, group_cleanup = None, None, False, False
    process = None
    with (attempt / 'stdout.log').open('xb') as stdout, (attempt / 'stderr.log').open('xb') as stderr:
        try:
            process = subprocess.Popen(command, cwd=attempt / 'workspace', stdout=stdout,
                                       stderr=stderr, start_new_session=True)
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            timedout, error = True, str(e)
        except OSError as e:
            error = repr(e)
        finally:
            # POSIX: remove remaining members of this dedicated process group before freezing.
            # Deliberately detached processes and external writes are outside this utility.
            if process is not None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                    group_cleanup = True
                except ProcessLookupError:
                    pass
                process.wait()
                if returncode is None:
                    returncode = process.returncode
    found = {}
    for name in artifacts:
        p = attempt / 'workspace' / name
        found[name] = {'present': p.is_file(), 'sha256': digest(p) if p.is_file() else None}
    source_unchanged = inventory(source) == before
    result = {'started_utc': started, 'finished_utc': utc(),
              'elapsed_seconds_monotonic': time.monotonic() - tick,
              'returncode': returncode, 'timeout': timedout, 'execution_error': error,
              'process_group_cleanup_sent': group_cleanup,
              'artifacts': found, 'source_unchanged': source_unchanged,
              'command_succeeded_and_artifacts_present': returncode == 0 and all(x['present'] for x in found.values()),
              'scientific_or_layout_pass': None,
              'note': 'A generated PDF may fail layout/science. An absent artifact after compilation failure is recorded honestly. No award or completeness score.'}
    write_new(attempt / 'result.json', result)
    write_new(attempt / 'FREEZE.json', {'frozen_utc': utc(), 'files': inventory(attempt)})
    assert verified(attempt)['valid']
    return dict(result, archive_manifest_sha256=digest(attempt / 'FREEZE.json'))


def select(attempt, artifact, output, receipt, expected_manifest_sha256):
    attempt, output, receipt = attempt.resolve(), output.resolve(), receipt.resolve()
    if output == receipt or output.exists() or receipt.exists():
        raise ValueError('Output and receipt must be distinct new paths')
    if attempt in output.parents or attempt in receipt.parents:
        raise ValueError('Selection must not modify frozen attempt')
    check = verified(attempt, expected_manifest_sha256)
    if not check['valid']:
        raise ValueError('Frozen attempt changed: ' + json.dumps(check))
    artifact = relative(artifact)
    result = json.loads((attempt / 'result.json').read_text())
    item = result['artifacts'].get(artifact)
    if result['returncode'] != 0 or not item or not item['present']:
        raise ValueError('Selection requires successful command and registered present artifact')
    origin = attempt / 'workspace' / artifact
    # Exclusive creation prevents silently overwriting an earlier final version.
    with origin.open('rb') as src, output.open('xb') as dst:
        shutil.copyfileobj(src, dst)
    if digest(output) != item['sha256']:
        raise ValueError('Copied artifact hash mismatch; partial selection retained')
    record = {'selected_utc': utc(), 'attempt': str(attempt), 'artifact': artifact,
              'artifact_sha256': item['sha256'], 'attempt_FREEZE_sha256': check['manifest_sha256'],
              'output': str(output), 'science_or_layout_approval': 'Not provided by this utility; select only after actual review.'}
    write_new(receipt, record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    run = sub.add_parser('run')
    run.add_argument('--source', type=Path, required=True)
    run.add_argument('--attempt', type=Path, required=True)
    run.add_argument('--artifact', action='append', required=True)
    run.add_argument('--timeout', type=float)
    run.add_argument('command', nargs=argparse.REMAINDER)
    ver = sub.add_parser('verify')
    ver.add_argument('attempt', type=Path)
    ver.add_argument('--expected-manifest-sha256')
    sel = sub.add_parser('select')
    sel.add_argument('--attempt', type=Path, required=True)
    sel.add_argument('--artifact', required=True)
    sel.add_argument('--output', type=Path, required=True)
    sel.add_argument('--receipt', type=Path, required=True)
    sel.add_argument('--expected-manifest-sha256', required=True)
    args = parser.parse_args()
    try:
        if args.mode == 'run':
            command = args.command[1:] if args.command[:1] == ['--'] else args.command
            result = run_build(args.source, args.attempt, args.artifact, command, args.timeout)
            exitcode = 0 if result['command_succeeded_and_artifacts_present'] and result['source_unchanged'] else 2
        elif args.mode == 'verify':
            result = verified(args.attempt, args.expected_manifest_sha256)
            exitcode = 0 if result['valid'] else 2
        else:
            result = select(args.attempt, args.artifact, args.output, args.receipt, args.expected_manifest_sha256)
            exitcode = 0
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return exitcode
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({'error': str(e), 'status': 'REJECTED_OR_PARTIAL_RETAINED'}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
