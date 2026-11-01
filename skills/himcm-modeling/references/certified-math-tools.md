# 按结构选择精确工具

这些是有限适用范围的实现，不是算法配额。先写原问题、全部约束和工具模型的对应关系；不适用就自行建模。数值、概率、偏好和边界的来源必须说明。下面路径均相对技能根目录。

## 同一模型下的联合范围

观测允许一族非递减函数A，已知区间长度L、0≤A0≤A≤A1及总积分I，目标是同一函数的区间[a,b]积分。分别给两个前缀范围再相减可能用到两条不同极端曲线，范围过松。直接优化共同函数可给更紧且可达的上下界。

写A(t)=A0+(A1−A0)Pr(T≤t)，端点单点赋值不影响积分；μ=E[T]=(A1L−I)/(A1−A0)，目标J=A0(b−a)+(A1−A0)E[max(0,b−max(a,T))]。分段线性函数在相邻断点的质量可移到端点而保持均值与期望，因此只需枚举断点0,a,b,L中至多两个原子。质量和一阶矩两个等式使最优顶点至多两点支撑；紧集保证达到。仿射下/上支撑线在所有断点的限制推广到整段，原子可行且原/对偶值相等认证紧界。A0=A1单独处理。

```json
{"kind":"bounded_monotone_integral","length":10,"lower_area":2,"upper_area":8,"total_integral":44,"start":3,"stop":7,"available":18}
```

```bash
python scripts/moment_bounds.py input.json --output bounds.json
python scripts/moment_bounds.py input.json --verify bounds.json --output check.json
```

此例界为80/7至152/7，同信息下独立前缀相减为34/5至124/5。18不能覆盖全类，22可以；证书给出具体反例。工具允许跳跃；若真实类别要求连续、斜率限制或额外观测，此界仍可作外界，但不能说两端在较小类别中可达或决策必然不确定。也支持`{"kind":"first_moment_piecewise_linear","points":[[0,0],[1,2],[2,1]],"mean":1}`的一阶矩期望界。没有实现高阶矩、带噪声识别或动力学。验证模式从独立原输入检查证书，不把优化器成功当证明。

## 参数未知而行动可已确定

对共同可行的有限纯行动，损失L_a(θ)=b_a+d_a·θ、θ在给定闭盒域，R_a=max_b max_θ[L_a−L_b]。有限max可交换；线性差在每个坐标按系数符号取上下端，得到精确最坏遗憾与达到点。R_a=0说明这个行动在整个所给范围最优，不要求参数已精确识别。无概率时不自行等概率。

```json
{"schema_version":1,"parameter_names":["x","y"],"bounds":[[0,1],[0,1]],"actions":["A","B","C"],"offsets":[0,0,"3/5"],"coefficients":[[1,0],[0,1],[0,0]],"all_actions_feasible_for_entire_box":true}
```

`python scripts/affine_box_decisions.py input.json --output result.json`。此例遗憾1/1/3/5；收窄到[7/10,9/10]后C全域最优。若允许各半概率的A/B混合，其期望损失遗憾为1/2，原纯行动答案不再是扩展类最优。共同仿射平移不改遗憾，但可能改变最坏绝对损失排序，先明确目标。相关不确定集合的外包盒只有保守覆盖；非线性损失或状态相关可行性不能直接套用。输出见证指向需要辨别的条件，不自动证明获取该信息值得其成本；信息价值另用finite_decisions.py或匹配原题的模型。

## 时间口径与状态变换

原目标T=Σw_i V⁻¹(V(h_i)+C_i)，C_i=C0+Σ_{k≤i}Δ_k。Δ_k是已按时间段积分的存量增量，不能直接输入年率；观测权重按原目标给出。年末增量加到平均基线再反演通常不同，也不能以先平均信用修复所有非线性偏差。真实反馈使Δ依赖状态时先解联合动态系统。

`temporal_state.py`只适用给定严格双坐标递增分段线性V和有限观测权重。JSON需schema=`finite-state-stock-v1`、increment_kind=`interval_stock_change`、state_unit/stock_unit/time_unit、initial_time、initial_incremental_stock、curve为[state,stock]对、samples行包含time/baseline_state/interval_increment/weight。数值用整数或精确十进制/分数字符串；此工具拒绝裸JSON小数。时间严格递增、权重非负且和1、所有原/新观测状态须在域内（包括权重0的行），拒绝外推/裁剪。原题目标有效时分别判断两种比较代理是否在域内，不能因错误代理无定义而丢弃合法目标。

前向修订的输出schema为`finite-state-stock-result-v2`，输入schema仍为v1。`EXACT_TARGET_WITH_UNDEFINED_PROXY`表示有限观测目标已算出，但至少一项代理的存量自变量越界；对应值为null，`proxy_diagnostics`给出具体自变量及合法区间。年末代理无定义时，其差值、误差界和`bound_verified`也为null，不能当成误差0、界成立或完整比较通过。年末代理有效而均值增量代理无定义时，前者的界仍独立有效。读取输出的程序须检查各项状态，不能只看退出码0。原输入或任何观测状态不合法仍退出2；程序不补造曲线延长段。此字段变化须随新快照独立验收，不回写历史结果。

```bash
python scripts/temporal_state.py input.json > NEW-result.json
```

重定向前确认路径全新；保存输入/脚本哈希和退出码。工具不提供`--output`。若所有段斜率≥a_min>0，则|P−T|≤Σw_i|V(h_i)+C_i−V(Σw_jh_j)−C_n|/a_min，其中P为年末代理。三次基线10、V=100h、增量均4，等权T=10.08、P=10.12；非线性节点(0,0),(1,1),(2,4)、两次基线1/2和3/2、增量均1/4，T=29/24而P=7/6，偏差可以反向。界只覆盖给定曲线内有限观测，不含模型识别、单位转换、连续时间积分或反馈误差。

一般矩界思路参考Bertsimas–Popescu (2005), DOI10.1137/S1052623401399903；这里的特例证明与实现独立展开。所有工具来自已留证根开发原型，尚无本集成版独立作者能力验收。源码、精确证书和反例用于约束主张，不据工具数量加分。
