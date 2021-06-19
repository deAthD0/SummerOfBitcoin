import pandas as pd

global data
data = pd.read_csv("mempool.csv") 
data= data.sort_values(by='fee',ascending=False) 


def check_list(row):
    if str(row) in df:
        return True
    else:
        return False

def checkParents(row):
    global df, total_weight,current_fees, max_weight
    if(str(data.at[row,'parents '])!="nan"):
        list_of_parents=data.at[row,'parents '].split(";")
        for i in list_of_parents:   
            if(check_list(i)==True):
                continue
            else:
                if(total_weight+data.at[row,'weight']<=max_weight):
                    temp=data.index[data['tx_id'] == str(i)]
                    nRow=temp[0]
                    total_weight=total_weight+data.at[nRow,'weight']
                    current_fees=current_fees+data.at[nRow,'fee']
                    new_Row={'tx_id':data.at[nRow,'tx_id'], 'fee':data.at[nRow,'fee'], 'weight':data.at[nRow,'weight'],'parents ':str(data.at[nRow,'parents '])}
                    df=df.append(new_Row, ignore_index = True)                

        new_Row={'tx_id':data.at[row,'tx_id'], 'fee':data.at[row,'fee'], 'weight':data.at[row,'weight'],'parents ':str(data.at[row,'parents '])}
        df=df.append(new_Row, ignore_index = True)
    else:
        new_Row={'tx_id':data.at[row,'tx_id'], 'fee':data.at[row,'fee'], 'weight':data.at[row,'weight'],'parents ':str(data.at[row,'parents '])}
        df=df.append(new_Row, ignore_index = True)


def recurssive_checker():
    changed=False
    for row in data.index:
        if(check_list(data.at[row,'tx_id'])==True):
            continue
        else:
            for r in df.index:
                if(max_weight>=(total_weight-df.at[r,'weight']+data.at[row,'weight'])):
                    temp_fees=current_fees-df.at[r,'fee']+data.at[row,'fee']
                    if(temp_fees>current_fees):
                        checkParents(row)
                        df = df.drop(labels=r, axis=0)
                        new_Row={'tx_id':data.at[row,'tx_id'], 'fee':data.at[row,'fee'], 'weight':data.at[row,'weight'],'parents ':str(data.at[row,'parents '])}
                        df=df.append(new_Row, ignore_index = True)
                        changed=True
                        recurssive_checker()
        
def optimizer():

    changed=False
    for r in df.index:
        tempWeight=0
        tempFee=0
        l=[]      
        for row in data.index:
            tempWeight=tempWeight+data.at[row,'weight']
            tempFee=tempFee+data.at[row,'fee']
            if(df.at[r,'weight']>=tempWeight):
                if(df.at[r,'fee']<tempFee):
                    tWeight=tempWeight
                    tFee=tempFee
                    changed=True
                    l=l.append(l)

    if(changed==True):
        df = df.drop(labels=r, axis=0)
        for row in l:
            checkParents(row)
            new_Row={'tx_id':data.at[row,'tx_id'], 'fee':data.at[row,'fee'], 'weight':data.at[row,'weight'],'parents ':str(data.at[row,'parents '])}
            df=df.append(new_Row, ignore_index = True)
    
    optimizer()





                        

    

total_weight=0
current_fees=0
max_weight=4000000

df = pd.DataFrame(columns=['tx_id', 'fee', 'weight','parents '])
# Created a basic block filled with transactions
for row in data.index:
    if(total_weight+data.at[row,'weight']<=max_weight):
        total_weight=total_weight+data.at[row,'weight']
        current_fees=current_fees+data.at[row,'fee']
        checkParents(row)


for row in data.index:
    if(check_list(data.at[row,'tx_id'])==True):
        continue
    else:
        for r in df.index:
            if(max_weight>=(total_weight-df.at[r,'weight']+data.at[row,'weight'])):
                temp_fees=current_fees-df.at[r,'fee']+data.at[row,'fee']
                if(temp_fees>current_fees):
                    df = df.drop(labels=r, axis=0)
                    new_Row={'tx_id':data.at[row,'tx_id'], 'fee':data.at[row,'fee'], 'weight':data.at[row,'weight'],'parents ':str(data.at[row,'parents '])}
                    df=df.append(new_Row, ignore_index = True)



print(df)
print(total_weight)
print(current_fees)

with open('block.txt', 'w') as filehandle:
    for r in df.index:
        try:
            filehandle.write(str(df.at[r,'tx_id'])+'\n')
        except:
            pass

