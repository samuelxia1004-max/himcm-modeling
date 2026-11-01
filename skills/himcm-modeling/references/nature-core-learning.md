# Nature正刊建模文献学习参考（80篇）

本参考为100篇正刊主清单中的新增C001–C080共80篇Nature正刊原始研究：47篇Article、33篇Letter。题名、DOI与出版社页面及Crossref记录逐项核对。80篇完整摘要已阅读，其中22篇另有指定正文段落摘读，58篇为摘要阅读。

`ABSTRACT_REVIEWED`表示完整摘要阅读；`FULL_TEXT_SECTION_REVIEWED`表示摘要及所列正文段落摘读。包内 [nature-core-index.json](nature-core-index.json) 列出100篇正刊身份与阅读范围。原20篇N001–N020的学习卡见 [literature-learning.md](literature-learning.md)。逐段定位对应单独交付研究库的 `text/Cxxx_sections.json`（从1开始计数）；运行本skill不依赖该研究库。本文方法、验证与范围信息均按实际阅读层次表达。

每篇“迁移（推断）”是面向HiMCM的适配研究假设，应结合题目数据重新定义状态、目标、约束与检验。“验证问题”是应用该思路时建议提出的检查。具体参数、公式和定量结果应回查原文及关联更正。年份取Crossref首次出版日期，可能与卷期纸本年不同。

