# 13篇原文方法链及HiMCM迁移

本参考直接核查以下13篇当前本地PDF的指定数据、处理、建模、验证、局限和决策段落：N008、N051、N064、N076、C025、R01、R06、R09、R15、R20、R28、R43、R50。页码均为**当前文件从1开始的物理PDF页序**，包含封面、附录和扩展数据；与期刊印刷页码分别记录。方法链覆盖从输入到输出的关键环节，读取方式主要为逐页PDF文本提取；R28公式另经页面图像核对。原始数据、源程序和结果未在本任务中重新运行。

背景学习库有231个独立DOI，按任一已保存版本的最高学习深度计，134篇有指定正文段落学习、97篇仅摘要学习。该范围来自现有学习卡与最终整合审计；与本次13篇直接核查分开。三份基础卡库的130篇正文/101篇摘要，在7份既有DOI的补充版本卡中有4篇新增正文段落学习，形成134/97。这里的“正文学习”是指定段落摘读。各文件SHA-256、实际读取页和旧卡定位核对见包内[来源方法链审计](../validation/nature-source-synthesis.json)。

下列“原文链”与“验证证据”陈述源论文内容；每篇“HiMCM迁移（推论）”是本技能提出的执行设计，其效果由赛题资料验证。文中精确输入年份、阈值、样本数、成本松弛及重复次数属于源研究设定。

## N008 — A universal model for mobility and migration patterns

