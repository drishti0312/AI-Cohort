#!/usr/bin/env python
# coding: utf-8

# In[246]:


# 1. Imports and data loading

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df_trans = pd.read_csv(r"C:\Users\user\Desktop\AI-Cohort\csv\fraud_transactions.csv")
df_cust = pd.read_csv(r"C:\Users\user\Desktop\AI-Cohort\csv\customer_profiles.csv")

df_trans["timestamp"] = pd.to_datetime(df_trans["timestamp"])

print("Transactions:", df_trans.shape)
print("Customers:", df_cust.shape)


# In[247]:


# 2. Add customer profile information

df_trans = df_trans.merge(df_cust[["customer_id", "home_location"]],on="customer_id",how="left")

print(df_trans[["customer_id", "location", "home_location"]].head())


# In[248]:


customer_histories = {
    customer_id: customer_df
    for customer_id, customer_df
    in df_trans.groupby("customer_id")
}


# In[337]:


df_trans.shape


# In[ ]:


evidence_rows = []

for _, row in df_trans.iterrows():

    evidence_rows.append(
        get_evidence(
            row,
            customer_histories
        )
    )

evidence_df = pd.DataFrame(
    evidence_rows,
    index=df_trans.index
)

for column in evidence_df.columns:
    df_trans[column] = evidence_df[column]
print("\nAMOUNT")
print(
    pd.crosstab(
        df_trans["amount_unusual"],
        df_trans["fraud"],
        normalize="columns"
    )
)

print("\nLOCATION")
print(
    pd.crosstab(
        df_trans["location_unusual"],
        df_trans["fraud"],
        normalize="columns"
    )
)

print("\nMERCHANT")
print(
    pd.crosstab(
        df_trans["merchant_unusual"],
        df_trans["fraud"],
        normalize="columns"
    )
)

print("\nFREQUENCY")
print(
    pd.crosstab(
        df_trans["frequency_unusual"],
        df_trans["fraud"],
        normalize="columns"
    )
)


# In[279]:


# 4. Evidence functions

def get_customer_history(customer_id, timestamp, customer_histories):
    customer = customer_histories[customer_id]
    current_time = pd.to_datetime(timestamp)

    history = customer.loc[customer["timestamp"] < current_time]

    return history.drop(columns="fraud")


def check_amount(current_amount, history):
    if history.empty:
        return False

    avg_amount = history["amount"].mean()

    if current_amount > 4 * avg_amount:
        return True

    return False


def check_location(current_location, historical_locations):
    if pd.isna(current_location):
        return None

    if current_location in historical_locations.values:
        return False

    return True


def check_merchant(current_merchant, historical_merchants):
    if pd.isna(current_merchant):
        return None

    if current_merchant in historical_merchants.values:
        return False

    return True


def check_frequency(current_timestamp, history):
    if history.empty:
        return False
    current_timestamp = pd.to_datetime(current_timestamp)
    history = history.sort_values("timestamp")
    prev_transaction = history.iloc[-1]["timestamp"]
    current_gap = current_timestamp - prev_transaction
    # print("Current Gap: ",current_gap)
    historical_gaps = history["timestamp"].diff().dropna()
    if historical_gaps.empty:
        return False
    normal_median_gap = historical_gaps.median()
    # print("Normal Median Gap ",normal_median_gap)
    frequency_threshold = normal_median_gap * 0.5
    return current_gap < frequency_threshold

def check_velocity(timestamp, history):
    if history.empty:
        return False

    recent_transactions = history[((timestamp - history["timestamp"]).dt.total_seconds() / 60) <= 30]

    return len(recent_transactions) >= 3


# In[257]:


# 5. Generate evidence for every transaction

def get_evidence(transaction, customer_histories):
    history = get_customer_history(transaction["customer_id"],transaction["timestamp"],customer_histories)

    amount_unusual = check_amount(transaction["amount"],history)

    location_unusual = check_location(transaction["location"],history["location"])

    merchant_unusual = check_merchant(transaction["merchant"],history["merchant"])

    frequency_unusual = check_frequency(transaction["timestamp"],history)

    velocity_unusual = check_velocity(transaction["timestamp"],history)

    return {
        "amount_unusual": amount_unusual,
        "location_unusual": location_unusual,
        "merchant_unusual": merchant_unusual,
        "frequency_unusual": frequency_unusual,
        "velocity_unusual": velocity_unusual
    }


evidence_rows = []

for _, row in df_trans.iterrows():
    evidence_rows.append(
        get_evidence(row, customer_histories)
    )

evidence_df = pd.DataFrame(evidence_rows, index=df_trans.index)

