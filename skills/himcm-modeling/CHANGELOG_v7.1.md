# CHANGELOG v7.1（2026-10-18，从 v7 复制后修改；v7 原样保留）

依据：v7 低成本预试（2 道回归题，记录见 `/workspace/fwd_test/V7_PROGRESS.md` 与各项目 `PROJECT_CONTEXT.md`）。两篇都拿到 GATE_PASS，但暴露出 gate 可被绕过或误报的地方：批评者复审证据缺失、模型输给预登记基线仍"pass"、摘录逐字匹配被弯引号/连字符断行卡住等。v7.1 只改门槛与说明，不改建模方法。

## 改动（对应预试报告的 9 条建议）
1. **批评复审证据（check_gate.py）。** critic.md 每轮写 `Round: K | critic | fresh_session | pdf_sha256 | raw`。`Status: FIXED` 必须写 `(verified round K)`，且该条**最新**一轮的原始裁决为 `Verdict: FIXED`，否则记为 FIXED_UNREVIEWED（警告）；最新裁决是 NOT FIXED → 失败。原始输出里提出的每条问题（含后续轮的新问题）都必须在 critic.md 有对应编号 → 否则失败；Status 不在编号问题下、编号重复 → 失败。**最后一轮必须审最终 PDF**：sha256 不符 → 失败；每轮原始输出前 5 行必须有批评者写的 `pdf_sha256:` 且与 critic.md 一致 → 否则失败；fresh_session 不是 yes → 失败；没有 Round 行 → INCOMPLETE。新增 `assets/critic_template.md`、`assets/critic_prompt_template.md`（默认用全新会话的 Codex）。
2. **摘录归一化。** NFKC、弯引号→直引号、各种破折号/减号→连字符、软连字符（Arial 会把断行连字符抽成 U+00AD）、成对的 Markdown 强调符号；字母之间的连字符（词内或断行）两边都去掉，其他断行连字符只去空格（"8- layer"→"8-layer"）。数字区间、减号、标识符保留："10-20"≠"1020"，"x−3"≠"x3"，"a_b"≠"ab"，"-3.2"≠"3.2"。少于 10 个字符的摘录视为缺失。匹配失败时提示从第几个字符起对不上。
3. **independent_ideas "Chosen" 正则。** 取 Chosen 行的第一个冒号，内容可以在同行或紧接的下一行（空行之后的文字不算）；不再被行内多个冒号误判。
4. **main_pages。** 填了就和 AI 报告标题核对（不符 → 失败）；没填就按 "Report on Use of AI" 自动识别并警告；都没有 → INCOMPLETE，且**不再用总页数做页数判定**（v7 会把 AI 页算进主报告，使 17 页的稿子逃过 18 页下限）。
5. **按年份的页数规则。** 新增 `rules.rules_year`（必须等于截止日期年份，不符 → 失败）、`rules.rules_source`（规则出处）、`rules.excluded_from_cap`（默认空；每项必须有 `rule_quote` 当年规则原句，否则失败；`first_text` 起始原文，加 `last_text` 或显式 `to_end: true`；锚点找不到/不唯一 → INCOMPLETE 且不排除；首尾颠倒 → 失败）。check_pdf.py 去掉写死的 25 页上限，改为 `--max-main-pages`。init_project.py 自动填 rules_year。
6. **半空页（含图片页）。** 按页面内容覆盖率（文字、图片、矢量绘图，去掉页眉页脚带）判定；<60% 记半空页（第 1 页摘要除外，主报告最后一页也计入），1–2 页警告，≥3 页失败；确需留白的页在 `pdf.short_page_reasons` 写理由，被豁免的页单独列出警告供审阅。阈值用预试稿子校准：一份因大图挤页造成的稿子 4 页被抓到（0.51–0.56），两份最终稿 0–2 页被提示。旧的 THIN_PAGES 词数检查删除（对数字密集的表格页误报）。
7. **模型输给预登记基线 → 警告。** 外部检验必须填 `metric_direction`（缺 → INCOMPLETE）；model_value / baseline_value 必须是有限数字（字符串、NaN、布尔 → INCOMPLETE）；模型劣于基线时警告 MODEL_LOSES_TO_BASELINE，并检查正文是否用 `baseline_loss_excerpt` 说明（空字符串不算）。
8. **验证数据必须进来源日志。** 每个 external_holdout / external_check / development_holdout 填 `source_log_match`（字符串或列表，每个数据集一条；缺 → INCOMPLETE）；找不到 → 失败；匹配多行 → INCOMPLETE；该行 Use 不含整词 validation（开发集可为 calibration）或含 not/no → 失败；data_source 与匹配行没有共同词 → 警告。
9. **SKILL.md 文字。** 第 3 条（验证数据进日志）、第 7 条（选择层不碰留出集；看过留出后提出的规则须在新数据上先登记再检验；基线方向与输给基线要写明；比例口径 ≠ 时间/事件口径）、第 9 条（自定义渲染模板、关闭缩放、字号自检、图片限高、摘录说明）、第 10 条（全新会话 Codex 批评、Round 行、verified round K、最后一轮审最终 PDF、不设轮数上限）、当届规则一节（rules_year / rules_source / excluded_from_cap / main_pages）。

