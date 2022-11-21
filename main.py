import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

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
    print("Plat pred rokem:\n", data[
        "Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"].describe())
    print("Plat pred rokem:\n", data[
        "Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"].median())
    print("Bonusy pred rokem:\n",
          data["Annual bonus+stocks one year ago. Only answer if staying in same country"].describe())
    print("Dovolena:\n", data["Number of vacation days"].describe())
    print("Typ uvazku:\n", data["Employment status"].describe())
    print("Doba uvazku:\n", data["Сontract duration"].describe())
    print("Jazyk:\n", data["Main language at work"].describe())
    print("Velikost firmy:\n", data["Company size"].describe())
    print("Typ firmy:\n", data["Company type"].describe())
    print("Ztratily praci kvuli covidu?\n", data["Have you lost your job due to the coronavirus outbreak?"].describe())
    print("Kurzarbeit?:\n", data[
        "Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week"].describe())
    print("Kurzarbeit?:\n", data[
        "Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week"].median())
    print("covid bonusy?:\n", data[
        "Have you received additional monetary support from your employer due to Work From Home? If yes, how much in 2020 in EUR"].describe())


def piegender():
    # Pohlavi
    data['Gender'].value_counts().plot.pie(autopct="%1.1f%%", fontsize=12, startangle=90, explode=[0.02] * 3,
                                           pctdistance=1.2, labeldistance=1.4)
    plt.ylabel("")
    plt.savefig('piegender.png')


def pay():
    # Need to remove the outlier data cuz they do be scuffed
    p01 = data['Yearly brutto salary (without bonus and stocks) in EUR'].quantile(0.1)
    p09 = data['Yearly brutto salary (without bonus and stocks) in EUR'].quantile(0.9)
    diff = p09 - p01  # diff between lowest 10% and top 90%

    upper_limit = p09 + 1.5 * diff  # multiply that difference by 1.5 and add to the upper limit
    lower_limit = p01 - 1.5 * diff  # same for low limit, but substract instead

    paydata = data[(data['Yearly brutto salary (without bonus and stocks) in EUR'] > lower_limit) & (
                data['Yearly brutto salary (without bonus and stocks) in EUR'] < upper_limit)]
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
    plt.figure(figsize=(15, 8))
    # sns.histplot(x='Yearly brutto salary (without bonus and stocks) in EUR', data=paydata,
    #            bins=20, hue='Age',multiple="stack")
    sns.boxplot(x='Age', y='Yearly brutto salary (without bonus and stocks) in EUR', data=paydata)
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
    plt.figure(figsize=(15, 8))
    sns.scatterplot(data=paydata, x="Total years of experience",
                    y="Yearly brutto salary (without bonus and stocks) in EUR")
    plt.xlabel("Total years of experience")
    plt.ylabel("Yearly brutto salary (without bonus and stocks) in EUR")
    plt.savefig('expsalary.png', bbox_inches='tight')


def technology():
    plt.figure(figsize=(15, 8))
    sns.countplot(x=data['Your main technology / programming language'],
                  order=data['Your main technology / programming language'].value_counts().iloc[:15].index)
    plt.xlabel("Main technology")
    plt.ylabel("Count")
    plt.savefig('technology.png', bbox_inches='tight')


def spreadout():
    piegender()
    pay()
    technology()


def lowerupper(column, given_data):
    Q1 = given_data[column].quantile(0.25)
    Q3 = given_data[column].quantile(0.75)
    IQR = Q3 - Q1  # diff between lowest 25% and top 75%

    upper_limit = Q3 + 1.5 * IQR  # multiply that difference by 1.5 and add to the upper limit
    lower_limit = Q1 - 1.5 * IQR  # same for low limit, but substract instead
    return lower_limit, upper_limit


def printoutliers(column, given_data=data):
    lower_limit, upper_limit = lowerupper(column, given_data)
    outliers_c = given_data[column][given_data[column] < lower_limit].count()
    outliers_c += given_data[column][given_data[column] > upper_limit].count()
    print("Odlehle hodnoty u " + column + ":", outliers_c)


def print_edit_data(column, func):
    tmp = data
    tmp[column] = tmp[column].apply(func)  # convert to int
    tmp = tmp[tmp[column] != None]  # remove invalid values
    print(tmp[column].describe())
    print(tmp[column].median())
    printoutliers(column, given_data=tmp)


def outliers():
    printoutliers("Age")
    printoutliers("Yearly brutto salary (without bonus and stocks) in EUR")
    printoutliers(
        "Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country")
    printoutliers("Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week")

    ## look numerical, arent really -- need to convert them  first

    def tryInt(x):
        try:
            x = int(x)
        except:
            x = None  # random value
        return x

    print_edit_data('Total years of experience', tryInt)
    print_edit_data('Years of experience in Germany', tryInt)
    print_edit_data('Yearly bonus + stocks in EUR', tryInt)
    print_edit_data('Annual bonus+stocks one year ago. Only answer if staying in same country', tryInt)
    print_edit_data('Number of vacation days', tryInt)