for column in evidence_df.columns:
    df_trans[column] = evidence_df[column]

print(df_trans[
    [
        "amount_unusual",
        "location_unusual",
        "merchant_unusual",
        "frequency_unusual",
        "velocity_unusual"
    ]
].value_counts(dropna=False))


# In[280]:


# 6. Calculate likelihoods

def calculate_likelihoods(df_trans):
    fraud_trans = df_trans.loc[df_trans["fraud"] == 1]
    legit_trans = df_trans.loc[df_trans["fraud"] == 0]

    total_fraud = len(fraud_trans)
    total_legit = len(legit_trans)

    fraud_amount_count = (fraud_trans["amount_unusual"] == True).sum()
    legit_amount_count = (legit_trans["amount_unusual"] == True).sum()

    fraud_location_count = (fraud_trans["location_unusual"] == True).sum()
    legit_location_count = (legit_trans["location_unusual"] == True).sum()

    fraud_merchant_count = (fraud_trans["merchant_unusual"] == True).sum()
    legit_merchant_count = (legit_trans["merchant_unusual"] == True).sum()

    fraud_frequency_count = (fraud_trans["frequency_unusual"] == True).sum()
    legit_frequency_count = (legit_trans["frequency_unusual"] == True).sum()

    fraud_velocity_count = (fraud_trans["velocity_unusual"] == True).sum()
    legit_velocity_count = (legit_trans["velocity_unusual"] == True).sum()

    # Laplace smoothing
    p_amount_fraud = (fraud_amount_count + 1) / (total_fraud + 2)
    p_amount_legit = (legit_amount_count + 1) / (total_legit + 2)

    p_location_fraud = (fraud_location_count + 1) / (total_fraud + 2)
    p_location_legit = (legit_location_count + 1) / (total_legit + 2)

    p_merchant_fraud = (fraud_merchant_count + 1) / (total_fraud + 2)
    p_merchant_legit = (legit_merchant_count + 1) / (total_legit + 2)

    p_frequency_fraud = (fraud_frequency_count + 1) / (total_fraud + 2)
    p_frequency_legit = (legit_frequency_count + 1) / (total_legit + 2)

    p_velocity_fraud = (fraud_velocity_count + 1) / (total_fraud + 2)
    p_velocity_legit = (legit_velocity_count + 1) / (total_legit + 2)

    return (
        p_amount_fraud, p_amount_legit,
        p_location_fraud, p_location_legit,
        p_merchant_fraud, p_merchant_legit,
        p_frequency_fraud, p_frequency_legit,
        p_velocity_fraud, p_velocity_legit
    )


likelihoods = calculate_likelihoods(df_trans)
print(likelihoods)



# In[282]:


print(
    df_trans.groupby("fraud")["fraud_belief"].describe()
)
print("\nAverage fraud belief by actual class:")
print(
    df_trans.groupby("fraud")["fraud_belief"].mean()
)


# In[259]:


# 7. Calculate fraud belief

def calculate_fraud_belief(evidence, likelihoods):

    prior_fraud = 0.05
    prior_legit = 1 - prior_fraud

    (
        p_amount_fraud,
        p_amount_legit,
        p_location_fraud,
        p_location_legit,
        p_merchant_fraud,
        p_merchant_legit,
        p_frequency_fraud,
        p_frequency_legit,
        p_velocity_fraud,
        p_velocity_legit
    ) = likelihoods

    if evidence["amount_unusual"] == True:
        amount_fraud = p_amount_fraud
        amount_legit = p_amount_legit
    else:
        amount_fraud = 1 - p_amount_fraud
        amount_legit = 1 - p_amount_legit

    if evidence["location_unusual"] == True:
        location_fraud = p_location_fraud
        location_legit = p_location_legit
    elif evidence["location_unusual"] == False:
        location_fraud = 1 - p_location_fraud
        location_legit = 1 - p_location_legit
    else:
        location_fraud = 1
        location_legit = 1

    if evidence["merchant_unusual"] == True:
        merchant_fraud = p_merchant_fraud
        merchant_legit = p_merchant_legit
    elif evidence["merchant_unusual"] == False:
        merchant_fraud = 1 - p_merchant_fraud
        merchant_legit = 1 - p_merchant_legit
    else:
        merchant_fraud = 1
        merchant_legit = 1

    if evidence["frequency_unusual"] == True:
        frequency_fraud = p_frequency_fraud
        frequency_legit = p_frequency_legit
    else:
        frequency_fraud = 1 - p_frequency_fraud
        frequency_legit = 1 - p_frequency_legit

    if evidence["velocity_unusual"] == True:
        velocity_fraud = p_velocity_fraud
        velocity_legit = p_velocity_legit
    else:
        velocity_fraud = 1 - p_velocity_fraud
        velocity_legit = 1 - p_velocity_legit

    fraud_probability = (prior_fraud * amount_fraud * location_fraud * merchant_fraud * frequency_fraud * velocity_fraud)

    legit_probability = (prior_legit  * amount_legit * location_legit * merchant_legit * frequency_legit * velocity_legit)

    return fraud_probability / (fraud_probability + legit_probability)