DOI：[10.1038/nature10856](https://doi.org/10.1038/nature10856)。读取版本：arXiv仓储发表前稿，来源记录标为 `submittedVersion`，当前PDF共45页；封面未显示可核验的arXiv修订号，发表版逐字一致性尚未核验。标题核对p1。定位：模型构造p4–5；流量、距离、目的地检验p6–7；非均匀人口和改进p8–9；`1 Datasets / 1.1 US commuting` p20，迁移p20，货运和电话数据库p21，小时出行聚合p22；空间聚合与拟合误差p31–32。

**原文链。** Census 2000县间通勤长表提供34,116,820名通勤者、3,141县的OD；IRS 2007–2008迁移按相邻年度报税地址匹配判定；FAF3提供2007年货运OD；欧洲电话记录提供天线位置、用户和时间。电话移动分析以市镇而非天线为区域，降低运营商份额不均引起的人口口径问题；在六个月内将7–22时相邻小时同一用户的市镇变化聚合成小时OD。对每个起终点计算人口 `m_i,n_j`、距离及起点周围比目的地更近的机会人口 `s_ij`。就业机会与人口成正比，收益随机抽样；个人选择最近且优于本县最佳机会的工作，由此推导 `T_ij=T_i m_i n_j/[(m_i+s_ij)(m_i+n_j+s_ij)]`。收益分布及就业密度从平均流量公式中消去；总流出 `T_i` 仍需观测或由全国通勤比例和人口给定。输出为OD流量及其距离、目的地人口和条件流量分布。

**验证、误差和适用条件。** 原文以美国县间已观测通勤同时比较两种重力距离函数与辐射模型，并检查距离峰、目的地规模及固定人口/距离下的流量分布；另对小时移动、迁移、电话及货运做跨资料比较。p31–32将县聚为等人口选区和等面积网格，重力模型正流量对数均方偏差分别为1.43和0.96，说明空间分区影响拟合。该文读取段落没有预先冻结的整地区留出检验。机会人口代理、最近可接受机会规则及长距离行为影响解释；p9另加相当于35,000人口的本县优势参数，属于扩展模型。流量方差来自模型随机规则，覆盖抽样和机会代理误差还需额外观测设计。

**HiMCM迁移（推论）。** 建立人口/机会和少量实测OD表→独立计算每对区域的介入机会→先实现辐射与受总流出约束的重力基线→以整地区留出同时检查OD误差、距离分布和目的地分布→更换就业机会代理、分区及长距离规则→把合格流量送入交通容量或设施覆盖模型，并传播总流出误差。交付机会表、OD矩阵、三类验证图及在流量误差下的容量建议。

**定位修正。** 旧卡把数据来源列为p17；当前p17是图3图注。通勤数据正文在p20，完整数据来源链在p20–22。

## N051 — Model structures amplify uncertainty in predicted soil carbon responses to climate change

DOI：[10.1038/s41467-018-04526-9](https://doi.org/10.1038/s41467-018-04526-9)。读取版本：出版PDF，Nature Communications 9:2171 (2018)，11页。定位：`Posterior distribution of model parameters` p3；`Steady states in soil carbon stock` p3–4；`Uncertainties in soil carbon projections` p4；讨论与 `Methods / Models` p7–8；`Solutions for steady-state estimation` p8–9；`Datasets`、`Model-data fusion`、`Projection in soil carbon under RCP 8.5`、`Convergence of MCMC` p9–10。

**原文链。** HWSD土壤碳、NCSCD冻土碳及全球土壤微生物碳经NCL/ESMF保守重网格至CLM网格，保持区域碳总量；冻土区域以NCSCD替换HWSD。碳深度支持不同：普通模型聚合至非冻土1 m/冻土3 m，深度模型分层吸收数据，MIMICS仅1 m。三种结构分别为三碳库Century型、10层共30碳库的CLM4.5深度模型、显式土壤微生物碳模型；参数数目10、13、22。各模型用相同CLM历史凋落物输入，假定数据库碳库处于稳态，先解稳态状态，再以对数观测和观测映射构造似然。参数先验在指定范围均匀，部分MIMICS范围按默认值的1/3到3倍设定；Metropolis–Hastings构造后验，丢弃前2,500个接受样本，使用50,000个接受样本。每结构抽1,000组后验参数，在同一RCP8.5气候/凋落物驱动下推演2005–2100；普通和深度结构用月步长，非线性微生物结构用日步长避免长步长不稳定。

**验证、误差和决策含义。** 图3比较拟合数据库的空间偏差与误差，表1–2和p9–10用5条链的Gelman–Rubin统计检查收敛；它们支持拟合与数值过程。读取段落没有独立未来碳库预测检验。三结构的2100年碳变化区间分别为−71至−17、−222至583、−397至144 Pg C（原文称95% confidence interval），显示参数集合与结构共同改变范围和方向。三模型吸收的土深不同，因此比较还受观测支持差异影响；稳态、默认水分修正和先验范围限制外推。原文建议用多结构集合及额外约束数据提高投影可信度；该区间是本结构/驱动/参数集合范围的结果。

**HiMCM迁移（推论）。** 把碳、库存或资源观测对齐到共同边界→建立一简一繁的守恒结构→分别校准并检查收敛/残差→保留近似等价参数与结构→共同驱动下传播到政策输出→报告何种结构使方案排序改变。交付模型/观测映射表、结构×参数的输出分布及能够区分结构的新增数据需求。

## N064 — Learning about climate change uncertainty enables flexible water infrastructure planning

DOI：[10.1038/s41467-019-09677-x](https://doi.org/10.1038/s41467-019-09677-x)。读取版本：出版PDF，Nature Communications 10:1782 (2019)，11页。定位：`Planning framework and scenarios` p2、4；`Bayesian learning about climate change uncertainty` p4；讨论p7；`Bayesian modeling of climate change uncertainty` p7–9；`Estimating transition probabilities`、`Stochastic dynamic programming` p9–10；天气生成、径流模型和基础设施运行p10。

[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

## N076 — Multi-year field measurements of home storage systems and their use in capacity estimation

DOI：[10.1038/s41560-024-01620-9](https://doi.org/10.1038/s41560-024-01620-9)。读取版本：出版PDF，Nature Energy 9,1438–1447 (2024)，10页；物理p1对应印刷1438。定位：`Dataset of 21 home storage systems over 8 years` p2；运行与数据缺口p2–3；`Field capacity tests for method validation` p3–4；`Capacity estimation based on operational data` p4–6；`Battery model and relaxation phase detection` p6；`SOC calculation and current correction`、`SOH calculation` p7。

**原文链。按系统设计/电芯体系分组，审查数据可用性、缺口、电压/C率分布、温度、等效全循环和rainflow放电深度；BMS软件与截止电压改变作为解释条件。识别近满充/满放端点的低电流松弛阶段，以二阶RC等效模型的快/慢指数松弛和两阶段拟合估计OCV，限定时间常数范围。满充、满放松弛端点间进行库仑积分；用空到空/满到满闭环积分偏差校正未直接测量的BMS和平衡耗电电流偏置，并在端点重新校准SOC。可用容量除以名义容量得SOH，积分功率计算能量，容量估计随年龄拟合线性趋势。

**验证与不确定性。** 60次现场容量测试先满充、再以系统最大功率放至截止，用作运行数据估计对照。图4的浅蓝区含75%的算法估计点，属于估计点分布带；它不等价于未来SOH预测覆盖率。系统组平均宽度约4.4、6.8、8.0个百分点，LFP平坦OCV和全循环较少增加端点误差。LFP最大C率测试较早达到截止，现场测试系统性位于运行估计下端。论文以21系统验证当前估计，读取段落没有新系统整机留出测试。线性衰减长期外推受非线性拐点影响，额定容量、实际可用容量和厂商老化预留需要分开。决策输出支持寿命/容量判断，其工况和BMS边界随结果保留。

**HiMCM迁移（推论）。** 对一组设备建立缺口和端点日志→按电压/电流机制估可用容量并校正漂移→用测量途径独立的容量测试验证→保留设备间差异与容量误差→将衰减后的可用能量、功率和循环限制放进调度→用低容量/高负荷情景评估寿命成本。交付单位正确的Ah/kWh转换、设备级残差及随年份变化的可行容量。

## C025 — Human mobility networks reveal increased segregation in large cities

DOI：[10.1038/s41586-023-06757-3](https://doi.org/10.1038/s41586-023-06757-3)。读取版本：出版PDF，Nature 624,586–591 (2023)，当前文件26页，含Methods和Extended Data。定位：主结果p3、5，`Discussion` p6；`Datasets / SafeGraph` p8；`Data processing / Inferring home location / Inferring SES / Constructing the exposure network` p9–10；`Estimating exposure segregation / Bridging index` p10–12；`Hypothesis testing` p12；`Extended Data Fig. 2` p14。

**原文链。** 2017年3/7/11月SafeGraph原始资料为91,755,502用户、61,730,645,084个GPS点；联结CoreLogic住宅、Zillow估租、ACS、POI和TIGER道路。删除精度差于100 m点、低于500点用户、不能识别家/租金者以及>80%点重合的重复设备。住宅推断先线性插值到1小时，在18:00–09:00筛下小时移动<50 m的静止点，要求至少3日、至少60%点在50 m范围，取中位位置；最近住宅地址再查租金，检查住宅定位差异、异常同住映射，租金>20,000美元截尾。最终9,567,559用户。以5分钟内且50 m内的点对建立带时空属性的无向暴露网络，k-d树加速，得到1,570,782,460次暴露；POI标记可重叠。隔离指标定义为个人SES与其暴露对象平均SES相关性，线性混合模型通过个人随机项分开有限暴露噪声，以REML估计修正相关。桥接指数按最近枢纽聚类，计算各簇人口加权Gini相对于城市Gini；输出都市区隔离、活动/时间分解和枢纽布局指标。

**验证与局限。** p9报告89%的静止夜间观测在推定住宅50 m内，是住宅推断一致性。p10报告时间/距离/重复接触阈值改变的稳健性，p14将网络与Facebook友谊（县对Spearman 0.85、邮区对0.73）及代际向上经济流动（都市区−0.37）比较，支持暴露指标外部关联。10,000次bootstrap形成区间；p12声明未调整多重比较。关系是观察性空间关联，枢纽桥接与隔离相关不能单独证明新建设施的因果效果。采样偏向活跃手机用户、定位误差、租金SES代理及物理邻近与实际关系强度差别影响推广；稠密点对仍嵌套于个人和地区。

**HiMCM迁移（推论）。** 用可取得的聚合访问/接触资料定义设施服务网络→把同源定位、群体标签和指标误差逐项登记→计算覆盖与群体接触，保留住宅与访问两种基线→变动距离/时段/SES代理并按地区检查→对候选设施位置比较覆盖、公平和桥接，增加实际容量/通行约束。建议以条件关联或模型方案比较表达，实施效果需要适合的前后对照设计。

## R01 — Regional impacts of electricity system transition in Central Europe until 2035

DOI：[10.1038/s41467-020-18812-y](https://doi.org/10.1038/s41467-020-18812-y)。读取版本：出版PDF，Nature Communications 11:4972 (2020)，14页。定位：`Methods / Modeling approach / Soft-linked EXANSE-PyPSA model` p10–11（原小节标题拼作EXANSE，正文模型名EXPANSE）；`Input data and assumptions / Definitions of distinct scenarios` p11–12；`Evaluating regional impacts and regional equality` p12；讨论及边界p10。

**原文链。年度需求分配至650个NUTS-3区域，小时需求分配至100个电网节点；当前设备多源合并，资产寿命/最大增长/国家目标作为可行边界。EXPANSE以年分辨率分配发电容量；MGA对成本最优允许0–20%随机松弛，搜索100个尽量不同的布局。加1个冻结2018发电资产的共同2035假设基线，共101个方案。发电量/容量乘技术影响因子得到直接就业、排放、土地；成本等按人均、土地按总区域面积统一，区域平等为 `1−Gini`。从方案集合选最低成本、成本最平等、最多可再生发电方案并绘制权衡。

**验证与不确定性。未读取到独立2035预测验证。20%松弛引用既有英国1990–2014模型/现实成本差9–23%的研究，属于设定依据。100个MGA布局表达近优替代，不是带概率的未来置信区间。国家年需求必须本土发电满足，小时交易仍允许；5%资金成本、无显式税补贴、仅电力部门、直接影响因子和电网聚类限制解释。平等优化针对成本，其他影响分别评价，区域等权Gini与人口权决策有不同含义。

**HiMCM迁移（推论）。** 建立小型年度容量线性规划→围绕最优允许与本题预算相称的成本增加→产生差异较大的候选布局→以细时段供需/库存独立复算→按同一人口与土地分母比较公平、成本和资源→改变需求峰值、资源相关短缺及松弛预算。交付近优备选、细时段约束证书及公平目标变化时的方案切换。

## R06 — Traffic light optimization with low penetration rate vehicle trajectory data

DOI：[10.1038/s41467-024-45427-4](https://doi.org/10.1038/s41467-024-45427-4)。读取版本：出版PDF，Nature Communications 15:1306 (2024)，13页。定位：多周期轨迹聚合p5；重建验证/诊断p6；`Field implementation results` p7–8；讨论与离散队列p8–10；`Traffic state and parameter estimation` p10–11；`Traffic signal optimization` p11；`Vehicle trajectories, map, and signal timing data` p12。

**原文链。** GM轨迹点含trip ID、经纬度、时间、速度，约3秒间隔、3–5 m精度，每日约200万点/2.5万trip；估计渗透率约7%。匹配OpenStreetMap路段后将位置转为路段距离，联结道路机构SPaT信号表；同一时段多个周期的轨迹按整周期平移叠加成复发时空图，提取到达/离开直方图。离散随机点队列令到达为独立Bernoulli变量、绿灯且队列非空时离开，以队长概率递推构建概率时空图。假定时段内渗透率/到达率稳定，通过匹配观测平均延误与Little定律队列延误估计渗透率；多路口共同拟合加渗透率离散度正则。校准后固定需求，以总延误加权停车数为目标：周期/绿时调整沿梯度，走廊相对偏移用坐标下降和线搜索。输出诊断最优差距与可实施定时信号表。

**验证与局限。** p6比较校准数据的队列热图，IoU约69.92%，属于复发交通状态重建一致性。34个Birmingham（Michigan）路口系统部署后，走廊指标对照实施前3/7–3/25及后4/4–4/22的三周工作日数据；实际安装p12为3/31和4/1。Adams Road总体延误−12.23%、停车−18.51%，不同走廊/时段幅度不同，Old Woodward午间延误略增。分母是车辆经过**一个路口**的一条轨迹，不能把该数值写成整段旅程延误。前后比较是观察性实施证据；预处理窗口已用于拟合。模型要求平均需求低于能力，低渗透实时估计和溢出条件有限；偏移评价排除侧路，原始轨迹/SPaT受限。

**HiMCM迁移（推论）。** 聚合重复时段稀疏轨迹并保留日/路口单位→估需求/渗透并检查队列残差→先实现固定方案和简化队列基线→在固定外生需求下优化明确单位的延误/停车目标→用独立日期和拥堵压力情景验证→若使用现场前后证据，加对照走廊与季节/需求检查。交付每路口轨迹分母、可执行信号表和在溢出时失效的条件。

## R09 — Ecosystem-based fisheries management forestalls climate-driven collapse

DOI：[10.1038/s41467-020-18300-3](https://doi.org/10.1038/s41467-020-18300-3)。读取版本：出版PDF，Nature Communications 11:4579 (2020)，10页。定位：结果p3；讨论p6–7；区域气候降尺度、`Climate-enhanced multispecies stock assessment model / Evaluation of harvest management approaches` p7；`Determine the annual ABC / Simulate TAC / Simulate annual harvest (catch)` p8；风险/阈值分析p8–9。

**原文链。** 三种GCM×RCP4.5/8.5投影经ROMSNPZ/BESTNPZ降尺度；按历史底拖网调查的时空位置抽取海表/底温，并用调查区多边形提取季节浮游动物。以2006–2017回算期的均值/方差delta校正未来指数，另建气候保持历史均值的persistence基线。CEATTLE年龄结构模型以1979–2017调查生物量、摄食和渔获数据做惩罚最大似然拟合；温度改变生长/捕食，环境协变量和对数随机残差驱动繁殖。逐年投影资源→依据生物量和斜坡捕捞规则得ABC→ATTACH的历史ABC/TAC/政策回归推TAC与实际渔获→总TAC超过2百万吨时按比例压缩→将渔获从资源状态移除并推进一年。ATTACH含相互关联误差的SUR与回归集合，其他物种ABC固定历史均值。输出管理方案下生物量、渔获、衰退/崩溃风险；温度阈值用GAM平滑、导数及1,000次残差bootstrap。

**验证与不确定性。** p7引用降尺度回算模型既有评估；p8明确ATTACH作者以1992–2017逐年留一交叉验证比较TAC/渔获模型，优于“渔获=ABC”基线。该组件证据不等价于2018–2100整链验证。情景有过程波动、替代气候和实施差异；本文明确省略观测和运行模型参数估计误差，运行模型与隐含估计模型相同。100重复用于无捕捞/无总量帽、30用于总量帽情景；风险以相对基线>10%、>50%、>80%衰退定义。总量帽模拟既有制度分配，不是资源配置最优解。短期稳定可能掩盖资源下降，原文强调独立生物量早期预警。

**HiMCM迁移（推论）。** 为鱼群、森林或再生资源建立环境→增长→配额→执行→库存反馈→用多观测目标校准→组件分别留出验证→固定同一环境路径比较管理策略→加入观测偏差、参数误差、执行时延和不同结构→同时报告产出与资源存量、尾部衰退和预警阈值。交付逐期守恒账与稳定产出下资源恶化的诊断图。

## R15 — A Deep Gravity model for mobility flows generation

DOI：[10.1038/s41467-021-26752-4](https://doi.org/10.1038/s41467-021-26752-4)。读取版本：出版PDF，Nature Communications 12:6576 (2021)，13页。定位：评价和 `Derivation / Architecture of Deep Gravity` p3–4；训练与 `Experiments` p5；`Geographic transferability` p8–9；解释p9；`Regions of interest` p10；`Locations / Location features / Mobility flows` p10–11。

**原文链。** 英国/意大利2011普查通勤和纽约州手机访问流联结行政位置多边形及OSM土地、道路、POI。25 km方格为不重叠区域，再用位置质心分配OAs/CAs/CTs；只计算同一方格内OD。OSM节点/线/面分别变为计数、长度、面积，18类地理特征按位置面积标准化，另含两端人口与地理距离，共39个输入。单约束重力 `flow=origin_total×destination_probability` 等价于线性softmax目的地分类；Deep Gravity增加15层非线性，将分数softmax为概率后乘**已知起点总流出**。训练交叉熵，20 epochs、RMSprop、64起点batch、最多512负采样目的地。以重力G、仅非线性NG、仅多特征MFG作可解释复杂度对照；输出满足起点总量的OD和SHAP特征贡献。

**验证与局限。** 英国885、意大利1551、纽约475个25 km区域，按人口十分位将一半区域训练、一半测试，重复5次，评价CPC、Pearson、NRMSE和JSD；另改变10 km尺度。p8–9将英国9座主要城市逐个整城留出，防止同城不同方格互相泄漏，结果接近常规DG。CPC在起点总量一致条件下反映正确分配比例；结果没有验证未知总流出的生成。纽约“人口”由总流出估计，与普查人口口径不同；跨国和城乡迁移是原文提出的后续问题。SHAP解释模型分数贡献，支持关联解释；五次切分的波动不是所有未来地区预测区间。

**HiMCM迁移（推论）。** 先明确定量OD的起点总量来源→统一空间分区、位置面积和输入可用时点→实现约束重力/辐射基线→仅在整地区或整城市留出改善时增加特征和非线性→将总量误差另外抽样传播→用同一流量矩阵评价设施/运力。比赛的小资料可用多项logit或浅层模型实现核心思想，无需照搬网络规模。

## R20 — Solving groundwater depletion in India while achieving food security

DOI：[10.1038/s41467-022-31122-9](https://doi.org/10.1038/s41467-022-31122-9)。读取版本：出版PDF，Nature Communications 13:3374 (2022)，10页。定位：`Crop allocation optimization` p3；`Optimal cropping patterns, water, and energy use` p4；`Climate and groundwater data / Agricultural data / Estimating crop water deficit and yields` p7；`Objective function / Constraints / Scenarios` p8。

[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

**验证与局限。** p4与当前布局汇总比较，并将每类作物净单位收入逐次降低10–50%做稳定性检查，豆类更敏感。历史种植相似性来自农民网络交流的定性说明，读取正文没有独立产量预测或实施采购政策验证。期望生产/补给约束支持平均可行，旱年可靠性另需检验。统一补给/效率、成本和气温补足、历史种植适宜性及营养全国汇总影响可行域；平均优化可能把产地转型成本和群体承受能力留在模型外。

[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]

## R28 — River plastic emissions to the world’s oceans

DOI：[10.1038/ncomms15611](https://doi.org/10.1038/ncomms15611)。读取版本：出版PDF，Nature Communications 8:15611 (2017)，10页。定位：校准/结果p3；`Figure 2` p5；`Discussion` p5–7；`Model approach / Model formulation / Correction for surface waters / Estimating MPW mass in catchments worldwide` p7–8；月径流与图4流程、表4相关p8。公式p7同时做图像核查。

**原文链。** 182国人均垃圾/管理不当塑料废弃物（MPW）、人口栅格、地形自然排水、40,760流域、大坝以及GLDAS/NOAH月地表+地下径流组成输入。人均MPW×人口成1/4度废物源栅格，沿地形累计到河口；不通海流域排除、大坝作为全部截留汇，上游源不计入河口输入。校准资料为7研究、13河、30采样事件；数量/面积浓度经网深转体积浓度，再用微/宏比例和平均粒质量统一为质量浓度，乘采样表层水体通量成日质量释放。缺河深时用674条美/加河的流量—深度经验关系，河口用海图。以对应采样月份径流和坝下源量拟合 `M_out=(k M_mpw R)^a`，中点k=1.85×10⁻³、a=1.52。改变粒质量/比例得到低/中/高三条校准曲线，逐月计算后汇成全球年总量和河流/季节排名，用于监测与治理选点。

**验证与局限。** 中点r²=0.93来自同30记录拟合；p8表4去掉长江高杠杆点后，源量×月径流与质量浓度相关r=0.4132、p=0.026、n=29。加入坝和月而非年径流改善观测一致性；读取段落没有整河留出。源模型GLDAS引用66流域既有评价，主要支持季节峰值时序，未在本任务独立读取该研究。转换参数使全球低/高结果约相差一倍，1.15–2.41百万吨/年是这套转换/情景范围；还受浮性表层采样、粒径范围、亚洲观测不足、完全坝截留和人工渠道缺省影响。正文结果段用2005–2014月径流，方法段写2005–2015平均，此来源年份差别需复现时确认。MPW累计量正文及表4以t/年描述，图4以kg/日标注；单位转换时参数k也需按相同口径转换或重新校准。

**HiMCM迁移（推论）。** 以流域或服务区建立源—运输—汇图→明确质量/数量、表层/全水柱和瞬时/日量的转换→用采样同期外生变量校准→整河/整区留出并检验高杠杆观测→把源生成、观测转换和截留率分别变动→仅在这些变化下排名稳定时推荐治理点。交付源量守恒账、转换假设表及不确定性下排名切换图。

## R43 — Inherent spatiotemporal uncertainty of renewable power in China

DOI：[10.1038/s41467-023-40670-7](https://doi.org/10.1038/s41467-023-40670-7)。读取版本：出版PDF，Nature Communications 14:5379 (2023)，11页。定位：全国基准与因素p2；季节与利用率分析p4；`Discussions` p4–5；`Benchmark prediction model / Comparative prediction models / Prediction error calculation` p8–9；`First-order difference / Analysis and calculation of the peak ratio` p9。

**原文链。** 既有2016年30省小时风/光出力及装机容量，源文报告8,760小时，部分地理/资源省略。按装机容量归一化，太阳日变量取每天24小时**最大功率**，用于日波动分析。ARIMA先用ADF确定最少差分阶数d，以年中随机5周穷举各省p/q；其他参数随滑窗数据估计。168小时输入、6小时预测，逐小时滚动形成残差数据库；并用RF、FCNN、RNN、SVM比较2/6/24小时提前量。残差定义为(预测−实际)/装机容量，形成省、季、出力区间的分布；风按小时、太阳按日最大值算一阶差分，并以四时点上升再下降、累计增幅≥10%装机的规则算峰比。

**验证与局限。** 同年同源预测法/提前量比较、出力差分和误差关联支持这个基准下的误差刻画；读取段落没有另一年份前瞻检验。全年随机选调参周与严格只用过去数据的信息集不同。源文“inherent”通过指定时序模型与提前量操作化；天气预测、弃电和保守调度策略会改变误差分布。误差与差分须区分有符号偏差、绝对误差和分布宽度；汇总口径在复现时逐项对照方程/实现。2016与8,760小时的覆盖说明需要保留，时间戳完整性在使用原始数据时重新审核。

**HiMCM迁移（推论）。交付有符号偏差、MAE/RMSE和区间覆盖，日最大功率与日电量分别计算。

## R50 — Deforestation reduces rainfall and agricultural revenues in the Brazilian Amazon

DOI：[10.1038/s41467-021-22840-7](https://doi.org/10.1038/s41467-021-22840-7)。读取版本：出版PDF，Nature Communications 12:2591 (2021)，7页。定位：`Relationship between deforestation and rainfall at different geographical scales` p2–3；`Additional evidence for forest loss causation of rainfall reduction / Future critical forest loss thresholds and associated agricultural economic losses` p4–5；`Rainfall data / Deforestation data / Anomalies of annual rainfall` p5–6；`LUCC modelling and associated agricultural economic impact` p6。

**原文链。** 1999–2019 TRMM 3B43 v7月雨量汇成年量，约28 km栅格；PRODES约30 m森林损失汇为28/56/112/224 km格的森林损失比例。先以纬度、经度、海拔二次模型估地理雨量背景，原文r²=0.72；观测减空间背景，再减全区当年平均雨量，得到假定不被地理/共同年变化解释的残差。在各尺度拟合森林损失与雨量残差：较小三尺度用两段MARS，224 km用线性模型；比较小/大损失格在1999–2009和2010–2019两期的雨量，另用水分亏缺与损失空间关系检查反向解释。Otimizagro/Dinamica EGO的土地变化链模拟2015–2050弱/强治理，外生作物需求、损失和再生率决定土地面积；联结文献雨量—大豆/牧场减产效应和未来潜在生产力，算面积加权年收入、3.75%贴现NPV及年等值，用治理情景收入差计算机会成本。

**验证与局限。** 已有TRMM验证来自论文引用；本研究两期t检验、尺度比较、Cramer’s V/Spearman关联和反向解释检查增加观察性关系证据。p4明确称关系correlational；去趋势未保证所有混杂消除，读取段落没有空间/时间独立留出。小尺度阈值约55–60%、56 km约45–50%、112 km约25–30%，224 km线性下降；p3正文还出现112 km“≈23%”，p4和图示用27.5%，因此保留尺度范围和原文差异。未来收入是假定价格/农业实践固定、外生土地需求下的情景，原文的统计误差条不能自动覆盖价格、阈值和适应行为。该链将森林服务转为农业经济比较，推荐依赖空间范围和增长边界。

**HiMCM迁移（推论）。** 对齐遥感/气候时间与空间支持→分开背景趋势和研究关联→在数个聚合尺度比较线性/阈值模型→以空间块/后期年份留出、替代去趋势及混杂代理检查→将效应范围送入土地—收益情景→改变价格、折现、邻区森林变化及适应成本，报告阈值与方案排名的稳定范围。交付尺度×阈值证据表、情景经济账和条件化土地管理建议。

## 把13条链接回比赛工作

| 比赛需要 | 原文方法可提供的接口 | 本题须完成的核验（推论） |
|---|---|---|
| 稀疏观测转状态/流量 | N008机会排序；R06复发队列；N076端点与漂移校正 | 代理/抽样误差、独立日期/设备、单位与守恒 |
| 复杂模型是否值得 | R15基线与特征/非线性对照；N051多结构后验 | 冻结留出、参数可辨识、共同观测支持、决策分歧 |
[v5 已移出：含测试题主题词，原文见 _skills/v5_quarantine/quarantine_lines.jsonl]
| 空间汇总与行动排序 | R28源/汇网络；C025暴露与桥接；R50多尺度阈值 | 分母、尺度、样本覆盖、空间留出、指标/因果声明 |
| 不确定性进入优化 | R43条件预测残差；R01近优布局；N064学习触发 | 情景依赖、信息时点、独立可行性复算、排序切换 |

每个赛题只选择与声明相称的接口，先在一页分析合同中定义行动、时间、单位、外推对象和验收证据。最小输出链为 `原始来源/版本→处理记录→模型及观测映射→相称验证→不确定性→条件化建议`。模型内比较、独立预测、实地前后关联和因果效果分别提供所需证据；13篇案例给出了这些接口的实际使用和明确边界。
