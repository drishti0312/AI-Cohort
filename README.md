# Credit Card Transaction Decision Agent

## 1. Problem Statement

The agent observes a credit-card transaction and must select one of four actions:

* **Approve**
* **Question**
* **Examine**
* **Decline**

The true state of the transaction — whether it is legitimate or fraudulent — is not known at the time of the decision.

The project explores how an AI agent can make sequential decisions under uncertainty by using customer history, estimating fraud probability, considering the cost of different actions, and requesting additional information when necessary.

---

## 2. Project Objective

The objective is to build a small, testable AI agent that can:

1. Observe a new transaction.
2. Compare it with the customer's historical behaviour.
3. Identify unusual transaction patterns.
4. Estimate the probability that the transaction is fraudulent.
5. Select an action based on the estimated fraud belief and action costs.
6. Ask for additional information when appropriate.
7. Make a final decision after receiving additional information.
8. Evaluate different decision policies using labeled test data.

The goal is not to build a production-ready fraud detection system, but to study decision-making under uncertainty using a working prototype.

---

## 3. Agent Design

The agent treats **fraud vs. legitimate** as a hidden state.

### Observable information

The agent can observe:

* Transaction amount
* Merchant
* Location
* Timestamp
* Customer's previous transactions
* Customer's home location

### Hidden state

The hidden state is:

* Legitimate transaction
* Fraudulent transaction

The agent does not use the fraud label when making its initial decision.

### Available actions

| Action       | Purpose                                                     |
| ------------ | ----------------------------------------------------------- |
| **Approve**  | Allow the transaction when the estimated fraud risk is low  |
| **Question** | Request additional information from the customer            |
| **Examine**  | Escalate an uncertain transaction for further investigation |
| **Decline**  | Stop the transaction when fraud risk is sufficiently high   |

---

## 4. Evidence Used

The agent compares the current transaction with the customer's transaction history.

It currently evaluates five types of evidence:

### Amount

Checks whether the current transaction is more than four times the customer's historical average transaction amount.

### Location

Checks whether the transaction location has appeared in the customer's previous transaction history.

### Merchant

Checks whether the merchant has appeared in the customer's previous transaction history.

### Frequency

Compares the time gap between the current transaction and the customer's previous transaction with the customer's historical transaction gaps.

### Velocity

Checks whether the customer has made at least three transactions within the previous 30 minutes.

These signals are represented as unusual/not unusual evidence, with missing information represented separately where applicable.

---

## 5. Decision Process

The agent follows this general process:

```text
Transaction
     ↓
Customer History
     ↓
Generate Evidence
     ↓
Estimate Fraud Belief
     ↓
Calculate Action Costs
     ↓
Select Action
     ↓
 ┌──────────┬──────────┬──────────┬──────────┐
 ↓          ↓          ↓          ↓
Approve   Question   Examine    Decline
             ↓
       Get additional
          information
             ↓
       Make final decision
```

For a Question action, the current prototype can request transaction confirmation. Missing location information can also trigger a location question.

---

## 6. Probability Model

The agent uses a simple Bayesian-style probability model to estimate fraud belief.

A **5% prior probability of fraud** is used as a design assumption.

This prior was intentionally chosen for the experiment and is not the same as the fraud prevalence in the synthetic dataset.

The model uses the likelihood of observing unusual evidence under:

* Fraudulent transactions
* Legitimate transactions

The evidence likelihoods are combined with the prior to calculate the agent's fraud belief.

### Important assumption

The current probability model treats the evidence signals as conditionally independent.

This is a simplification. In a real fraud-detection system, signals such as unusual location, merchant, amount, and transaction timing may be correlated.

---

## 7. Cost-Sensitive Decision Making

The agent does not select an action using fraud probability alone.

Each action has a different expected cost.

The current cost model is:

| Action   | Cost                                      |
| -------- | ----------------------------------------- |
| Approve  | Fraud belief × 100                        |
| Question | Fraud belief × 10 + Legitimate belief × 2 |
| Examine  | Fraud belief × 5 + Legitimate belief × 8  |
| Decline  | Legitimate belief × 20                    |

The agent selects the action with the lowest expected cost.

This allows the project to represent the fact that different mistakes have different consequences.

