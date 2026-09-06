# Credit Card Fraud Detection Agent

## Abstract

Credit card fraud detection requires making decisions when the true state of a transaction is not immediately known. This project presents an AI agent that observes a credit card transaction and selects one of four actions: **Approve, Question, Examine, or Decline**. The agent uses information from a customer's past transactions to identify unusual patterns in amount, location, merchant, transaction frequency, and velocity. These observations are used to estimate the agent's belief that a transaction is fraudulent. The agent then selects an action based on this belief and the relative costs of different decisions. When additional information is required, the agent can question the customer or examine the transaction before making a final decision. The project explores how probability-based reasoning and sequential decision-making can be used to make transaction decisions under uncertainty.

## 1. Introduction

Credit card fraud is a common problem in digital payments. When someone obtains another person's card information, they may attempt to make transactions without the cardholder's permission. For a fraud detection system, however, the most important information—the true state of the transaction—is not immediately known. The system must decide whether to approve, question, examine, or decline the transaction using the evidence available at that moment.

This project focuses on designing an AI agent that makes these decisions under uncertainty. Instead of looking at a transaction in isolation, the agent compares it with the customer's previous transaction history. It examines factors such as transaction amount, location, merchant, frequency, and transaction velocity to identify behavior that is unusual for that customer.

The agent converts these observations into a belief about whether the transaction is fraudulent. It then combines this belief with the costs associated with different actions to select an initial action. In some situations, the agent can request additional information from the customer. The new information can then influence the final decision.

The goal of this project is not simply to classify every transaction as fraudulent or legitimate. Instead, the goal is to explore how an agent can make **sequential decisions when the correct state is hidden**, while balancing fraud risk against unnecessary customer friction.

## Related Work and Human Discussions

Credit card fraud detection has been widely studied using machine learning and statistical method. Exisiting research highlights multiple challenges faced which makes fraud detection different from other classifications. Simce the fraudelent transactions made are much less in frequency that the legitimate transactions hence agent does not have that enough fraudelent data which creates a class embalance.
In addition, customers purchasing pattern can change over the type. Previous research has therefore explored methods based on feature engineering, sequential transaction modeling, and models that can adapt to changing data distributions [1, 2].

One more challenge is that fraud detection is not only a prediction problem. A system must make a decision considering the concequences it will face depending on the transaction. For e.g. It a fraudelent transaction is improved it will create a financial loss, whereas if it incorrectly stopped a legitimate transaction that it will cratea bad customer experience.
This motivates a decision-making approach in which the estimated fraud risk is considered together with the consequences of different actions. 

My project usus a small and simpler version of this idea. instead of directly making any decision that whether the transaction is legitimate or fraudlenet, the agemt will choose between four actions : Approve, Question, Examine, Decline.
The agent uses customers transaction history to identify the agent to use different level if intervention rather than immediately making a decision.

### 2.1 Human Discussions

In addition to reviewing technical literature, we used online discussions to understand how people think about fraud investigations and transaction evidence in practice. These discussions were not treated as formal scientific evidence, but they helped identify questions and design considerations that were difficult to obtain from technical papers alone.

A discussion in r/legaladvice was particularly relevant to the role of additional evidence in fraud investigations. In the discussion, a user described a credit-card fraud claim that had been rejected because the transactions occurred in the same state as the cardholder. Responses suggested looking at additional evidence such as where and when the transaction occurred and whether other evidence could demonstrate that the cardholder could not have made the transaction.

This discussion influenced an important aspect of our agent design: **the initial decision does not always have to be the final decision**. When the available evidence is insufficient, the agent can Question or Examine the transaction instead of immediately approving or declining it.

Other discussions in communities related to small businesses, fintech, and machine learning were used to think about the types of evidence that could be useful in fraud detection and the trade-off between detecting suspicious behavior and creating unnecessary friction for legitimate customers. These discussions contributed to the choice of customer history, transaction frequency, location, merchant behavior, and transaction amount as initial evidence signals.

The human discussions also highlighted a limitation of simple anomaly-based reasoning. An unusual transaction is not necessarily fraudulent. A customer may legitimately travel, make an unusually large purchase, use a new merchant, or make several transactions within a short period. Therefore, the agent's evidence signals should be interpreted as indicators of risk rather than proof of fraud.

Based on the literature and human discussions, we designed the prototype around three principles:

1. **Use customer history rather than evaluating transactions in isolation.**
2. **Represent uncertainty explicitly through a fraud belief rather than assuming that an unusual transaction is automatically fraudulent.**
3. **Allow the agent to request or examine additional information when the available evidence is insufficient for a confident decision.**

These principles form the basis for the probability model and sequential decision process described in the following sections.

## 3. Agent Design

The proposed agent is designed as a sequential decision-making system for credit card transactions. The agent does not directly observe whether a transaction is fraudulent. Instead, it observes transaction information and customer history, estimates its belief about the hidden state, and selects an action based on the available evidence.