# In[260]:


# 8. Cost model and action selection

def calculate_action_costs(fraud_belief):
    legit_belief = 1 - fraud_belief

    approve_cost = fraud_belief * 100
    question_cost = (fraud_belief * 10 + legit_belief * 2)
    examine_cost = (fraud_belief * 5  + legit_belief * 8)
    decline_cost = legit_belief * 20

    return {
        "Approve": approve_cost,
        "Question": question_cost,
        "Examine": examine_cost,
        "Decline": decline_cost
    }


def choose_action(costs):
    return min(costs, key=costs.get)


# In[261]:


# 9. Missing-information handling

def get_questions(evidence):
    questions = []

    # Ask customer to confirm the transaction
    if evidence["amount_unusual"] == True or evidence["frequency_unusual"] == True:
        questions.append("transaction_confirmation")

    # Ask for missing location
    if evidence["location_unusual"] is None:
        questions.append("location")

    return questions


def update_transaction(transaction, answers):
    transaction = transaction.copy()

    for question, answer in answers.items():
        if answer is not None:
            transaction[question] = answer

    return transaction


def simulate_customer_response(transaction, questions):
    answers = {}

    for question in questions:
        ####### Need Human in Loop tp confirm whether the transaction was made by person or not
        if question == "transaction_confirmation":
            if transaction["fraud"] == 0:
                answers["transaction_confirmation"] = True
            else:
                answers["transaction_confirmation"] = False
        elif question == "location":
            answers["location"] = transaction["home_location"]

        elif question == "merchant":
            # Keep None to simulate an unanswered merchant question.
            answers["merchant"] = None

    return answers
def handle_transaction_confirmation(answer):
    if answer == True:
        return "Approve"

    elif answer == False:
        return "Decline"

    else:
        return "Examine"
def execute_action(action, transaction, evidence):

    if action == "Approve":
        return "Approve"

    elif action == "Decline":
        return "Decline"

    elif action == "Examine":
        return "Examine"

    elif action == "Question":

        questions = get_questions(evidence)

        answers = simulate_customer_response(
            transaction,
            questions
        )

        if "transaction_confirmation" in answers:
            return handle_transaction_confirmation(
                answers["transaction_confirmation"]
            )

        return "Examine"
test_transaction = df_trans.iloc[2000]


# In[262]:


result = process_transaction(
    fraud_transaction,
    likelihoods
)

print(result)


# In[263]:


def make_decision(evidence, transaction, likelihoods):

    fraud_belief = calculate_fraud_belief(
        evidence,
        likelihoods
    )

    costs = calculate_action_costs(fraud_belief)

    action = choose_action(costs)
    # If the agent chooses Question
    if action == "Question":

        questions = get_questions(evidence)

        answers = simulate_customer_response(
            transaction,
            questions
        )

        # Customer confirmed the transaction
        if "transaction_confirmation" in answers:
            final_action = handle_transaction_confirmation(
                answers["transaction_confirmation"]
            )

            return fraud_belief, costs, action, final_action
    return fraud_belief, costs, action, action

def process_transaction(transaction, likelihoods):

    evidence = {
        "amount_unusual": transaction["amount_unusual"],
        "location_unusual": transaction["location_unusual"],
        "merchant_unusual": transaction["merchant_unusual"],
        "frequency_unusual": transaction["frequency_unusual"],
        "velocity_unusual": transaction["velocity_unusual"]
    }

    fraud_belief, costs, initial_action, final_action = make_decision(
        evidence,
        transaction,
        likelihoods
    )

    return fraud_belief, initial_action, final_action
result = process_transaction(
    test_transaction,
    likelihoods
)

print(result)


# In[264]:


print("*"*10,"Initial Action","*"*10)
print(results_df["initial_action"].value_counts())
print("*"*10,"Final Action","*"*10)
print(results_df["final_action"].value_counts())


# In[285]:


# 12. Run the agent on the complete dataset

results = []

for _, transaction in df_trans.iterrows():

    fraud_belief, initial_action, final_action = process_transaction(
        transaction,
        likelihoods
    )

    results.append({
        "transaction_id": transaction["transaction_id"],
        "fraud_belief": fraud_belief,
        "initial_action": initial_action,
        "final_action": final_action,
        "actual_fraud": transaction["fraud"]
    })

