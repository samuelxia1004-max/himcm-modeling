---
name: himcm-modeling
description: "HiMCM 专用数学建模工作流（v7.1）。收到 HiMCM A/B 题、附件、团队方案或论文时使用：真实数据扎根、按主张类型验证、独立批评、可执行的交付门槛（check_gate.py）、英文论文与 PDF 交付。"
---

# HiMCM mathematical modeling (v7.1)

目标：一份真实数据扎根、每个子问都有结果、核心结论经过能推翻它的检验、篇幅 18–25 页（内部目标，见第 9 条）的英文报告。内部门槛不预测奖项。

## v7.1 的规则：交付由脚本判定，不由自己打勾判定

- 唯一的完成判定：`python scripts/check_gate.py PROJECT --pdf final/TEAM.pdf`。
  - 退出码 0 = GATE_PASS，可以交付（数学和原创性仍需批评者与人工把关）。
  - 1 = GATE_FAIL，2 = GATE_INCOMPLETE：**不得称为完成**。时间用完时只能作为 PARTIAL 交付，并把每条失败写进 `PROJECT_CONTEXT.md` 的 "Known gaps"，同时写进 AI 使用报告。
- 开工就运行 `python scripts/init_project.py PROJECT --year Y --problem A|B`。它会生成 `artifacts/gate.json`、`data/source_log.md`、`artifacts/review/critic.md` 的模板，边做边填，不要最后补。
- 进程卫生：只在自己的项目目录和项目内 scratch 里工作，**不用公共 /tmp**；不删除任何文件，包括自己的临时渲染。旧版本改名保留。

## 时间预算（按总时长比例，可按题调整，调整要记在 PROJECT_CONTEXT.md）

| 阶段 | 比例 | 到点必须有的产物 |
|---|---|---|
| 读题、附件、截止线、gate.json 的 requirements | 10% | 每个子问一行；附件已核对文件类型 |
| 取数与来源日志 | 20% | source_log.md 覆盖关键参数 |
| 构思、基线、主模型 | 30% | **50% 时：完整初稿骨架（全部章节）+ 基线结果** |
| 验证与灵敏度 | 20% | **75% 时：第一次运行 check_gate.py** |
| 写作、批评、返修 | 20% | 批评者问题全部关闭，gate 通过 |

拿不到数据时：按预设额度换合法来源、收缩目标或标 BLOCKED，不无限搜索，也不用合成数据冒充题给材料。

## 必做核心清单

1. **读题与截止线。** 逐条读题面和全部附件，把每个子问写进 `gate.json` 的 `requirements`。记录比赛日期截止线：之后发布的数据、事件、文献不得用于输入、校准或验证；确需引用的，在正文和 source_log 标 "post-contest, context only"（gate 会拦截"post-contest 却用于校准/验证"）。
2. **附件逐字使用。** 题给地图、表格、数据、图片原样转成模型输入，转换过程和误差记在 `data/attachments_log.md`，并在 `gate.json` 的 `attachments` 里写明被哪个子问使用（或为什么用不上）。先检查文件真实类型：下载失败的 HTML 页面伪装成 xlsx 时 gate 会失败。镜像副本要核对内容；找不到官方附件就标 BLOCKED_INPUT，**不得用合成数据代替**。
3. **真实数据采集与来源日志。** 每个外部检验（external_holdout / external_check / development_holdout）用到的数据都要在 source_log 里有一行，Use 写 validation（开发集可写 calibration），并在 gate.json 的该检验里填 `source_log_match`（该行中的一段原文）；后补的检验数据也一样。 关键参数都先找真实来源，记入 `data/source_log.md`（列：Parameter｜Value｜Class｜Use｜Source/URL/accessed｜Note）。Class ∈ observed / attachment / external / estimated / assumed；Use ∈ input / calibration / validation / context。假设必须给理由和范围，并进灵敏度分析。**禁止凭记忆填数并写成事实**；`[unverified]` 只是缺口标签，决定性事实不能靠它免责——换来源、改为假设或收缩结论。
4. **独立构思。** 在看任何同题解答之前写 `artifacts/independent_ideas.md`：一个最便宜的基线 + ≥3 个候选思路（新机制、新指标、跨领域类比、决策者需要的延伸）。按"能否被数据检验、能否改变决策"选一个作为本文的核心贡献，在摘要中说清它是什么。命名可选。
5. **建模与求解。** 假设表要有"理由/证据"列。先手算小例和基线，再跑正式模型；优化结果独立复算可行性和目标值；随机方法报告多次运行的波动。增强模型若不优于基线，保留基线或说明增强多回答了什么。
6. **合理性检查。** 关键输出对照守恒、量纲、单调性、极端情形和历史观测范围，写进 `artifacts/plausibility.md`。违反守恒或硬约束必须修模型；超出历史范围要先判断是错误、参数失效、超出适用域还是有依据的外推，再决定修改或标注，不能机械截断。
7. **按主张类型验证（写进 gate.json 的 claims 和 validations）。** 先列摘要里的 3–6 条核心主张，标类型，再为每条选一项**能推翻它**的检验，**在看结果前登记**：
   - 预测 / 经验效应：用未参与拟合和选模的截止线前真实数据做留出或外部对照，并和朴素基线比较（上一期值、持续性、均值、单一变量排序等）。看过留出结果后再改模型，这个留出集就降为 `development_holdout`，需要新数据或在正文写明"开发验证"。
   - 优化：独立复算约束和目标、小规模精确解或界、与现行方案或简单启发式比较。
   - 机理 / 规范 / 偏好类：量纲、极端情形、反例、一致性，再加决策翻转边界；没有真实结果数据时写 `no_independent_data_reason`，并在正文明说未经实证。
   - 检验失败时必须处置：`repair`（修机制后用新数据再测）、`restrict_scope`（收缩结论）或 `withdraw`，并在正文写出来。**不得在测试集上调参直到通过，也不得隐藏失败。**
   - **选择层不碰留出集。** 偏好打分、加权、阈值、"推荐哪一个"等任何选择步骤只用设计期数据。看过留出结果后才提出的规则（例如"设计时把阈值收紧一档，实际才能达标"），会让该留出集变成开发集；要在**另一份从未用过的截止线前数据**上先登记、再检验（写进 validation_plan 的追加条目），否则只能写成探索性建议。
   - **基线对比要有方向。** 每个外部检验填 `metric_direction`（lower_is_better / higher_is_better）。模型输给预登记基线时 gate 会警告 `MODEL_LOSES_TO_BASELINE`；正文必须明说（填 `baseline_loss_excerpt`），并说明模型多回答了什么（例如成本更低），不能只写"通过阈值"。
   - **指标要对得上用户关心的量。** 比例或年度总量（如"满足 99% 的需求总量"）不等于时间或事件口径（未满足的小时数、次数、最长持续时间）；平均误差不等于极端误差。结论用哪种口径，就报告哪种；两种都相关时都报告。
   - 灵敏度：说明哪些参数会改变推荐，以及翻转点在哪里。
   - 前向测试的证据：有截止线前真实数据检验、且讲清检验范围的论文，胜过没有检验的论文；诚实失败本身不加分，处置得当才加分。