### 3.1 Problem Formulation

For each transaction, the agent observes information such as transaction amount, location, merchant, timestamp, and the customer's previous transaction history. The hidden state is one of two possibilities:

* **Legitimate:** the transaction was authorized by the cardholder.
* **Fraudulent:** the transaction was not authorized by the cardholder.

The agent must select one of four actions:

1. **Approve:** allow the transaction to proceed.
2. **Question:** request additional information from the customer.
3. **Examine:** escalate the transaction for additional investigation.
4. **Decline:** reject the transaction.

The agent therefore follows the general process:

$$
\text{Transaction} \rightarrow \text{Evidence} \rightarrow \text{Fraud Belief} \rightarrow \text{Action}
$$

When the available information is insufficient, the agent can request additional information before making its final decision.

### 3.2 Customer History

Rather than evaluating every transaction independently, the agent maintains access to the customer's previous transactions. The historical transactions are used to establish what is relatively normal for that customer.

For each new transaction, the agent retrieves transactions belonging to the same customer that occurred before the current transaction. The historical information is then used to evaluate five types of behavioral evidence:

* **Amount:** whether the transaction amount is unusually high compared with the customer's historical average.
* **Location:** whether the transaction location has previously appeared in the customer's transaction history.
* **Merchant:** whether the merchant has previously appeared in the customer's transaction history.
* **Frequency:** whether the time gap since the previous transaction is unusually short compared with historical transaction gaps.
* **Velocity:** whether several transactions have occurred within a short recent time window.

These signals are represented initially as Boolean evidence indicating whether a behavior is unusual.

### 3.3 Evidence and Belief

The evidence collected by the agent is converted into a belief about the probability that the transaction is fraudulent. The prototype uses a Bayesian-style calculation in which the prior belief about fraud is combined with the likelihood of observing each piece of evidence under fraudulent and legitimate states.

A prior fraud probability of 5% is used in the prototype. This value is a design assumption rather than a calibrated estimate of real-world fraud prevalence.

For each evidence signal, the agent estimates how frequently that unusual behavior occurs among fraudulent and legitimate transactions in the training data. Laplace smoothing is used when calculating these likelihoods to avoid zero probabilities for evidence that occurs rarely.

The resulting belief represents the agent's current assessment of the transaction. Missing location or merchant information is treated as neutral evidence rather than being interpreted as either suspicious or legitimate.

### 3.4 Cost-Sensitive Action Selection

The agent does not select an action based only on whether the fraud belief crosses a single classification threshold. Each action has an associated cost that represents the consequence of taking that action under different hidden states.

For example, approving a fraudulent transaction has a high cost, while declining a legitimate transaction also has a cost because it can create unnecessary customer friction. Questioning and examining a transaction have their own costs because they require additional interaction or investigation.

The agent calculates the expected cost of each action using its current fraud belief and selects the action with the lowest expected cost.

This creates the following decision process:

$$
\text{Fraud Belief}
\rightarrow
\text{Expected Action Costs}
\rightarrow
\text{Lowest-Cost Action}
$$

This approach allows the same fraud belief to lead to different decisions depending on the relative costs assigned to the actions.

### 3.5 Sequential Questioning

An important feature of the agent is that the initial action does not always have to be the final decision.

When the agent selects **Question**, it determines whether additional information should be requested. In the current prototype, a transaction confirmation question can be triggered when the amount or transaction frequency is unusual. A location question can also be generated when the transaction location is missing.

After receiving the simulated response, the agent can change its final action. For example, a confirmation that the customer did not make the transaction results in a **Decline** decision.

Thus, the agent follows a sequential process:

$$
\text{Observe}
\rightarrow
\text{Estimate}
\rightarrow
\text{Question}
\rightarrow
\text{Receive Information}
\rightarrow
\text{Final Decision}
$$

This design reflects the idea that uncertainty can sometimes be reduced by obtaining additional information rather than immediately making an irreversible decision.

### 3.6 Alternative Decision Policy

To evaluate whether the cost-based policy behaves differently from a simpler decision rule, a second policy was implemented using fixed fraud-belief thresholds.

The threshold policy maps different ranges of fraud belief to actions:

* Belief below 0.20: **Approve**
* Belief from 0.20 to below 0.50: **Examine**
* Belief from 0.50 to below 0.80: **Question**
* Belief of 0.80 or higher: **Decline**

These thresholds were selected as experimental design choices rather than learned or optimized values. Comparing this policy with the cost-based policy allows the experiment to examine how different decision rules affect fraud detection and customer interaction.

### 3.7 Agent Design Summary

The complete prototype can therefore be summarized as:

$$
\boxed{
\text{Transaction}
\rightarrow
\text{Customer History}
\rightarrow
\text{Behavioral Evidence}
\rightarrow
\text{Fraud Belief}
\rightarrow
\text{Action}
}
$$

