import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('./IT_Salary_Survey_EU _2020.csv').drop_duplicates()

def printValues():
    print("Pohlavi:\n", data["Gender"].describe())
    print("Vek:\n", data["Age"].describe())
    print("Mesto:\n", data["City"].describe())
    print("Pozice:\n", data["Position "].describe())
    print("Zkusenosti:\n", data["Total years of experience"].describe())
    print("Zkusenosti v Nemecku:\n", data["Years of experience in Germany"].describe())
    print("Hlavni technologie technologie:\n", data["Your main technology / programming language"].describe())
    print("Ostatni technologie:\n", data["Other technologies/programming languages you use often"].describe())
    print("Rocni brutto plat:\n", data["Yearly brutto salary (without bonus and stocks) in EUR"].describe())
    print("Rocni brutto plat:\n", data["Yearly brutto salary (without bonus and stocks) in EUR"].median())
    print("Rocni bonusy:\n", data["Yearly bonus + stocks in EUR"].describe())
    print("Plat pred rokem:\n", data["Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"].describe())
    print("Plat pred rokem:\n", data["Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"].median())
    print("Bonusy pred rokem:\n", data["Annual bonus+stocks one year ago. Only answer if staying in same country"].describe())
    print("Dovolena:\n", data["Number of vacation days"].describe())
    print("Typ uvazku:\n", data["Employment status"].describe())
    print("Doba uvazku:\n", data["Сontract duration"].describe())
    print("Jazyk:\n", data["Main language at work"].describe())
    print("Velikost firmy:\n", data["Company size"].describe())
    print("Typ firmy:\n", data["Company type"].describe())
    print("Ztratily praci kvuli covidu?\n", data["Have you lost your job due to the coronavirus outbreak?"].describe())
    print("Kurzarbeit?:\n", data["Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week"].describe())
    print("Kurzarbeit?:\n", data["Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week"].median())
    print("covid bonusy?:\n", data["Have you received additional monetary support from your employer due to Work From Home? If yes, how much in 2020 in EUR"].describe())

def piegender():
    # Pohlavi
    data['Gender'].value_counts().plot.pie(autopct="%1.1f%%",fontsize=12,startangle=90, explode=[0.02] * 3, pctdistance=1.2, labeldistance=1.4)
    plt.ylabel("")
    plt.savefig('piegender.png')

def pay():

    # Need to remove the outlier data cuz they do be scuffed
    p01 = data['Yearly brutto salary (without bonus and stocks) in EUR'].quantile(0.1)
    p09 = data['Yearly brutto salary (without bonus and stocks) in EUR'].quantile(0.9)
    diff = p09 - p01 # diff between lowest 10% and top 90%

    upper_limit = p09 + 1.5 * diff  # multiply that difference by 1.5 and add to the upper limit
    lower_limit = p01 - 1.5 * diff  # same for low limit, but substract instead

    paydata = data[(data['Yearly brutto salary (without bonus and stocks) in EUR'] > lower_limit) & (data['Yearly brutto salary (without bonus and stocks) in EUR'] < upper_limit)]
    plt.hist(paydata['Yearly brutto salary (without bonus and stocks) in EUR'], bins=20, rwidth=0.9)
    plt.xlabel('Yearly brutto salary (without bonuses) in EUR')
    plt.ylabel("Number of responses")
    plt.savefig('payhisto.png', bbox_inches='tight')

    # make an interval out of age
    def lambda_interval(x):
        try:
            x = int(x)
        except:
            return "Unspecified"
        # intervals by 10 years
        if x < 20:
            x = "0-20"
        elif x < 30:
            x = "21-30"
        elif x < 40:
            x = "31-40"
        elif x < 50:
            x = "41-50"
        elif x < 60:
            x = "51-60"
        elif x < 70:
            x = "61-70"
        else:
            x = "71+"
        return x

    paydata['Age'] = paydata['Age'].apply(lambda_interval)
    plt.figure(figsize=(15,8)) 
    #sns.histplot(x='Yearly brutto salary (without bonus and stocks) in EUR', data=paydata,
    #            bins=20, hue='Age',multiple="stack")
    sns.boxplot(x='Age',y='Yearly brutto salary (without bonus and stocks) in EUR',data=paydata)
    plt.xlabel("Age")
    plt.ylabel("Yearly brutto salary (without bonus and stocks) in EUR")
    plt.savefig('payage.png', bbox_inches='tight')

    def lambda_experience(x):
        x = str(x)
        if x == '-1':
            return "0"
        # intervals by 2 years
        """
        if x < 3:
            x = "0-2"
        elif x < 5:
            x = "3-4"
        elif x < 7:
            x = "5-6"
        elif x < 9:
            x = "7-8"
        elif x < 11:
            x = "9-10"
        elif x < 13:
            x = "11-12"
        elif x < 15:
            x = "13-14"
        else:
            x = "15+"
        """
        return x
    
    def lambda_experience_sort(x):
        try:
            x = int(x)
        except:
            return -1
        # intervals by 2 years
        """
        if x < 3:
            x = 2
        elif x < 5:
            x = 4
        elif x < 7:
            x = 6
        elif x < 9:
            x = 8
        elif x < 11:
            x = 10
        elif x < 13:
            x = 12
        elif x < 15:
            x = 14
        else:
            x = 15
        """
        return x

    paydata['Total years of experience'] = paydata['Total years of experience'].apply(lambda_experience_sort)
    p099 = paydata['Total years of experience'].quantile(0.99)

    paydata = paydata[(paydata['Total years of experience'] != -1) & (paydata['Total years of experience'] < p099)]
    paydata = paydata.sort_values(by='Total years of experience', ascending=True)
    paydata['Total years of experience'] = paydata['Total years of experience'].apply(lambda_experience)
    plt.figure(figsize=(15,8)) 
    sns.scatterplot(data=paydata, x="Total years of experience", y="Yearly brutto salary (without bonus and stocks) in EUR")
    plt.xlabel("Total years of experience")
    plt.ylabel("Yearly brutto salary (without bonus and stocks) in EUR")
    plt.savefig('expsalary.png', bbox_inches='tight')

