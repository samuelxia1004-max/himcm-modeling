# O/F 获奖论文的可观察共同模式与反例

本文件依据 95 份已保存完整报告的逐篇阅读记录（O 55、National O 29、F 8、National F 3），并直接重读其中 31 份跨年份/题目的模型、试验及局限选页。来源覆盖与独立构思流程见 [award-thinking.md](award-thinking.md)。奖项由既有官方结果行核验字段确认；本次没有重新在线核验。93 份为独立报告，H140/H146 的完整报告位于 2025 Consortium 130 原合集。

“共同模式”指跨不同任务反复观察到、适合迁移的定性做法；下面的例证和反例支持其解释，未对 95 篇逐项统计发生率。**E** 标明报告实际内容，**I** 标明本次迁移推论，**U** 指未发表思考过程。奖项不能认证公式、程序或预测；这里没有重跑作者代码，也不预测或保证获奖。关键词频率未作为人工编码或官方评分使用。

页码是本地 PDF 从 1 开始的物理页序；与报告页眉可能不同。H140/H146 使用原始合集物理页序，合集本地文件名虽含 2024，内容为 2025 Consortium 130。定位同时给出章节或段落线索；来源 ID 对应末尾目录及包内 corpus 索引。


新增23篇标准O/F完整主文的逐页量化复核见[award-quantified-audit.md](award-quantified-audit.md)与对应索引；它与这里的31篇选页集重叠，阅读深度分别记录。量化不改变本文定性模式的范围。

## 1. 将任务变成有对象、有边界的可计算输出

p.15 “Parking Lot Method versus Popular Trail Method” 将两种搜索接成可执行时间线。H074（2012 B，购油，O）p.14 §3.3.4 把预测转成购买动作、成本及相对理想策略收益。H140（2025 A，清扫，O）pp.95/105 §1.2/3.4 先列每房确认和救助任务，再取各响应者完成时间最大值、报告分布。

**I：** 先写动作和成功的操作定义，选择与题意一致的均值、最大值、总量、覆盖或概率，再选模型。

