# CHANGELOG v7（2026-10-18，从 v5 复制后修改；v5、v6 原样保留）

依据：前向盲测 `/workspace/fwd_test/_judge/RESULTS.md`（V5 9-3-2、V6 7-4-3、无 skill 0-3-11；V6 对 V5 2-2-3）、Codex 审阅 `~/himcm_v7_work/codex/REVIEW.md` 与 `ROUND2.md`、计划 `~/himcm_v7_work/PLAN_v7.md`。

## 核心判断
v5/v6 的问题不是缺规则，而是"写了没执行"：22 篇论文里 20 篇低于 18 页，执行者在 PROGRESS 里写明"below 18-page target"后照样标 DONE；v6 有论文 10 页却把 1–10 项全部打勾。v5/v6 的 check_pdf.py 只查上限不查下限。v7 把关键要求改成脚本门槛。

## 改动
1. **新增 `scripts/check_gate.py`（唯一完成判定，退出码 0/1/2）。** 检查：主报告页数（低于 18 页失败，除非批评者写 SHORT_EXCEPTION_APPROVED）、超当届上限、摘要溢出第 1 页（锚文本定位）、AI 报告边界、每个子问的结果/解释摘录确实出现在正文、量化子问有数字、图表编号存在、核心主张与摘要一致并绑定验证、留出集被用于选模则失败、预测类主张没有独立真实数据检验且无理由则失败、失败检验必须有处置并写进正文、附件是 HTML 假文件则失败、post-contest 来源用于输入/校准/验证则失败、假设缺范围、独立构思 ≥3 候选、批评者 ≥5 条问题且全部关闭。
2. **新增 `scripts/selftest_gate.py`**：9 个虚构、与题目无关的用例，全部按预期通过。
3. **`init_project.py` 重写**：生成 gate.json、source_log.md（含 Class/Use 列）、critic.md、independent_ideas.md 模板；不覆盖、不删除已有文件；项目内 scratch，不用 /tmp。
4. **新增 `assets/gate_template.json`。**
5. **SKILL.md**：
   - 交付由 gate 判定；未通过只能标 PARTIAL 并列出 Known gaps。
   - 时间预算表，50% 时必须有完整骨架+基线，75% 时第一次跑 gate。
   - 第 7 条改为"按主张类型验证"：预测类用未参与选模的截止线前数据并对比朴素基线；看过结果再改模型则降为开发验证；失败必须 repair / restrict_scope / withdraw。
   - 第 9 条：18 页内部目标 + 可审查的短稿例外 + 不凑字数的扩写顺序；摘要必须落在第 1 页。
   - 第 10 条：独立批评由可选改为必做。
   - 第 4 条：保留"≥3 个候选思路"，去掉"必须起名字"。
   - 第 6 条：超出历史范围先判断原因，不机械截断。
   - 第 8 条：建议优先级综合效果、可控性、成本、风险，不只按灵敏度。
   - 进程卫生：不用公共 /tmp，不删任何文件。
6. **v6 元素的处理**：15 项 v6 规则全部从"必做"降为"按触发条件启用的插件"（总览图、耦合表、基础→增强、分组、情景、迁移、区间、信件骨架、现状对照）；保留 `references/o-paper-practices-v6.md` 作参考。理由：V6 对 V5 无优势（2-2-3）；V6-2020-A 出现"命名了但没计算"的情景；V6-2018-A 增强模型在留出集不如简单基线。
7. **参考库换成 v6 清理后的版本**（17 个文件），v5 原件移入 `../quarantine_v7/v5_reference_originals/`。Codex 发现 v5 的 corpus-index.json 有 8 条封存题条目（v6 已清理），这是 V5-vs-V6 比较的混杂因素。另外在 `himcm-corpus-lessons.md` 中隔离了 2 处含封存题队号的子句（`../quarantine_v7/removed.jsonl`，原件在 `../quarantine_v7/originals/`）。

## 泄漏检查（2026-10-18）
- 结构化 JSON（year+problem 字段）、文本"年份+题号"、12 个封存题队号、主题词三种扫描：剩 1 条命中，是"GISS-E2"中的子串误报。
- 用 v6 的主题词表扫描：剩余命中与 v6 记录相同（biodiversity 文献标题、bottleneck、2013-B/2022-B），人工判断保留。新增的 SKILL.md、脚本、模板零命中。
- 扫描脚本：`/workspace/v7_work/leakscan_v7.py`；结果：`/workspace/v7_work/leakscan_v7_final.tsv`。

## 尚未做
v7 未经前向测试，不能声称它提高了分数。封存 8 题已被用于诊断 v5/v6 的输出（但没把题目内容写进 skill），对 v7 只能当回归集，不能当未见确认集。