If the selected action requires additional information:

$$
\boxed{
\text{Action}
\rightarrow
\text{Question}
\rightarrow
\text{New Evidence}
\rightarrow
\text{Final Action}
}
$$

The design intentionally focuses on a small number of interpretable behavioral signals. This makes the prototype easier to inspect and reason about while providing a testable example of decision-making under an unknown hidden state.

## 4. Probability Model and Decision Rule

The agent must make decisions without directly observing whether a transaction is legitimate or fraudulent. To represent this uncertainty, the agent maintains a belief about the hidden state of the transaction. The belief is updated using observed evidence and is then used to determine which action has the lowest expected cost.

### 4.1 Prior Belief

Before considering the transaction-specific evidence, the agent begins with a prior belief about the probability that a transaction is fraudulent. In this prototype, the prior probability of fraud is set to 5%.

$$
P(F)=0.05
$$

where \(F\) represents the event that the transaction is fraudulent. The probability of a legitimate transaction is therefore:

$$
P(L)=1-P(F)=0.95
$$

The 5% value is a design assumption rather than an estimate calibrated to the prevalence of the generated dataset. The dataset used in the experiment has a higher fraud proportion. This difference is treated as a limitation of the current prototype.

### 4.2 Evidence Likelihoods

For each transaction, the agent observes several evidence signals:

$$
E = \{A, L, M, F_r, V\}
$$

where:

* \(A\) represents unusual transaction amount,
* \(L\) represents unusual location,
* \(M\) represents unusual merchant,
* \(F_r\) represents unusual transaction frequency,
* \(V\) represents unusual transaction velocity.

For each signal, the agent estimates the likelihood of observing the evidence under the two possible hidden states. For example:

$$
P(A|F)
$$

represents the probability of observing an unusual transaction amount when the transaction is fraudulent, while:

$$
P(A|L)
$$

represents the probability of observing an unusual transaction amount when the transaction is legitimate.

The likelihoods are estimated from historical labeled transactions in the training data. Laplace smoothing is applied when calculating these probabilities:

$$
P(E|S)=\frac{N(E,S)+1}{N(S)+2}
$$

where \(N(E,S)\) is the number of transactions in state \(S\) where the evidence is observed, and \(N(S)\) is the total number of transactions in that state.

Laplace smoothing prevents a likelihood from becoming exactly zero when an evidence pattern is not observed in the available data.

### 4.3 Fraud Belief

The prototype combines the prior probability with the observed evidence using a Bayesian-style calculation. The model assumes conditional independence between the evidence signals given the hidden state.

Under this assumption, the unnormalized probability of the fraudulent state is:

$$
P(F)\prod_i P(E_i|F)
$$

and the corresponding value for the legitimate state is:

$$
P(L)\prod_i P(E_i|L)
$$

The fraud belief is then obtained by normalizing these two values:

$$
Belief(F|E)=
\frac{
P(F)\prod_iP(E_i|F)
}{
P(F)\prod_iP(E_i|F)
+
P(L)\prod_iP(E_i|L)
}
$$

This produces a value between 0 and 1 representing the agent's current belief that the transaction is fraudulent.

For example, if the evidence strongly favors the fraudulent state, the resulting belief will move closer to 1. If the evidence is more consistent with legitimate behavior, the belief will move closer to 0.

The model uses Boolean evidence in the current prototype. When an evidence signal is marked as unusual, its estimated \(P(E_i|S)\) value is used. When it is not unusual, the complementary probability is used.

### 4.4 Missing Evidence

Location and merchant information can be missing from some transactions. The current prototype does not treat missing information as evidence for either state. Instead, the corresponding likelihood factors are set to 1 for both fraud and legitimate states.

This means that missing information does not directly increase or decrease the fraud belief. This is a simple neutral treatment appropriate for the prototype, although more sophisticated approaches could explicitly model the probability of missingness.

### 4.5 Expected Action Costs

A fraud belief alone does not determine the final action. The agent also considers the consequences associated with each possible action.

For a transaction with fraud belief \(b\), the belief that it is legitimate is:

$$
1-b
$$

The prototype assigns the following expected costs:

$$
C(\text{Approve}) = 100b
$$

$$
C(\text{Question}) = 10b + 2(1-b)
$$

$$
C(\text{Examine}) = 5b + 8(1-b)
$$

$$
C(\text{Decline}) = 20(1-b)
$$

These costs represent experimental assumptions rather than real financial or operational costs.

The intuition behind the costs is that approving a fraudulent transaction should be expensive, while declining a legitimate transaction should also have a significant cost because of customer friction. Question and Examine provide intermediate options when the agent is uncertain.

### 4.6 Cost-Based Decision Rule

The first policy selects the action with the smallest expected cost:

$$
a^* = \arg\min_a C(a|b)
$$

where \(a\) represents one of the four available actions.

