location_list = ['New Delhi', 'Mumbai', 'Goa', 'Pune']
merchant = "Amazon"
merchant_list = ['Amazon','Reliance','Max','HnM','Zara','Spar','Big Chill','Burger King']


transaction = [ {'current_amt':1478899000000000000,
                'avg_transaction':None,
                'location':None,
                'merchant':'Amazon',
                'transactions_in_the_last_hour':20,
              'avg_transaction_frequency_in_day':3},
               {'current_amt':150000,
                'avg_transaction':200,
                'location':None,
                'merchant':"HnM",
                'transactions_in_the_last_hour':20,
              'avg_transaction_frequency_in_day':3},
                {'current_amt':150000,
                'avg_transaction':None,
                'location':None,
                'merchant':'Big Chill',
                'transactions_in_the_last_hour':None,
              'avg_transaction_frequency_in_day':3}]

def check_amount(transaction,risk):
    if transaction['avg_transaction'] == None or transaction['current_amt'] > transaction['avg_transaction'] * 4:
        risk += 30
    return risk
def check_merchant(transaction,risk):
    if transaction['merchant'] == None:
        risk += 5
    elif transaction['merchant'] not in merchant_list:
        risk += 10
    return risk
def check_location(transaction,risk):
    if transaction['location'] == None:
        risk += 10
    elif transaction['location'] not in location_list:
        risk += 30
    return risk
def check_frequency(transaction,risk):
    if transaction['transactions_in_the_last_hour'] == None:
        risk += 20
    elif transaction['transactions_in_the_last_hour'] > transaction['avg_transaction_frequency_in_day'] * 2:
        risk += 30
    return risk
def count_missing(transaction,count):
    if transaction['avg_transaction'] == None:
        count+=1
    if transaction['location'] == None:
        count+=1
    if transaction['merchant'] == None:
        count+=1
    if transaction['transactions_in_the_last_hour'] == None:
        count+=1
    return count
def ask_questions(transaction,count):
    if transaction['avg_transaction'] == None:
        transaction['avg_transaction'] = input("Previous Transaction is missing, Is this a new Card?")
        count-=1
    if transaction['location'] == None:
        transaction['location'] = input("What is the location of your transaction?:")
        count-=1

    if transaction['merchant'] == None:
        transaction['merchant'] = input("What is the name of your merchant?:")
        count-=1
    if transaction['transactions_in_the_last_hour'] == None:
        print("Transaction Frequency data is unavaiable.")
        count-=1
    return count

j = 1
for i in transaction:
    risk = 0
    count = 0
    current_transaction = i

    print("Transaction:",j)
    risk = check_amount(current_transaction,risk)
    print("After amount:", risk)
    risk = check_frequency(current_transaction,risk)
    print("After frequency:", risk)
    
    risk = check_location(current_transaction,risk)
    print("After location:", risk)
    
    risk = check_merchant(current_transaction,risk)
    count = count_missing(current_transaction,count)
    print("Count of missing",count)
    if count >= 2:
        count = ask_questions(current_transaction,count)
        print("Updated",count)
    decision(risk,count)
    j+=1
    # print("After merchant:", risNnk)
    # # print(transaction[1])
def decision(risk,count):
    if count >= 2:       
        print("Missing value is more than 2 hence,Examine")
        return
    if risk <= 25:
        print("Approve")
    elif risk <= 50:
        print("Question")
    elif risk <= 70:
        print("Examine")
    else:
        print("Decline")