results_df = pd.DataFrame(results)

print(results_df.shape)


# In[286]:


print(results_df.head())


# In[287]:


print("\nINITIAL ACTIONS")
print(results_df["initial_action"].value_counts())

print("\nFINAL ACTIONS")
print(results_df["final_action"].value_counts())


# In[288]:


print("\nFINAL ACTION BY ACTUAL STATE")
print(
    pd.crosstab(
        results_df["actual_fraud"],
        results_df["final_action"]
    )
)


# In[ ]:





# In[ ]:


#### print("\nEXAMINED TRANSACTIONS")
print(
    results_df[results_df["final_action"] == "Examine"][
        ["transaction_id", "fraud_belief", "actual_fraud"]
    ].sort_values("fraud_belief")
)


# In[266]:


pd.crosstab(results_df["final_action"],results_df["actual_fraud"])


# In[267]:





# In[268]:


########################## Caculating Customer Impact ###################
legit_total = (results_df["actual_fraud"] == 0).sum()

legit_approved = ((results_df["actual_fraud"] == 0) &(results_df["final_action"] == "Approve")).sum()

legit_examined = ((results_df["actual_fraud"] == 0) & (results_df["final_action"] == "Examine")).sum()

legit_declined = ((results_df["actual_fraud"] == 0) &(results_df["final_action"] == "Decline")).sum()

print("Total legitimate:", legit_total)
print("Legitimate approved:", legit_approved)
print("Legitimate examined:", legit_examined)
print("Legitimate declined:", legit_declined)

print("Legitimate approval rate:",legit_approved / legit_total)


# In[269]:


def calculate_final_cost(row):
    if row["final_action"] == "Approve":                        ### Fraud + Approve = 100, Legit + approve = 0
        return 100 if row["actual_fraud"] == 1 else 0

    elif row["final_action"] == "Examine":                      #### Fraud + Examine = 5. Legit + examine = 8
        return 5 if row["actual_fraud"] == 1 else 8

    elif row["final_action"] == "Decline":                      ###### Fraud + Decline = 0 , Legit + decline = 20
        return 0 if row["actual_fraud"] == 1 else 20

    return 0


results_df["final_cost"] = results_df.apply(calculate_final_cost,axis=1)

print("Total actual cost:", results_df["final_cost"].sum())
print("Average cost per transaction:", results_df["final_cost"].mean())


# In[270]:


question_count = (
    results_df["initial_action"] == "Question").sum()

print("Transactions questioned:", question_count)


# In[271]:


question_results = results_df[
    results_df["initial_action"] == "Question"
]

print(question_results[["initial_action", "final_action", "actual_fraud"]].value_counts())


# In[272]:


question_cost = 0
for _,row in question_results.iterrows():
    if row["actual_fraud"] == 1:
        question_cost += 10
    else:
        question_cost += 5
print("Total cost in Question",question_cost)


# In[274]:


print(
    pd.crosstab(
        baseline_df["baseline_action"],
        baseline_df["actual_fraud"]
    )
)


# In[283]:


print(
    df_trans.groupby("fraud")["fraud_belief"].describe()
)


# In[284]:


print("\nAverage fraud belief by actual class:")
print(
    df_trans.groupby("fraud")["fraud_belief"].mean()
)


# In[290]:


# Creating 40 case test set
test_df = df_trans.sample(n=40,random_state=42).copy()

print(test_df["fraud"].value_counts())


# In[291]:


print(
    test_df[
        [
            "transaction_id",
            "fraud",
            "amount_unusual",
            "location_unusual",
            "merchant_unusual",
            "frequency_unusual",
            "velocity_unusual",
            "fraud_belief"
        ]
    ].to_string(index=False)
)


# In[292]:


test_results = []

for _, transaction in test_df.iterrows():

    fraud_belief, initial_action, final_action = process_transaction(
        transaction,
        likelihoods
    )

    test_results.append({
        "transaction_id": transaction["transaction_id"],
        "fraud_belief": fraud_belief,
        "initial_action": initial_action,
        "final_action": final_action,
        "actual_fraud": transaction["fraud"]
    })

test_results_df = pd.DataFrame(test_results)

print(test_results_df)


# In[293]:


print("\nFINAL ACTION BY ACTUAL STATE")
print(
    pd.crosstab(
        test_results_df["actual_fraud"],
        test_results_df["final_action"]
    )
)


# In[294]:


print(test_results_df["initial_action"].value_counts())


# In[295]:


