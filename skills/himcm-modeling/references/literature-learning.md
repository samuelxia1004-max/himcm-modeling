# Nature 系列数学建模文献学习卡（100篇）

本参考逐篇保留经出版社页面与 Crossref 记录核对的英文题名和 DOI。100篇摘要已阅读，其中57篇进一步阅读了模型、方法、校准、验证或研究范围的正文段落，其余43篇为摘要阅读。`ABSTRACT_REVIEWED` 表示摘要阅读；`FULL_TEXT_SECTION_REVIEWED` 表示摘要及指定正文段落摘读。包内身份、版本与阅读范围见 [literature-index.json](literature-index.json)。完整下载路径、访问记录与逐篇学习卡保存在单独交付的研究库 `literature/learning_cards.json` 与 `literature/reading_audit.md` 中；本 skill 运行不依赖该研究库。

“迁移（推断）”是面向 HiMCM 的适配研究假设，需要结合题目数据重新定义变量、约束和检验标准。“验证问题”是使用该方法时建议提出的检查问题。

阅读时先确定对象、尺度与核算边界，再选择复杂度与数据量相称的模型。

1. **N001 — Quantifying the dynamics of failure across science, startups and security**
   Nature（2019；Article） · [DOI](https://doi.org/10.1038/s41586-019-1725-y) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用少参数的尝试记忆机制分析累积改进，并从时间序列中提出可检验的分界行为。
   - 迁移（推断）：将维护或迭代改进过程建成带历史记忆的状态模型，比较持续改进与重新开始两种规则。
   - 验证问题：不同记忆长度下，改进趋势能否在留出的尝试序列中重现？

   Nature（2017；Letter） · [DOI](https://doi.org/10.1038/nature21071) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把植物—传粉者相互作用网络与实际繁殖表现连接起来，区分物种数和功能冗余。
   - 迁移（推断）：保护区修复题可同时跟踪连接多样性、替代通道与生态服务产出。
   - 验证问题：网络指标对功能产出的解释是否仍优于仅使用物种数量？

3. **N003 — Hidden resilience and adaptive dynamics of the global online hate ecology**
   Nature（2019；Letter） · [DOI](https://doi.org/10.1038/s41586-019-1494-7) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把跨平台群体视为相互连接的网络，并考虑受干预后重新连边的适应行为。
   - 迁移（推断）：谣言治理题可建多层传播网络，让节点在干预后改变连接，再比较资源配置。
   - 验证问题：允许重新连边后，局部干预的效果与固定网络情形相差多大？

4. **N004 — Strong effect of dispersal network structure on ecological dynamics**
   Nature（2008；Letter） · [DOI](https://doi.org/10.1038/nature07395) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：捕食—被捕食斑块模型中，扩散拓扑、强耦合和暂态共同影响同步及波动。
   - 迁移（推断）：栖息地连接题可在相同迁移总量下比较不同连接布局的长期和暂态风险。
   - 验证问题：更换网络结构后，结论是否随耦合强度、观察窗口而改变？

5. **N005 — Higher-order interactions stabilize dynamics in competitive network models**
   Nature（2017；Letter） · [DOI](https://doi.org/10.1038/nature23273) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：在竞争网络中加入第三个物种对两物种交互的影响，检验共存及扰动响应。
   - 迁移（推断）：生态群落题可把成对模型作为基线，再增加少量有依据的高阶相互作用。
   - 验证问题：高阶项是否改善独立数据拟合，还是仅增加参数自由度？

6. **N006 — Universal resilience patterns in complex networks**
   Nature（2016；Letter） · [DOI](https://doi.org/10.1038/nature16948) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Model formulation / resilience reduction / perturbation comparisons（指定段落摘读）。
   - 方法启发：通过有效低维动力学分离网络拓扑与节点动态的作用，研究多维系统的韧性。
   - 迁移（推断）：网络韧性题可尝试少量系统级指标的降维，并用完整网络模拟检查近似适用范围。
   - 验证问题：改变网络异质性和节点动力学后，降维预测能否仍解释系统失稳？
   - 来源附注：该文关联2016及2019更正（10.1038/nature18019；10.1038/s41586-019-1091-9）；使用图3时应同时核对更正。

7. **N007 — Addressing the minimum fleet problem in on-demand urban mobility**
   Nature（2018；Letter） · [DOI](https://doi.org/10.1038/s41586-018-0095-1) · 疏散与网络流
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：将具有起点、终点和时间的行程连接成车辆共享网络，用可衔接关系处理最小车队。
   - 迁移（推断）：校车、接送或救援车辆题可用时间兼容图组织连续任务，并加入换乘和准备时间。
   - 验证问题：旅行时间延误或需求峰值改变时，车队规模和服务率是否稳定？

8. **N008 — A universal model for mobility and migration patterns**
   Nature（2012；Letter） · [DOI](https://doi.org/10.1038/nature10856) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：PDF第4–5页 模型构造；PDF第6–7页 验证比较；PDF第8页 假设与空间背景（指定段落摘读）。
   - 版本：发表前稿（submittedVersion）；发表版逐字一致性未核验。
   - 方法启发：把就业机会视为人口代理，按最近可接受机会规则推导辐射流量，并比较流量、距离及目的地分布。
   - 迁移（推断）：缺少完整OD数据时，可用人口及周边机会生成候选流量，并用本地观测校验机会代理和行为规则。
   - 验证问题：同一组机会代理能否同时解释流量、距离和目的地规模分布，并通过地区留出检验？
   - 来源附注：发表前稿第4页假定就业机会数量与居民人口成正比，并采用最近可接受机会规则；其适用性需在迁移场景中检验。公式符号及上下标在文本提取中存在错位。

9. **N009 — Allowable carbon emissions lowered by multiple climate targets**
   Nature（2013；Letter） · [DOI](https://doi.org/10.1038/nature12269) · 气候与碳核算
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用观测约束的贝叶斯地球系统模型同时考察多个气候目标及参数不确定性。
   - 迁移（推断）：校园减排题可把碳预算、水耗及污染约束一并加入可行域，并报告达标概率。
   - 验证问题：增加约束后，可行方案如何变化，哪项约束最敏感？

10. **N010 — Long-term relationships between ecological stability and biodiversity in Phanerozoic reefs**
   Nature（2005；Letter） · [DOI](https://doi.org/10.1038/nature03152) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用带时间滞后的历史关系分析生物多样性与稳定性，并区分稳定性和产出指标。
   - 迁移（推断）：生态恢复评价可分别考察波动、恢复和产出，选择与题目时间尺度匹配的指标。
   - 验证问题：改变时间聚合尺度和滞后长度后，多样性—稳定性关系是否保持？

11. **N011 — Biodiversity as a barrier to ecological invasion**
   Nature（2002；Letter） · [DOI](https://doi.org/10.1038/nature00776) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：以局部邻域的拥挤和物种丰富度解释入侵建立与后续生长的差异。
   - 迁移（推断）：入侵防控题可把局部空间竞争写入扩散规则，分别预测建立概率和后续规模。
   - 验证问题：局部邻域尺度变化后，模型能否仍解释独立地块的入侵数据？

12. **N012 — Coherent ecological dynamics induced by large-scale disturbance**
   Nature（2008；Letter） · [DOI](https://doi.org/10.1038/nature06935) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用小波分析区分不同时间尺度的同步，检验季节互补与总生物量波动。
   - 迁移（推断）：生态或用能题可分析季节性互补，避免用单一全年相关系数描述系统稳定性。
   - 验证问题：去除季节趋势或改变分析窗口后，观察到的同步是否仍存在？

13. **N013 — Effects of household dynamics on resource consumption and biodiversity**
   Nature（2003；Letter） · [DOI](https://doi.org/10.1038/nature01359) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：家庭数量和家庭规模会改变人均资源需求，人口总量可能掩盖消费结构变化。
   - 迁移（推断）：社区水、电或垃圾预测可按家庭类型建需求模型，再汇总到总人口。
   - 验证问题：相同人口但不同家庭规模分布时，预测总需求差异是否符合数据？

14. **N014 — Synchronization of animal population dynamics by large-scale climate**
   Nature（2002；Letter） · [DOI](https://doi.org/10.1038/nature01064) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：利用地理隔离的种群比较气候驱动同步，区分共同环境影响与直接扩散。
   - 迁移（推断）：跨地区风险题可把共同天气驱动作为独立输入，再评估地点间连接的额外影响。
   - 验证问题：控制共同气候变量后，地区间同步还剩多少？

15. **N015 — Rapid evolution drives ecological dynamics in a predator–prey system**
   Nature（2003；Letter） · [DOI](https://doi.org/10.1038/nature01767) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：捕食—被捕食模型把猎物性状演化与种群周期耦合，并通过操纵实验检验机制。
   - 迁移（推断）：生态题可比较固定性状与可适应性状模型，观察周期和相位是否改变。
   - 验证问题：增加适应机制后，模型是否同时解释周期长度与捕食者—猎物相位？

16. **N016 — A simple model of bipartite cooperation for ecological and organizational networks**
   Nature（2008；Letter） · [DOI](https://doi.org/10.1038/nature07532) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用简洁的随机专化和连接规则生成二部合作网络，并比较度分布、嵌套性和模块性。
   - 迁移（推断）：供需匹配题可建服务者—需求者二部图，以少量规则生成缺失连接的备选网络。
   - 验证问题：生成网络能否同时再现多个结构指标，而非只匹配平均连接数？

17. **N017 — Evolutionary dynamics on any population structure**
   Nature（2017；Letter） · [DOI](https://doi.org/10.1038/nature21723) · 排序与决策
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：PDF第2页 模型适用条件；PDF第4–5页 模型与推导；PDF第6页 Monte Carlo核验（指定段落摘读）。
   - 版本：发表前稿（submittedVersion）；发表版逐字一致性未核验。
   - 方法启发：在弱选择条件下，将死亡—出生策略更新与随机游走合并时间连接，用线性方程分析合作选择条件。
   - 迁移（推断）：公共资源合作题可先写明策略更新与收益规则，再比较连接结构影响，并用仿真检查弱选择近似。
   - 验证问题：改变选择强度、平均或累积收益、更新规则后，图结构的合作排序是否稳定？
   - 来源附注：发表前稿第4–6页的解析结果依赖弱选择及指定更新规则；第42页另说明新类型在各节点等概率出现的假设。正文中的公式与图形符号有文本提取错位。

18. **N018 — Coupled dynamics of body mass and population growth in response to environmental change**
   Nature（2010；Letter） · [DOI](https://doi.org/10.1038/nature09210) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：将体重等个体性状、生命史过程和种群增长联系起来，区分直接与性状介导效应。
   - 迁移（推断）：野生动物管理题可先建年龄或性状分组，再研究环境变化如何影响存活和繁殖。
   - 验证问题：直接环境模型与加入性状机制的模型，在留出年份的表现有何差异？

19. **N019 — Resource-use efficiency and plant invasion in low-resource systems**
   Nature（2007；Letter） · [DOI](https://doi.org/10.1038/nature05719) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：资源利用效率的结论与测量时间尺度有关，可比较短期效率与生命周期整合效率。
   - 迁移（推断）：入侵或资源管理题可分别核算单位时间利用率与整个生命周期的资源成本。
   - 验证问题：把效率积分到更长时期后，候选物种或管理方案的排序是否变化？

20. **N020 — Modelling the effects of subjective and objective decision making in scientific peer review**
   Nature（2013；Letter） · [DOI](https://doi.org/10.1038/nature12786) · 排序与决策
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把个体判断与从众机制纳入动态信息聚合模型，研究决策规则如何影响群体判断。
   - 迁移（推断）：评奖或方案评审题可模拟独立打分与可见他人评分的流程，分析相关误差。
   - 验证问题：评分者偏差或信息相关性变化时，最终排序有多稳定？

21. **N021 — Disease-economy trade-offs under alternative epidemic control strategies**
   Nature Communications（2022；Article） · [DOI](https://doi.org/10.1038/s41467-022-30642-8) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Methodological contributions；Results / Robustness to assumptions on coupling parameters and functions（指定段落摘读）。
   - 方法启发：把疾病传播与经济活动、个体选择耦合，并对接触函数及校准假设做敏感性分析。
   - 迁移（推断）：校园防疫题可同时估计健康损失和活动成本，让检测质量、延迟与执行率进入情景。
   - 验证问题：换一种接触函数或执行率假设后，策略的成本—风险比较是否改变？

22. **N022 — Epidemic graph diagrams as analytics for epidemic control in the data-rich era**
   Nature Communications（2023；Article） · [DOI](https://doi.org/10.1038/s41467-023-43856-1) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Infection propagator and epidemic threshold（指定段落摘读）。
   - 方法启发：感染传播算子和图式组合规则把接触时序、疾病阶段及干预连接到传播阈值。
   - 迁移（推断）：传播题可保留潜伏期及接触先后顺序，并与更简单的平均接触模型比较。
   - 验证问题：忽略非传染阶段或打乱接触时序时，估计阈值偏移多少？

23. **N023 — A network model of Italy shows that intermittent regional strategies can alleviate the COVID-19 epidemic**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-18827-5) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Model formulation and fitting procedure；Methods / Model parameterization from real data and model validation（指定段落摘读）。
   - 方法启发：把地区建成节点、人员流动建成边，按地区拟合分舱动力学并计入医疗容量。
   - 迁移（推断）：校园分区或地区防疫题可用分区传播模型比较统一策略与容量触发的局部策略。
   - 验证问题：留出时段预测、跨区流量扰动和容量变化是否支持同一策略？

24. **N024 — Discontinuous epidemic transition due to limited testing**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-22725-9) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Spatial epidemic model；Methods / Testing and quarantining model（指定段落摘读）。
   - 方法启发：空间SEIR模型显式加入有限检测队列、检测延迟和隔离状态，考察容量饱和。
   - 迁移（推断）：应急检测题可把每日处理上限写成队列约束，寻找需求超过能力时的转折。
   - 验证问题：检测能力和报告延迟的小幅变化是否导致明显不同的传播轨迹？

25. **N025 — Importance of social inequalities to contact patterns, vaccine uptake, and epidemic dynamics**
   Nature Communications（2024；Article） · [DOI](https://doi.org/10.1038/s41467-024-48332-y) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Stratified modelling of the Hungarian scenario；Results / The main determinants of human contact patterns（指定段落摘读）。
   - 方法启发：将年龄、就业和收入等分组对应的接触矩阵、疫苗接种差异纳入传播模型。
   - 迁移（推断）：校园传播题可按活动角色或年级分组，以接触数据支持差异化参数。
   - 验证问题：分组模型在留出数据上是否优于均匀混合模型，且各组误差是否可接受？
   - 来源附注：讨论指出，接触对象的非年龄社会特征缺失，限制了跨社会维度接触结构的表达。

26. **N026 — Compensating for population sampling in simulations of epidemic spread on temporal contact networks**
   Nature Communications（2015；Article） · [DOI](https://doi.org/10.1038/ncomms9860) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Data and methodology；Results / Limitations（指定段落摘读）。
   - 方法启发：通过受控抽样和替代接触网络重建，评估缺失参与者对传播模拟的影响。
   - 迁移（推断）：接触或通行数据不完整时，可生成多份合理补全网络并报告预测范围。
   - 验证问题：人工删去已知数据后，补全方法能否恢复原网络上的模拟分布？
   - 来源附注：讨论指出，大比例缺失时，重建所依赖的抽样统计稳定性可能减弱。

27. **N027 — Effects of social distancing and isolation on epidemic spreading modeled via dynamical density functional theory**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-19024-0) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / SIR-DDFT model（指定段落摘读）。
   - 方法启发：将SIR分舱模型与空间密度动力学结合，显式表达社交距离和感染者隔离。
   - 迁移（推断）：人群传播题可比较均匀混合、空间扩散和主动避让三种机制的效果。
   - 验证问题：空间模型的额外机制能否解释聚集及分离现象，并保持人数守恒？

28. **N028 — Nationwide rollout reveals efficacy of epidemic control through digital contact tracing**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-26144-8) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Modelling the technological efficacy（指定段落摘读）。
   - 方法启发：用实际设备接触数据估计数字追踪效力，方法区分技术检测与参与率的影响。
   - 迁移（推断）：校园接触追踪题可拆分覆盖率、识别率和响应速度，逐项分析系统效果。
   - 验证问题：设备相互检测独立性的假设和不同参与率会怎样改变有效覆盖？

29. **N029 — Realistic control of network dynamics**
   Nature Communications（2013；Article） · [DOI](https://doi.org/10.1038/ncomms2939) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Identification of compensatory perturbations；Results / Application to the identification of therapeutic interventions（指定段落摘读）。
   - 方法启发：在非线性系统中迭代选择受约束的小扰动，尝试把轨迹引入目标状态。
   - 迁移（推断）：网络恢复题可在可操作节点和预算范围内搜索干预，并检查完整动态轨迹。
   - 验证问题：候选干预在完整非线性模拟和多个初始状态下能否到达目标？

30. **N030 — Interconnectedness enhances network resilience of multimodal public transportation systems for Safe-to-Fail urban mobility**
   Nature Communications（2023；Article） · [DOI](https://doi.org/10.1038/s41467-023-39999-w) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Network preparedness；Results / Interconnectedness and network robustness of MPTN（指定段落摘读）。
   - 方法启发：用多方式交通网络分析节点不均衡、攻击退化和跨方式连接的恢复作用。
   - 迁移（推断）：疏散题可建步行、公交与轨道多层网络，比较增加换乘边后的失效性能。
   - 验证问题：随机失效与关键节点失效下，连通性改善能否转化为可完成的出行？

31. **N031 — Dynamically induced cascading failures in power grids**
   Nature Communications（2018；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Modeling power grids；Introduction / Introduction（指定段落摘读）。
   - 方法启发：用摆动方程结合事件触发的线路失效，揭示暂态流量与稳态分析的差别。
   - 迁移（推断）：供电韧性题可同时模拟负荷再分配和短时超载，比较动态与静态风险排序。
   - 验证问题：用稳态模型选出的关键线路，在包含暂态的模拟中是否仍最脆弱？
   - 来源附注：讨论中的摆动方程是简化电网描述；文中未同时覆盖电压动态及电厂节点停运。

32. **N032 — Model-free inference of direct network interactions from nonlinear collective dynamics**
   Nature Communications（2017；Article） · [DOI](https://doi.org/10.1038/s41467-017-02288-4) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Revealing direct links in model systems；Introduction / Introduction（指定段落摘读）。
   - 方法启发：用依赖矩阵和分块回归从非线性时间序列推断直接交互，并与相关性方法比较。
   - 迁移（推断）：多变量系统题可比较相关网络和动力学推断网络，再用已知或模拟结构检验。
   - 验证问题：缩短记录、加入噪声或隐藏节点后，边识别及外推能力如何变化？
   - 来源附注：所读结果段指出，交互基函数类别的选择影响推断性能。

33. **N033 — Network isolators inhibit failure spreading in complex networks**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-23292-9) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / A model for supply networks；Results / A model for supply networks（指定段落摘读）。
   - 方法启发：在线性势差流网络中，模块间连接矩阵的结构可限制局部失效对其他模块的影响。
   - 验证问题：在线性模型中有效的隔离结构，在容量限制或非线性流量下仍有效吗？

34. **N034 — Spatio-temporal propagation of cascading overload failures in spatially embedded networks**
   Nature Communications（2016；Article） · [DOI](https://doi.org/10.1038/ncomms10094) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Comparison between simulation and theory；Results / Comparison between simulation and theory（指定段落摘读）。
   - 方法启发：跟踪空间网络中过载再分配的传播位置和速度，并比较理论与模拟。
   - 迁移（推断）：道路或配送失效题可记录故障扩散半径及时间，而不仅计算最终损失节点数。
   - 验证问题：不同容量裕量、攻击位置和网络形状下，传播速度能否被同一关系解释？

35. **N035 — Memory in network flows and its effects on spreading dynamics and community detection**
   Nature Communications（2014；Article） · [DOI](https://doi.org/10.1038/ncomms5630) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Modelling second-order Markov dynamics；Results / Memory and spreading processes（指定段落摘读）。
   - 方法启发：用二阶马尔可夫记忆网络表达下一步移动对上一地点的依赖，并考察流量与排名。
   - 迁移（推断）：疏散路径或人流题可将上一路段加入状态，以表达转向与连续路径约束。
   - 验证问题：二阶模型对留出路径的预测改善，是否足以抵偿更多状态和数据需求？
   - 来源附注：方法对非遍历及稀疏二阶路径引入处理规则；缺少二阶数据时会回退使用一阶信息。

36. **N036 — Similarity and economy of scale in urban transportation networks and optimal transport-based infrastructures**
   Nature Communications（2024；Article） · [DOI](https://doi.org/10.1038/s41467-024-52313-6) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Modeling network design in transportation networks；Introduction / Introduction（指定段落摘读）。
   - 方法启发：从起终点和规模经济出发，用最优运输思想生成网络并量化与现实结构的相似度。
   - 迁移（推断）：交通或设施布局题可从需求点生成候选连接，在建造成本与共享通道效率间权衡。
   - 验证问题：候选网络在不同需求分布下能否兼顾成本、服务覆盖和断边韧性？
   - 来源附注：讨论明确指出该最优运输模型不能直接表达含环基础设施。

37. **N037 — A digital twin framework for urban parking management and mobility forecasting**
   Nature Communications（2025；Article） · [DOI](https://doi.org/10.1038/s41467-025-65306-w) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Simulation and what-if scenarios；Results / Statistical outputs and distributions（指定段落摘读）。
   - 方法启发：把历史与实时停车数据、时空预测和情景生成结合到城市停车管理框架。
   - 迁移（推断）：停车题可先建立可检验的时空需求预测，再用仿真比较停车位布局和管理规则。
   - 验证问题：留出地点及高峰时段的预测误差如何，生成情景是否符合独立统计规律？

38. **N038 — The effect of sustainable mobility transition policies on cumulative urban transport emissions and energy demand**
   Nature Communications（2023；Article） · [DOI](https://doi.org/10.1038/s41467-023-37728-x) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods；Methods / Limitations of the model（指定段落摘读）。
   - 方法启发：按年份模拟车辆淘汰与新增，将多种交通政策连接到累计排放和能源需求。
   - 迁移（推断）：交通减排题可用车队存量—流量模型比较换车、减量与出行方式转移。
   - 验证问题：改变车辆寿命和排放边界后，政策累计减排排序是否稳定？
   - 来源附注：讨论区分内生车辆改进政策与外生施加的出行需求减少。

39. **N039 — A stochastic model of randomly accelerated walkers for human mobility**
   Nature Communications（2016；Article） · [DOI](https://doi.org/10.1038/ncomms12600) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Private transportation data；Results / The current empirical view（指定段落摘读）。
   - 方法启发：用随机加速与出行时间机制解释移动距离，并检验单凭距离分布拟合的歧义。
   - 迁移（推断）：人流题可要求模型同时解释距离、时间和速度，比较多种生成机制。
   - 验证问题：不同机制都拟合同一距离分布时，哪一机制还能解释留出的速度和时间？

40. **N040 — Big-data empowered traffic signal control could reduce urban carbon emission**
   Nature Communications（2025；Article） · [DOI](https://doi.org/10.1038/s41467-025-56701-4) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Data sources；Methods / Simulation environment calibration（指定段落摘读）。
   - 方法启发：将城市道路及合成行程输入交通模拟，并通过校准连接信号控制与出行、排放指标。
   - 迁移（推断）：信号灯题可用可校准的交通模型比较控制规则，再核算时间、燃料和碳排放。
   - 验证问题：不同需求及校准误差下，信号控制收益是否仍存在且没有转移拥堵？

41. **N041 — Universal model of individual and population mobility on diverse spatial scales**
   Nature Communications（2017；Article） · [DOI](https://doi.org/10.1038/s41467-017-01892-8) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Model；Results / Model prediction and validation（指定段落摘读）。
   - 方法启发：将移动记忆与人口相关的机会竞争结合，并比较个人和总体的移动模式。
   - 迁移（推断）：出行需求题可在地点吸引力之外加入重复访问记忆，检验个体与总体的一致性。
   - 验证问题：同一模型能否同时再现访问频次、转移概率和总体OD流量？

42. **N042 — A simple contagion process describes spreading of traffic jams in urban networks**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-15353-2) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Modeling contagion dynamics of network traffic jams；Results / Empirical evidence（指定段落摘读）。
   - 方法启发：把道路拥堵传播和消散概括为宏观速率，以类似SIR的方程刻画拥堵路段比例。
   - 迁移（推断）：拥堵题可用传播—消散模型作为简洁基线，跟踪全网拥堵比例。
   - 验证问题：模型能否在留出城市或时段预测拥堵增长和恢复，而不仅拟合峰值？

43. **N043 — Data-driven analysis and forecasting of highway traffic dynamics**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-15582-5) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Spatiotemporal binning method；Introduction / Introduction（指定段落摘读）。
   - 方法启发：先把车辆轨迹聚合到时空网格，再用Koopman模态分解提取及预测交通模式。
   - 迁移（推断）：交通预测题可用低维模态表达时空变化，并与简单时序基线比较。
   - 验证问题：网格大小、模态数和预测时距改变时，留出预测是否稳定？

44. **N044 — Anomalous supply shortages from dynamic pricing in on-demand mobility**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-18370-3) · 排序与决策
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Data sources and acquisition；Methods / Comparison of surge dynamics（指定段落摘读）。
   - 方法启发：结合博弈模型与价格时间序列，分析动态定价下供给者的集体响应及供需失衡。
   - 迁移（推断）：共享服务定价题可让服务者响应价格规则，检验激励与实际可用供给的关系。
   - 验证问题：在需求冲击及不同响应规则下，定价是否仍改善服务可用性？

45. **N045 — Uncovering the spatial structure of mobility networks**
   Nature Communications（2015；Article） · [DOI](https://doi.org/10.1038/ncomms7007) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / A null model；Results / Robustness（指定段落摘读）。
   - 方法启发：把OD流量分成热点间等四类结构，再用保留边际信息的随机网络检验特征。
   - 迁移（推断）：城市出行题可用粗粒度流量签名比较区域，并用随机基线识别结构差异。
   - 验证问题：改变热点定义并保留OD边际总量后，城市分类还稳定吗？

46. **N046 — Reversible Power-to-Gas systems for energy conversion and storage**
   Nature Communications（2022；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Derivation of the aggregate contribution margins；Introduction / Introduction（指定段落摘读）。
   - 方法启发：建立可逆电—氢转换的经济模型，以电价波动、氢价与设备特征分析运行价值。

   - 验证问题：使用不同年份电价、转换效率和设备成本时，经济可行性如何变化？
   - 来源附注：基本模型简化假定可从冷态瞬时进入运行状态；文中另讨论启动过程。

47. **N047 — Climate change and its influence on water systems increases the cost of electricity system decarbonization**
   Nature Communications（2024；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods；Introduction / Introduction（指定段落摘读）。
   - 方法启发：耦合水系统与电力扩张模型，纳入气候对水电、制水用电和冷暖负荷的影响。
   - 迁移（推断）：水电或城市基础设施题可联合核算水与电需求，再设计多气候情景下的容量。

48. **N048 — Scenario-adaptive hierarchical optimisation framework for design in hybrid energy storage systems**
   Nature Communications（2025；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / A general design framework of HESSs for industrial parks；Results / Operational robustness of HESSs under uncertainties（指定段落摘读）。

   - 迁移（推断）：校园综合能源题可分别决策设备容量和逐时调度，并迭代检查两者一致性。
   - 验证问题：多气候及多负荷情景下，分层方案与联合优化基线的成本差距多大？


   Nature Communications（2022；Article） · [DOI](https://doi.org/10.1038/s41467-022-31233-3) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Stochastic programming model；Results / Results（指定段落摘读）。
   - 方法启发：两阶段随机规划共同决策发电、输电及淡化投资，并用情景调度处理需求和资源变化。
   - 验证问题：联合规划相比分开规划的优势，是否在相同边界、可靠性和情景下成立？

50. **N050 — A low-carbon electricity sector in Europe risks sustaining regional inequalities in benefits and vulnerabilities**
   Nature Communications（2023；Article） · [DOI](https://doi.org/10.1038/s41467-023-37946-3) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods；Methods / Evaluating regional sensitivity and adaptive capacity（指定段落摘读）。
   - 方法启发：把空间电力模型与收益—脆弱性框架连接，分别核算地区收益、敏感性和适应能力。
   - 迁移（推断）：设施布局题可同时评估总收益及其地区分配，明确谁获益、谁承担风险。
   - 验证问题：权重和地区聚合方式变化后，公平性结论及方案排序是否改变？

51. **N051 — Model structures amplify uncertainty in predicted soil carbon responses to climate change**
   Nature Communications（2018；Article） · [DOI](https://doi.org/10.1038/s41467-018-04526-9) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Posterior distribution of model parameters；Results / Uncertainties in soil carbon projections（指定段落摘读）。
   - 方法启发：比较不同土壤碳模型结构，并用贝叶斯参数集合区分参数与结构带来的预测不确定性。
   - 迁移（推断）：碳核算题可保留多个有依据的结构，再分别传播参数误差，比较结论范围。
   - 验证问题：即使参数均拟合良好，不同结构的预测方向是否仍有分歧？
   - 来源附注：讨论指出小尺度观测向全球模型约束的转换仍带来尺度与参数挑战。

52. **N052 — Constraining climate sensitivity and continental versus seafloor weathering using an inverse geological carbon cycle model**
   Nature Communications（2017；Article） · [DOI](https://doi.org/10.1038/ncomms15423) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Forward modelling；Results / Bayesian analysis sensitivity tests（指定段落摘读）。
   - 方法启发：用地质碳循环正向模型与代理观测比较，再通过贝叶斯反演约束参数。
   - 迁移（推断）：环境参数难直接测量时，可建立正向机制模型并用多类观测共同约束。
   - 验证问题：替换观测误差或代理数据后，反演参数与预测是否仍被约束？
   - 来源附注：讨论指出部分参数的线性趋势可能造成欠拟合和不确定性低估，并描述补充敏感性检查。

53. **N053 — Energy requirements and carbon emissions for a low-carbon energy transition**
   Nature Communications（2022；Article） · [DOI](https://doi.org/10.1038/s41467-022-33976-5) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Energy transition pathways；Methods / Energy requirements of fossil fuel and biomass technologies（指定段落摘读）。
   - 方法启发：在能源转型路径中核算建设、运行和维护所需能量与排放，区分毛供能和净供能。
   - 迁移（推断）：校园能源转型题可把设备建设及更新纳入生命周期，跟踪净可用能量和累计碳。
   - 验证问题：改变系统边界和设备寿命后，转型能量成本与碳回收期如何变化？

54. **N054 — Pricing indirect emissions accelerates low—carbon transition of US light vehicle sector**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-27247-y) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Demand﻿–side framework；Methods / Uncertainty analysis（指定段落摘读）。
   - 方法启发：把综合能源模型与生命周期评价结合，比较只计尾气和同时计间接排放的政策。
   - 迁移（推断）：车辆选择题可统一比较尾气、电力、燃料与电池生产排放，并设电网变化情景。
   - 验证问题：统一生命周期边界后，电力结构和电池成本变化是否改变技术排序？

55. **N055 — 21st-century modeled permafrost carbon emissions accelerated by abrupt thaw beneath lakes**
   Nature Communications（2018；Article） · [DOI](https://doi.org/10.1038/s41467-018-05738-9) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Permafrost carbon models and present-day emissions；Methods / Uncertainty（指定段落摘读）。
   - 方法启发：将渐进融化与湖下突变融化机制并列，结合多类观测评估碳反馈及不确定性。
   - 迁移（推断）：环境碳预算题可检查是否遗漏突变释放过程，再用情景加入相应排放项。
   - 验证问题：加入突变过程后，总排放变化主要来自结构选择还是参数取值？

56. **N056 — Intrinsic ecological dynamics drive biodiversity turnover in model metacommunities**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-23769-7) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Metacommunity assembly（指定段落摘读）。
   - 方法启发：空间多物种竞争模型表明，交互与扩散自身也可产生群落更替。
   - 迁移（推断）：生态变化题可先模拟无外部冲击的基线，再识别观测变化超出基线的部分。
   - 验证问题：固定环境下的内部波动能否解释数据中的更替幅度及时间尺度？

57. **N057 — Biodiversity stabilizes plant communities through statistical-averaging effects rather than compensatory dynamics**
   Nature Communications（2022；Article） · [DOI](https://doi.org/10.1038/s41467-022-35514-9) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Theoretical framework；Results / Empirical analyses（指定段落摘读）。
   - 方法启发：把群落异步性数学分解成统计平均与补偿效应，再用调查及实验数据检验。
   - 迁移（推断）：生态组合题可分解整体波动的来源，区分资源互补和独立波动平均化。
   - 验证问题：随机化物种时间序列后，稳定性改善中还有多少来自真实补偿关系？

58. **N058 — Temporal dynamics of climate change exposure and opportunities for global marine biodiversity**
   Nature Communications（2024；Article） · [DOI](https://doi.org/10.1038/s41467-024-49736-6) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Climate data；Introduction / Introduction（指定段落摘读）。
   - 方法启发：按年将温度轨迹与物种热适宜范围比较，分别统计暴露、机会和持续时间。
   - 迁移（推断）：栖息地变化题可用逐年阈值记录失去及新增适宜区域，加入迁移限制。
   - 验证问题：温度阈值、排放情景及扩散假设改变时，适宜机会能持续多久？

59. **N059 — The spatiotemporal scaling laws of urban population dynamics**
   Nature Communications（2025；Article） · [DOI](https://doi.org/10.1038/s41467-025-58286-4) · 疏散与网络流
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Data description；Results / Spatial and temporal scale invariance of population fluctuations（指定段落摘读）。
   - 方法启发：对移动设备人口网格时间序列做去趋势分形分析，比较时空尺度上的波动。
   - 迁移（推断）：城市服务配置题可检验需求波动随空间密度和时间聚合尺度的关系。
   - 验证问题：不同设备样本和网格尺度下，波动标度是否仍成立？

60. **N060 — More frequent extreme climate events stabilize reindeer population dynamics**
   Nature Communications（2019；Article） · [DOI](https://doi.org/10.1038/s41467-019-09332-5) · 传播与生态
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Study area and species；Introduction / Introduction（指定段落摘读）。
   - 方法启发：随机种群模型把年龄结构、密度依赖和极端天气共同纳入长期动态。
   - 迁移（推断）：野生动物题可比较一次冲击和重复冲击情景，跟踪年龄结构与灭绝风险。
   - 验证问题：保持平均天气相同而改变极端事件频率时，长期风险如何变化？

61. **N061 — Integrated optimization modelling framework for low-carbon and green regional transitions through resource-based industrial symbiosis**
   Nature Communications（2024；Article） · [DOI](https://doi.org/10.1038/s41467-024-48249-6) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods（指定段落摘读）。
   - 方法启发：从资源和技术数据库构建工业共生超结构，再做多目标优化和转型情景分析。
   - 迁移（推断）：循环经济题可把企业余热、废物和资源需求建成网络，比较成本、碳和利用效率。
   - 验证问题：所有物料与能量流是否守恒，方案对技术效率及资源价格是否敏感？

62. **N062 — Impacts of irrigated agriculture on food–energy–water–CO2 nexus across metacoupled systems**
   Nature Communications（2020；Article） · [DOI](https://doi.org/10.1038/s41467-020-19520-3) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Environmental impacts under model scenarios；Methods / Step 4: uncertainty calculation（指定段落摘读）。
   - 方法启发：用生命周期和跨地区联系框架同时核算农业的食物、能源、水、碳及外部地区影响。
   - 验证问题：扩大核算边界后，原先节省的水或碳是否转移到其他地区？

63. **N063 — Emulator-based Bayesian optimization for efficient multi-objective calibration of an individual-based model of malaria**
   Nature Communications（2021；Article） · [DOI](https://doi.org/10.1038/s41467-021-27486-z) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Calibration workflow；Results / Calibration workflow（指定段落摘读）。
   - 方法启发：用代理模型与贝叶斯优化寻找个体模型参数，并通过多个拟合目标及敏感性诊断校准。
   - 迁移（推断）：计算昂贵的仿真题可用代理模型筛选参数，再返回原模拟核验候选解。
   - 验证问题：代理选择的参数能否在原模拟及各个留出目标上保持良好拟合？
   - 来源附注：讨论说明校准搜索尚未系统证明到达全局最优。

64. **N064 — Learning about climate change uncertainty enables flexible water infrastructure planning**
   Nature Communications（2019；Article） · [DOI](https://doi.org/10.1038/s41467-019-09677-x) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Planning framework and scenarios；Results / Bayesian learning about climate change uncertainty（指定段落摘读）。
   - 方法启发：将未来观测带来的气候学习纳入基础设施规划，比较分阶段扩建与一次建设。

   - 验证问题：学习缓慢或观测误差较大时，分阶段方案仍能满足服务可靠性吗？

65. **N065 — Uncertainty in ensembles of global biodiversity scenarios**
   Nature Communications（2019；Article） · [DOI](https://doi.org/10.1038/s41467-019-09519-w) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Statistical analyses；Results / Species-level uncertainty analyses（指定段落摘读）。
   - 方法启发：交叉改变物种分布模型、扩散假设、气候模型及排放情景，分析多源预测分歧。
   - 迁移（推断）：生态预测题可做结构—参数—情景的组合实验，分别报告其对输出的影响。
   - 验证问题：不确定性来源的排序是否随地点、物种和评价指标而变化？

66. **N066 — Model-based financial regulations impair the transition to net-zero carbon emissions**
   Nature Climate Change（2024；Article） · [DOI](https://doi.org/10.1038/s41558-024-01972-w) · 排序与决策
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Simulation of a divestment strategy；Main / Main（指定段落摘读）。
   - 方法启发：比较不同碳强度行业的历史风险计量及投资组合调整，考察规则的激励效应。
   - 迁移（推断）：投资配置题可比较历史风险指标与面向未来的情景风险，说明规则如何改变资金流。
   - 验证问题：结构转变后，历史风险排序能否解释新时期损失和投资选择？

67. **N067 — Constraining the increased frequency of global precipitation extremes under warming**
   Nature Climate Change（2022；Article） · [DOI](https://doi.org/10.1038/s41558-022-01329-1) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：在气候模型集合中寻找历史极端降水变化与未来频率变化的关系，用观测约束分歧。
   - 迁移（推断）：极端天气题可检验历史可观测指标与未来响应的联系，再将观测误差纳入约束。
   - 验证问题：跨模型代际和排放情景验证时，历史—未来关系是否保持？

68. **N068 — Uncertainty in temperature projections reduced using carbon cycle and climate observations**
   Nature Climate Change（2013；Letter） · [DOI](https://doi.org/10.1038/nclimate1903) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用简化气候模型及温度、二氧化碳历史观测共同约束碳循环、气候敏感度与气溶胶影响。
   - 迁移（推断）：气候预测题可联合约束多个机制，保留参数间的权衡和相关性再传播不确定性。
   - 验证问题：独立扰动参数与保留联合观测约束时，预测区间及尾部概率差异多大？

69. **N069 — The costs of achieving climate targets and the sources of uncertainty**
   Nature Climate Change（2020；Article） · [DOI](https://doi.org/10.1038/s41558-020-0732-1) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用气候与综合评估模型构建元模型，校准文献范围并分解气候目标成本的不确定来源。
   - 迁移（推断）：减排成本题可用简化代理关系连接预算、经济情景和成本，比较目标约束与情景差异。
   - 验证问题：换用成本结构、经济路径及贴现假设后，不确定性来源的排序如何变化？

   Nature Climate Change（2021；Analysis） · [DOI](https://doi.org/10.1038/s41558-021-00998-8) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。

   - 迁移（推断）：技术推广题可建立情景来源表，比较预测分歧与结构假设的关联。
   - 验证问题：分组留出机构或模型后，解释预测差异的关联仍然成立吗？

71. **N071 — Observational constraints on low cloud feedback reduce uncertainty of climate sensitivity**
   Nature Climate Change（2021；Article） · [DOI](https://doi.org/10.1038/s41558-021-01039-0) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：PDF第6–7页 模型与方法；PDF第8页 Marine heatwave test case；PDF第13–16页 Implications for climate sensitivity（指定段落摘读）。
   - 版本：发表前稿（submittedVersion）；发表版逐字一致性未核验。
   - 方法启发：用去季节、去趋势的卫星异常估计多变量局部响应，以独立观测事件检验，再结合气候情景驱动。
   - 迁移（推断）：环境预测题可将局部响应模型与未来驱动分开，利用独立数据来源及异常事件检查外推。
   - 验证问题：换用独立观测系统和异常事件后，局部响应是否保持，未解释残差如何传播到预测？
   - 来源附注：发表前稿第15–16页指出，单篇涌现约束依赖气候模型给出的先验分布，应联合其他证据。第6–7页将线性模型未解释的变化计入不确定性；提取文本的公式符号有失真。

72. **N072 — Uncertainty in simulating wheat yields under climate change**
   Nature Climate Change（2013；Letter） · [DOI](https://doi.org/10.1038/nclimate1916) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：标准化作物模型比较区分作物结构、参数和气候输入导致的产量预测差异。
   - 迁移（推断）：农业预测题可统一输入及校准条件，比较多个产量模型的当前拟合与未来响应。
   - 验证问题：当前拟合同样好的模型，在升温及二氧化碳变化情景中是否仍一致？

73. **N073 — Assessing the size and uncertainty of remaining carbon budgets**
   Nature Climate Change（2023；Article） · [DOI](https://doi.org/10.1038/s41558-023-01848-5) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods；Main / Main（指定段落摘读）。
   - 方法启发：把剩余碳预算连接到温度目标、非CO2贡献和净零后的升温，并做计算稳健性检查。
   - 迁移（推断）：碳预算题可明确基准日期、累计量和概率目标，再传播关键项的不确定性。
   - 验证问题：改变非CO2路径和净零后温度假设时，剩余预算及达标时间变化多大？
   - 来源附注：所读方法对部分预算项独立抽样，并另用气候模拟器检查稳健性；应用时应核对变量依赖。

74. **N074 — Quantified, localized health benefits of accelerated carbon dioxide emissions reductions**
   Nature Climate Change（2018；Letter） · [DOI](https://doi.org/10.1038/s41558-018-0108-y) · 气候与碳核算
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Atmospheric Modeling；Methods / Health Impact Methodology（指定段落摘读）。
   - 方法启发：把加速减碳路径连接到空气污染协同变化，区分局部近期收益与全球长期收益。
   - 迁移（推断）：校园或城市减排题可同时估计碳和空气质量收益，并按地区及时段呈现。
   - 验证问题：排放因子、暴露分布和健康响应的不确定性是否改变方案优先级？
   - 来源附注：所读方法固定成对情景的气象条件；健康响应函数的地域适用性仍需检查。

75. **N075 — Damage function uncertainty increases the social cost of methane and nitrous oxide**
   Nature Climate Change（2023；Analysis） · [DOI](https://doi.org/10.1038/s41558-023-01803-4) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用多模型框架比较损害函数、气候和经济情景对温室气体社会成本的影响。
   - 迁移（推断）：环境损失评价题可把损害函数作为备选结构，分别展示贴现及经济路径的影响。
   - 验证问题：更换损害函数时，边际成本变化是否比参数扰动更大？

76. **N076 — Multi-year field measurements of home storage systems and their use in capacity estimation**
   Nature Energy（2024；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Battery model and relaxation phase detection；Main / Main（指定段落摘读）。


   - 验证问题：运行数据估计的容量能否预测独立容量试验及后续调度表现？
   - 来源附注：所读方法说明，电池管理系统内部耗电及平衡活动可能带来电流与荷电状态估计偏移，需要校正。

   Nature Energy（2024；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：分析水文、可再生发电和用电需求的时间关联，识别持续及复合能源短缺。

   - 验证问题：打乱气象序列后，长时间能源缺口是否被明显低估？

   Nature Energy（2022；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：在简化最小成本电力模型中比较核电灵活性、风光资源和深度减排约束。
   - 迁移（推断）：能源组合题可统一技术成本与资源条件，研究调节能力何时具有系统价值。
   - 验证问题：加入不同灵活性资源后，技术成本阈值和最佳组合是否变化？

79. **N079 — Implications of intercontinental renewable electricity trade for energy systems and emissions**
   Nature Energy（2022；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：在综合评估模型中加入跨洲输电连接，比较可再生贸易、投资与累计排放。

   - 验证问题：考虑输电容量、损耗和共同天气风险后，共享方案的收益是否保持？

80. **N080 — Heavy-duty truck electrification and the impacts of depot charging on electricity distribution systems**
   Nature Energy（2021；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。



81. **N081 — Hydropower plans in eastern and southern Africa increase risk of concurrent climate-related electricity supply disruption**
   Nature Energy（2017；
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：PDF第16–17页 Methods / Defining rainfall clusters；PDF第8、18–19页数据源与稳健性检查；PDF第7、12–14、19页假设与范围（指定段落摘读）。
   - 版本：发表前稿／作者接受稿（仓储元数据submittedVersion；PDF封面Accepted version）；发表版逐字一致性未核验。
   - 方法启发：将降雨时间序列用PCA降维和K-means聚类，再叠加流域与水电站容量，识别共同气候暴露。
   - 迁移（推断）：能源规划题可按共同天气动态对电源分组，在相同总容量下比较地区互补与冗余配置。
   - 验证问题：更换气象数据、聚类数及分析时段后，共同短缺分组是否稳定，降雨代理能否解释实际发电？
   - 来源附注：稿件第7、12、19页区分降雨、径流与实际发电，并说明待建坝完工及空间相关性延续等情景假设。第1页标为作者接受稿；仓储元数据记为submittedVersion。

82. **N082 — The design space for long-duration energy storage in decarbonized power systems**
   Nature Energy（2021；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。


   - 验证问题：能量成本与放电效率的扰动，对系统成本的影响是否大于其他参数？

83. **N083 — Asymmetric risk and fuel neutrality in electricity capacity markets**
   Nature Energy（2019；Article） · [DOI](https://doi.org/10.1038/s41560-019-0476-1) · 排序与决策
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用随机均衡模型分析容量市场对不同技术风险和投资结构的不对称影响。
   - 迁移（推断）：资源激励题可把参与者风险偏好与支付规则写入模型，再比较最终供给结构。
   - 验证问题：同一补贴规则在不同固定成本和运行成本技术间是否产生偏向？

84. **N084 — The role of flexible geothermal power in decarbonized electricity systems**
   Nature Energy（2024；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。

   - 迁移（推断）：综合能源题可让可调电源跨时段转移输出，再比较系统成本和替代容量。

85. **N085 — Modelling the potential for wind energy integration on China’s coal-heavy electricity grid**
   Nature Energy（2016；
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：将风资源潜力与电力系统运行约束结合，区分可发电量与可整合进电网的供给。
   - 迁移（推断）：能源题可先估计资源潜力，再用负荷、煤电灵活性及容量约束核算可利用量。
   - 验证问题：同一风资源下，改变调节约束和负荷形状会使弃风量变化多少？

86. **N086 — Historical dynamics of landslide risk from population and forest-cover changes in the Kivu Rift**
   Nature Sustainability（2021；Article） · [DOI](https://doi.org/10.1038/s41893-021-00757-9) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把人口位置、森林变化和滑坡危险联系到长期风险模型，区分危险与暴露。
   - 迁移（推断）：灾害疏散题可把危险度、居民分布及土地覆盖分开建图，再计算风险。
   - 验证问题：历史回放中，模型能否解释新增居住点与森林变化带来的风险变化？

87. **N087 — Actors’ diversity and the resilience of social-ecological systems to global change**
   Nature Sustainability（2019；Article） · [DOI](https://doi.org/10.1038/s41893-019-0236-z) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用实证支持的主体模型分析行动者数量、能力多样性和互补性与系统韧性的关系。
   - 迁移（推断）：社区应急题可用不同技能和响应规则的主体，比较同质团队与互补团队。
   - 验证问题：在相同人数和资源下，能力互补的优势是否跨冲击情景成立？

88. **N088 — Ecological risk assessment of marine plastic pollution**
   Nature Sustainability（2025；Article） · [DOI](https://doi.org/10.1038/s41893-025-01620-x) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：耦合海洋塑料空间分布、生物体型和污染物数据，分别评估摄入、缠绕及毒性路径。
   - 迁移（推断）：污染治理题可分开建暴露路径和受影响群体，比较多路径风险下的空间治理优先级。
   - 验证问题：改变体型分布、暴露关系和排放情景时，风险热点及治理排序是否稳定？

89. **N089 — Wisdom of stakeholder crowds in complex social–ecological systems**
   Nature Sustainability（2020；Article） · [DOI](https://doi.org/10.1038/s41893-019-0467-z) · 排序与决策
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：通过利益相关者图式模型聚合系统知识，并比较直接平均与分组后再聚合。
   - 迁移（推断）：多方决策题可先收集关系图，按角色分组整合，再以独立知识检验整体模型。
   - 验证问题：群体比例变化时，聚合图的偏差和关键关系是否稳定？

90. **N090 — Integrated scenarios to support analysis of the food–energy–water nexus**
   Nature Sustainability（2019；Analysis） · [DOI](https://doi.org/10.1038/s41893-019-0418-8) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用统一情景和桑基流图描述食物、能源、水之间的生产消费联系及策略响应。
   - 迁移（推断）：资源规划题可先建物质与能量账本，再比较饮食、节约和技术情景。
   - 验证问题：各流图是否守恒，跨情景比较是否使用一致的需求及排放边界？

91. **N091 — Global assessment of water challenges under uncertainty in water scarcity projections**
   Nature Sustainability（2018；Article） · [DOI](https://doi.org/10.1038/s41893-018-0134-9) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把社会经济与排放情景组合成概率水稀缺投影，同时分析中位数和不确定范围。
[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

92. **N092 — COVID-19 medical waste dataset and city-level disposal optimization strategies**
   Nature Sustainability（2025；Resource） · [DOI](https://doi.org/10.1038/s41893-025-01550-8) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：由检测—隔离—治疗链估计每日医疗废物，并结合城市处理能力设计处置策略。
   - 迁移（推断）：应急废物题可把病例阶段转化为每日处理需求，再用容量、运输与时效约束调度。
   - 验证问题：在需求峰值及跨城运输受阻时，积压量和处理时限是否仍可接受？

93. **N093 — African food system and biodiversity mainly affected by urbanization via dietary shifts**
   Nature Sustainability（2024；Article） · [DOI](https://doi.org/10.1038/s41893-024-01362-2) · 资源配置
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Model design；Methods / Model design（指定段落摘读）。
   - 方法启发：把城市扩张、观测饮食变化与土地利用部分均衡模型耦合，追踪生产转移及生态影响。
   - 迁移（推断）：城市粮食题可同时模拟土地占用和需求结构变化，并核算外地生产及间接排放。
   - 验证问题：只计城市占地与同时计饮食、生产转移时，粮食和生态结论差异多大？
   - 来源附注：所读方法不显式考虑食品间交叉价格效应，也不显式模拟果蔬系统。

94. **N094 — Leveraging biodiversity to maximize nutrition and resilience of global fisheries**
   Nature Sustainability（2025；Article） · [DOI](https://doi.org/10.1038/s41893-025-01577-x) · 资源配置
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：用鱼类地理分布和营养数据做分配优化，以互补物种组合满足多种营养需求并考虑韧性。
   - 迁移（推断）：营养或采购题可把多种营养下限与可持续供给写入约束，探索多样化组合。
   - 验证问题：相同总量下，组合能否满足所有营养约束，并在供应中断时保持可替代性？

95. **N095 — A multi-model assessment of food security implications of climate change mitigation**
   Nature Sustainability（2019；Article） · [DOI](https://doi.org/10.1038/s41893-019-0286-2) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：多模型比较气候减排政策与粮食安全的权衡，并明确未覆盖的直接产量效应。
   - 迁移（推断）：土地或碳政策题可同时分析价格、供给和弱势群体需求，并列出核算边界。
   - 验证问题：统一政策与输入后，模型分歧是否改变对粮食风险的判断？
   - 来源附注：摘要说明研究未评估气候变化对作物产量的直接影响。

96. **N096 — Discovering network dynamics with neural symbolic regression**
   Nature Computational Science（2025；Article） · [DOI](https://doi.org/10.1038/s43588-025-00893-8) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：以神经引导的符号回归搜索网络动力学公式，将高维搜索转化为等价低维问题。
   - 迁移（推断）：动态预测题可比较少量可解释候选公式，采用复杂度约束并用原系统数据检验。
   - 验证问题：推断公式在不同初始状态及含噪留出序列上是否有效且参数可识别？

97. **N097 — Autonomous inference of complex network dynamics from incomplete and noisy data**
   Nature Computational Science（2022；Article） · [DOI](https://doi.org/10.1038/s43588-022-00217-0) · 不确定性与模型比较
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：两阶段动力学推断同时学习节点及交互规则，并用缺失、噪声和异质性情景检验。
   - 迁移（推断）：网络数据题可推断候选动态关系，再在已知结构的模拟及留出观测上核验。
   - 验证问题：漏边、伪边及观测噪声增加时，推断机制与预测误差如何变化？

98. **N098 — A laboratory and simulation platform to integrate individual life history traits and population dynamics**
   Nature Computational Science（2022；Article） · [DOI](https://doi.org/10.1038/s43588-022-00190-8) · 传播与生态
   - 阅读：`ABSTRACT_REVIEWED`；证据：摘要。
   - 方法启发：把个体寿命、繁殖与食物条件的实测信息输入个体仿真，再连接到群体出生死亡动态。
   - 迁移（推断）：种群管理题可从个体生命史规则生成群体变化，比较寿命、繁殖和资源情景。
   - 验证问题：个体规则能否同时重现留出的年龄分布、出生死亡率和总数量轨迹？

99. **N099 — The impact of uncertainty on predictions of the CovidSim epidemiological code**
   Nature Computational Science（2021；Article） · [DOI](https://doi.org/10.1038/s43588-021-00028-9) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Methods / Methods；Results / Uncertainty in CovidSim（指定段落摘读）。
   - 方法启发：对大型流行病代码做参数敏感性和不确定性量化，并把观测验证与参数分析并列。
   - 迁移（推断）：传播题可筛选影响大的参数，再单独检查结构及情景偏差，不以窄参数区间代替验证。
   - 验证问题：收紧参数范围后，留出观测中的系统偏差是否仍然存在？
   - 来源附注：摘要明确区分参数、结构和情景不确定性，并报告需要观测验证。

100. **N100 — Constructing custom thermodynamics using deep learning**
   Nature Computational Science（2023；Article） · [DOI](https://doi.org/10.1038/s43588-023-00581-5) · 不确定性与模型比较
   - 阅读：`FULL_TEXT_SECTION_REVIEWED`；证据：Results / Modeling spatial epidemics；Results / Experimental validation（指定段落摘读）。
   - 方法启发：以已知物理原则约束数据学习，同时构建低维热力学坐标与宏观随机动力学。
   - 迁移（推断）：复杂仿真题可提取少量可解释状态变量，并要求其动态遵守守恒等已知约束。
   - 验证问题：低维模型能否解释留出轨迹及稳定状态，并满足所声明的物理约束？
