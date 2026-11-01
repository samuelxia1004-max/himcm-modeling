# 来源与工作流适配记录

本组参考是 HiMCM 建模、验证和论文审阅的队内工具。官方要求、评委经验和本地建议在正文分开标注。包内相对路径以本参考目录为基准；contest-profile.json 的快照路径以安装技能根目录为基准。论文原件保存在单独交付的研究库中，安装包使用官方链接与包内阅读索引，运行不依赖研究库。当届官方规则和适用 AI 政策决定提交要求，历年评论与技能提供经验和流程。原技能绝对路径只用于创建来源清点，不是运行依赖；迁移后的规则已写入本包。

## 官方材料

| 实际文件 | 采用内容与定位 |
|---|---|
| `official/rules_2026.txt`，同名 HTML | IV：A/B 选题、独立团队工作、来源和 AI 披露；VI：建模建议、英文 PDF、首页摘要、25 页、至少 12 点、页眉匿名、控制号文件名、小于 20 MB、单文件提交 |
| `official/AI_policy.txt`，同名 PDF，v102025 | 第 1 页：覆盖研究、代码、翻译及嵌入 AI，使用责任；第 2 页：正文与参考引用、附后报告、示例中的准确输入／完整输出及纯翻译例外 |
| [2025 Consortium 130](https://www.contest.comap.org/highschool/contests/himcm/flyers/Cons_HiMCM.pdf)，公开原件 | 文件正文是 2025 HiMCM、Consortium 130；第 2 至 3 页：高中数学与评审；第 5 至 12 页：摘要、理解、假设、选择、实施、连贯性、敏感性、非技术文本、图表、引用；第 16 页起为 2025 Example Appendix |

页码采用 PDF 实际页，TXT 的 `=== PDF PAGE n ===` 标记可定位；期刊印刷页与 PDF 页有差异。范例仅支持对应文章的具体观察，不能推出通用模型胜率或奖项保证。2025 案例和评论中的方法名称用于解释问题结构；2026 题目发布后重新建立约定。

## 建模主技能

已完整读取以下主文件，并采用其可迁移的事实与验证边界：

| 技能文件 | 适配到本组参考的内容 |
|---|---|
| `math-modeling-solver/SKILL.md` | 题意约定、独立候选先于完整方案、结构驱动选模、正式评价器、风险驱动反证、结果证据与最优性声明 |
| `math-modeling-paper/SKILL.md` | 当前结果到正文的绑定、模型与结果叙事、引用使用位置、摘要后写、真实 AI 记录 |
| `math-modeling-finalizer/SKILL.md` | 冻结、审阅、最小修复、受影响内容复查、行为回归和实际 PDF 检查 |
| `mathskills/SKILL.md`、`mathskills/skills/registry.yaml` | 规范名称与阶段路由、原始输入保护、基准、失败导向验证、复现和最终一致性 |

## 全部 16 个规范子技能

已完整读取以下 `mathskills/skills/<名称>/SKILL.md`。表中“采用”指参考流程吸收该原则；具体项目仍按需要启用。

| 名称 | 采用或条件用途 |
|---|---|
| workflow-orchestration | 一个产物一个事实源，任务合同和状态 |
| plan-and-execution | 输入、输出、依赖、验收与停止条件 |
| data-analysis | 单位、缺失、异常、清洗记录和泄漏检查 |
| jupyter-live-analysis | 探索后干净重跑，正式结果转为可复现脚本 |
| sql-data-analysis | 有数据库时核查键、连接倍增和汇总口径 |
| literature-evidence | 外部主张对应实际来源和使用范围 |
| model-deliberation | 实质不同候选、失效方式和改变选择的条件 |
| validation-and-robustness | 统一比较协议、反证、敏感性和失败记录 |
| measured-experiment-loop | 需要迭代实验时先设指标、独立正确性检查及预算 |
| scientific-visualization | 图表任务、冻结数据、单位和视觉复核 |
| academic-writing | 主张与证据、符号和结果一致性 |
| national-award-paper-style | 问题匹配结构、图表说明和来源索引；赛事格式改用 HiMCM 当前规则 |
| academic-translation | 保留数字、方程、方向、术语和声明强度 |
| research-presentation | 需展示时沿用同一证据链；不增设竞赛提交要求 |
| reproducibility-audit | 干净复算、相对路径和跨产物一致性 |
| academic-humanization | 一次受控编辑、技术事实保护和改后核对 |

## 全部 6 个收口子技能

已完整读取 `math-modeling-finalizer/skills/<名称>/SKILL.md`：

| 名称 | 采用内容 |
|---|---|
| modeling-behavior-refactor | 代码简化后验证正式结果和约束保持 |
| modeling-solution-auditor | 稿件、结果、引用和剩余风险交叉检查 |
| modeling-repair-regression | 按证据定位修复范围并复查下游 |
| modeling-abstract-finalizer | 当前摘要对照当前结果及正文 |
| modeling-paper-compressor | 页数超限或有压缩需求时保留核心证据 |
| modeling-delivery-gate | 匿名、格式、AI 披露及实际 PDF 全页检查 |

## 表达技能与整合方式

已完整读取 `humanizer/SKILL.md`、`stop-slop/SKILL.md`、`anti-defensive-writing/SKILL.md`、`no-negative-echo/SKILL.md`、`humanize/SKILL.md`。采用具体表达审查、完整句子、正向范围、真实限制及最终文稿独立可读的原则。数学精度和官方披露优先；这些技能在一个编辑回合中各司其职，规范子技能的别名不重复作为独立流程执行。

`no-negative-echo` 的生产方法按正向目标生成标题、正文和交付说明，再完整读回核查。若使用独立生产与验证上下文，宿主需确认其上下文模式；可读回检查支持已检查表面的结论。AI 报告属于读者必需的真实记录，编辑时保护。

## HiMCM 适配决定

CUMCM 模板、中文论文习惯、固定文献数量、固定实验数量及特定摘要字数均属来源技能中的场景或默认建议。HiMCM 使用当前官方英文 PDF 和页数规则。验证深度由最大剩余风险决定；简单题用手算、解析和直接复算即可，复杂问题再增加有区分度的实验。

技能中的 DOCX、ZIP 和内部台账用于编辑及本地复现。2026 HiMCM 只接收指定 PDF，程序、软件、数据库和其他文件不进入评审提交；AI 报告随 PDF 附后。两轮内部评审和诊断表属于本地质量检查，官方没有在所读材料中给出可供这些表使用的数字评分权重。

当前技能包的主入口、参考文件与脚本提供可执行流程。实际项目保存题面版本、采用路线、正式结果、测试记录和最终 PDF 复核证据；历史演练不能替未来项目宣告通过。

## 本次完整技能的额外适配

本次另核对了 math-modeling-growth 与 cumcm-latex-paper 主文件：采用以真实阶段产物复盘、从题意和运行证据还原论文的方法，HiMCM 的语言、页数、提交方式、限制披露由当前规则决定。nature-math-modeling-writing 的基准对比、消融、计算成本和可复现性提供写作线索；其场景字数与内部语料统计不作为本 skill 的实测结论。nature-literature-pipeline 的标题/DOI 去重与阅读深度标签用于本次证据库；下载与核验记录保持真实访问状态。

`source-skill-inventory.json` 清点 100 份本地技能文档，其中包含规范子技能、兼容别名和参考副本，不能把此数解释为 100 项独立能力或全部逐行人工精读。每个文件保留来源路径、描述和 SHA-256。实际完整读取与采用范围由上表和当前研究记录说明，兼容别名归并到规范能力。

## 正刊主库与扩展文献

第一阶段文献按DOI去重后为Nature正刊100篇（其中25篇正文段落摘读、75篇摘要阅读）和子刊80篇扩展，共180篇。包内nature-core-index.json列出主库100个精确题名/DOI；nature-core-learning.md提供新增80篇原创学习卡，原20篇及子刊80篇在literature-learning.md。获取状态、稿本版本、阅读深度与HiMCM迁移推断分别记录。原件、元数据、访问/修复过程在单独交付的研究库；安装包无需该库即可使用。

Grok补充文件先按字节哈希与队号去重，再重新取得COMAP主来源、映射实际源页并阅读。最终HiMCM语料为121篇四方面报告选读及47队节选；作品奖级按官方结果行保留历史名称。新增28队例文、2024评委评论与3份补全报告的分析见[grokbot-corpus-lessons.md](grokbot-corpus-lessons.md)。

Grok期刊补充49篇Nature Communications Article及2篇方法评论经出版商/Crossref/PDF身份交叉核对并实际段落阅读；与原180篇去重后共231个DOI。7个原记录稿本按版本关联，不新增论文。N047/N050为已有PDF的字节重复；N074已有PMC正文；N001/N070/N097/N098提供新正文来源。N001/N097/N098为预印本，具体定量结论须核对发表版。新增模型、验证、边界与迁移问题见grok-literature-learning.md。

## 本机技能的进一步学习

本次进一步完整读取15份Nature相关与15份其他研究/统计/写作入口，并重读建模核心、规范子技能与收口模块；兼容别名归并到实际工作流。新增测量有效性、竞争解释、统计单位、公平比较、引用支撑与图注/评审规则，见[local-skill-learning.md](local-skill-learning.md)。具体读取范围和当前源哈希保存在validation/local-skills-nature-reading.json及validation/local-skills-research-reading.json。文档整合不扩大此前合成案例的验证范围。

## 历史题演练与本次互补

冻结v2与原版mathskills各取得11道官方历史题的完整首次产物，保留22份快照。最初计划另含2014-B，但两臂均在取得产物前被平台过滤器中止，未计完成。执行期间有容量中断、模型切换和从各自文件恢复；它们不是同一模型恒定预算的受控试验。用户另要求的6.1 sol/high、0–1三臂实验属于后续独立研究。

最终v3吸收原版的实体归并、独立求解、硬准入与条件建议、分组验证、运行与资金尺度，以及新稿的独立构思覆盖、简洁主线、机制消融、翻转阈值和下游结果绑定。两套共同出现的同址资源与强必要性范围、单套的计数代理、别名实体与配对伪数据问题，分别归入decision-contracts.md与data-analysis-playbook.md；动态积分和新增净资源账本的经验也迁移为机制检查。按需要调用，不能把某个旧题参数或答案当通用规则。

全部首次产物、独立复算、反馈后修订与最终v3前向验证在交付的研究记录中分开列出。修订使用了根反馈，原v2的整题演练不能自动当作最终v3已完成相同的全程重跑，也不能证明消除了所有缺点。每项结果仍须保留测试范围和反例。