def choose_action_threshold(fraud_belief):

    if fraud_belief < 0.20:
        return "Approve"

    elif fraud_belief < 0.50:
        return "Examine"

    elif fraud_belief < 0.80:
        return "Question"

    else:
        return "Decline"


# In[296]:


policy_b_results = []

for _, transaction in test_df.iterrows():

    belief = transaction["fraud_belief"]

    initial_action = choose_action_threshold(belief)

    final_action = initial_action

    if initial_action == "Question":

        questions = get_questions(
            {
                "amount_unusual": transaction["amount_unusual"],
                "location_unusual": transaction["location_unusual"],
                "merchant_unusual": transaction["merchant_unusual"],
                "frequency_unusual": transaction["frequency_unusual"],
                "velocity_unusual": transaction["velocity_unusual"]
            }
        )

        answers = simulate_customer_response(
            transaction,
            questions
        )

        if "transaction_confirmation" in answers:
            final_action = handle_transaction_confirmation(
                answers["transaction_confirmation"]
            )

    policy_b_results.append({
        "transaction_id": transaction["transaction_id"],
        "fraud_belief": belief,
        "initial_action": initial_action,
        "final_action": final_action,
        "actual_fraud": transaction["fraud"]
    })

policy_b_results_df = pd.DataFrame(policy_b_results)


# In[297]:


print("\nPOLICY B — INITIAL ACTIONS")
print(
    policy_b_results_df["initial_action"].value_counts()
)

print("\nPOLICY B — FINAL ACTIONS")
print(
    policy_b_results_df["final_action"].value_counts()
)


# In[298]:


belief = transaction["fraud_belief"]


# In[299]:


def calculate_interaction_metrics(results_df):

    total = len(results_df)

    question_rate = (
        (results_df["initial_action"] == "Question").sum()
        / total
    )

    examine_rate = (
        (results_df["initial_action"] == "Examine").sum()
        / total
    )

    interaction_rate = question_rate + examine_rate

    return {
        "Question rate": question_rate,
        "Examine rate": examine_rate,
        "Interaction rate": interaction_rate
    }


# In[300]:


print("Policy A:")
print(calculate_interaction_metrics(test_results_df))

print("\nPolicy B:")
print(calculate_interaction_metrics(policy_b_results_df))


# In[301]:


print("POLICY A")
print(
    pd.crosstab(
        test_results_df["actual_fraud"],
        test_results_df["final_action"]
    )
)

print("\nPOLICY B")
print(
    pd.crosstab(
        policy_b_results_df["actual_fraud"],
        policy_b_results_df["final_action"]
    )
)


# In[304]:


from sklearn.model_selection import train_test_split

train_df ,test_df = train_test_split(df_trans,test_size = 0.20,random_state = 42,stratify=df_trans["fraud"])
print("Training transactions:",len(train_df))
print("Test transactions:",len(test_df))

print("*"*20)
print("Training fraud distribution")
print(train_df["fraud"].value_counts())

print("*"*20)
print("Test fraud distribution")
print(test_df["fraud"].value_counts())


# In[306]:


# New - Calculate likelihoods

def calculate_likelihoods(df):
    fraud_trans = df_trans.loc[df_trans["fraud"] == 1]
    legit_trans = df_trans.loc[df_trans["fraud"] == 0]

    total_fraud = len(fraud_trans)
    total_legit = len(legit_trans)

    fraud_amount_count = (fraud_trans["amount_unusual"] == True).sum()
    legit_amount_count = (legit_trans["amount_unusual"] == True).sum()

    fraud_location_count = (fraud_trans["location_unusual"] == True).sum()
    legit_location_count = (legit_trans["location_unusual"] == True).sum()

    fraud_merchant_count = (fraud_trans["merchant_unusual"] == True).sum()
    legit_merchant_count = (legit_trans["merchant_unusual"] == True).sum()

    fraud_frequency_count = (fraud_trans["frequency_unusual"] == True).sum()
    legit_frequency_count = (legit_trans["frequency_unusual"] == True).sum()

    fraud_velocity_count = (fraud_trans["velocity_unusual"] == True).sum()
    legit_velocity_count = (legit_trans["velocity_unusual"] == True).sum()

    # Laplace smoothing
    p_amount_fraud = (fraud_amount_count + 1) / (total_fraud + 2)
    p_amount_legit = (legit_amount_count + 1) / (total_legit + 2)

    p_location_fraud = (fraud_location_count + 1) / (total_fraud + 2)
    p_location_legit = (legit_location_count + 1) / (total_legit + 2)

    p_merchant_fraud = (fraud_merchant_count + 1) / (total_fraud + 2)
    p_merchant_legit = (legit_merchant_count + 1) / (total_legit + 2)

    p_frequency_fraud = (fraud_frequency_count + 1) / (total_fraud + 2)
    p_frequency_legit = (legit_frequency_count + 1) / (total_legit + 2)

    p_velocity_fraud = (fraud_velocity_count + 1) / (total_fraud + 2)
    p_velocity_legit = (legit_velocity_count + 1) / (total_legit + 2)

    return (
        p_amount_fraud, p_amount_legit,
        p_location_fraud, p_location_legit,
        p_merchant_fraud, p_merchant_legit,
        p_frequency_fraud, p_frequency_legit,
        p_velocity_fraud, p_velocity_legit
    )


