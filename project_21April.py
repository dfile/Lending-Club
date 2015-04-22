#Data Incubator Challenge
#Project Proposal


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PATH_FUNDED = "/Users/danielwfile/Documents/Data Incubator Challenge/LoanStats3c.csv"
PATH_REJECT = "/Users/danielwfile/Documents/Data Incubator Challenge/RejectStatsb.csv"

SIZE = 5000

funded = pd.read_csv(PATH_FUNDED, nrows=SIZE, skiprows=1)
chunker = pd.read_csv(PATH_FUNDED, chunksize=100000, skiprows=1)



fundedE = funded[ funded['grade'] == "E" ]
fundedE =  fundedE[ (fundedE['home_ownership']=="MORTGAGE") | (fundedE['home_ownership']=="RENT" ) ]


fundedD = funded[ funded['grade'] == "D" ]
fundedD =  fundedD[ (fundedD['home_ownership']=="MORTGAGE") | (fundedD['home_ownership']=="RENT" ) ]

fundedA = funded[ funded['grade'] == "A" ]
fundedA =  fundedA[ (fundedA['home_ownership']=="MORTGAGE") | (fundedA['home_ownership']=="RENT" ) ]


#apply Current
def cur(status):
    if status == "Current" or status=="Fully Paid":
        return "Current"
    elif status == "Charged Off" or status == "Default":
        return "Default/Charged Off"
    else:
        return "Late"

fundedA["Current"] = fundedA["loan_status"].apply(cur)
fundedD["Current"] = fundedD["loan_status"].apply(cur)
fundedE["Current"] = fundedE["loan_status"].apply(cur)

ownershipLateD = pd.crosstab(fundedD.home_ownership, fundedD.Current)
ownershipLateD_pcts = ownershipLateD.div( ownershipLateD.sum(1).astype(float), axis=0)
#ownershipLateD_pcts.plot(kind='bar', stacked=True)
#plt.title('D Rated Loans')


ownershipLateA = pd.crosstab(fundedA.home_ownership, fundedA.Current)
ownershipLateA_pcts = ownershipLateA.div( ownershipLateA.sum(1).astype(float), axis=0)
#ownershipLateA_pcts.plot(kind='bar', stacked=True)

ownershipLateE = pd.crosstab(fundedE.home_ownership, fundedE.Current)
ownershipLateE_pcts = ownershipLateE.div( ownershipLateE.sum(1).astype(float), axis=0)
#ownershipLateE_pcts.plot(kind='bar', stacked=True)

def mortgageDefault(grade):
    chunker = pd.read_csv(PATH_FUNDED, chunksize=10000, skiprows=1)
    mort = 0
    mortLate = 0
    mortDefault = 0
    rent = 0
    rentLate = 0
    rentDefault = 0
    for part in chunker:
        part1 = part[ part['grade'] == grade ]
        part1 =  part1[ (part1['home_ownership']=="MORTGAGE") | (part1['home_ownership']=="RENT" ) ]
        part1["Current"] = part1["loan_status"].apply(cur)
        
        #crosstabs
        partTabs = pd.crosstab(part1.home_ownership, part1.Current)
        
        #count
        mort += part1[ part1["home_ownership"] == "MORTGAGE"].count()[1]
        mortLate += partTabs["Late"]["MORTGAGE"]
        if "Default/Charged Off" in partTabs.keys():
            mortDefault += partTabs["Default/Charged Off"]["MORTGAGE"]
        
        rent += part1[ part1["home_ownership"] == "RENT"].count()[1]
        rentLate += partTabs["Late"]["RENT"]
        if "Default/Charged Off" in partTabs.keys():
            rentDefault += partTabs["Default/Charged Off"]["RENT"]

    
    return {"Mortgage":(mort, mortLate, mortDefault, float(mortLate)/mort,
    float(mortDefault)/mort ), "Rent":(rent, rentLate, rentDefault,
    float(rentLate)/rent, float(rentDefault)/rent)}
        
#make a vector of default rates
defaultByGradeMort = [mortgageDefault(key)["Mortgage"][4] for key in ["A", "B", "C", "D", "E", "F"]]
defaultByGradeRent = [mortgageDefault(key)["Rent"][4] for key in ["A", "B", "C", "D", "E", "F"]]
lateByGradeMort = [mortgageDefault(key)["Mortgage"][3] for key in ["A", "B", "C", "D", "E", "F"]]
lateByGradeRent = [mortgageDefault(key)["Rent"][3] for key in ["A", "B", "C", "D", "E", "F"]]

    
#plot default rates
n_groups = 6
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4


rects1 = plt.bar(index, defaultByGradeMort, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Mortgage')

rects2 = plt.bar(index + bar_width, defaultByGradeRent, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Rent')
                 
plt.xlabel('Lending Club Grade')
plt.ylabel('Default Rate')
plt.title('Default Rates by Ownership Status and Lending Club Grade')
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F'))
plt.legend()

plt.tight_layout()
plt.show()

#plot lateness rates
n_groups = 6
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4


rects1 = plt.bar(index, lateByGradeMort, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Mortgage')

rects2 = plt.bar(index + bar_width, lateByGradeRent, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Rent')
                 
plt.xlabel('Lending Club Grade')
plt.ylabel('Lateness Rate')
plt.title('Lateness Rates by Ownership Status and Lending Club Grade')
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F'))
plt.legend()

plt.tight_layout()
plt.show()