For example, approving a fraudulent transaction can be more costly than investigating an uncertain transaction, while unnecessarily interrupting a legitimate customer creates customer friction.

---

## 8. Dataset

A synthetic dataset was created specifically for this project.

### Dataset summary

* **Customers:** 1,000
* **Normal transactions:** 10,000
* **Fraudulent transactions:** 2,000
* **Total transactions:** 12,000
* **Fraud prevalence:** approximately 16.67%

The fraudulent transactions were generated using several patterns:

* High-amount fraud
* Location-based fraud
* High-frequency fraud
* Merchant novelty
* Mixed fraud involving multiple unusual signals

Some transaction records also contain missing location and merchant information to test how the agent handles incomplete information.

---

## 9. Experimental Setup

The dataset was divided into:

* **80% training data**
* **20% test data**

The split was stratified by the fraud label.

The test set contained:

* 2,400 transactions
* 2,000 legitimate transactions
* 400 fraudulent transactions

The fraud label was hidden from the agent during the decision process and was used only afterward to evaluate the decisions.

---

## 10. Decision Policies

Two policies were tested.

### Policy A

The agent uses the cost-based action selection described above.

### Policy B

A threshold-based policy was also tested:

| Fraud belief | Action   |
| ------------ | -------- |
| `< 0.20`     | Approve  |
| `0.20–<0.50` | Examine  |
| `0.50–<0.80` | Question |
| `≥ 0.80`     | Decline  |

Testing both policies allowed the project to examine how different decision rules change the balance between automatic decisions and additional investigation.

---

## 11. Results

### Policy A

| Metric                           |  Result |
| -------------------------------- | ------: |
| Accuracy                         |  99.62% |
| Precision                        | 100.00% |
| Recall                           |  97.75% |
| F1                               |  98.86% |
| Fraud automatically declined     |  97.75% |
| Fraud examined                   |   2.25% |
| Fraud approved                   |      0% |
| Legitimate transactions declined |       0 |
| Overall interaction rate         |   8.58% |

Policy A automatically declined 391 of the 400 fraudulent test transactions and sent the remaining 9 fraudulent transactions to Examine.

It did not automatically decline any legitimate transactions.

### Policy B

| Metric                           |  Result |
| -------------------------------- | ------: |
| Accuracy                         |  98.38% |
| Precision                        | 100.00% |
| Recall                           |  90.25% |
| F1                               |  94.88% |
| Fraud automatically declined     |  90.25% |
| Fraud examined                   |   9.75% |
| Fraud approved                   |      0% |
| Legitimate transactions declined |       0 |
| Overall interaction rate         |   8.54% |

Policy B was more cautious around uncertain transactions.

It sent 52 transactions to Examine, of which:

* 39 were fraudulent
* 13 were legitimate

Therefore, Policy B examined more cases instead of automatically declining them.

### Policy comparison

Policy A and Policy B demonstrate a trade-off.

Policy A automatically declines more fraudulent transactions.

Policy B moves more uncertain transactions into Examine, which gives the system more opportunities for additional investigation but also results in more legitimate transactions being examined.

Therefore, neither policy should simply be described as universally better. The preferred policy depends on how the system values fraud prevention, customer friction, and investigation capacity.

---

## 12. Failure Analysis

Five of the fraud cases that were not automatically declined were examined in detail under Policy A.

Examples included transactions with:

* Unusual frequency
* Missing location information
* Normal amount
* Familiar merchant

One additional case also had missing merchant information.

These cases received similar fraud beliefs because the agent currently represents evidence using relatively coarse Boolean signals.

### Important observation

The 9 fraudulent transactions not automatically declined by Policy A were **sent to Examine rather than Approved**.

Therefore, they are false negatives only when considering automatic decline as the fraud interception mechanism.

The agent still intercepted these transactions through escalation.

This distinction is important when evaluating the agent because an Examine action is different from an automatic approval.

---

## 13. Probability Decision Example

One transaction was selected for a detailed probability decision record:

**Transaction:** FREQ_C0514

The agent initially observed:

* Amount: 2496.94
* Location: Bengaluru
* Merchant: Max
* Amount unusual: No
* Location unusual: No
* Merchant unusual: No
* Frequency unusual: Yes
* Velocity unusual: No

The agent estimated:

**Fraud belief: 53.84%**

The initial action was:

**Question**

The agent requested transaction confirmation.

The simulated response indicated that the transaction was not made by the customer, resulting in:

**Final action: Decline**

The actual hidden label was fraudulent.

This example demonstrates the intended sequential process:

```text
Observe
   ↓
Estimate belief
   ↓
Question
   ↓
Receive additional information
   ↓
Final decision
```

The detailed record is available in:

`decisions/probability-decision-record.md`

---

## 14. Limitations

This project is an experimental prototype and has several important limitations.

### Synthetic data

The dataset is artificially generated and may not represent the complexity of real-world payment transactions.

### Simplified evidence

The evidence signals are mostly Boolean. This loses information about the degree of unusualness.

### Independence assumption

The probability model assumes conditional independence between evidence signals, which may not hold in real transactions.

### Manually selected prior

The 5% fraud prior is a design assumption rather than an estimate learned from the dataset.

### Customer-response simulator

The current Question flow uses a simulated customer response.

The simulator currently uses the hidden fraud label to determine whether the simulated customer confirms the transaction. This is an **oracle-based limitation** and should not be interpreted as realistic human feedback.

A future version should use noisy/probabilistic customer responses or actual human feedback.

### Immediate labels during evaluation

The true fraud label is available after the decision for evaluation purposes. Real fraud systems may receive confirmation much later through disputes, investigations, or customer reports.

### Not production-ready

The current system should not be considered suitable for deployment in a real payment environment. It is intended as a small experimental system for studying decision-making under uncertainty.

---

## 15. Project Structure

```text
student-project/
│
├── README.md
├── research-file.md
├── discussion-record.md
├── review-record.md
│
├── paper/
│   ├── main.tex
│   ├── references.bib
│   ├── figures/
│   └── preprint.pdf
│
├── src/
├── data/
├── experiments/
├── results/
│
├── decisions/
│   └── probability-decision-record.md
│
└── social/
    ├── linkedin-post.md
    └── x-thread.md
```

---

## 16. How to Run

### Requirements

The project uses Python and common data-science libraries including:

* pandas
* NumPy
* scikit-learn

### Steps

1. Place the customer profile and transaction CSV files in the project's data directory.
2. Open the Jupyter notebook containing the agent implementation.
3. Run the data-loading and preprocessing cells.
4. Generate customer histories and transaction evidence.
5. Calculate the training likelihoods.
6. Calculate fraud beliefs for the test set.
7. Run Policy A and Policy B.
8. Compare the resulting actions with the hidden fraud labels.
9. Generate the evaluation metrics and failure analysis.

The exact data paths may need to be changed depending on the local environment.

---

## 17. AI and Human Contributions

AI tools were used throughout the project to:

* Explain technical concepts
* Help reason about probability and decision-making
* Debug Python code
* Explore agent design alternatives
* Review the agent design
* Help structure the research and preprint

Human discussion is being conducted through relevant Reddit communities and X accounts as part of the project workflow.

The discussion record is maintained separately in:

`discussion-record.md`

AI-generated suggestions are treated as suggestions and are evaluated before being incorporated into the project.

---

## 18. Future Work

Potential improvements include:

1. Replace Boolean evidence with continuous risk features.
2. Model dependencies between evidence signals.
3. Replace the oracle-based customer simulator with realistic noisy feedback.
4. Update the fraud belief after receiving new evidence.
5. Test the agent on more diverse transaction patterns.
6. Evaluate calibration of the fraud probabilities.
7. Introduce delayed fraud feedback.
8. Test additional decision policies.
9. Compare against a simple baseline.
10. Study how decision thresholds affect customer friction and fraud interception.

---

## 19. Conclusion

This project demonstrates a small AI agent that makes transaction decisions when the true fraud state is hidden.

Instead of treating fraud detection only as a classification problem, the agent combines:

* Historical customer behaviour
* Multiple evidence signals
* Fraud probability
* Action costs
* Additional questioning
* Escalation through examination

The experiments show that changing the decision policy changes how the agent balances automatic fraud interception against additional investigation.

The main lesson from the project is that **building a fraud agent is not only about predicting whether a transaction is fraudulent. It is also about deciding what to do when the system is uncertain.**