**反例边界：** H083（2013 B，银行排队，National F）pp.6–7/15 把等待目标表述为每位顾客少于两分钟或零超限；[2013 官方题面](https://www.contest.comap.org/highschool/contests/himcm/2013problems.html) “Bank Service Problem” 开头明确是平均等待和平均队长（保存文本第184行，本次已核对）。p.7 另已视觉确认。迁移时用原题验收句校对指标与建议强度。高奖身份不免除题意复核。

## 2. 从机制建立状态、流量或空间表示

**E：** H033（2008 A，国债，National O）p.6 §III.a 从旧债、利息、支出和收入建立年度递推，并给单位和整数年时间域。

**I：** 从对象、资源和过程推导表示；逐条核对守恒、量纲、边界和转换。宏观与微观表示各有要回答的问题。

**反例边界：** H140（2025 A，清扫，O）p.104 §3.1.6 写搜索速度为基础步速的一半、搜索时间为面积除该速度。若单位仍是长度/时间，缺少有效搜索宽度或面积扫描率定义；正文选读不能确认程序如何处理。新模型需独立建立单位一致的时间式。

## 3. 用具体失败机制决定模型复杂度

**E：** H068（2012 A，麋鹿，O）p.6 §4.1 说明线性出生拟合残差虽无明显趋势，但无承载上限，因生态机制而重新表示人口依赖。H087（2014 A，疏散，O）p.16 §3.6 列出聚合吞吐无法区分少宽/多窄楼梯及其位置，随后引入元胞模型；p.22 §4.2 的配置比较展示其区分能力。H052（2010 B，社会议题，National O）p.9 记下八次多项式舍入敏感、过于繁复而降低阶数；p.33 外部州资料使作者反思原假设。

**I：** 先用自然基线暴露难点，再增加能改变关键输出、且可识别或可检验的机制。

**反例边界：** H095（2014 B，疾病，O）p.10 “Limitations” 明确死亡/疫苗扩展需要更多数据。p.17 “Weaknesses” 承认便利采样不代表总体。模型表达的丰富程度受参数证据和数据覆盖约束。

## 4. 多模型承担互补作用，并共享依赖链

**E：** H074（2012 B，购油，O）pp.9/14/16 是因素选择→概率预测→油箱购买决策，§4 说明模块间依赖与内部结构可替换。H034（2008 B，碳中和，National O）pp.5/16 把植树、土壤、燃料、藻类和 CCS 技术放进总收支与预算。

**I：** 把解释、预测、优化和评估分别分配给需要的模块；接口共享单位、时间尺度、来源和最终评价器。

**反例边界：** H006（2022 B，CO₂，F）pp.22/24 对多个模型输出求远期相关，并承认反馈函数人为设计、缺少支持。模型之间相关不提供真实远期观测。H034 p.16 “Weaknesses” 承认未计树木死亡再排放；模块组合仍要核对全生命周期净量。

## 5. 让权衡可见，重新标定评价尺度

**E：** H109（2016 A，铁人三项，O）p.19 §9.2 给封路、拥堵与公平权重变化后的方案选择表。p.30 指出分数范围过窄或偏低。

**I：** 保留原始目标及量纲，说明权重偏好和评分标定；扩展指标后重新检查分数与阈值的含义。

**反例边界：** H049（2010 A，共享单车，National O）p.18 “Calculations” 以不同变量的导数比形成权重；这种比较受单位选择影响。H146（2025 B，主办地，O）p.130 §5.2 明确熵权由数据变异量提供信息；p.142 列州级代理与静态政策限制。数据区分度、矩阵一致性和偏好合理性需要各自证据。

## 6. 使用基线、精确小例和独立对照解释结果

**E：** H074（2012 B，购油，O）p.14 §3.3.4 用后一年数据比较可实施策略与完全预见动态规划参照。p.40 “Overall remarks” 解释替代路径如何影响方案。

**I：** 把可行性、算法质量、数值稳定、真实准确性和决策收益分别核验；测试选择应能暴露当前模型失败。


## 7. 将敏感性连接到行动与数据优先级

H146（2025 B，主办地，O）p.134 §6 报混合系数下分数和名次，另列观众 ±10% 扰动；该页已视觉确认。

**I：** 先测试会翻转建议的参数、结构和偏好；记录扰动范围、抽样、重复量、原始输出与行动变化。高敏感输入指向优先采集的数据。

**反例边界：** H109（2016 A，铁人三项，O）p.20 §9.3 明确关键超越概率未经敏感性、每条件仅 5 次仿真。权重测试没有覆盖行为机制。仍需独立观测与联合扰动来支持真实影响强度。

## 8. 对建议复算资源、范围与现实可行性

H118（2017 A，无人机，O）p.24 给起飞、旋转、过渡、降落及总时长，与 20 分钟电池条件衔接。H123（2017 B，雪道，O）pp.13–14 把候选节点连成线路再作二元选择。H125（2024 B，HPC，F）p.23 §5.1 将能源、利用率与水耗结果分别写给政策制定者和公司。

**I：** 输出动作必须落到整数、地点、日程、预算、容量及合法路径；优化器输出后独立复算约束。

取整后约束及目标需要重新检查。H123 p.14 难度配比的文字指总长度，公式按选路计数表达；该页已视觉确认。同页写总长至少 160 miles，而[2017 官方题面](https://www.contest.comap.org/highschool/contests/himcm/2017problems.html) Part I 写 160 km（保存文本第63行，本次已核对）。移用前需复算单位、计数对象与路径可行性。H118 p.28 在 100 步离散检测中允许短暂低于安全间距，表内仍有接近机对；需检查连续轨迹最小间距再支持安全结论。

## 9. 局限要指向哪个输出会失效

**E：** H033（2008 A，国债，National O）p.20 “Weaknesses” 指 Hauser 假设、恒定增长/利率和中间年可靠性。H125（2024 B，HPC，F）p.23 §5.2.2 说明只有运营阶段，排除建设与硬件更新。H146（2025 B，主办地，O）p.142 “Weaknesses” 指州数据代理、单位和静态政策。

**I：** 写清假设→受影响结果→失效场景→修复需要的数据或机制；推荐范围据此收窄。

**反例边界：** H052（2010 B，社会议题，National O）p.33 外部资料使原假设受到挑战；这应改变下游政策结论，不能停在局限清单。H125 p.23 的“Accurate / Objective”等作者自评仍需独立证据支持。局限与优点文字各自只是报告声明。

## 10. 以统一的任务—结果链组织沟通，并终审一致性

**E：** H068（2012 A，麋鹿，O）p.16 将敏感出生率连接到监测繁殖建议；H125（2024 B，HPC，F）p.23 分受众建议。这些段落显示方法、结果和行动之间的沟通连接。

**I：** 先冻结结果，最后写能独立读懂的摘要；每项数字、图表和行动绑定同一要求及当前计算证据。主线清晰与真实校验需要同时完成。

需要用保存输入复算定位。H140（2025 A，清扫，O）p.112 表中 School–Fire 的 K=8、95th=28.63，而紧接 §6 写所有验证用 K=3、§6.1 写 School–Fire 95th=43.7。这里仅确认文内冲突，未判断哪个运行正确。高奖报告同样需要数字、场景、单位和摘要终审。

## 可以观察到多少“构思”

把这些理由归纳成“先找结构、用失败场景决定扩展、让实验选择方案”属于 I。实际先后顺序、所有未采用方案、搜索来源、失败运行及团队对话属于 U；本文件不代替真实实验日志。

## 本次正文来源目录

下列 31 份的 90 个页段全部在本次直接选读。题目名称是任务描述，原奖项标签保留。其他引用主要依据抽取正文，并沿用既有阅读记录中的提取限制。

| ID / 队号 / 年题与任务 | 奖项 | 直接读的物理页 | 原始来源 |
|---|---|---|---|
| H006 / 12664 / 2022 B CO₂ 与温度预测 | Finalist | 12, 22, 24 | [PDF](https://raw.githubusercontent.com/lycLTb/HiMCM_2022/main/paper/latex/12664.pdf) |
| H011 / 14632 / 2023 A 蒲公英传播与入侵影响 | Outstanding | 4, 10, 12, 13 | [PDF](https://charlestang.dev/HiMCM2023.pdf) |
| H033 / 2159 / 2008 A 国债与财政政策 | National Outstanding | 5, 6, 19, 20 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2008/A/2159.pdf) |
| H034 / 1955 / 2008 B 碳中和技术组合 | National Outstanding | 5, 16 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2008/B/1955.pdf) |
| H049 / 2543 / 2010 A 共享单车站点 | National Outstanding | 18, 29, 31 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2010/A/2543.pdf) |
| H068 / 3697 / 2012 A 麋鹿种群 | Outstanding | 6, 16 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2012/A/3697.pdf) |
| H074 / 3874 / 2012 B 油价预测与购油 | Outstanding | 9, 14, 16 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2012/B/3874.pdf) |
| H081 / 3956 / 2013 B 银行排队 | Outstanding | 7, 20, 22 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2013/B/3956.pdf) |
| H083 / 4093 / 2013 B 银行排队 | National Finalist | 6, 7, 15 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2013/B/4093.pdf) |
| H087 / 4671 / 2014 A 列车站台疏散 | Outstanding | 8, 16, 22 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2014/A/4671.pdf) |
| H095 / 5325 / 2014 B 未知疾病与控制 | Outstanding | 10, 14 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2014/B/5325.pdf) |
| H109 / 7055 / 2016 A 铁人三项分波 | Outstanding | 13, 19, 20 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2016/A/7055.pdf) |
| H111 / 6829 / 2016 B 仓库覆盖与税负 | Outstanding | 13, 28, 29 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2016/B/6829.pdf) |
| H118 / 8028 / 2017 A 无人机灯光与过渡 | Outstanding | 24, 28, 31 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2017/A/8028.pdf) |
| H123 / 8124 / 2017 B 雪道设计与评价 | Outstanding | 13, 14, 26 | [PDF](https://raw.githubusercontent.com/CanfengMenghan/HiMCM/master/Past%20Essays/2017/B/8124.pdf) |
| H125 / 15803 / 2024 B HPC 能耗与环境影响 | Finalist | 6, 19, 23 | [PDF](https://raw.githubusercontent.com/q1zhen/2024-himcm/master/15803.pdf) |
| H140 / 16603 / 2025 A 建筑紧急清扫 | Outstanding | 95, 104, 105, 112, 113 | [PDF](https://www.contest.comap.org/highschool/contests/himcm/flyers/Cons_HiMCM.pdf) |
| H146 / 16442 / 2025 B 赛事主办地环境评价 | Outstanding | 124, 130, 134, 142 | [PDF](https://www.contest.comap.org/highschool/contests/himcm/flyers/Cons_HiMCM.pdf) |

2025 两条 PDF 链接是会更新的 COMAP 同名入口；精确对象是本次保存的 2025 Consortium 130，需按页首队号核对版本。原合集 SHA-256：`57d53ff270caeabf94bb446e7cc72f7c7ea0be3b3e7227af04450d5865796bcc`。两队的派生节选文件及其页序不能替代原合集定位。

完整 95 条记录及正文选页证据见包内[来源阅读审计](../validation/award-source-synthesis.json)；原始论文的大型资料库用于溯源核查，执行本流程无需载入它。语料是便利样本，无法据此证明某做法导致某奖项；正文选页也没有完成逐式、逐图、逐程序正确性认证。使用这些经验时先按新题独立构思，再用原题约束和本地实验验证。
