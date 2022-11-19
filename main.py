import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('./IT_Salary_Survey_EU _2020.csv')

def printValues():
    print("Pohlavi:\n", data["Gender"].describe())
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

def spreadout():
    piegender()


#printValues()
spreadout()