def technology():
    plt.figure(figsize=(15,8))
    sns.countplot(x=data['Your main technology / programming language'], order=data['Your main technology / programming language'].value_counts().iloc[:15].index)
    plt.xlabel("Main technology")
    plt.ylabel("Count")
    plt.savefig('technology.png', bbox_inches='tight')


def spreadout():
    piegender()
    pay()
    technology()


def lowerupper(column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1 # diff between lowest 25% and top 75%

    upper_limit = Q3 + 1.5 * IQR  # multiply that difference by 1.5 and add to the upper limit
    lower_limit = Q1 - 1.5 * IQR  # same for low limit, but substract instead
    return lower_limit, upper_limit

def outliers():

    lower_limit, upper_limit = lowerupper('Age')
    outliers_c = data['Age'][data['Age'] < lower_limit].count()
    outliers_c += data['Age'][data['Age'] > upper_limit].count()
    print("Odlehle hodnoty u veku:" ,outliers_c)

    lower_limit, upper_limit = lowerupper('Yearly brutto salary (without bonus and stocks) in EUR')
    outliers_c = data['Yearly brutto salary (without bonus and stocks) in EUR'][data['Yearly brutto salary (without bonus and stocks) in EUR'] < lower_limit].count()
    outliers_c += data['Yearly brutto salary (without bonus and stocks) in EUR'][data['Yearly brutto salary (without bonus and stocks) in EUR'] > upper_limit].count()
    print("Odlehle hodnoty u platu:" ,outliers_c)

    lower_limit, upper_limit = lowerupper('Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country')
    outliers_c = data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country']\
        [data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country'] < lower_limit].count()
    outliers_c += data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country']\
        [data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country'] > upper_limit].count()
    print("Odlehle hodnoty u platu pred rokem:" ,outliers_c)

    lower_limit, upper_limit = lowerupper('Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week')
    outliers_c = data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week']\
        [data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week'] < lower_limit].count()
    outliers_c += data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week']\
        [data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week'] > upper_limit].count()
    print("Odlehle hodnoty u kurzarbeitu:" ,outliers_c)

def missing():
    neccesary_data = data
    neccesary_data= neccesary_data.drop(columns=["Have you received additional monetary support from your employer due to Work From Home? If yes, how much in 2020 in EUR", \
        "Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week", "Annual bonus+stocks one year ago. Only answer if staying in same country",\
            "Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"])

    print("Pocet radku s chybejici hodnotou:", neccesary_data.isnull().any(axis=1).sum())
    n_of_missing = neccesary_data.isnull().sum(axis=1).tolist()
    empty_2_more = 0
    for value in n_of_missing:
        if value > 1:
            empty_2_more += 1
    print("Pocet radku, kde chybi vic nez 1 hodnota:", empty_2_more)
    	
    print(neccesary_data.isna().sum())

def correlate():
    print("Korelace mezi vekem a platem", data['Age'].corr(data['Yearly brutto salary (without bonus and stocks) in EUR']))
    print("Korelace mezi vekem a platem pred rokem",data['Age'].corr(data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country']))
    print("Korelace mezi vekem a kurzarbeitem",data['Age'].corr(data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week']))

    print("Korelace mezi platem a kurzarbeitem", data['Yearly brutto salary (without bonus and stocks) in EUR'].corr(data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week']))
    print("Korelace mezi platem a platem pred rokem", data['Yearly brutto salary (without bonus and stocks) in EUR'].corr(data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country']))
    
    print("Korelace mezi platem pred rokem a kurzarbeitem", data['Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country'].corr(data['Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week']))


#printValues()  # Prozkoumani atributu
#spreadout()    # Grafy
#outliers()     # Odlehle hodnoty, vychazi i z prozkoumani atributu
#missing()      # Chybejici hodnoty
correlate()     # Korelacni koeficienty