likelihoods = calculate_likelihoods(train_df)
print(likelihoods)



# In[307]:


def calculate_test_belief(transaction, likelihoods):

    evidence = {
        "amount_unusual": transaction["amount_unusual"],
        "location_unusual": transaction["location_unusual"],
        "merchant_unusual": transaction["merchant_unusual"],
        "frequency_unusual": transaction["frequency_unusual"],
        "velocity_unusual": transaction["velocity_unusual"]
    }

    return calculate_fraud_belief(
        evidence,
        likelihoods
    )


test_df["fraud_belief_new"] = test_df.apply(
    lambda row: calculate_test_belief(row, likelihoods),
    axis=1
)

print(
    test_df["fraud_belief_new"].describe()
)


# In[308]:


test_results = []

for _, transaction in test_df.iterrows():

    fraud_belief = transaction["fraud_belief_new"]

    costs = calculate_action_costs(fraud_belief)
    initial_action = choose_action(costs)

    final_action = initial_action

    if initial_action == "Question":

        evidence = {
            "amount_unusual": transaction["amount_unusual"],
            "location_unusual": transaction["location_unusual"],
            "merchant_unusual": transaction["merchant_unusual"],
            "frequency_unusual": transaction["frequency_unusual"],
            "velocity_unusual": transaction["velocity_unusual"]
        }

        questions = get_questions(evidence)

        answers = simulate_customer_response(
            transaction,
            questions
        )

        if "transaction_confirmation" in answers:
            final_action = handle_transaction_confirmation(
                answers["transaction_confirmation"]
            )

    test_results.append({
        "transaction_id": transaction["transaction_id"],
        "fraud_belief": fraud_belief,
        "initial_action": initial_action,
        "final_action": final_action,
        "actual_fraud": transaction["fraud"]
    })

test_results_df = pd.DataFrame(test_results)

print(test_results_df.head())


# In[309]:


print("\nINITIAL ACTIONS")
print(test_results_df["initial_action"].value_counts())

print("\nFINAL ACTIONS")
print(test_results_df["final_action"].value_counts())


# In[310]:


print("\nFINAL ACTION BY ACTUAL STATE")
print(
    pd.crosstab(
        test_results_df["actual_fraud"],
        test_results_df["final_action"]
    )
)


# In[311]:


#################### Legitimate transaction which was examined###############
print(
    test_results_df[
        (test_results_df["actual_fraud"] == 0) &
        (test_results_df["final_action"] == "Examine")
    ][
        [
            "transaction_id",
            "fraud_belief",
            "initial_action",
            "final_action"
        ]
    ]
)


# In[312]:


print(
    test_results_df[
        (test_results_df["actual_fraud"] == 1) &
        (test_results_df["final_action"] == "Examine")
    ][
        [
            "transaction_id",
            "fraud_belief",
            "initial_action",
            "final_action"
        ]
    ]
)


# In[313]:


from sklearn.metrics import precision_score, recall_score, confusion_matrix

y_true = test_results_df["actual_fraud"]

y_pred = (
    test_results_df["final_action"] == "Decline"
).astype(int)

print("Precision-every transaction automatically declined was actually fraud:", precision_score(y_true, y_pred))
print("Recall:", recall_score(y_true, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))


# In[314]:


total_legit = (test_results_df["actual_fraud"] == 0).sum()

legit_approved = (
    (test_results_df["actual_fraud"] == 0) &
    (test_results_df["final_action"] == "Approve")
).sum()

legit_examine = (
    (test_results_df["actual_fraud"] == 0) &
    (test_results_df["final_action"] == "Examine")
).sum()

question_count = (
    test_results_df["initial_action"] == "Question"
).sum()

examine_count = (
    test_results_df["initial_action"] == "Examine"
).sum()

print("Legitimate approval rate:",
      legit_approved / total_legit)

print("Legitimate examine rate:",
      legit_examine / total_legit)

print("Question rate:",
      question_count / len(test_results_df))

