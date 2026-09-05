# Probability Decision Record

## 1. Problem

The agent observes a credit-card transaction and must select one of four actions:

* Approve
* Question
* Examine
* Decline

The hidden state is whether the transaction is legitimate or fraudulent.

The agent does not observe the true fraud label when making its decision.

---

## 2. Case

**Transaction ID:** LOC_C0997

**Actual hidden state:** Fraud

The actual state was hidden from the agent during decision-making and was only used afterward for evaluation.

---

## 3. Evidence Available to the Agent

For this transaction, the observed evidence was:

| Evidence          | Observation        |
| ----------------- | ------------------ |
| Amount unusual    | False              |
| Location unusual  | None / unavailable |
| Merchant unusual  | False              |
| Frequency unusual | True               |
| Velocity unusual  | False              |

The strongest available signal was unusual transaction frequency.

---

## 4. Prior Belief

The agent used a prior fraud probability of **5%**:

* P(Fraud) = 0.05
* P(Legitimate) = 0.95

This prior was chosen as a design assumption representing a lower real-world fraud prevalence than the synthetic dataset.

---

## 5. Posterior Belief

After combining the prior with the observed evidence and the likelihood estimates learned from the training data, the agent calculated:

**P(Fraud | Evidence) = 0.619666**

Therefore:

* Fraud belief = **61.97%**
* Legitimate belief = **38.03%**

The probabilities sum to 100%.

---

## 6. Actions and Costs

The agent evaluates four possible actions using the following cost model:

| Action   | Cost                                      |
| -------- | ----------------------------------------- |
| Approve  | Fraud belief × 100                        |
| Question | Fraud belief × 10 + Legitimate belief × 2 |
| Examine  | Fraud belief × 5 + Legitimate belief × 8  |
| Decline  | Legitimate belief × 20                    |

For a fraud belief of approximately 0.6197, the agent's decision rule selected:

**Examine**

The purpose of the Examine action is to avoid making an irreversible automatic decision when the evidence indicates substantial risk but does not provide enough confidence for automatic decline.

---

## 7. Decision

**Initial action: Examine**

The transaction was not automatically approved or declined.

This was an uncertainty-management decision: the agent identified meaningful fraud risk but did not consider the evidence sufficiently strong for automatic rejection under the selected policy.

---

## 8. New Evidence

The examination stage was designed to inspect additional recent customer activity.

For the current prototype, examination is treated as an escalation endpoint rather than automatically updating the posterior belief.

Therefore, no new posterior probability was generated for this case.

This is a limitation of the current prototype and an important direction for future work.

---

## 9. Final Outcome

The actual hidden state was later revealed during evaluation:

**Actual state: Fraud**

The agent had therefore identified the transaction as sufficiently suspicious to examine, but it did not automatically decline it.

Under the evaluation definition, this counted as a false negative for automatic fraud classification because only `Decline` was treated as an automatic fraud prediction.

However, the transaction was still intercepted by the agent's broader escalation process.

---

## 10. Reason for the Decision

The main reason for choosing Examine was the combination of:

* relatively high fraud belief (61.97%);
* unusual transaction frequency;
* unavailable location information;
* normal amount;
* normal merchant history;
* normal velocity.

The agent therefore had evidence of risk but incomplete supporting evidence.

---

## 11. Audit Information

The following information should be retained for an auditable decision:

* Transaction ID: LOC_C0997
* Fraud belief: 0.619666
* Amount unusual: False
* Location unusual: Missing
* Merchant unusual: False
* Frequency unusual: True
* Velocity unusual: False
* Initial action: Examine
* Actual state: Fraud
* Evaluation result: Automatic false negative / escalated fraud

---

## 12. Decision Insight

This case demonstrates why a transaction agent should not be evaluated only as a binary fraud classifier.

The agent had a substantial fraud belief but did not automatically decline the transaction. Instead, it selected an escalation action because the evidence was incomplete.

The case also exposed a limitation: the current Examine action does not yet feed additional evidence back into the probability model.

This motivates future work on sequential evidence gathering and posterior updating.