8. **实施覆盖清单。** 逐项回答：谁来执行、时间表、成本按科目拆分、风险与应急预案、利益相关方与公平性、推广沟通、监测指标与更新机制；不适用的写一句理由。建议的优先级同时考虑效果、可控性、成本和风险，不能只按灵敏度大小排。
9. **写作与篇幅。** 结构：Summary Sheet → 目录 → 问题重述 → 假设与理由 → 数据 → 模型 → 结果 → 验证/灵敏度 → 实施与建议 → 优缺点 → 题目要求的信件/文章 → 参考文献。
   - **篇幅：** 主报告 18–25 页是内部目标（不得超过当届上限）。低于 18 页 gate 会失败，除非批评者在 critic.md 写 `SHORT_EXCEPTION_APPROVED: <理由>`，说明已无可增加的实质证据。
   - **不凑字数的扩写顺序：** 缺失的子问答案 → 关键推导与手算例 → 参数来源与可辨识性 → 更强的基线对比 → 误差分解与失败案例 → 改变结论的边界条件 → 实施成本与取舍 → 必要的推广/迁移。禁止空页、加大行距、重复图表、堆附录。
   - **摘要页：** 最后写；必须完整落在第 1 页，字号 ≥12 pt（gate 用 `summary_last_text` 检查是否溢页）；每个子问给出关键数字和单位；写清验证做了什么、结果如何（包括失败）。摘要中的核心主张要和 `claims` 一致。
   - 每个子问至少"模型 + 结果图表 + 解释"；所有正文字号 ≥12 pt；每页有队号和页码，不出现姓名或学校。
   - **排版与字号自检。** 用自己的模板渲染（例如 pandoc 自定义 HTML 模板 + `@page` 页眉 + 无头浏览器打印，或 LaTeX），关闭"缩放以适应页面"；第一稿就跑 `check_pdf.py` 看有没有 <12 pt 的正文（表格和图注按当届规则判断）。图片设最大高度（例如 3.1 in），避免大图被挤到下一页留下半页空白：gate 用内容覆盖率检查半空页（图片也算），≥3 页低于 60% 会失败；确需整页留白的页（如信件、文章必须单独成页）在 `pdf.short_page_reasons` 写理由。
   - **摘录用正文原句。** gate 会统一弯引号、连字符断行、Markdown 强调符号，但仍以 PDF 文字为准；改稿后重跑 gate，失败信息会提示从第几个字符起对不上。
