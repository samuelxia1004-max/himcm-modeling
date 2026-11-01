# 本机建模相关技能：长处与HiMCM适配

本次学习覆盖数学建模核心、16个规范子技能、6个收口子模块，以及15份Nature相关和15份其他研究/统计/写作入口。来源文档清点共100份，含兼容别名和技能创建辅助文件；它们不是100项独立能力。主入口完整阅读、别名归并及保留的先前读取分别标记在[source-skill-inventory.json](source-skill-inventory.json)。引用的全部资产和参考文件不自动计作已读。

| 能力 | 吸收的具体长处 | 本技能中的行动 |
|---|---|---|
| 独立建模 | math-modeling-solver、model-deliberation、hypothesis-generation先澄清对象和表示，比较实质不同的机制 | 先保存独立构思；把目标概念落实为可观测变量；候选解释配预测及区分测试 |
| 数据与统计 | data-analysis、nature-data/statistics、statistical-analysis区分单位、依赖、估计对象和不确定性 | 记录清洗与信息时点；检验代理指标、泄漏与伪重复；用匹配设计的区间及比较 |
| 验证与实验 | validation-and-robustness、measured-experiment-loop、Nature建模写作强调可信对比和可复验贡献 | 匹配基线信息、约束和预算；记录实现版本；围绕主要风险检验敏感性、简化对照和切换条件 |
| 引用与文献 | literature-evidence、nature-citation/ref-verifier、citation-management区分书目身份和内容支撑 | 核验题名/DOI/版本及真实支撑位置；保留部分、背景和相反证据；访问失败保持未核验 |
| 科学写作与图表 | math-modeling-paper、scientific-writing、nature-writing/figure用证据组织论证 | 每段承担一个任务；关键结果给条件、基线、差值和单位；图注明确单位、重复数和区间含义 |
| 评审与复现 | math-modeling-finalizer、reproducibility-audit、peer-review/nature-reviewer追踪事实和最小返修 | 数字回链当前证书；问题保留编号和解决测试；改动后复验受影响链并检查实际PDF |
| 自然表达 | academic-humanization、academic-humanizer、humanizer、stop-slop、ultimate-de-ai保护内容再改文字 | 一个受控编辑回合，保护公式、数字、因果强度、来源及真实AI披露；复用术语表 |
| 复盘与成长 | math-modeling-growth从真实决策、失败和证据提炼下一步 | 记录可复用的失败模式、改变建议的条件与下一次可验收的行动 |

本次进一步补入关键概念的测量规则与代理边界、竞争解释检验、等价拟合对决策的影响、基线实现与公平预算、独立统计单位和成对差异、书目/支撑双层核验、图注口径及稳定评审编号。具体规则分布在problem-to-model、model-atlas、validation-review和paper-and-style中。

来源中的固定词数、标题命名、图数、全模块消融、公共代码仓库、国赛中文/Word模板和固定审阅人数按HiMCM任务适配。简单确定性模型使用解析、小例和边界证据；随机模型报告相应重复与波动。当届官方规则决定英文PDF、摘要、页数、匿名与AI披露。来源技能的语料百分比是其自述，本次未独立复算，未当作本研究库统计或获奖预测依据。

误差条的重叠本身不决定成对差异是否受支持；登记服务404本身不证明DOI错误；拟合相同的参数组合也可能给出不同建议。重要的是这些区别怎样改变本题的验证和决策。

此前两个合成案例验证保持其原范围。冻结v2已进入12题双臂真实完整解答比较；当前v3吸收初次产物中已确认的范围、实体身份和误差传递问题。各题完成状态及模型切换记录在独立验证包，未完成题不计入通过数；v2结果不能冒称后续v3已复测，更不等于获奖效果验证。