This produces a decision process in which the same evidence can lead to different actions depending on the estimated fraud belief and the relative costs assigned to the actions.

For example, a low fraud belief generally makes Approve attractive, while a high fraud belief makes Decline more attractive. Intermediate beliefs can make Question or Examine preferable because they allow additional information to be obtained or the transaction to be investigated.

### 4.7 Threshold-Based Decision Rule

A second policy was implemented to provide a simpler alternative to cost minimization. This policy maps the fraud belief directly to actions using fixed thresholds:

$$
a(b)=
\begin{cases}
\text{Approve}, & b < 0.20\\
\text{Examine}, & 0.20 \leq b < 0.50\\
\text{Question}, & 0.50 \leq b < 0.80\\
\text{Decline}, & b \geq 0.80
\end{cases}
$$

The thresholds were selected manually for the experiment and were not learned from a validation set. Therefore, this policy should be interpreted as a comparison policy rather than an optimized production policy.

Comparing the two policies allows the experiment to examine whether explicitly modeling action costs produces different decisions from a fixed threshold strategy.

### 4.8 Sequential Decision Update

When the initial action is Question, the agent can request additional information. The new information can affect the final decision.

For example, if a transaction is considered unusual because of its amount or frequency, the agent can ask the customer to confirm the transaction. In the current simulation, a negative confirmation leads to a Decline decision, while a positive confirmation leads to an Approve decision.

The overall decision process is therefore:

$$
\text{Prior}
\rightarrow
\text{Evidence}
\rightarrow
\text{Posterior Belief}
\rightarrow
\text{Initial Action}
\rightarrow
\text{Additional Information}
\rightarrow
\text{Final Action}
$$

This sequential structure is important because the objective of the agent is not simply to classify transactions. It is to decide **what to do next when the true state is uncertain**.

## 5. Experimental Setup

The purpose of the experiment was to evaluate whether the proposed agent could make useful transaction decisions under uncertainty and whether different decision policies would produce different trade-offs between fraud detection and customer interaction.

### 5.1 Dataset

A synthetic credit-card transaction dataset was created for the experiment. The dataset contains transactions generated for 1,000 customers, with each customer having a history of normal transactions and potentially fraudulent transactions.

The final dataset contains 12,000 transactions:

* 10,000 legitimate transactions
* 2,000 fraudulent transactions

The fraudulent transactions were generated using several behavioral patterns, including:

* unusually high transaction amounts,
* unusual transaction locations,
* unusually high transaction frequency, and
* unusual or previously unseen merchants, including combinations of multiple unusual behaviors.

The dataset also contains missing values for some transaction locations and merchants. This was intentional so that the agent could be evaluated when some information was unavailable.

The dataset is synthetic and therefore does not represent the complexity or distribution of real-world credit-card transactions. It was created to provide a controlled environment for testing the agent's decision-making process.

### 5.2 Train-Test Split

The dataset was divided into training and test sets using an 80/20 stratified split.

The training set contained 9,600 transactions and the test set contained 2,400 transactions. Stratification was used to maintain a similar proportion of legitimate and fraudulent transactions in both sets.

The training data was intended to provide the likelihood estimates used by the probability model, while the test data was used to evaluate the agent's decisions.

### 5.3 Evidence Generation

For each transaction, the agent examined the customer's previous transactions to generate five behavioral evidence signals:

1. **Amount unusualness**
2. **Location unusualness**
3. **Merchant unusualness**
4. **Frequency unusualness**
5. **Velocity unusualness**

The agent only considered transactions occurring before the current transaction when constructing the customer's historical context. The fraud label of the current transaction was not provided to the agent during its decision.

The resulting evidence was then passed to the probability model to calculate the agent's fraud belief.

### 5.4 Policies

Two decision policies were evaluated.

**Policy A — Cost-Based Decision**

Policy A calculates the expected cost of Approve, Question, Examine, and Decline using the agent's estimated fraud belief. The action with the lowest expected cost is selected.

When Question is selected, the agent can request additional information and produce a final action based on the simulated response.

**Policy B — Threshold-Based Decision**

Policy B uses manually selected fraud-belief thresholds:

| Fraud Belief | Action   |
| ------------ | -------- |
| < 0.20       | Approve  |
| 0.20–<0.50   | Examine  |
| 0.50–<0.80   | Question |
| ≥ 0.80       | Decline  |

These thresholds were selected for the experiment and were not optimized using a validation dataset.

### 5.5 Evaluation Metrics

The policies were evaluated using several metrics rather than accuracy alone.

The evaluation included:

* **Accuracy:** overall proportion of correct fraud/legitimate decisions.
* **Precision:** proportion of transactions identified as fraud that were actually fraudulent.
* **Recall:** proportion of fraudulent transactions identified by the agent.
* **F1 score:** balance between precision and recall.
* **False positives:** legitimate transactions incorrectly treated as fraudulent.
* **False negatives:** fraudulent transactions not automatically identified as fraudulent.
* **Legitimate approval rate:** proportion of legitimate transactions ultimately approved.
* **Fraud interception rate:** proportion of fraudulent transactions that were not ultimately approved.
* **Examination rate:** proportion of transactions sent for examination.
* **Interaction rate:** proportion of transactions requiring additional questioning or intervention.

These metrics were selected because a fraud-detection agent has to balance fraud prevention with the customer experience. A model that detects more fraud but unnecessarily interrupts legitimate customers may not be preferable in every setting.

### 5.6 Sequential Decision Evaluation

For transactions initially assigned the Question action, the prototype simulated a customer response. The response was then used to determine the final action.

For example, when the simulated customer did not confirm a suspicious transaction, the agent declined it. This allowed the experiment to distinguish between the agent's **initial action** and its **final action** after additional information.

The customer-response mechanism is a simulation rather than real human feedback. In the current implementation, the simulator uses the known transaction label to generate the response. Therefore, this mechanism is useful for demonstrating the sequential decision process but should not be interpreted as evidence of real-world customer behavior.

### 5.7 Implementation and Evaluation Limitation

During the probability review, an implementation issue was identified in the likelihood-estimation function. The function accepts a dataset as an argument but internally references the global `df_trans` object when calculating likelihoods. As a result, the reported implementation does not fully isolate the likelihood estimation to the training set as originally intended.

In addition, customer histories were constructed from the complete dataset before the train-test split. Although the fraud label is not used when generating evidence for a transaction, historical transactions from the test set can therefore be present in the history used for another test transaction.

These issues do not mean that the agent directly observes the fraud label during its decision, but they mean that the experimental evaluation is not a perfectly isolated train-test experiment. This limitation is documented rather than hidden and is identified as a correction for a future experimental iteration.

## 5. Experimental Setup

The purpose of the experiment was to evaluate whether the proposed agent could make useful transaction decisions under uncertainty and whether different decision policies would produce different trade-offs between fraud detection and customer interaction.

### 5.1 Dataset

A synthetic credit-card transaction dataset was created for the experiment. The dataset contains transactions generated for 1,000 customers, with each customer having a history of normal transactions and potentially fraudulent transactions.

The final dataset contains 12,000 transactions:

* 10,000 legitimate transactions
* 2,000 fraudulent transactions

The fraudulent transactions were generated using several behavioral patterns, including:

* unusually high transaction amounts,
* unusual transaction locations,
* unusually high transaction frequency, and
* unusual or previously unseen merchants, including combinations of multiple unusual behaviors.

The dataset also contains missing values for some transaction locations and merchants. This was intentional so that the agent could be evaluated when some information was unavailable.

The dataset is synthetic and therefore does not represent the complexity or distribution of real-world credit-card transactions. It was created to provide a controlled environment for testing the agent's decision-making process.

### 5.2 Train-Test Split

The dataset was divided into training and test sets using an 80/20 stratified split.

The training set contained 9,600 transactions and the test set contained 2,400 transactions. Stratification was used to maintain a similar proportion of legitimate and fraudulent transactions in both sets.

The training data was intended to provide the likelihood estimates used by the probability model, while the test data was used to evaluate the agent's decisions.

### 5.3 Evidence Generation

For each transaction, the agent examined the customer's previous transactions to generate five behavioral evidence signals:

1. **Amount unusualness**
2. **Location unusualness**
3. **Merchant unusualness**
4. **Frequency unusualness**
5. **Velocity unusualness**

The agent only considered transactions occurring before the current transaction when constructing the customer's historical context. The fraud label of the current transaction was not provided to the agent during its decision.

The resulting evidence was then passed to the probability model to calculate the agent's fraud belief.

### 5.4 Policies

Two decision policies were evaluated.

**Policy A — Cost-Based Decision**

Policy A calculates the expected cost of Approve, Question, Examine, and Decline using the agent's estimated fraud belief. The action with the lowest expected cost is selected.

When Question is selected, the agent can request additional information and produce a final action based on the simulated response.

**Policy B — Threshold-Based Decision**

Policy B uses manually selected fraud-belief thresholds:

| Fraud Belief | Action   |
| ------------ | -------- |
| < 0.20       | Approve  |
| 0.20–<0.50   | Examine  |
| 0.50–<0.80   | Question |
| ≥ 0.80       | Decline  |

These thresholds were selected for the experiment and were not optimized using a validation dataset.

### 5.5 Evaluation Metrics

The policies were evaluated using several metrics rather than accuracy alone.

The evaluation included:

* **Accuracy:** overall proportion of correct fraud/legitimate decisions.
* **Precision:** proportion of transactions identified as fraud that were actually fraudulent.
* **Recall:** proportion of fraudulent transactions identified by the agent.
* **F1 score:** balance between precision and recall.
* **False positives:** legitimate transactions incorrectly treated as fraudulent.
* **False negatives:** fraudulent transactions not automatically identified as fraudulent.
* **Legitimate approval rate:** proportion of legitimate transactions ultimately approved.
* **Fraud interception rate:** proportion of fraudulent transactions that were not ultimately approved.
* **Examination rate:** proportion of transactions sent for examination.
* **Interaction rate:** proportion of transactions requiring additional questioning or intervention.

These metrics were selected because a fraud-detection agent has to balance fraud prevention with the customer experience. A model that detects more fraud but unnecessarily interrupts legitimate customers may not be preferable in every setting.

### 5.6 Sequential Decision Evaluation

For transactions initially assigned the Question action, the prototype simulated a customer response. The response was then used to determine the final action.

For example, when the simulated customer did not confirm a suspicious transaction, the agent declined it. This allowed the experiment to distinguish between the agent's **initial action** and its **final action** after additional information.

The customer-response mechanism is a simulation rather than real human feedback. In the current implementation, the simulator uses the known transaction label to generate the response. Therefore, this mechanism is useful for demonstrating the sequential decision process but should not be interpreted as evidence of real-world customer behavior.

### 5.7 Implementation and Evaluation Limitation

During the probability review, an implementation issue was identified in the likelihood-estimation function. The function accepts a dataset as an argument but internally references the global `df_trans` object when calculating likelihoods. As a result, the reported implementation does not fully isolate the likelihood estimation to the training set as originally intended.

In addition, customer histories were constructed from the complete dataset before the train-test split. Although the fraud label is not used when generating evidence for a transaction, historical transactions from the test set can therefore be present in the history used for another test transaction.

These issues do not mean that the agent directly observes the fraud label during its decision, but they mean that the experimental evaluation is not a perfectly isolated train-test experiment. This limitation is documented rather than hidden and is identified as a correction for a future experimental iteration.

## 7. Failure Analysis

Although the agent achieved high overall performance, examining its incorrect and uncertain decisions provides more insight than reporting aggregate metrics alone. Under Policy A, nine of the 400 fraudulent transactions were not automatically declined. All nine were assigned to the Examine action. Therefore, the main failure mode was not approving fraudulent transactions, but failing to assign a sufficiently high fraud belief for automatic decline.

### 7.1 Examples of Difficult Cases

Five of the nine fraudulent transactions were examined in greater detail.

| Transaction | Main Evidence                                    | Fraud Belief | Final Action | True State |
| ----------- | ------------------------------------------------ | -----------: | ------------ | ---------- |
| FREQ_C0467  | Unusual frequency; location missing              |       0.6197 | Examine      | Fraud      |
| FREQ_C0834  | Unusual frequency; location missing              |       0.6197 | Examine      | Fraud      |
| LOC_C0622   | Unusual frequency; location missing              |       0.6197 | Examine      | Fraud      |
| LOC_C0997   | Unusual frequency; location missing              |       0.6197 | Examine      | Fraud      |
| MERCH_C0718 | Unusual frequency; location and merchant missing |       0.5749 | Examine      | Fraud      |

The first four cases produced almost identical evidence patterns. Their transaction amount was not considered unusual, the merchant was considered familiar, location information was unavailable, frequency was unusual, and velocity was not unusual. The resulting fraud belief was approximately 0.62.

The fifth case had an even more limited evidence set because both location and merchant information were unavailable. Its fraud belief was approximately 0.57.

In all five cases, the fraud belief was high enough to trigger additional examination but not high enough for the cost-based policy to select automatic decline.

### 7.2 Main Failure Condition

The examples indicate that the agent can struggle when a fraudulent transaction exhibits only one strong behavioral signal while other evidence is either normal or unavailable.

For example, unusual transaction frequency by itself does not necessarily provide enough evidence for the current cost model to select Decline. The agent therefore produces a moderate-to-high fraud belief but remains below the decision boundary required for automatic decline.

Missing information makes this problem more pronounced. In the current probability model, missing location or merchant information is treated as neutral evidence. Consequently, the absence of information does not directly increase the fraud belief, but it also does not provide additional evidence that could distinguish the transaction from legitimate behavior.

### 7.3 Coarse Evidence Representation

Another limitation is the Boolean representation of the evidence.

The current system records whether an observation is unusual as either `True` or `False`. This simplifies the model but removes information about the degree of unusualness.

For example, two transactions may both be classified as having unusual frequency even though one occurred slightly faster than normal while another occurred immediately after a previous transaction. Both observations are represented by the same Boolean value.

This can result in several transactions receiving similar fraud beliefs even when their underlying behavior differs.

### 7.4 Highest-Cost Error

The most important potential error in a fraud-detection system is approving a fraudulent transaction. In the evaluated test set, no fraudulent transaction was ultimately approved by either Policy A or Policy B.

Therefore, the highest-cost error type did not occur in the evaluated sample.

