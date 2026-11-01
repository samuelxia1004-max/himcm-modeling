# 当届规则与 2026 快照

核验日期：2026-10-12。主办方原文优先于培训网站、历史论文与本 skill 的默认建议。

| 项目 | 已核验 2026 规则 | 主要依据 |
|---|---|---|
| 题目 | HiMCM A/B 任选一题；C 为 MidMCM | Instructions VI |
| 开始 | 2026-11-04 15:00 EST，即北京时间 11-05 04:00 | Instructions VI |
| 停止修改 | 2026-11-17 20:00 EST，即北京时间 11-18 09:00 | Instructions VI |
| 提交截止 | 2026-11-17 21:00 EST，即北京时间 11-18 10:00 | Instructions VI 提交节 |
| 报告 | 一个英文 PDF，字号至少 12 pt | Preparing a Solution Document |
| 页数 | 一页 Summary Sheet + 至多 24 页；目录、引用、信函、附录计入 | Preparing a Solution Document |
| AI | 正文引用和参考文献披露；其后附 Report on Use of AI Tools，不计入 25 页 | AI policy v102025 |
| 匿名 | 每页队号和页码；不出现本队学生、指导者、学校身份 | Instructions IV/VI |
| 文件 | 队号.pdf，小于 20 MB；一个提交表单一份 PDF | After the Contest — NEW for 2026 |
| 代码 | 不随正式 PDF 单独提交代码、软件、数据库等文件 | Instructions VI |

2026 官方页仍有少数旧年份句子与旧式“send”措辞。日期采用当届日期区与明确写为 2026 的停止/提交节；渠道采用标注 NEW for 2026 的在线提交说明。保存原文中的冲突与解决依据，不把整页视为无矛盾。

规则来源：

- [COMAP Instructions](https://www.contest.comap.org/highschool/contests/himcm/instructions.html)
- [COMAP AI policy](https://www.contest.comap.org/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)
- [历届题目与结果](https://www.contest.comap.org/highschool/contests/himcm/previous%20problems.html)
- [2025 官方评委文章与示例](https://www.contest.comap.org/highschool/contests/himcm/flyers/Cons_HiMCM.pdf)

AI 台账至少包含实际工具/模型、版本或访问日期、用途、输入与输出记录、采用位置、团队核验和修改。按当届政策整理要求的 Query/Output；翻译类例外按原文执行。保护无关个人信息与凭据，保存完整本地历史。不得编造团队核验或回忆中不存在的交互。

官方 Finalist 定义强调完整、逻辑、组织、清楚与综合性；Outstanding 是终审中的相对最高水平。官方评委说明开放题没有唯一答案或单一答案表；复杂数学仅在适用、能解释时有价值。Skill 中的选题分数、页数分配、审阅轮次和验证预算均是本地建议。


## 逐年份计页登记

`pdf.main_pages` 是实际 AI 报告起点之前的正文页数。它与 `total_pages` 和当年 `counted_pages` 分别记录，不能自动把后附 AI 报告视为豁免。`rules.ai_report_excluded_from_main_limit` 用真正 JSON 布尔值；缺省或 false 时，物理总页数扣除当年有原文及锚点支持的其它豁免。只有目标年份官方规则明确排除 AI 报告时才设 true，并在 `rules.ai_report_exclusion_rule_quote` 写出原文，和 rules_year、rules_source、已知截止年份一致。后来年份的豁免不能倒推历史。未知或无法取得原文时保留缺口；默认计入避免擅加豁免，不证明历史政策已经完整恢复。

当前快照中2026的AI豁免属于有来源的具体规则；历史训练需重新按原题核验。2022-B这次训练的AI记录计入25总页，2024-A原题则明确AI报告不计入25页。references/appendix等其它例外仍依当年原文和实际PDF锚点登记。门槛只能检查登记一致性，不能独立认证引用的规则真实有效。