print("Examine rate:",
      examine_count / len(test_results_df))

print("Interaction rate:",
      (question_count + examine_count) / len(test_results_df))


# In[315]:


################# Threshold based ###############
policy_b_results = []

for _, transaction in test_df.iterrows():

    belief = transaction["fraud_belief_new"]

    initial_action = choose_action_threshold(belief)

    final_action = initial_action

    if initial_action == "Question":

        evidence = {
            "amount_unusual": transaction["amount_unusual"],
            "location_unusual": transaction["location_unusual"],
            "merchant_unusual": transaction["merchant_unusual"],
            "frequency_unusual": transaction["frequency_unusual"],
            "velocity_unusual": transaction["velocity_unusual"]
        }

        questions = get_questions(evidence)

        answers = simulate_customer_response(
            transaction,
            questions
        )

        if "transaction_confirmation" in answers:
            final_action = handle_transaction_confirmation(
                answers["transaction_confirmation"]
            )

    policy_b_results.append({
        "transaction_id": transaction["transaction_id"],
        "fraud_belief": belief,
        "initial_action": initial_action,
        "final_action": final_action,
        "actual_fraud": transaction["fraud"]
    })

policy_b_results_df = pd.DataFrame(policy_b_results)


# In[316]:


print("\nPOLICY B — INITIAL ACTIONS")
print(
    policy_b_results_df["initial_action"].value_counts()
)

print("\nPOLICY B — FINAL ACTIONS")
print(
    policy_b_results_df["final_action"].value_counts()
)


# In[317]:


print("\nPOLICY B — FINAL ACTION BY ACTUAL STATE")

print(
    pd.crosstab(
        policy_b_results_df["actual_fraud"],
        policy_b_results_df["final_action"]
    )
)


# In[318]:


def calculate_customer_metrics(results_df):

    legit = results_df[results_df["actual_fraud"] == 0]

    metrics = {
        "Legitimate approval rate":
            (legit["final_action"] == "Approve").mean(),

        "Legitimate question rate":
            (legit["initial_action"] == "Question").mean(),

        "Legitimate examine rate":
            (legit["final_action"] == "Examine").mean(),

        "Legitimate decline rate":
            (legit["final_action"] == "Decline").mean(),

        "Overall interaction rate":
            (results_df["initial_action"] == "Question").mean()
    }

    return metrics


print("POLICY A — CUSTOMER METRICS")
print(calculate_customer_metrics(test_results_df))

print("\nPOLICY B — CUSTOMER METRICS")
print(calculate_customer_metrics(policy_b_results_df))


# In[319]:


examined_b = policy_b_results_df[
    policy_b_results_df["initial_action"] == "Examine"
]

print("Number of examined transactions:", len(examined_b))

print("\nActual fraud distribution:")
print(examined_b["actual_fraud"].value_counts())

print("\nExamined transactions:")
print(
    examined_b[
        [
            "transaction_id",
            "fraud_belief",
            "actual_fraud",
            "final_action"
        ]
    ].sort_values("fraud_belief", ascending=False)
)

Transaction
     ↓
Initial evidence
     ↓
Calculate fraud belief
     ↓
Choose action
     ↓
 ┌─────────┬─────────┬─────────┐
Approve   Question  Examine
                       ↓
              Check last 24h activity
                       ↓
               Update evidence
                       ↓
              Recalculate belief
                       ↓
                Final action
# In[320]:


############### Enhancing Examine Action ####################
def examine_transaction(transaction, history):

    recent_transactions = history[
        (transaction["timestamp"] - history["timestamp"]).dt.total_seconds() / 3600 <= 24
    ]

    transactions_last_24h = len(recent_transactions)

    return {
        "transactions_last_24h": transactions_last_24h
    }


# In[322]:


# Pick one transaction from the test set
transaction = test_df.iloc[0]

# Get that customer's history
history = get_customer_history(
    transaction["customer_id"],
    transaction["timestamp"],
    customer_histories
)

# Run the examination
examination_result = examine_transaction(
    transaction,
    history
)

print(examination_result)


# In[323]:


# Find transactions where the examination finds at least 1
recent_activity_cases = []

for _, transaction in test_df.iterrows():

    history = get_customer_history(
        transaction["customer_id"],
        transaction["timestamp"],
        customer_histories
    )

    result = examine_transaction(transaction, history)

    if result["transactions_last_24h"] > 0:
        recent_activity_cases.append(
            (
                transaction["transaction_id"],
                transaction["fraud"],
                result["transactions_last_24h"]
            )
        )

print(recent_activity_cases[:10])


# In[324]:


