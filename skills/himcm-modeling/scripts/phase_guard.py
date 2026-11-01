#!/usr/bin/env python3
"""POSIX command deadline guard; local evidence, not a sandbox or scientific gate."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time


def now():
    return datetime.now(timezone.utc)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(data):
    return json.loads(data, object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON: ' + value)))


def write_new(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError('Clock timestamp must be an aware ISO string')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('Naive timestamp is forbidden')
    return parsed.astimezone(timezone.utc)


def read_clock(raw):
    clock = load_json(raw)
    if not isinstance(clock, dict):
        raise ValueError('Clock must be an object')
    start, deadline = timestamp(clock['start_utc']), timestamp(clock['deadline_utc'])
    duration = (deadline - start).total_seconds()
    if duration <= 0:
        raise ValueError('Deadline must be later than original start')
    if 'budget_seconds' in clock:
        budget = clock['budget_seconds']
        if isinstance(budget, bool) or not isinstance(budget, (int, float)) or not math.isfinite(budget) or abs(budget - duration) > 1e-6:
            raise ValueError('Original budget and endpoints disagree')
    return start, deadline


def inventory(root):
    files = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Evidence symlink is forbidden: ' + str(path))
        if path.is_file():
            raw = path.read_bytes()
            files[path.relative_to(root).as_posix()] = {'sha256': sha(raw), 'bytes': len(raw)}
    return files


def verify(root, expected):
    raw = (root / 'FREEZE.json').read_bytes()
    manifest = load_json(raw)
    current = inventory(root)
    current.pop('FREEZE.json', None)
    return {'valid': sha(raw) == expected and manifest['files'] == current,
            'manifest_sha256': sha(raw), 'external_binding_checked': True,
            'scope': 'Integrity relative to supplied hash only; no trusted time, authenticity, science, or completeness approval.'}


def guard(clock_path, expected, attempt, stage, cwd, command, cap):
    if os.name != 'posix':
        raise ValueError('This prototype supports POSIX process groups only')
    if not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('Expected clock SHA256 must be 64 lowercase hex characters')
    if cap is not None and (not math.isfinite(cap) or cap <= 0):
        raise ValueError('Command cap must be finite and positive')
    if not stage.strip() or not cwd.is_dir():
        raise ValueError('Nonempty stage and existing working directory required')
    # A fresh directory is required even for a failed or expired invocation.
    attempt.mkdir(parents=True, exist_ok=False)
    entry = now()
    tick = time.monotonic()
    request = {'mode': 'run' if command else 'check', 'stage': stage, 'entry_utc': entry.isoformat(),
               'clock_path': str(clock_path), 'expected_clock_sha256': expected,
               'command': command, 'cwd': str(cwd), 'cap_seconds': cap,
               'runner_sha256': sha(Path(__file__).read_bytes()),
               'scope': 'Only commands launched here are bounded. A check receipt is not permission for later unguarded work. External LLM/API waits, detached processes, external writes and guard termination are not controlled.'}
    write_new(attempt / 'request.json', request)
    result = {'status': 'REJECTED', 'command_launched': False, 'command_returncode': None,
              'command_exit_observed_utc': None, 'stop_reason': None, 'error': None,
              'process_group_cleanup_sent': False, 'clock_unchanged_at_finish': False,
              'command_finished_within_observed_deadline': False,
              'scientific_or_overall_pass': None}
    process, raw, deadline = None, None, None

    def event(name, **values):
        value = {'event': name, 'observed_utc': now().isoformat(),
                 'elapsed_monotonic_seconds': time.monotonic() - tick, **values}
        with (attempt / 'events.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n')

    def clock_matches():
        try:
            return not clock_path.is_symlink() and sha(clock_path.read_bytes()) == expected
        except OSError:
            return False

    event('entry')
    try:
        if clock_path.is_symlink():
            raise ValueError('Original clock symlink is forbidden')
        raw = clock_path.read_bytes()
        (attempt / 'original-clock.json').write_bytes(raw)
        if sha(raw) != expected:
            raise ValueError('Original clock SHA256 mismatch')
        start, deadline = read_clock(raw)
        result.update(original_start_utc=start.isoformat(), original_deadline_utc=deadline.isoformat())
        pre = now()
        if pre < start:
            raise ValueError('Original clock start is in the future; no reset or wait')
        remaining = (deadline - pre).total_seconds()
        event('precheck', remaining_seconds=remaining)
        if remaining <= 0:
            result.update(status='SKIPPED_DEADLINE', stop_reason='deadline_already_elapsed')
        elif not command:
            result['status'] = 'CHECK_ONLY_WITHIN_DEADLINE'
        else:
            # Recheck after disk writes, immediately before spawn. This is not a hard-real-time scheduler.
            if not clock_matches():
                raise ValueError('Original clock changed before spawn')
            launch_time = now()
            remaining = (deadline - launch_time).total_seconds()
            if remaining <= 0:
                result.update(status='SKIPPED_DEADLINE', stop_reason='deadline_elapsed_before_spawn')
            else:
                launch_tick = time.monotonic()
                monotonic_deadline = launch_tick + remaining
                cap_deadline = launch_tick + cap if cap is not None else math.inf
                result.update(launch_observation_utc=launch_time.isoformat(),
                              remaining_at_launch_seconds=remaining)
                with (attempt / 'stdout.log').open('xb') as stdout, (attempt / 'stderr.log').open('xb') as stderr:
                    try:
                        process = subprocess.Popen(command, cwd=cwd, stdout=stdout, stderr=stderr,
                                                   start_new_session=True)
                        result.update(command_launched=True, pid=process.pid)
                        event('spawned', pid=process.pid)
                        while True:
                            wall, mono = now(), time.monotonic()
                            returncode = process.poll()
                            if not clock_matches():
                                result.update(status='CLOCK_CHANGED', stop_reason='original_clock_changed')
                                break
                            if wall >= deadline or mono >= monotonic_deadline:
                                result.update(status='DEADLINE_EXCEEDED', stop_reason='original_deadline_elapsed')
                                break
                            if mono >= cap_deadline:
                                result.update(status='COMMAND_TIMEOUT', stop_reason='command_cap_elapsed')
                                break
                            if returncode is not None:
                                result.update(status='COMMAND_OK' if returncode == 0 else 'COMMAND_FAILED',
                                              command_exit_observed_utc=wall.isoformat(),
                                              command_finished_within_observed_deadline=True)
                                break
                            time.sleep(min(0.05, (deadline - wall).total_seconds(), monotonic_deadline - mono,
                                           cap_deadline - mono))
                    finally:
                        # Kill ordinary descendants even after a successful parent exit; intentionally
                        # detached children can escape. This utility is not a security boundary.
                        if process is not None:
                            try:
                                os.killpg(process.pid, signal.SIGKILL)
                                result['process_group_cleanup_sent'] = True
                            except ProcessLookupError:
                                pass
                            process.wait()
                            result['command_returncode'] = process.returncode
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as error:
        result.update(status='REJECTED' if not result['command_launched'] else 'EXECUTION_ERROR',
                      error=repr(error))
    result['clock_unchanged_at_finish'] = raw is not None and clock_matches()
    finish = now()
    result.update(finished_utc=finish.isoformat(), elapsed_monotonic_seconds=time.monotonic() - tick,
                  original_deadline_remaining_at_finish_seconds=(deadline - finish).total_seconds() if deadline else None)
    if result['status'] in ('COMMAND_OK', 'CHECK_ONLY_WITHIN_DEADLINE'):
        if not result['clock_unchanged_at_finish']:
            result['status'] = 'CLOCK_CHANGED'
        elif finish >= deadline:
            result['status'] = 'DEADLINE_EXCEEDED'
    event('finished', status=result['status'])
    write_new(attempt / 'result.json', result)
    write_new(attempt / 'FREEZE.json', {'frozen_utc': now().isoformat(), 'files': inventory(attempt)})
    result['manifest_sha256'] = sha((attempt / 'FREEZE.json').read_bytes())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='mode', required=True)
    for name in ('check', 'run'):
        sub = subs.add_parser(name)
        sub.add_argument('--clock', type=Path, required=True)
        sub.add_argument('--expected-clock-sha256', required=True)
        sub.add_argument('--attempt', type=Path, required=True)
        sub.add_argument('--stage', required=True)
        sub.add_argument('--cwd', type=Path, default=Path.cwd())
        if name == 'run':
            sub.add_argument('--cap-seconds', type=float)
            sub.add_argument('command', nargs=argparse.REMAINDER)
    ver = subs.add_parser('verify')
    ver.add_argument('attempt', type=Path)
    ver.add_argument('--expected-manifest-sha256', required=True)
    args = parser.parse_args()
    try:
        if args.mode == 'verify':
            result = verify(args.attempt.resolve(), args.expected_manifest_sha256)
            code = 0 if result['valid'] else 2
        else:
            command = getattr(args, 'command', [])
            command = command[1:] if command[:1] == ['--'] else command
            if args.mode == 'run' and not command:
                raise ValueError('run requires a nonempty argv after --')
            result = guard(args.clock.absolute(), args.expected_clock_sha256, args.attempt.absolute(),
                           args.stage, args.cwd.resolve(), command, getattr(args, 'cap_seconds', None))
            code = 0 if result['status'] in ('COMMAND_OK', 'CHECK_ONLY_WITHIN_DEADLINE') else (124 if result['status'] in ('SKIPPED_DEADLINE', 'DEADLINE_EXCEEDED', 'COMMAND_TIMEOUT') else 2)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return code
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'REJECTED_OR_PARTIAL_RETAINED', 'error': repr(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
