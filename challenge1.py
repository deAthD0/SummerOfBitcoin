import pandas as pd

data = pd.read_csv("mempool.csv") 

# print(data)


global max_weight=4000000
global total_weight=0
global current_fees=0

# def parent_checker(row):
#     if str(data.at[row,'parents']) != "nan":
#         parent_list = str(data.at[row,'parents']).split(";")
#         for i in parent_list:
#             if(check_list(i)):
#                 continue
#             else:
#                 txnindex = df[df['tx_id'] == i].index.item()
#                 k = df.loc[txnindex]
#                 check_add_txn(k)

# print(type(max_weight))
# print(len(data))
# Adding number transactions till the block is filled
for row in data.index:
    if(total_weight+data.at[row,'weight']<=max_weight):
        total_weight=total_weight+data.at[row,'weight']
        current_fees=current_fees+data.at[row,'fee']
        # Todo add transactions here

print(total_weight)
print(current_fees)


# Todo create a  parent checker list
# If parennt added continue else add the paprent ------> recusrive funtion to check for parents
# Add transactions
# replace better values with worse ones
# Once a value has been changed try to iterate all value

# print(data.info)
# print(data.dtypes)
# print(data.describe)
# # def addToBlock(total_weight, weight , fees , tx_id):
# # 	if((total_weight + weight < max_weight)):
# # 		transactions.append(tx_id)
# # 		TOTAL_WEIGTH = TOTAL_WEIGTH + int(weight)
# # 		max_fees = max_fees + int(fees)
		
# # 		return True
# # 	else:
# # 		return False