The remaining nine fraudulent transactions under Policy A were instead routed to Examine. This means that the agent did not automatically intercept these cases through a Decline decision, but it also did not allow them to proceed as approved transactions.

From a decision-making perspective, this suggests that the current system has a relatively conservative failure mode in the tested dataset: uncertain fraudulent transactions tend to be escalated rather than approved.

### 7.5 Policy Comparison as Failure Analysis

Policy B provides another perspective on these difficult cases. It examined 52 transactions, including 39 fraudulent and 13 legitimate transactions.

Compared with Policy A, Policy B moved 30 fraudulent transactions from automatic Decline to Examine. At the same time, it increased the number of legitimate transactions sent for examination.

This demonstrates that changing the decision policy can change the treatment of uncertain cases without changing the underlying evidence or probability model.

Policy A therefore prioritized stronger automatic fraud interception, while Policy B allowed more uncertain cases to remain available for examination.

### 7.6 Lessons from the Failures

The failure analysis suggests several areas for future improvement:

1. **Use continuous evidence instead of only Boolean indicators.** The magnitude of unusual behavior could provide more information than simply labeling it unusual.
2. **Improve treatment of missing information.** Future versions could explicitly model whether missing information itself contains useful information.
3. **Calibrate fraud beliefs.** The current belief values have not been formally calibrated against observed probabilities.
4. **Improve the independence assumption.** Frequency and velocity, for example, may contain related information.
5. **Tune decision thresholds and costs using validation data and realistic business constraints.**

These improvements are not required to demonstrate the current prototype, but they would be important for a more reliable future version.

Overall, the failure analysis shows that the agent's main weakness was not an inability to detect fraud in general, but difficulty distinguishing some fraudulent transactions when the available evidence was limited or represented too coarsely.

## 8. Limitations, Ethics, and Human Control

The proposed system is a prototype designed to study decision-making under uncertainty. It is not intended to be used as a production credit-card fraud detection system. Several limitations affect the interpretation of the experimental results.

### 8.1 Synthetic Dataset

The experiment uses a synthetically generated dataset rather than real credit-card transactions. The fraud patterns were intentionally designed around a small number of behavioral signals, including amount, location, merchant, frequency, and velocity.

Real-world fraud is considerably more diverse. Fraudsters can adapt their behavior, customers can change their normal purchasing patterns, and legitimate transactions can appear unusual for many reasons. Therefore, the performance reported in this experiment should not be interpreted as an estimate of performance on real-world transaction data.

### 8.2 Simplified Hidden State

The prototype represents the hidden state using only two categories: legitimate and fraudulent. Real fraud detection may involve additional states or uncertainty, such as disputed transactions, account takeover, merchant-related issues, or transactions requiring further verification.

The binary representation was intentionally retained because it provides a simple starting point for studying the agent's decision-making process.

### 8.3 Probability Model Limitations

The probability model has several simplifying assumptions.

First, the fraud prior is fixed at 5% and is not calibrated to the observed prevalence of the generated dataset.

Second, the evidence is represented using Boolean indicators. This means that the model does not distinguish between different degrees of unusual behavior.

Third, the model assumes that the evidence signals are conditionally independent when calculating the combined belief. In reality, some signals may be related. For example, transaction frequency and velocity can describe closely related aspects of transaction behavior.

Finally, the resulting fraud beliefs have not been formally calibrated. Therefore, a belief such as 0.70 should not automatically be interpreted as meaning that exactly 70% of comparable transactions are fraudulent.

### 8.4 Experimental Data Isolation

A probability review identified an implementation issue in the likelihood-estimation function. Although the function receives the training dataset as an argument, its implementation references the global transaction dataset when calculating likelihoods. Consequently, the likelihood estimates used in the reported experiment were not completely isolated to the training set as originally intended.

In addition, customer histories were constructed from the complete dataset before the train-test split. Although the fraud label of the current transaction was not provided to the agent during evidence generation, historical transactions from the test set could be present in the customer's history.

These issues limit the strength of the reported evaluation. They are documented as methodological limitations and should be corrected in a future experimental iteration.

### 8.5 Simulated Customer Responses

The sequential questioning component is also simplified. Customer responses are simulated rather than collected from real users.

In the current simulation, the known fraud label is used to generate the customer's response. This creates an oracle-like behavior that would not exist in a real deployment. The agent itself does not use the fraud label to calculate its initial belief, but the response simulator has access to it.

Therefore, the improvement from Question to the final action should be interpreted only as a demonstration of the sequential decision mechanism, not as evidence that the agent would achieve the same results with real customers.

A future version should replace this mechanism with real human feedback or a probabilistic response model that does not directly access the hidden state.

### 8.6 Illustrative Action Costs

The costs assigned to Approve, Question, Examine, and Decline are manually selected experimental values. They are intended to represent relative consequences rather than actual financial costs or operational measurements.

