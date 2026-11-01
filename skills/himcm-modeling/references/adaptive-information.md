# Choose experiments by their effect on the decision

Use this only when observations arrive before a final action and a concrete unresolved mechanism could change that action. First propose physically distinct hypotheses and a simple no-observation baseline. Translate useful tests into what they would distinguish and what decision would follow. A large candidate list, information entropy or a new method name is not evidence of contribution.

A test with no worthwhile one-step gain can belong to a valuable complementary pair. Conditional stopping can also beat a fixed shopping list of tests. Construct the smallest discriminating case; do not assume either effect exists in every problem. Report cases where the simple baseline wins. Keep idea generation, choosing experiments and verifying a policy as separate evidentiary steps.

## Exact finite tool and scope

`python -B scripts/adaptive_information.py input.json --output NEW_RESULT.json`

The tool minimizes **expected terminal loss plus observation costs** under one explicitly supplied joint prior. It supports up to64 joint worlds,16 actions,8 one-use tests and integer path-resource budget0..64. Test results are deterministic within each joint world; correlated noise must be represented by joint worlds, never multiplied as independent likelihoods without evidence. Every action must be feasible in every world. Tests cannot change the world, future observations or available actions. Losses and test costs have the same units; the separate resource budget is a hard per-path constraint. Cost is constant per execution of that test, independent of world/result. Repeated iid experiments need separately represented jointly distributed worlds and test instances; reusing a named test is unsupported.

No missing prior is silently replaced by uniform probabilities. If probabilities are only design assumptions, state conditional conclusions and show useful sensitivity or counterexamples. This Bayes tool does not solve minimax regret, ambiguity sets of priors, state-changing interventions, partial action feasibility or continuous processes. Use another justified method when those define the original question; never alter the question to fit the tool. For a fixed whole-policy prior set, commitment or randomized minimax claims, consult [the decision contract](decision-contract.md) before selecting a different formulation.

Input fields are exact; rational values use integers or strings, not floats. Example of syntax only:

```json
{"schema_version":1,"actions":["actA","actB"],"worlds":["w1","w2"],"probabilities":["1/3","2/3"],"losses":[[0,3],[2,0]],"tests":[{"name":"inspect","outcomes_by_world":["low","high"],"loss_cost":"1/5","resource_cost":1}],"resource_budget":1,"all_actions_feasible_in_all_worlds":true}
```

Loss rows follow action order; columns and each outcome vector follow world order. The sample's probabilities are hypothetical, not a recommended prior. Outputs include no-information loss, free perfect-information lower bound, best fixed test set, repeated myopic policy loss, all first-step continuation values and an adaptive policy tree. Output is exclusively created; preserve previous attempts. `--max-nodes N` bounds Bellman states; exceeding it returns INCOMPLETE with no optimum. This is a combinatorial model certificate, not certification of real data or a universal runtime guarantee.

## Why it is exact within scope

For consistent worldsS, remaining testsT and path resourceb, use original unnormalised probability massm(S):

`V(S,T,b)=min{min_a sum_(w in S) p(w)L(a,w), min_(t in T,r_t<=b)[m(S)c_t+sum_z V(S intersect {z_t=z},T minus t,b-r_t)]}`.

Any legal policy begins by stopping with an action or selecting an affordable unused test. Its branches have fewer tests; induction proves the recurrence optimizes all nonanticipating deterministic policies in this finite model. Under this fixed-prior expectation objective, a randomized mixture cannot improve on its best deterministic component. That argument does not apply to minimax randomized policies. Stopping is always available; nonnegative observation costs give free perfect-information loss <= adaptive total loss <= repeated myopic total loss <= no-information loss, and adaptive <= best fixed set.

Independently verify the chosen tree by tracing each raw world: accumulate only tests reached on that path, check no repeats and path budget, then add its terminal action loss and average under the stated prior. For small cases, enumerate legal trees with a different implementation or prove a lower bound attained by the policy. Do not call the same solver twice and describe that as independent verification. Sensitivity should change decisions or expose scope, not just produce decorative parameter sweeps.

## Evidence boundary

The source prototype was root-tested on25 small instances by separately enumerating6001 policies, with81 checks and17 actual CLI calls. These are development tests, not independent authors, whole HiMCM tasks, Q/I, field performance or award evidence. Limited reading motivating the decision-cost framing: Chen et al.(2015), https://las.inf.ethz.ch/files/chen15submsrgtvoi-long.pdf (abstract/introduction only); Heckerman et al., UAI1991, https://arxiv.org/abs/1303.5720 (abstract/version only); Zhao et al.(2021), https://proceedings.mlr.press/v130/zhao21c/zhao21c.pdf (abstract/introduction only). Their algorithms/theorems are not claimed to be implemented or replicated here.