def apply_examination(evidence, examination_result):

    if examination_result["transactions_last_24h"] >= 3:
        evidence["frequency_unusual"] = True

    return evidence


# In[325]:


apply_examination(evidence, examination_result)


# In[327]:


from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score
)

def calculate_final_metrics(results_df, policy_name):

    actual = results_df["actual_fraud"]

    # Treat Decline as an automatic fraud decision
    predicted_fraud = (
        results_df["final_action"] == "Decline"
    ).astype(int)

    # Basic classification metrics
    accuracy = accuracy_score(actual, predicted_fraud)
    precision = precision_score(actual, predicted_fraud, zero_division=0)
    recall = recall_score(actual, predicted_fraud, zero_division=0)
    f1 = f1_score(actual, predicted_fraud, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(
        actual,
        predicted_fraud
    ).ravel()

    # Customer experience
    legitimate = results_df[
        results_df["actual_fraud"] == 0
    ]

    legitimate_approval_rate = (
        legitimate["final_action"] == "Approve"
    ).mean()

    legitimate_question_rate = (
        legitimate["initial_action"] == "Question"
    ).mean()

    legitimate_examine_rate = (
        legitimate["final_action"] == "Examine"
    ).mean()

    legitimate_decline_rate = (
        legitimate["final_action"] == "Decline"
    ).mean()

    # Fraud handling
    fraud = results_df[
        results_df["actual_fraud"] == 1
    ]

    fraud_decline_rate = (
        fraud["final_action"] == "Decline"
    ).mean()

    fraud_examine_rate = (
        fraud["final_action"] == "Examine"
    ).mean()

    fraud_approved = (
        fraud["final_action"] == "Approve"
    ).sum()

    # Overall interaction
    interaction_rate = (
        results_df["initial_action"] == "Question"
    ).mean()

    # All fraud either declined or examined
    fraud_intercepted = (
        fraud["final_action"].isin(
            ["Decline", "Examine"]
        )
    ).sum()

    fraud_interception_rate = (
        fraud_intercepted / len(fraud)
    )

    metrics = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "True Negatives": tn,
        "False Positives": fp,
        "False Negatives": fn,
        "True Positives": tp,
        "Legitimate Approval Rate": legitimate_approval_rate,
        "Legitimate Question Rate": legitimate_question_rate,
        "Legitimate Examine Rate": legitimate_examine_rate,
        "Legitimate Decline Rate": legitimate_decline_rate,
        "Fraud Automatic Decline Rate": fraud_decline_rate,
        "Fraud Examine Rate": fraud_examine_rate,
        "Fraud Approved": fraud_approved,
        "Fraud Interception Rate": fraud_interception_rate,
        "Overall Interaction Rate": interaction_rate
    }

    print("\n" + "=" * 60)
    print(policy_name)
    print("=" * 60)

    for metric, value in metrics.items():

        if isinstance(value, float):
            print(f"{metric}: {value:.4f}")

        else:
            print(f"{metric}: {value}")

    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            actual,
            predicted_fraud
        )
    )

    return metrics

policy_a_metrics = calculate_final_metrics(
    test_results_df,
    "POLICY A — FINAL RESULTS"
)

policy_b_metrics = calculate_final_metrics(
    policy_b_results_df,
    "POLICY B — FINAL RESULTS"
)


# In[328]:


######################### Indetifying Incorrect Decisions ###########################33
# Find Policy A's false negatives
false_negatives = test_results_df[(test_results_df["actual_fraud"] == 1) &(test_results_df["final_action"] != "Decline")]

print("False negatives:", len(false_negatives))

# Show 5 cases
print(false_negatives[[
            "transaction_id",
            "fraud_belief",
            "initial_action",
            "final_action",
            "actual_fraud"
        ]
    ].head(5)
)


# In[329]:


failure_ids = [
    "LOC_C0997",
    "MERCH_C0718",
    "FREQ_C0834",
    "FREQ_C0467",
    "LOC_C0622"
]

print(
    test_df[
        test_df["transaction_id"].isin(failure_ids)
    ][
        [
            "transaction_id",
            "amount_unusual",
            "location_unusual",
            "merchant_unusual",
            "frequency_unusual",
            "velocity_unusual",
            "fraud_belief_new",
            "fraud"
        ]
    ].sort_values("transaction_id")
)


# In[333]:


df_trans[
    df_trans["transaction_id"] == "FREQ_C0514"
][
    [
        "transaction_id",
        "amount",
        "location",
        "merchant",
        "timestamp",
        "amount_unusual",
        "location_unusual",
        "merchant_unusual",
        "frequency_unusual",
        "velocity_unusual",
        "fraud"
    ]
]


# In[ ]:




