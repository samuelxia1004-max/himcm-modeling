# 有固定截止的运行：逐阶段观察与命令保护

首次实际UTC与原截止只保存一次，用带时区ISO的 `start_utc`、`deadline_utc`；可附一致的 `budget_seconds`。立即保存该文件原SHA-256，后续都使用同一哈希。工具只核它与该哈希一致，不能证明原时钟来自可信服务，也不能阻止同时伪改文件和预期哈希。原预算包含阅读、思考、工具、独评等待和封包。

有总截止时，在开始写作/编译、派发或等待独评、返修、复现、封包前，以及长工具返回后，执行下列 `check`，用唯一新目录留记录。它记录此刻，不授权之后无限时工作。拒绝或过期就停止新增科学工作，保全已有稿和缺项为PARTIAL；保全的实际时刻另记，不倒填截止前完成。

```bash
python -B /path/to/skill/scripts/phase_guard.py check \
  --clock ORIGINAL_CLOCK.json --expected-clock-sha256 ORIGINAL_SHA256 \
  --attempt artifacts/phases/001-before-review --stage before-review
```

普通同步计算、渲染或复现命令用 `run` 包裹，不只在前面写一条检查后无期限执行。`--cap-seconds`可限制本命令，不能延长原截止。每次失败也换新目录，不覆盖。

```bash
python -B /path/to/skill/scripts/phase_guard.py run \
  --clock ORIGINAL_CLOCK.json --expected-clock-sha256 ORIGINAL_SHA256 \
  --attempt artifacts/phases/002-compute --stage compute --cwd PROJECT \
  --cap-seconds 120 -- python -B code/solve.py
python -B /path/to/skill/scripts/phase_guard.py verify artifacts/phases/002-compute \
  --expected-manifest-sha256 RECEIVED_MANIFEST_SHA256
```

相对命令路径按 `--cwd` 解释；钟和attempt路径按调用者目录解释。`check`的退出0只表示观察时尚未截止；`run`的退出0仅表示命令返回0、观察时仍在原截止且原钟未改，不证明输出正确或完整。124是拒启/截止/单命令超时，2是错误/命令失败/钟变化。原命令返回码另存，原stdout/stderr和时序均保留。未形成FREEZE的目录仍保留为中断现场，不算通过。

此工具只支持POSIX普通进程组，不是沙箱或硬实时保证。独立新会话的子进程可脱离该组；`build_archive.py`就是另开会话的构建器，必须给其自身适当的 `--timeout`（小于检查时原剩余时间并预留归档），外层guard不能替它终止脱离的编译器。完整构建来源和每次失败仍按[构建归档](build-archive.md)保存。模型思考、外部评委API、主机暂停与被终止的guard都不能被此工具可靠抢占；这些等待仍算原预算，返回后检查原钟。未知间隔原因继续记未知。

父级不代作者读钟、派评委或恢复流程。检查工具的数值或日志不是数学、idea、独立评审或完整作品验收分；总截止验收仍由完整实际产物和真实时钟判断。