In a real payment system, these costs would need to incorporate factors such as financial loss, customer experience, investigation resources, regulatory requirements, and business priorities.

The cost values should therefore be treated as part of the experimental setup rather than as recommendations for a real financial institution.

### 8.7 Ethical Considerations

Automated fraud decisions can directly affect customers. Incorrectly declining a legitimate transaction can prevent a customer from accessing their money or completing an important purchase. At the same time, approving fraudulent transactions can create financial losses for customers and financial institutions.

There is therefore a risk in treating unusual behavior as proof of fraud. An unusual location, merchant, amount, or transaction frequency can have legitimate explanations.

The system should consequently treat the estimated fraud belief as decision-support information rather than unquestionable truth. High-impact decisions should have appropriate safeguards and avenues for review.

The use of behavioral information also raises privacy considerations. A production system would need to follow applicable data-protection requirements and carefully control how transaction histories are collected, stored, and used.

### 8.8 Human Control

Human involvement is particularly important for transactions where the agent is uncertain. The Examine action provides a mechanism for escalating transactions rather than forcing the automated system to make every final decision.

A possible real-world workflow would therefore be:

$$
\text{Agent Observation}
\rightarrow
\text{Risk Assessment}
\rightarrow
\text{Automated Decision or Escalation}
\rightarrow
\text{Human Review}
$$

The agent should support human decision-makers rather than remove human oversight from high-impact financial decisions.

### 8.9 Future Improvements

Based on the experiment and subsequent reviews, the following improvements are identified for future versions:

* isolate likelihood estimation and historical evidence strictly to training data;
* use a time-based evaluation strategy where appropriate;
* replace Boolean evidence with continuous behavioral features;
* calibrate the fraud probabilities;
* learn or validate the fraud prior using appropriate data;
* model dependencies between evidence signals;
* replace the oracle-like customer simulator with realistic human feedback;
* tune action costs and thresholds using validation data and realistic business objectives.

These improvements would make the system more suitable for rigorous evaluation, but they are outside the scope of the current prototype.

## 9. Conclusion and New Questions

This project explored the design of an AI agent that makes credit-card transaction decisions when the true state of the transaction is hidden. Rather than treating fraud detection as a simple binary classification problem, the agent estimates a belief about whether a transaction is fraudulent and uses that belief to select among four actions: Approve, Question, Examine, and Decline.

The prototype uses customer transaction history to identify unusual behavioral patterns in transaction amount, location, merchant, frequency, and velocity. These signals are combined using a Bayesian-style probability model, after which the agent selects an action using either a cost-based policy or a threshold-based policy. The Question action also demonstrates how an agent can obtain additional information before making a final decision.

The experiment showed that the two decision policies produced different outcomes even though they used the same underlying evidence and fraud-belief model. Policy A achieved a recall of 97.75%, while Policy B achieved a recall of 90.25%. Neither policy approved a fraudulent transaction or declined a legitimate transaction in the evaluated test set. Policy B, however, sent more transactions for examination, demonstrating the trade-off between automatic fraud interception and additional review.

The failure analysis showed that the agent struggled primarily when fraudulent transactions had limited or ambiguous evidence. Several difficult cases were associated with unusual frequency combined with missing location information. This highlighted an important limitation of representing behavioral evidence using simple Boolean indicators.

The probability review also identified methodological limitations in the current implementation, including the use of a fixed fraud prior, the conditional-independence assumption, lack of probability calibration, illustrative action costs, and incomplete isolation between training and test data. The customer-response simulator also uses the hidden fraud label to generate responses, which limits the interpretation of the sequential-questioning results.

The most important lesson from the project is that fraud detection can be viewed not only as predicting whether a transaction is fraudulent, but also as deciding **what action to take when the system is uncertain**. Allowing an agent to Question or Examine a transaction provides alternatives to immediately approving or declining it.

### 9.1 New Questions

The project raises several questions for future work:

1. **How should an agent determine when it has enough evidence to act without asking the customer for more information?**

2. **Can continuous behavioral features produce better-calibrated fraud beliefs than Boolean unusual/not-unusual signals?**

3. **How should action costs be learned from real customer and business outcomes rather than manually selected?**

4. **Would a time-based evaluation produce different results from the random train-test split used in this prototype?**

5. **How should the agent update its belief when customer responses are uncertain or potentially unreliable?**

6. **Can human review be incorporated as genuine feedback that improves future decisions without introducing label leakage?**

7. **How should the agent adapt when normal customer behavior changes over time or when fraud patterns evolve?**

These questions provide directions for extending the prototype from a controlled demonstration into a more rigorous study of sequential decision-making under uncertainty.

### 9.2 Request for Comments

I would particularly welcome feedback on three aspects of this work:

* whether the probability model is an appropriate starting point for this type of agent;
* how the costs of customer friction and fraud prevention should be represented;
* and how additional human feedback could be incorporated without giving the agent access to the hidden transaction state.