1. **C001 — Acceleration of global warming due to carbon-cycle feedbacks in a coupled climate model**
   Nature（2000；Letter） · [DOI](https://doi.org/10.1038/35041539) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用耦合气候—碳循环模型表达陆地与海洋吸收能力对环境变化的反馈。
   - 迁移（推断）：校园碳核算可将排放、吸收与环境反馈分别设为动态项，再比较固定与动态吸收情景。
   - 验证问题：加入反馈后，参数范围和初始状态变化能否改变长期趋势？
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

2. **C002 — Protecting the global ocean for biodiversity, food and climate**
   Nature（2021；Article） · [DOI](https://doi.org/10.1038/s41586-021-03371-z) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。

   - 迁移（推断）：保护区布局可建多目标空间选择模型，比较地区单独规划与协同规划。
   - 验证问题：统一预算和目标后，方案在不同权重及地区约束下是否仍有效？
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

3. **C003 — Diagnosing destabilization risk in global land carbon sinks**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-05725-1) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：结合反演、监测与植被模型，区分碳吸收均值、波动及自相关的变化。
   - 迁移（推断）：生态稳定性题可同时检验状态水平、波动和记忆性，避免用单一指标判定风险。
   - 验证问题：改变时间窗口或趋势处理后，稳定性指标是否仍指向相同风险？

4. **C004 — Quantifying climate loss and damage consistent with a social cost of carbon**
   Nature（2026；Article） · [DOI](https://doi.org/10.1038/s41586-026-10272-6) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Climate modelling，段落19；另见逐篇阅读审计。
   - 方法启发：把排放来源、气候响应与非线性经济损害连接，区分过去损害与未来延续损害。
   - 迁移（推断）：碳决策题可逐时累计环境影响，分别展示历史与未来成本的核算边界。
   - 验证问题：损害关系、贴现和时间边界改变时，方案排序如何变化？
   - 来源附注：讨论区分抽样、模型选择及政策约定不确定性；贴现、期限与损害关系影响核算。

5. **C005 — Quantifying the uncertainty in forecasts of anthropogenic climate change**
   Nature（2000；Letter） · [DOI](https://doi.org/10.1038/35036559) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用历史温度及多个气候模型响应共同约束未来升温范围，并区分短期与平衡响应。
   - 迁移（推断）：预测题可用观测约束模型集合，再检验近程预测与长期外推的不同不确定来源。
   - 验证问题：模型误差持续或随时间变化时，观测约束的预测范围是否仍可靠？

6. **C006 — Quantifying global soil carbon losses in response to warming**
   Nature（2016；Letter） · [DOI](https://doi.org/10.1038/nature20150) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：汇集增温实验，建立初始土壤碳与响应的经验关系，再进行全球外推。
   - 迁移（推断）：环境核算题可按初始储量分层估计响应，并将实验尺度与应用尺度分开核验。
   - 验证问题：更换外推尺度、响应实现时间和样本地区后，结论是否稳定？

7. **C007 — Population dynamics of human helminth infections: control by chemotherapy**
   Nature（1982；Article） · [DOI](https://doi.org/10.1038/297557a0) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用寄生虫种群模型解释年龄相关感染强度，并比较整体与选择性控制。
   - 迁移（推断）：传播题可把感染负担分组，再在有限资源下比较平均分配与重点干预。
   - 验证问题：年龄分组、负担分布及干预执行率变化时，控制效果排序是否改变？

8. **C008 — Equity is more important for the social cost of methane than climate uncertainty**
   Nature（2021；Article） · [DOI](https://doi.org/10.1038/s41586-021-03386-6) · 排序与决策
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：将简化气候模型与综合评估模型组合，比较模型结构、相关参数及公平权重的影响。
   - 迁移（推断）：环境损失评价可并列展示总福利指标与群体分布，检验权重带来的决策变化。
   - 验证问题：模型组合和公平权重变化时，成本排序与地区负担如何变化？

9. **C009 — Mobility network models of COVID-19 explain inequities and inform reopening**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2923-3) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model dynamics，段落21；另见逐篇阅读审计。
   - 方法启发：将分区SEIR动力学与逐时地点访问网络耦合，连接人数、地点拥挤和群体差异。
   - 迁移（推断）：校园传播题可建立区域—活动地点二部网络，用逐时人数和容量约束比较干预。
   - 验证问题：留出时段预测、设备抽样偏差及人数上限变化是否支持同一策略？
   - 来源附注：移动数据不能覆盖全部人群、地点及分区内部异质性；简化传播模型的范围另在讨论说明。

10. **C010 — Global effects of land use on local terrestrial biodiversity**
   Nature（2015；Article） · [DOI](https://doi.org/10.1038/nature14324) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用地理与分类覆盖广的群落数据估计土地利用响应，并投影到未来情景。
   - 迁移（推断）：土地规划题可建立利用强度—生态指标关系，再按情景计算空间影响。
   - 验证问题：留出地区及未来情景中，响应关系是否仍适用，各指标是否一致？

11. **C011 — Magnitude of urban heat islands largely explained by climate and population**
   Nature（2019；Article） · [DOI](https://doi.org/10.1038/s41586-019-1512-9) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用粗粒度模型连接人口、背景气候、蒸散和对流效率，解释城市热岛差异。
   - 迁移（推断）：城市降温题可按水和能量限制建机制模型，比较绿地、反照率及城市布局。
   - 验证问题：模型能否同时解释不同气候区的热岛变化，干预效果对水资源条件是否敏感？

12. **C012 — Global threats to human water security and river biodiversity**
   Nature（2010；Article） · [DOI](https://doi.org/10.1038/nature09440) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：在空间框架中累计多种河流压力并考虑下游影响，联合评价人与生态水安全。
   - 迁移（推断）：水资源题可沿河网累计污染、取水与工程压力，再分开评估服务和生态指标。
   - 验证问题：改变压力权重、上下游传递及技术缓解假设后，优先治理地点是否改变？
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

13. **C013 — Global supply chains amplify economic costs of future extreme heat risk**
   Nature（2024；Article） · [DOI](https://doi.org/10.1038/s41586-024-07147-z) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Simulation module，段落40；另见逐篇阅读审计。
   - 方法启发：耦合气候、健康与投入产出及一般均衡模型，追踪直接损失和供应链间接损失。
   - 迁移（推断）：灾害资源题可把本地停工通过供应网络传播，再比较冗余及替代供给方案。
   - 验证问题：供应替代规则、网络连接和灾害共现变化时，间接损失是否仍可解释？
   - 来源附注：企业产出受库存、主要投入与订单约束；气候模块采用偏差校正及模型集合不确定性分析。

14. **C014 — A global resource allocation strategy governs growth transition kinetics of Escherichia coli**
   Nature（2017；Letter） · [DOI](https://doi.org/10.1038/nature24299) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：在通量平衡条件下把稳态资源配置模型扩展到动态过程，追踪环境切换后的恢复。
   - 迁移（推断）：资源调度题可将平衡约束与配置规则结合，比较静态配置和需求切换后的恢复时间。
   - 验证问题：同一配置规则能否同时解释需求上升、下降及恢复过程？

15. **C015 — Impact of changes in diffuse radiation on the global land carbon sink**
   Nature（2009；Letter） · [DOI](https://doi.org/10.1038/nature07949) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：在全球植被模型中区分直接和散射辐射对光合作用的影响，分析大气变化的间接反馈。
   - 迁移（推断）：碳核算题可把环境驱动分解为总量与构成，检验忽略构成变化的估计偏差。
   - 验证问题：相同总辐射下，改变构成及植被响应会使碳吸收预测变化多少？

16. **C016 — Uncertainty in predictions of the climate response to rising levels of greenhouse gases**
   Nature（2005；Letter） · [DOI](https://doi.org/10.1038/nature03301) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用大量气候模型变体集合探索响应不确定性，并检查与当前观测相容的模型范围。
   - 迁移（推断）：模型选择题可保留多个拟合相近的参数或结构，再比较外推范围及尾部情景。
   - 验证问题：拟合当前数据同样好的模型，在未来情景中是否仍给出相近预测？

17. **C017 — Generation time and temporal scaling of bird population dynamics**
   Nature（2005；Letter） · [DOI](https://doi.org/10.1038/nature03666) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用随机、密度依赖和年龄结构模型拟合鸟类时间序列，按世代尺度比较动态差异。
   - 迁移（推断）：种群题可将年龄结构与环境噪声加入模型，再检验年度和世代尺度的结论。
   - 验证问题：改变时间尺度后，密度调节与环境噪声的相对影响是否保持？

18. **C018 — Scaling behaviour in the dynamics of an economic index**
   Nature（1995；Letter） · [DOI](https://doi.org/10.1038/376046a0) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：分析经济指数变化的分布标度，区分中心行为和尾部分布而非假定全范围同一规律。
   - 迁移（推断）：需求波动题可分别拟合常见变化与极端变化，比较不同时间聚合尺度的风险。
   - 验证问题：留出年份与聚合尺度变化时，分布中心和尾部能否同时被解释？

19. **C019 — Indirect radiative forcing of climate change through ozone effects on the land-carbon sink**
   Nature（2007；Letter） · [DOI](https://doi.org/10.1038/nature06059) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把臭氧沉降、光合作用及气孔反应加入陆地碳循环模型，表达多气体交互。
   - 迁移（推断）：生态碳核算题可检验污染物对吸收能力的影响，再与只计二氧化碳情景比较。
   - 验证问题：不同污染敏感性和气体交互假设下，吸收变化的方向是否稳定？

20. **C020 — Collective dynamics of ‘small-world’ networks**
   Nature（1998；Letter） · [DOI](https://doi.org/10.1038/30918) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：在规则图与随机图之间改变重连程度，用聚类和路径长度连接拓扑与动态传播。
   - 迁移（推断）：疏散网络题可在相同边数下增加少量远程连接，比较通行、传播和失效表现。
   - 验证问题：保持节点与边数后，重连对路径长度的改善是否带来真实通行收益？

21. **C021 — Model estimates of CO2 emissions from soil in response to global warming**
   Nature（1991；Letter） · [DOI](https://doi.org/10.1038/351304a0) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用土壤有机质周转模型将温度路径转化为分解排放，并明确固定植物残体输入假设。
   - 迁移（推断）：碳核算题可分别建输入、储量和分解通量，再比较不同环境及输入情景。
   - 验证问题：放宽输入固定假设后，储量与累计排放预测如何改变？

22. **C022 — The proportionality of global warming to cumulative carbon emissions**
   Nature（2009；Letter） · [DOI](https://doi.org/10.1038/nature08047) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用碳—气候响应把累计排放与温度变化联系，结合观测及理想化模型比较。
   - 迁移（推断）：减排题可把累计预算作为核心变量，同时检验时间尺度与非碳驱动的适用范围。
   - 验证问题：不同排放时间路径和碳汇反馈下，同一累计量是否仍对应相近响应？

23. **C023 — Population dynamics of fox rabies in Europe**
   Nature（1981；Article） · [DOI](https://doi.org/10.1038/289765a0) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用狐种群与狂犬病耦合模型解释周期、密度阈值和感染负担，比较控制组合。
   - 迁移（推断）：动物传播题可同时跟踪宿主数量和疾病状态，在预算下比较免疫与数量控制。
   - 验证问题：宿主补充、季节性和执行率变化后，控制组合是否仍有效？

24. **C024 — Controllability of complex networks**
   Nature（2011；Article） · [DOI](https://doi.org/10.1038/nature10011) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用网络可控性分析识别驱动节点，区分控制需求与节点连接数量。
   - 迁移（推断）：基础设施题可把可操作节点与目标状态写清，再分析控制位置和数量。
   - 验证问题：可控性结论在容量、非线性动态与输入幅度约束下是否仍成立？

25. **C025 — Human mobility networks reveal increased segregation in large cities**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-06757-3) · 排序与决策
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / SafeGraph，段落10；另见逐篇阅读审计。
   - 方法启发：从实际出行接触定义暴露隔离指标，把居住分布和日常相遇分开评价。
   - 迁移（推断）：公共设施题可用访问网络评价不同群体接触机会，再比较设施位置与覆盖。
   - 验证问题：设备抽样、群体标签及时间窗口变化时，隔离指标是否稳定？
   - 来源附注：物理邻近被用作相遇代理，关系强度及未充分覆盖人群仍影响指标解释。

26. **C026 — Global hotspots of salt marsh change and carbon emissions**
   Nature（2022；Article） · [DOI](https://doi.org/10.1038/s41586-022-05355-z) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Mapping year，段落11；另见逐篇阅读审计。
   - 方法启发：用遥感变化分析区分盐沼损失、增长和恢复，再连接到蓝碳储量与埋藏。
   - 迁移（推断）：生态碳预算题可分别核算面积状态转移和单位面积碳量，并传播分类误差。
   - 验证问题：分类误差、恢复规则与碳密度假设变化时，总量和热点是否稳定？
   - 来源附注：碳监测部分将盐沼损失视为地上生物量、埋藏与土壤碳损失；核算结果依赖此边界。
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

27. **C027 — A meta-analysis on global change drivers and the risk of infectious disease**
   Nature（2024；Article） · [DOI](https://doi.org/10.1038/s41586-024-07380-6) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用多宿主—寄生物研究的元分析比较全球变化驱动，并考察情境差异。
   - 迁移（推断）：传播风险题可从多来源数据估计分组效应，分开报告平均关系与地区适用性。
   - 验证问题：研究间异质性、样本权重和驱动分类改变时，效应排序是否稳定？

28. **C028 — Food systems transformation would reshape global agriculture**
   Nature（2026；Article） · [DOI](https://doi.org/10.1038/s41586-026-10775-2) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Multimodel ensemble approach，段落14；另见逐篇阅读审计。
   - 方法启发：用多经济模型集合模拟饮食、生产率和废物减少的联合情景，比较土地与产业配置。
   - 迁移（推断）：食物资源题可统一需求情景，比较多个供给或配置模型的结果范围。
   - 验证问题：相同输入与政策下，不同结构对土地、供给和利益分配的判断是否一致？
   - 来源附注：情景假定饮食偏好可无成本转变，并未显式解决消费者负担能力等现实条件。

29. **C029 — Impacts of climate change on global agriculture accounting for adaptation**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09085-w) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model overview，段落13；另见逐篇阅读审计。
   - 方法启发：用多地区作物纵向数据估计适应响应，再将气候与收入情景用于产量预测。
   - 迁移（推断）：农业规划题可将当前响应与适应能力分开，比较固定和可调整生产情景。
   - 验证问题：留出地区及更极端天气下，适应关系能否持续解释产量变化？
   - 来源附注：简化计量方法估计适应的综合效果，未逐项辨识每个中间生物物理或决策机制。

30. **C030 — Delayed use of bioenergy crops might threaten climate and food security**
   Nature（2022；Article） · [DOI](https://doi.org/10.1038/s41586-022-05055-8) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把作物响应加入简化地球系统模型，耦合食物需求、生物能源与气候反馈。
   - 迁移（推断）：土地规划题可把能源作物与食物用地联立，比较减排时序及供给能力。
   - 验证问题：放宽作物响应、需求和负排放技术假设后，策略可行性如何改变？

31. **C031 — Emerging climate impact on carbon sinks in a consolidated carbon budget**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09802-5) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Land-use change emissions and transient carbon densities correction，段落4；另见逐篇阅读审计。
   - 方法启发：整合碳源、碳汇的观测与过程认识，检验预算闭合及来源分解。
   - 迁移（推断）：碳预算题可统一核算边界，逐项检查输入、输出、储量变化和预算残差。
   - 验证问题：来源归类或观测误差变化时，预算能否闭合，残差是否具有系统模式？
   - 来源附注：记账模型的静态与动态碳密度处理不同；海洋调整后仍存在模型与观测产品差异。

32. **C032 — Temporary carbon dioxide removal to offset short-lived climate forcers**
   Nature（2026；Article） · [DOI](https://doi.org/10.1038/s41586-026-10607-3) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Conceptual framework for temporary CDR，段落5；另见逐篇阅读审计。
   - 方法启发：用气候作用持续时间比较暂时储碳与不同温室气体的补偿关系。
   - 迁移（推断）：减排题可将储存时长、释放及气体寿命写入动态核算，比较不同时间边界。
   - 验证问题：储存期限、释放规则和评价时窗变化时，补偿关系是否仍一致？
   - 来源附注：暂时储碳的释放过程与长期累计影响不同；应用时需明确保留时长及释放形式。

33. **C033 — Global warming amplifies wildfire health burden and reshapes inequality**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09612-9) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用可解释机器学习预测火烧面积及排放，再连接污染暴露、健康和气候影响。
   - 迁移（推断）：野火题可把起火或扩散预测与下游暴露模型分开验证，再合并评估情景。
   - 验证问题：地理留出及未来气候超出训练范围时，风险预测与误差传播是否可靠？

34. **C034 — Mapping carbon accumulation potential from global natural forest regrowth**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2686-x) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把地理定位的碳积累观测与环境协变量结合，估计森林恢复的空间潜力。
   - 迁移（推断）：生态恢复题可按环境条件预测吸收速率，并把训练覆盖与外推区域分开。
   - 验证问题：地理留出及缺少样本的环境区中，预测误差和不确定范围如何变化？

35. **C035 — Cost-effective mitigation of nitrogen pollution from global croplands**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-022-05481-8) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Meta-analysis of mitigation measures，段落6；另见逐篇阅读审计。
   - 方法启发：综合田间措施的产量、氮利用及排放响应，联合核算减排成本与社会收益。
   - 迁移（推断）：农业资源题可把措施成本与多种结果纳入组合选择，并加入实施约束。
   - 验证问题：措施效应异质性、成本和采用率变化时，最佳组合是否稳定？
   - 来源附注：部分输入研究缺少方差或重复次数；元分析的重采样、加权和地区外推需结合方法说明。
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

36. **C036 — Climate benefit and ecological cost trade-offs for ocean iron fertilization**
   Nature（2026；Article） · [DOI](https://doi.org/10.1038/s41586-026-10795-y) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用海洋生物地球化学模型追踪局部施肥的下游碳输出、生态影响及恢复。
   - 迁移（推断）：生态干预题可模拟影响跨区域传播及停止后的恢复，联合比较服务与风险。
   - 验证问题：计入下游影响和撤除干预后的释放时，候选地点的收益排序是否改变？

37. **C037 — Microbial carbon use efficiency promotes global soil carbon storage**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-06042-3) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / The microbial model for representing processes underlying SOC storage，段落28；另见逐篇阅读审计。
   - 方法启发：结合微生物过程模型、数据同化、学习及元分析，比较土壤碳储存的影响因素。
   - 迁移（推断）：生态碳题可让机制模型与经验预测相互核验，再比较参数及空间解释能力。
   - 验证问题：用不同结构和留出观测检验时，因素重要性排序是否保持？
   - 来源附注：营养限制、化学计量及食物网交互可能改变效率的空间模式，解释应结合所用结构。

38. **C038 — Soil moisture–atmosphere feedback dominates land carbon uptake variability**
   Nature（2021；Article） · [DOI](https://doi.org/10.1038/s41586-021-03325-5) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model experiment，段落18；另见逐篇阅读审计。
   - 方法启发：通过因子气候模拟区分土壤水分的直接作用与大气反馈，解释碳吸收波动。
   - 迁移（推断）：生态响应题可设计有无反馈的因子情景，区分直接影响和间接路径。
   - 验证问题：反馈被固定或关闭时，系统变化能否与完整模型的差异相互对应？
   - 来源附注：温度和水汽压亏缺相关，单变量效应归因可能受限；作者同时分析联合贡献。

39. **C039 — Assessing the efficiency of changes in land use for mitigating climate change**
   Nature（2018；Letter） · [DOI](https://doi.org/10.1038/s41586-018-0757-z) · 排序与决策
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用碳收益指标统一比较土地的产出、生产排放及潜在储碳机会成本。
   - 迁移（推断）：土地选择题可统一不同产出的核算指标，再与生态等其他目标并列。
   - 验证问题：更换机会成本、生产边界及需求替代假设后，土地用途排序是否稳定？
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

40. **C040 — Global protected area expansion is compromised by projected land-use and parochialism**
   Nature（2014；Letter） · [DOI](https://doi.org/10.1038/nature14032) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：结合物种分布、土地利用情景及平衡空间优先级技术，比较保护区扩张。
   - 迁移（推断）：保护布局题可加入未来栖息地损失和地区覆盖约束，比较协同配置。
   - 验证问题：未来土地变化及地区目标改变时，新增保护区能否持续覆盖目标对象？

41. **C041 — A global timekeeping problem postponed by global warming**
   Nature（2024；Article） · [DOI](https://doi.org/10.1038/s41586-024-07170-0) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：分解观测地球旋转的不同驱动，再对核心过程及相关趋势做预测外推。
   - 迁移（推断）：时间预测题可拆分机制项、观测趋势和外部驱动，比较简单趋势与机制预测。
   - 验证问题：留出时段及驱动变化下，趋势外推误差是否仍在报告范围内？

42. **C042 — Advancing operational global aerosol forecasting with machine learning**
   Nature（2026；Article） · [DOI](https://doi.org/10.1038/s41586-026-10234-y) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / GEOS-FP analyses and forecasts，段落8；另见逐篇阅读审计。
   - 方法启发：用时空学习模型连接气溶胶与气象变化，并以独立地面观测比较预报。
   - 迁移（推断）：空气质量题可将多变量时空预测与机制或持续性基线比较，明确独立观测检验。
   - 验证问题：地理留出、极端事件及不同预报时距下，误差与校准表现是否稳定？
   - 来源附注：讨论提出滚动输入、动态排放清单及时间变化背景场等改进方向，需检查分布变化。

43. **C043 — Marine heatwaves under global warming**
   Nature（2018；Letter） · [DOI](https://doi.org/10.1038/s41586-018-0383-9) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：结合卫星观测与地球系统模拟，按频率、持续时间、强度和范围描述海洋热浪。
   - 迁移（推断）：生态极端事件题可同时建强度及持续时间指标，再比较连续冲击风险。
   - 验证问题：阈值、基准期与气候模型变化时，极端事件风险是否稳定？

44. **C044 — Anthropogenic greenhouse gas contribution to flood risk in England and Wales in autumn 2000**
   Nature（2011；Letter） · [DOI](https://doi.org/10.1038/nature09762) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：将真实与反事实气候情景的模拟输入降水—径流模型，以概率比较事件风险。
   - 迁移（推断）：灾害归因题可构建保持其他条件一致的对照情景，区分风险变化与单次事件结果。
   - 验证问题：反事实假设、天气集合及水文结构变化时，归因风险范围如何改变？

45. **C045 — Warming caused by cumulative carbon emissions towards the trillionth tonne**
   Nature（2009；Letter） · [DOI](https://doi.org/10.1038/nature08019) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用观测约束的简化气候—碳循环模型集合比较多种排放路径与峰值升温。
   - 迁移（推断）：减排题可比较累计预算、排放速率与时间安排，并传播联合参数不确定性。
   - 验证问题：不同排放路径中，累计量与峰值响应的关系是否比速率关系更稳定？

46. **C046 — Global climate change and US agriculture**
   Nature（1990；Article） · [DOI](https://doi.org/10.1038/345219a0) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：耦合气候、植物与农业经济模型，追踪产量、灌溉和地区生产调整。
   - 迁移（推断）：粮水规划题可把环境响应和经济配置联立，再比较供给、用水及地区收益。
   - 验证问题：换用气候输入和作物响应后，最优配置与经济结果是否一致？

47. **C047 — Complex dynamics and phase synchronization in spatially extended ecological systems**
   Nature（1999；Letter） · [DOI](https://doi.org/10.1038/20676) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用多斑块三营养级动态模型区分周期相位同步与数量峰值的混沌变化。
   - 迁移（推断）：生态网络题可同时检验时间相位和波动幅度，分析迁移对整体动态的影响。
   - 验证问题：相位同步时，峰值和总量是否也同步，结论是否随迁移率而变？

48. **C048 — Allometric scaling of plant energetics and population density**
   Nature（1998；Letter） · [DOI](https://doi.org/10.1038/25977) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：从个体资源利用与体型关系构建资源受限植物的密度—质量机制模型。
   - 迁移（推断）：生态资源题可从个体需求推导可承载数量，再与单纯几何模型比较。
   - 验证问题：机制关系能否在不同环境与规模下解释密度，而非只拟合一个指数？

49. **C049 — Extinction risk from climate change**
   Nature（2004；Letter） · [DOI](https://doi.org/10.1038/nature02121) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用物种分布情景及多个范围—灭绝概率关系，比较气候和扩散假设的风险。
   - 迁移（推断）：生态风险题可同时保留多种空间分布及风险映射结构，报告结果分歧。
   - 验证问题：同一情景下，不同范围—风险关系及扩散假设是否改变治理优先级？

50. **C050 — Sensitivity of tropical carbon to climate change constrained by carbon dioxide variability**
   Nature（2013；Letter） · [DOI](https://doi.org/10.1038/nature11882) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：在模型集合中连接年际观测响应与长期碳敏感性，用观测形成涌现约束。
   - 迁移（推断）：环境预测题可检验可观测短期指标与长期响应的关系，再约束情景预测。
   - 验证问题：跨模型或数据源留出后，短期—长期关系能否保持，遗漏驱动是否改变约束？

51. **C051 — Ant-like task allocation and recruitment in cooperative robots**
   Nature（2000；Letter） · [DOI](https://doi.org/10.1038/35023164) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：以分工、招募和信息传递规则构建分散控制算法，并用机器人群体任务检验。
   - 迁移（推断）：协作调度题可让主体按局部信息领取和转交任务，分析群体规模及相互干扰。
   - 验证问题：相同资源下，信息共享是否改善效率，过大群体是否增加冲突？

52. **C052 — Nonlinear dynamics of ice-wedge networks and resulting sensitivity to severe cooling events**
   Nature（2002；Letter） · [DOI](https://doi.org/10.1038/nature00796) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用热应力、断裂及冰楔交互的数值模型研究空间网络演化和极端冷却记忆。
   - 迁移（推断）：环境网络题可比较平均驱动与少量极端冲击，追踪结构变化后的持续影响。
   - 验证问题：保留平均条件而改变极端事件时序时，网络形态是否仍相同？

53. **C053 — Epidemic models used to explain biogeographical distribution limits**
   Nature（1981；Letter） · [DOI](https://doi.org/10.1038/293644a0) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：将建立新地点的过程视为传播模型，通过阈值分析连接个体表现与地区分布边界。
   - 迁移（推断）：入侵题可分别建局部存活和新地点殖民过程，研究连接及建立阈值。
   - 验证问题：局部性能的小幅改变会否通过建立阈值产生明显不同的分布范围？

54. **C054 — Spatial structure and chaos in insect population dynamics**
   Nature（1991；Letter） · [DOI](https://doi.org/10.1038/353255a0) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：比较显式寄主—寄生物模型与定性元胞规则，分析局部扩散生成的空间动态。
   - 迁移（推断）：生态空间题可让机制方程与元胞基线使用相同迁移规则，比较持续性与空间结构。
   - 验证问题：不同模型结构是否都能再现斑块动态，空间复杂性是否只是随机噪声？

55. **C055 — Simulating dynamical features of escape panic**
   Nature（2000；Letter） · [DOI](https://doi.org/10.1038/35035023) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用行人行为仿真分析无协调运动、拥堵和跟随行为对逃生的影响。
   - 迁移（推断）：疏散题可建主体运动及出口约束，比较自主寻找与跟随混合规则。
   - 验证问题：出口布局、速度意愿及行为规则变化时，拥堵与完成时间是否稳定？

56. **C056 — The sensitivity of terrestrial carbon storage to climate change**
   Nature（1990；Letter） · [DOI](https://doi.org/10.1038/346048a0) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：耦合气候与植被空间分布，模拟生物圈碳储量及大气交换的情景变化。
   - 迁移（推断）：生态碳题可把面积、植被类型及单位储量设为动态变量，并检查储量转移。
   - 验证问题：不同气候、植被响应与地理边界下，碳收支是否守恒？

57. **C057 — Allometry and simple epidemic models for microparasites**
   Nature（1996；Letter） · [DOI](https://doi.org/10.1038/379720a0) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把出生、死亡及密度写成体型异速关系，用传播阈值连接不同宿主的感染动态。
   - 迁移（推断）：数据稀少的传播题可用有依据的尺度关系估计候选参数，再报告代理带来的误差。
   - 验证问题：尺度代理能否解释独立宿主数据，阈值是否对代理关系高度敏感？

58. **C058 — Transmission intensity and impact of control policies on the foot and mouth epidemic in Great Britain**
   Nature（2001；Letter） · [DOI](https://doi.org/10.1038/35097116) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：由农场疾病与牲畜数据估计传播差异，再用动态模型比较控制策略及时序。
   - 迁移（推断）：动物防疫题可按地点组成、数量和连接拟合传播参数，再比较容量受限策略。
   - 验证问题：空间留出预测和执行时延变化是否支持同一干预顺序？
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

59. **C059 — Learning from prepandemic data to forecast viral escape**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-06617-0) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把历史序列学习与物理结构信息组合成预测框架，用后续变异及跨病毒检验。
   - 迁移（推断）：预测题可严格按时间切分训练数据，再比较单数据源与多机制模型的外推。
   - 验证问题：在预测时尚未获得的数据被排除后，留出及跨对象性能是否保持？

60. **C060 — The scales of human mobility**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2909-1) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用轨迹推断限制出行的多层空间容器，并解释聚合后出现的标度模式。
   - 迁移（推断）：出行题可按建筑、社区和城市层级建转移规则，比较个体与汇总模式。
   - 验证问题：同一模型能否解释单人轨迹和总体距离分布，层级划分是否稳定？

61. **C061 — The universal visitation law of human mobility**
   Nature（2021；Article） · [DOI](https://doi.org/10.1038/s41586-021-03480-9) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：将访问频率与距离的标度联系到探索和优先返回机制，建模重复出行。
   - 迁移（推断）：服务设施题可把一次访问和重复访问分开预测，比较探索及惯性返回规则。
   - 验证问题：同一模型能否同时解释地点流量、访问频率和个体轨迹？

62. **C062 — Religion and educational mobility in Africa**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-06051-2) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Data，段落7；另见逐篇阅读审计。
   - 方法启发：把教育代际升降流动写成群体比例的动态关系，比较地区及家庭背景差异。
   - 迁移（推断）：教育资源题可建群体状态转移模型，区分已有结构与未来机会变化。
   - 验证问题：家庭匹配方式、地区控制及队列划分变化时，转移率与差距是否稳定？
   - 来源附注：代际转移估计依赖共同居住的家庭匹配及教育完成阈值；方法比较了替代匹配。
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

63. **C063 — Latitudinal scaling of aggregation with abundance and coexistence in forests**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-08604-z) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Basic multispecies model M1，段落37；另见逐篇阅读审计。
   - 方法启发：把树木空间聚集模式纳入种群模型，连接稀有物种入侵、人口统计和生态位重叠。
   - 迁移（推断）：生态布局题可将局部邻域模式与种群方程结合，研究低数量条件下的存续。
   - 验证问题：不同空间点模式与邻域尺度下，入侵判据能否解释留出地块？
   - 来源附注：示例把邻域拥挤作用于生存而把繁殖设为密度独立；替代过程在文中及补充推导讨论。

64. **C064 — No meta-analytical effect of economic inequality on well-being or mental health**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09797-z) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：以随机效应、元回归和多种模型设定分析关联，检查发表偏差与背景调节。
   - 迁移（推断）：社会评价题可比较研究间差异、偏差校正及不同设定，分别报告总体与分组关系。
   - 验证问题：更换模型设定、样本背景与偏差校正后，关联方向和不确定性是否保持？

65. **C065 — Ecosystem decay exacerbates biodiversity loss with habitat loss**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2531-2) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用多研究汇集数据比较被动抽样与生态衰退假说，控制采样努力与空间尺度。
   - 迁移（推断）：生态风险题可先建保持个体数量与抽样规则的基线，再识别额外损失机制。
   - 验证问题：人工调整样本量后，观察到的生态损失是否仍超出被动抽样预期？

66. **C066 — Overflow metabolism in Escherichia coli results from efficient proteome allocation**
   Nature（2015；Article） · [DOI](https://doi.org/10.1038/nature15765) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用资源配置模型表达能量产生与生物量合成的蛋白成本，并检验新扰动响应。
   - 迁移（推断）：资源组合题可让多条生产路径争用同一预算，比较效率与容量成本的权衡。
   - 验证问题：需求增加时，低成本低效率路径是否出现，模型能否预测留出扰动？

67. **C067 — Machine learning reveals the control mechanics of an insect wing hinge**
   Nature（2024；Article） · [DOI](https://doi.org/10.1038/s41586-024-07293-4) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用学习模型从肌肉活动预测运动，再把结构解释接入物理模拟与机器人检验。
   - 迁移（推断）：运动控制题可让数据预测与物理约束互相核验，分开检查预测和机制解释。
   - 验证问题：预测模型在新动作及物理模拟中是否一致，各结构贡献是否可独立检验？

68. **C068 — Scaling deep learning for materials discovery**
   Nature（2023；Article） · [DOI](https://doi.org/10.1038/s41586-023-06735-9) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Training structural and composition models，段落19；另见逐篇阅读审计。
   - 方法启发：用图学习模型与第一性原理计算探索材料空间，并用独立实验及下游任务核验。
   - 迁移（推断）：计算昂贵的搜索题可用代理模型筛选候选，再通过原模型和独立证据确认。
   - 验证问题：筛选候选在原模拟、独立数据和新任务上是否保持性能？
   - 来源附注：构成模型的训练标签未必代表基态，误差指标与新材料发现的适用性需要分别检查。

69. **C069 — Technological pathways for cost-effective steel decarbonization**
   Nature（2025；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Plant-level pathway design model，段落5；另见逐篇阅读审计。
   - 方法启发：以工厂特征和未来技术成本建立最小成本减碳路径，保留地区与设备异质性。
   - 迁移（推断）：能源改造题可逐设施选择更新技术及时间，联立预算、需求和排放约束。
   - 验证问题：技术成本、成熟时点及设备寿命变化时，路径与总成本是否稳定？
   - 来源附注：部分钢厂成本输入来自非公开商业数据库，完整结果复现依赖相应数据条件。

70. **C070 — Global terrestrial nitrogen fixation and its modification by agriculture**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09201-w) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用空间明确的固氮生态位丰度对田间测量上尺度，校正样本集中造成的估计偏差。
   - 迁移（推断）：环境总量估计题可按空间代表性加权观测，再比较直接样本平均与分层外推。
   - 验证问题：改变分层、权重及未覆盖环境的假设后，总量估计是否稳定？

71. **C071 — Extreme river flood exposes latent erosion risk**
   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09305-3) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Numerical modelling of water levels, shear stresses and initial erosion，段落21；另见逐篇阅读审计。
   - 方法启发：结合地形和沉积观测、二维流动模拟与水位重建，分析河流瓶颈的冲刷机制。
   - 迁移（推断）：洪水基础设施题可将通道布局与底层材料纳入流动风险，比较局部拓宽方案。
   - 验证问题：地形、沉积及水位重建误差变化时，风险瓶颈位置是否仍稳定？
   - 来源附注：水位及冲刷重建依赖几何、粗糙度和测量误差；校准使用与观测时期匹配的河流几何。

   Nature（2025；Article） · [DOI](https://doi.org/10.1038/s41586-025-09319-x) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用气候模拟及古气候记录验证海洋环流变化经大气和海气交互传播的降水机制。
   - 迁移（推断）：环境风险题可明确跨区域影响路径，再以独立时期或多模型验证情景响应。
   - 验证问题：不同气候模型与独立时期中，传播机制和区域响应是否一致？

73. **C073 — The origin of bursts and heavy tails in human dynamics**
   Nature（2005；Letter） · [DOI](https://doi.org/10.1038/nature03459) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用按优先级执行任务的排队机制解释活动突发与长等待，比较随机执行基线。
   - 迁移（推断）：服务调度题可让任务优先级进入队列，分析平均等待与少数极端等待。
   - 验证问题：不同优先级、到达规则和队列容量能否同时解释常见与极端等待？

74. **C074 — Catastrophic cascade of failures in interdependent networks**
   Nature（2010；Letter） · [DOI](https://doi.org/10.1038/nature08932) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：把节点间依赖跨越多个网络，分析递归失效及系统破碎的临界条件。
   - 验证问题：依赖比例、失效规则及修复能力变化时，系统风险是否仍被单网指标解释？

75. **C075 — The scaling laws of human travel**
   Nature（2006；Letter） · [DOI](https://doi.org/10.1038/nature04292) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：结合移动距离和停留时间的长尾统计，以连续时间随机游走描述空间扩散。
   - 迁移（推断）：移动题可将距离选择与等待时间分别建模，再比较普通扩散基线。
   - 验证问题：不同地区及时间窗口中，模型能否同时解释距离分布、停留与扩散速度？

76. **C076 — Estimating the effects of non-pharmaceutical interventions on COVID-19 in Europe**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2405-7) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model，段落18；另见逐篇阅读审计。
   - 方法启发：从死亡观测逆推感染过程，显式处理时滞并在地区间共享部分参数信息。
   - 迁移（推断）：传播题可用延迟观测反推隐状态，并比较完全共用、完全分开和部分共享估计。
   - 验证问题：感染到报告的时滞、固定参数和地区异质性变化时，干预效应是否可辨识？
   - 来源附注：死亡数据存在漏报且反推受感染至死亡的时滞限制，另有固定病程和共享效应假设。

77. **C077 — The effect of large-scale anti-contagion policies on the COVID-19 pandemic**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2404-8) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model，段落40；另见逐篇阅读审计。
   - 方法启发：用政策与病例面板数据做简化计量分析，比较控制措施与感染增长关系。
   - 迁移（推断）：政策评价题可设置地区、时间和趋势基线，并检验政策前后及反事实关系。
   - 验证问题：政策组合共现、报告变化和先前趋势能否混淆估计的干预效应？
   - 来源附注：早期指数增长近似适用于易感比例接近初始状态；分析未显式纳入相邻地点及移动网络交互。
   - 更正提示：关联元数据或页面更新链接已保留于JSON；具体公式、图表和数值应连同更新核查。

78. **C078 — Effect of non-pharmaceutical interventions to contain COVID-19 in China**
   Nature（2020；Article） · [DOI](https://doi.org/10.1038/s41586-020-2293-x) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model summary，段落10；另见逐篇阅读审计。
   - 方法启发：用每日出行网络和流行病数据仿真多种干预及实施时间情景。
   - 迁移（推断）：校园传播题可按逐日活动网络模拟检测、隔离和接触变化，再统一比较资源需求。
   - 验证问题：病例与出行留出检验、干预时序和执行率变化是否支持策略排序？
   - 来源附注：早期确诊病例的参数可能遗漏无症状或轻症感染，并存在其他时变因素混淆。

79. **C079 — Strategies for containing an emerging influenza pandemic in Southeast Asia**
   Nature（2005；Article） · [DOI](https://doi.org/10.1038/nature04017) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Transmission model，段落8；另见逐篇阅读审计。
   - 方法启发：用空间传播仿真比较定向干预组合，并把诊断和物资分配速度计入可行性。
   - 迁移（推断）：应急传播题可把响应延迟、地理覆盖和库存约束纳入干预模型。
   - 验证问题：识别延迟和配送速度改变时，策略能否在相同预算下达到控制目标？
   - 来源附注：目标病毒自然史尚未确定时，模型采用既有流感参数，并以敏感性情景检查偏离。

80. **C080 — Strategies for mitigating an influenza pandemic**
   Nature（2006；Letter） · [DOI](https://doi.org/10.1038/nature04795) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：出版社完整摘要。
   - 方法启发：用大规模传播模拟比较干预组合，区分延迟传播、峰值和累计负担。
   - 迁移（推断）：应急策略题可分别评价峰值、完成时间与总损失，并保留执行和物流约束。
   - 验证问题：不同病程、执行能力及干预组合下，峰值改善是否转化为总负担改善？
