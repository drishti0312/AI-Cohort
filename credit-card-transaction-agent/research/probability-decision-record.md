# Probability Decision Record

## 1. Problem

The agent's goal is to make a decision about a credit card transaction. For every transaction, the agent can choose one of the four actions:
1. Approve
2. Question
3. Examine
4. Decline

The hidden state is that the agent does not know whether the transaction is legitimate or fraudulent. The agent does not know the true state of the transaction.

So, this record shows how the agent decided under uncertainty and how additional information obtained through questioning changed the final decision.

---

## 2. Case

**Transaction ID:** FREQ_C0514

**Actual hidden state:** Fraud

The actual fraud label was hidden from the agent while the agent was making a decision. It was only used later to evaluate the decision.

---

## 3. Evidence Available to the Agent

For this transaction, the observed evidence was:

| Evidence          | Observation        |
| ----------------- | ------------------ |
| Amount            | ₹2,496.94          |
| Location          | Bengaluru          |
| Merchant          | Max                |
| Amount unusual    | No                 |
| Location unusual  | No                 |
| Merchant unusual  | No                 |
| Frequency unusual | True               |
| Velocity unusual  | No                 |

The main warning signal was unusual transaction frequency. Other signals do not appear to be unusual.

---

## 4. Prior Belief

The agent began with a **5% prior probability of fraud**:

* P(Fraud) = 5%
* P(Legitimate) = 95%

I chose this prior as a design assumption to represent a lower fraud rate than the one present in the synthetic dataset.
---

## 5. Posterior Belief

The agent combined the prior belief with the evidence and the likelihoods calculated from the training data.

**P(Fraud | Evidence) = 53.84%**

Therefore:

* Fraud belief = **53.84%**
* Legitimate belief = **46.16%**

The probabilities sum to 100%. 
At this point, the agent considered the transaction sufficiently uncertain that asking the customer 
for additional information was preferable to immediately approving or declining it.

---

## 6. Actions and Costs

The agent considers the cost of each possible action based on its current fraud belief

| Action   | Cost                                      |
| -------- | ----------------------------------------- |
| Approve  | Fraud belief × 100                        |
| Question | Fraud belief × 10 + Legitimate belief × 2 |
| Examine  | Fraud belief × 5 + Legitimate belief × 8  |
| Decline  | Legitimate belief × 20                    |

For this transaction, the lowest cost according to policy was to **Question**.
 This action allows the agent to get some additional information before making a final decision.

**Examine**

The idea behind examination is to avoid making an immediate decision when the transaction looks risky, but the evidence is not strong enough to decline that transaction.

---

## 7. Initial Decision

**Initial action: Question**

The agent did not automatically approve or decline the transaction.

Instead, it asks the customer for confirmation whether the transaction was made by the customer.

This was useful because the agent had a moderate fraud belief of 53.84%, but the evidence available to it was limited mainly to unusual transaction frequency. 

---

## 8. New Evidence after questioning

The simulated customer response was:

Transaction confirmation: False

In the current prototype, this means that the customer did not confirm making the transaction.

This new information strongly changes the interpretation of the transaction because it directly contradicts the assumption that the transaction was legitimate.

The response therefore provides additional evidence supporting the fraud state.

Important limitation: In this prototype, the customer-response simulator uses the hidden fraud label to generate the response. The agent itself does not receive or use the fraud label when calculating its initial belief. This simulation design is disclosed here because a real deployment would require an actual customer response or a separately designed response model.

---

## 9. Final Decision

After receiving a negative transaction confirmation, the agent selected:

**Final action: Decline**

The decision process was therefore:

**Observe → Estimate risk → Question → Receive confirmation response → Decline**

This demonstrates the intended role of Question as an information-gathering action rather than simply another classification label.

---

## 10. Actual Outcome

After the decision process, the hidden label was revealed for evaluation.

**Actual state: Fraud**

The final decision was **Decline**, which correctly prevented the fraudulent transaction from being approved.

For the automatic fraud-classification evaluation:

* Actual state = Fraud
* Final action = Decline
* Result = **True Positive**

---

## 11. Why Did the Agent Choose the Question?

The initial decision was influenced by the following factors:

* Fraud belief was **53.84%**.
* Transaction frequency was unusual.
* Amount was not unusual.
* Location was not unusual.
* Merchant was not unusual.
* Velocity was not unusual.

The agent therefore had a meaningful fraud signal but not enough evidence to immediately decline the transaction.

Instead of making a high-impact decision based only on one unusual pattern, it chose to **ask for additional information**.

The negative confirmation then provided a strong reason to decline the transaction.

---

## 12. Audit Information

The following information was recorded for this decision:

* **Transaction ID:** `FREQ_C0514`
* **Amount:** ₹2,496.94
* **Location:** Bengaluru
* **Merchant:** Max
* **Amount unusual:** No
* **Location unusual:** No
* **Merchant unusual:** No
* **Frequency unusual:** Yes
* **Velocity unusual:** No
* **Prior fraud belief:** 5%
* **Initial fraud belief:** 53.84%
* **Initial action:** Question
* **Question asked:** Transaction confirmation
* **Simulated response:** False
* **Final action:** Decline
* **Actual state:** Fraud
* **Evaluation result:** True positive

---

## 13. Key Takeaway

This case shows the value of treating the agent as a **sequential decision-maker rather than only a binary fraud classifier**.

The agent initially had only moderate confidence that the transaction was fraudulent. Instead of immediately declining it, it chose to ask a question and obtain additional information.

The negative transaction confirmation then led to a final **Decline** decision, which matched the actual fraud state.

This example demonstrates the basic decision loop:

**Observe → Estimate → Act to collect information → Update the decision → Take final action**

A major limitation of the current prototype is that the customer response is simulated using the hidden fraud label. A future version should replace this with real human feedback or an independently designed response model and explicitly calculate a second posterior probability after receiving the new evidence.