10. **独立批评（必做，有复审证据）。** 批评者默认是**全新会话的 Codex**（例如 `codex exec` 新开一次，长任务放 screen）；没有 Codex 时用另一个模型或子代理，只给题面、附件和 PDF，不给笔记。提示词模板：`assets/critic_prompt_template.md`；critic.md 模板：`assets/critic_template.md`。
    - 第 1 轮：≥5 条问题，优先找最可能推翻结论的问题（未被检验的核心主张、留出集被重用、截止线、附件没用上、摘要强于正文证据、数字与代码输出不一致）。每条写 位置｜证据｜Severity｜最小修复。
    - 第 2 轮起：新会话逐条给 `N. … | Verdict: FIXED / NOT FIXED`，再列新的高严重度问题。
    - critic.md 每轮写一行 `Round: K | critic: … | fresh_session: yes | pdf_sha256: … | raw: <批评者原始输出路径>`；原始输出不改动，开头由批评者自己写出它读到的 PDF 的 sha256。
    - 关闭方式：`Status: FIXED (verified round K)`（第 K 轮原始输出里该条必须是 `Verdict: FIXED`）、`Status: FIXED_UNREVIEWED`（自己改了但没复审，gate 警告）、`Status: WONTFIX <理由>`。引用的轮次写着 NOT FIXED 却标 FIXED，gate 失败。
    - **最后一轮必须审的是最终 PDF**（gate 比对 sha256）。最后一轮之后再改 PDF，就要再开一次新会话做简短复核。不设轮数上限，但每轮要计入时间预算。
    - 高严重度问题不能修就撤回或收缩相关结论。
11. **交付核查。** 引用要么核验过（打开过，标题作者年份对得上，发表于截止线前），要么标 `[unverified]`。依次运行：
    ```bash
    python scripts/check_pdf.py final/TEAM.pdf --team TEAM --main-pages N --max-main-pages CAP
    python scripts/check_gate.py PROJECT --pdf final/TEAM.pdf
    ```
    然后附上当届要求的 AI 使用报告（新起一页）。gate 输出保存到 `artifacts/review/gate_result.json`。

## 当届规则

开始前先读 [contest-rules.md](contest-rules.md)，并尽量查看当届 COMAP 官方说明，把页数上限写进 `gate.json` 的 `rules.max_main_pages`，同时填 `rules.rules_year`（必须等于截止日期所在年份）和 `rules.rules_source`（页数规则出自哪里，引一句原文）。某年规则把参考文献、附录等排除在页数之外时，用 `rules.excluded_from_cap` 逐项写明：`rule_quote`（当年规则原句，必填）、`first_text`（起始原文）、`last_text` 或 `"to_end": true`；gate 按当年规则计页，锚点找不到或不唯一不会默认排除。默认为空列表。`pdf.main_pages` 必须填；不填时 gate 用 AI 报告标题自动识别并警告，识别不到就不做页数判定（INCOMPLETE）。2026 年的快照：选 A 或 B；英文 PDF；字号 ≥12 pt；摘要为第一页；主报告 ≤25 页（目录、参考文献、信函、附录都计入）；AI 使用报告附在后面，不计页；匿名；文件 <20 MB。比赛期间不得接受队外的人为帮助，不得做调查访谈，不得公开传播赛题或方案。复盘旧题时用当年的规则。

## 可选插件（只在触发条件成立时做；不做不扣分）

细则和模板见 [o-paper-practices-v6.md](o-paper-practices-v6.md)，但其中的固定页码、数量、句式一律只作参考。

| 插件 | 触发条件 |
|---|---|
| 总览流程图（子问→模型→输出） | 三个以上模型之间有真实的数据依赖 |
| 模型耦合表 | 子问之间确有输出→输入关系；不强造关系 |
| 基础版→增强版差值 | 增强机制是本文核心贡献 |
| 分组建模 | 有异质性证据且每组样本足够 |
| 情景集 / 冲击情景 | 结论依赖不可控的外部条件；情景必须真正计算 |
| 迁移到第二个真实对象 | 论文声称可推广，或题目要求 |
| 区间 | 量来自估计或随机机制；确定值给误差界即可 |
| 信件 / 备忘录骨架 | 题目要求信件或有明确受众 |
| 与现状对照 | 决策或干预题且现行方案确实存在 |

## 何时读参考资料（按需）

- O/F 作品更好的做法：[o-paper-practices.md](o-paper-practices.md)
- 模型选择：[problem-to-model.md](problem-to-model.md)，[model-atlas.md](model-atlas.md)
- 数据处理：[data-analysis-playbook.md](data-analysis-playbook.md)
- 排名、准入、资源分配类：[decision-contracts.md](decision-contracts.md)
- 验证细节：[validation-review.md](validation-review.md)
- 写作与文风：[paper-and-style.md](paper-and-style.md)
- 获奖作品共同特点：[award-common-traits.md](award-common-traits.md)，[award-thinking.md](award-thinking.md)

## 附录

- v4 完整流程（证据账本、哈希绑定、两轮评审等），时间充裕时用：[full-workflow-v4.md](full-workflow-v4.md)
- 脚本：`init_project.py`（初始化+模板）、`check_gate.py`（交付门槛）、`selftest_gate.py`（门槛自测，用虚构项目）、`check_pdf.py`（格式）、`audit_project.py`（v4 证据结构，可选）、`prose_guard.py`（文风编辑保护，可选）
- 文献学习库：nature-core-*、literature-*、grok-literature-*、*-corpus-lessons.md，只作检索线索