## 自测
- `selftest_gate.py` 从 9 个用例扩到 53 个：保留 v7 的 9 个，每条修复都有正反用例，另加归一化单元检查和 check_pdf 无硬上限检查。夹具用 Unicode 字体渲染弯引号（box: DejaVuSans；Mac: Arial）。
- 结果：box 与 Mac 均 `SELFTEST PASS (53 cases)`（Codex 审阅前为 40 例，审阅后加 13 例对应其发现的绕过方式）。Mac 首跑暴露一个真实问题：Arial 把断行连字符抽取成软连字符（U+00AD），已改归一化规则。
- v7 gate 对照（同一批夹具）：归一化、Chosen 冒号两例 v7 误判；半空图片页、输给基线、验证源缺日志、未复审 FIXED、批评没审最终 PDF、规则年份不符，v7 全部放行（GATE_PASS）。
- 真实回放（预试的一篇论文，复制到 scratch 后补齐新字段）：v7.1 抓到——最后一轮批评审的不是最终 PDF、一条批评被标 FIXED 而复审写 NOT FIXED、旧批评原始输出没有 sha256 头、一个验证源匹配到两行；并警告模型输给预登记基线、2 条未复审 FIXED。预试两篇原项目在 v7.1 下为 GATE_INCOMPLETE（缺新字段），未改动原项目。

## 泄漏检查
- 用 `/workspace/v7_work/leakscan_v7.py`（结构化 JSON、年份+题号文本、封存队号、主题词）扫描 v7.1：4 条命中，与 v7 当前扫描**逐行相同**（均在 v7 原有文件中），新增内容零命中。SKILL.md 新增例子已改为与具体题目无关的说法。结果：`/workspace/fwd_test/V7_scratch/leakscan_v71.tsv`。

## 外部审阅
- Codex（Mac，screen `v71review`，全新会话，只读 diff 并在 scratch 里做对抗测试）一次审阅：`~/himcm_v7_work/review_v71/REVIEW.md`（box 副本 `/workspace/fwd_test/V7_scratch/codex_review_v71/REVIEW.md`）。结论：40 例自测全过，但找到绕过方式；fix 3/4/9 OK，fix 1/2/5/6/7/8 有问题。
- 已处理：
  - 批评按编号对账、用最新裁决、原始新问题必须入账、bullet/孤立 Status 失败、结构化 sha256 头。
  - 归一化不再吞掉数字区间/减号/下划线标识符。
  - 页数排除必须引用规则原句、末锚点缺失不默认到结尾、首尾颠倒失败。
  - 半空页检查包含最后一页；豁免页单独警告。
  - 基线值必须是有限数字，空披露不算。
  - source_log 匹配支持列表、拒绝多行歧义、Use 整词匹配并排除 not、data_source 不相似时警告。
  - Chosen 内容不跨空行；AI 报告标题须在页首 200 字符内；失败提示逐字符定位。
- 未处理（记录在案）：
  - 作者仍能伪造原始批评文件、fresh_session 声明和 sha256（门槛只能查一致性，不能证明来源）。
  - short_page_reasons 的理由质量靠人审。
  - 内部 18 页下限仍按"计入上限的页"算（更严格）。
  - 覆盖率按竖向区间，空白图片或零散排版可能误判。
  - 基线数值没有和预登记文件做哈希绑定。

## 尚未做
- v7.1 未经前向测试；只证明门槛按设计工作，不能声称提高分数。
- 门槛仍不能证明批评者真的是独立会话（sha256 与原始输出可以伪造，但会留下可查的伪造痕迹）。