def missing():
    neccesary_data = data
    neccesary_data = neccesary_data.drop(columns=[
        "Have you received additional monetary support from your employer due to Work From Home? If yes, how much in 2020 in EUR", \
        "Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week",
        "Annual bonus+stocks one year ago. Only answer if staying in same country", \
        "Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country"])

    print("Pocet radku s chybejici hodnotou:", neccesary_data.isnull().any(axis=1).sum())
    n_of_missing = neccesary_data.isnull().sum(axis=1).tolist()
    empty_2_more = 0
    for value in n_of_missing:
        if value > 1:
            empty_2_more += 1
    print("Pocet radku, kde chybi vic nez 1 hodnota:", empty_2_more)

    print(neccesary_data.isna().sum())


def prep_corr(attr1, attr2):
    def tryInt(x):
        try:
            x = int(x)
        except:
            x = None  # random value
        return x

    tmp = data
    tmp[attr1] = tmp[attr1].apply(tryInt)
    tmp = tmp[tmp[attr1] != None]  # remove invalid values
    tmp[attr2] = tmp[attr2].apply(tryInt)
    tmp = tmp[tmp[attr2] != None]  # remove invalid values

    print(attr1 + ",", attr2, (tmp[attr1].corr(tmp[attr2])))


def correlate():
    age = 'Age'
    yearlypay = 'Yearly brutto salary (without bonus and stocks) in EUR'
    yearlyyearago = 'Annual brutto salary (without bonus and stocks) one year ago. Only answer if staying in the same country'
    totexp = 'Total years of experience'
    germexp = 'Years of experience in Germany'
    kurzarbeit = 'Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week'
    yearlybonus = 'Yearly bonus + stocks in EUR'
    yearlybonusyearback = 'Annual bonus+stocks one year ago. Only answer if staying in same country'
    vacation = 'Number of vacation days'
    prep_corr(age, yearlypay)
    prep_corr(age, yearlyyearago)
    prep_corr(age, kurzarbeit)

    prep_corr(yearlypay, yearlyyearago)
    prep_corr(yearlypay, kurzarbeit)

    prep_corr(yearlyyearago, kurzarbeit)

    prep_corr(age, totexp)
    prep_corr(age, germexp)
    prep_corr(age, yearlybonus)
    prep_corr(age, yearlybonusyearback)
    prep_corr(age, vacation)

    prep_corr(yearlypay, totexp)
    prep_corr(yearlypay, germexp)
    prep_corr(yearlypay, yearlybonus)
    prep_corr(yearlypay, yearlybonusyearback)
    prep_corr(yearlypay, vacation)

    prep_corr(yearlyyearago, totexp)
    prep_corr(yearlyyearago, germexp)
    prep_corr(yearlyyearago, yearlybonus)
    prep_corr(yearlyyearago, yearlybonusyearback)
    prep_corr(yearlyyearago, vacation)

    prep_corr(kurzarbeit, totexp)
    prep_corr(kurzarbeit, germexp)
    prep_corr(kurzarbeit, yearlybonus)
    prep_corr(kurzarbeit, yearlybonusyearback)
    prep_corr(kurzarbeit, vacation)

    prep_corr(totexp, germexp)
    prep_corr(totexp, yearlybonus)
    prep_corr(totexp, yearlybonusyearback)
    prep_corr(totexp, vacation)

    prep_corr(germexp, yearlybonus)
    prep_corr(germexp, yearlybonusyearback)
    prep_corr(germexp, vacation)

    prep_corr(yearlybonus, yearlybonusyearback)
    prep_corr(yearlybonus, vacation)

    prep_corr(yearlybonusyearback, vacation)


# printValues()  # Prozkoumani atributu
# spreadout()    # Grafy
# outliers()     # Odlehle hodnoty, vychazi i z prozkoumani atributu
# missing()      # Chybejici hodnoty
correlate()  # Korelacni koeficienty



def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df
def remove_unrelated_attributes():
    data_filtered = data.drop(columns=["Timestamp", \
                                       "Yearly bonus + stocks in EUR", \
                                       "Annual bonus+stocks one year ago. Only answer if staying in same country", \
                                       "Have you lost your job due to the coronavirus outbreak?", \
                                       "Have you been forced to have a shorter working week (Kurzarbeit)? If yes, how many hours per week", \
                                       "Have you received additional monetary support from your employer due to Work From Home? If yes, how much in 2020 in EUR"])
    data_filtered = swap_columns(data_filtered, "Age", "Yearly brutto salary (without bonus and stocks) in EUR")
    data_filtered.to_csv("filtered_swaped.csv", index=True)


    data_filled = handle_missing_values(data_filtered)

    data_filled.to_csv("filtered_swaped_filled.csv", index=True)


    # differences
    pd.concat([data_filled, data_filtered]).drop_duplicates(keep=False)


def handle_missing_values(df:DataFrame) -> DataFrame:

    # To insert the mean value of each column into its missing rows:
    #df.fillna(df.mean(numeric_only=True).round(1), inplace=True)
    # For median:
    df.fillna(df.median(numeric_only=True), inplace=True)
    df.fillna("undefined", inplace=True)
    return df


if __name__ == "__main__":
    remove_unrelated_attributes()