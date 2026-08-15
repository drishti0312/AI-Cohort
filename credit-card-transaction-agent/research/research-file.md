# Credit Card Transaction Agent

## Problem Statement

The agent observes a transaction made using a credit card. It must select one of the four actions:
- Approve
- Question
- Examine
- Decline
because the true state of the transaction, i.e., whether the transaction is legitimate or fraudulent, is unknown.

## Project Objective

Design an AI agent that can make decisions and determine whether the credit card transaction is legit or not.

The agent should:
- Observe the transaction evidence.
- Check the probability that the transaction is fraudulent
- Compare the transaction with different factors
- Select an appropriate action 
- Review new evidence 
- Update the belief 
- Take the action

The goal is to create an AI Agent that will make better decisions under different situations.

## Technical Terms

- POMDP (Partially Observable Markov Decision Process) - a mathematical framework for making decisions when you cannot observe the complete environment.
- Sequential Decision-Making Under Uncertainty - making a series of decisions while dealing with incomplete information.
- Active Sensing - instead of quickly making a decision, the agent must actively collect more information.
- Cost-Sensitive Classification - treating different mistakes differently, as not all errors have the same cost
- Human-in-the-Loop - Humans are involved in the decision-making process 
- Dynamic Risk Scoring - Assigning a risk score that changes continuously as new evidence arrives
- Anomaly Detection - Finding transactions that do not follow the trend.
- Concept Drift - The relationship between inputs and outputs changes over time
- Credit Card Fraud Detection - The process of identifying fraudulent transactions in real time.
- Hidden State - Whether the transaction is actually fraudulent
- Delayed Feedback - The system may not know immediately whether it made the correct decision.
- Explainable AI (XAI) - Explaining why the transaction was flagged

---

## Search Queries

### Foundational Questions
1. Credit Card fraud detection under incomplete information.
2. POMDP fraud detection transaction approval.
3. Hidden State modeling in fraud detection.
4. Sequential decision-making in payment fraud detection.

### Machine-learning queries
1. Credit card fraud detection anomaly detection.
2. Cost-sensitive classification in fraud detection
3. Class imbalance in fraud detection
4. Fraud detection delayed feedback
5. Fraud detection concept drift
### Agent design queries
1. When should fraud detection systems send transactions for review
2. When should transactions be sent for manual review
3. Active learning in fraud detection

### Evaluation queries
1. Business impact of false positives in fraud detection
2. Precision-recall trade-off in fraud detection
3. Fraud detection evaluation metrics
4. Fraud detection ROC AUC vs precision-recall
---

## Reddit Communities

| Community | Why it is relevant |
| --- | --- |
| r/CreditCards | Customer experiences |
| r/FinTech | Payment systems |
| r/PaymentProcessing | Transaction authorization |
| r/MachineLearning | Fraud-detection models |
| r/MLQuestions | Beginner-friendly ML discussions |
| r/dataanalytics | Analytics-focused fraud projects and dashboards |
---

## Researchers and Engineers on X

- David Silver
- Michael I. Jordan
- Stripe
- Adyen
- Visa
- Mastercard
- Plaid
- PayPal

---

## Research questions about hidden state, evidence, actions, and errors

### Hidden-state questions
1. Is the transaction actually legitimate?
2. Is the card stolen?
3. Is the card physically with the cardholder?

### Evidence questions
1. What is the usual spending pattern of the cardholder?
2. How frequently does the cardholder use the card?
3. Is the merchant familiar?
4. Is the location new, or has the cardholder previously done the transaction from that particular location?

### Action questions
#### Approve
1. What is the confidence level required for approval?

#### Question
1. When should the system ask for otp verification?
2. When should the cardholder receive an approval message?

#### Examine
1. Which type of transaction should be sent to a human for investigation?
2. What evidence should the investigator need to look at?

#### Decline
1. How much evidence is needed for a transaction to get decline/block?

---
## Error questions
### False positive 
- What happens if a legitimate transaction gets blocked?
Possible cost -
1. Loss in sale
2. Bad customer experience
3. Merchant dissatisfaction

### False negative
- What happens if a fraudulent transaction gets approved?
1. Financial loss
2. Investigation costs
3. Harms reputation
4. Chargebacks
---
## Claims that require a source or an experiment
| Claim                                                           | Needs a source? | Needs a test? |
| --------------------------------------------------------------- | --------------- | ------------- |
| Fraudulent transactions are rare.                               | Yes             | Yes           |
| Fraud detection is a class-imbalance problem.                   | Yes             | Yes           |
| Sequence models outperform transaction-level models.            | Yes             | Yes           |
| Asking customers additional questions improves fraud detection. | Yes             | Yes           |
| Human review reduces fraud losses.                              | Yes             | Yes           |
| Concept drift reduces model performance over time.              | Yes             | Yes           |
| Dynamic risk scoring improves detection.                        | Yes             | Yes           |
| Explainable AI improves analyst decision-making.                | Yes             | Yes           |
| Real-time systems must balance speed and accuracy.              | Yes             | Yes           |
| False positives damage customer experience.                     | Yes             | Yes           |
