import pandas as pd
from matplotlib import pyplot as plt
from DataMgmt import *
from tqdm import tqdm
import warnings

def chromosomXprobsExtract(): #all probs of chromosomX related genes
    all_450 = ReadfCSV('all_450K')
    df = ReadfCSV('GeneralGenes')
    genes = df[df['chromosome'] == 'X']
    del(df)
    genes.drop_duplicates(inplace = True)
    refbase = ReadfPARQUET('Healthy_REFBASE')
    info = ReadfPARQUET('HEALTHY_INFO')
    flag = 0
    for inx in tqdm(range(genes.shape[0])):
        geneName = genes.iloc[inx]['Symbol']
        Geneprobs = all_450[all_450['UCSC_RefGene_Name'] == geneName]
        for idx,prob in enumerate(Geneprobs.iloc[:,0]):
            dict = {'cg':prob,'Symbol':genes.iloc[inx]['Symbol'] ,'MGP ID':genes.iloc[inx]['MGP ID'] ,'Entrez Gene ID':genes.iloc[inx]['Entrez Gene ID'] ,'Gene name':genes.iloc[inx]['Gene name'] ,'pathway_name':genes.iloc[inx]['pathway_name'] ,'geneSymbol_link':genes.iloc[inx]['geneSymbol_link'] ,'UCSC_RefGene_Group':Geneprobs.iloc[idx]['UCSC_RefGene_Group'],'UCSC_CpG_Islands_Name':Geneprobs.iloc[idx]['UCSC_CpG_Islands_Name'],'Relation_to_UCSC_CpG_Island':Geneprobs.iloc[idx]['Relation_to_UCSC_CpG_Island'],'Regulatory_Feature_Name':Geneprobs.iloc[idx]['Regulatory_Feature_Name'],'Regulatory_Feature_Group':Geneprobs.iloc[idx]['Regulatory_Feature_Group']}
            if flag == 1:
                tempdf = pd.DataFrame(dict, index=[0])
                df = pd.concat([df,tempdf], ignore_index=True)
            elif flag == 0:
                df = pd.DataFrame(dict, index=[0])
                flag = 1
    Savedf2CSV(df, 'Probs')


def chromosomXgraphGender(cgStart: str):
    probs = ReadfCSV('Probs')
    refbase = ReadfPARQUET('Healthy_REFBASE')
    info = ReadfPARQUET('HEALTHY_INFO')
    refcols = refbase.columns.values.tolist()
    gsmMaleList = [idx for idx in refcols if info['gender'][idx] == 'male']
    ageMalelist = info.loc[gsmMaleList]['age'].tolist()
    valuesMale = refbase[gsmMaleList]
    gsmFemaleList = [idx for idx in refcols if info['gender'][idx] == 'female']
    ageFemalelist = info.loc[gsmFemaleList]['age'].tolist()
    valuesFemale = refbase[gsmFemaleList]
    if cgStart == str(0):
        pass
    elif cgStart.isascii():
        idx = probs['cg'].tolist().index(cgStart)
        probs = probs.iloc[probs['cg'].tolist().index(cgStart):]
    for prob in probs['cg']:
        fig = plt.figure()
        fig.suptitle(prob)
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        valuesMalecurr = valuesMale.loc[prob]
        valuesFemalecurr = valuesFemale.loc[prob]
        ax1.scatter(ageMalelist, valuesMalecurr)
        ax1.set_title('Male')
        ax1.set_xlabel('Age')
        ax1.set_ylabel('beta value')
        ax2.scatter(ageFemalelist, valuesFemalecurr)
        ax2.set_title('Female')
        ax2.set_xlabel('Age')
        ax2.set_ylabel('beta value')
        fig.tight_layout()
        plt.show()

def chromosomXnonStationary():
    warnings.filterwarnings("ignore", category=UserWarning, module="pandas")
    from statsmodels.tsa.stattools import adfuller
    probs = ReadfCSV('Probs').index.values.tolist()
    refbase = ReadfPARQUET('HEALTHY_REFBASE')
    info = ReadfPARQUET('HEALTHY_INFO')
    df = refbase.T.copy()
    df = df[probs]
    df.index = info.loc[df.index.values.tolist()]['age']
    df2 = pd.DataFrame()
    df = df.T
    df.drop_duplicates(inplace=True)
    for col in tqdm(df.index.values.tolist()):
        series = df.loc[col].groupby(df.columns.values.tolist())
        series = series.mean()
        result = adfuller(series)
        p_value = result[1]
        if p_value <= 0.05:
            df2[col] = df.loc[col]
            Savedf2CSV(df2, 'probsNonStatinary')
        else:
            pass
    df2.index = refbase.columns
    Savedf2CSV(df2,'probsNonStatinary')

def IQR(data :pd.DataFrame, prob: str):
    df = data.copy()
    mean = df[prob].mean()
    std = df[prob].std()
    for idx in df.index:
        if df.loc[idx][prob] > mean + 2*std or df.loc[idx][prob] < mean - 2*std:
            df.drop(idx, axis=0, inplace=True)
    return df

def chromosomXgraphStationary():
    probsNonStatinary = ReadfCSV('probsNonStatinary')
    probs = probsNonStatinary.columns.values.tolist()
    info = ReadfPARQUET('HEALTHY_INFO')
    ages = info.loc[probsNonStatinary.index]['age']
    df = pd.DataFrame()
    for prob in probs:
        df['ages'] = ages
        df[prob] = probsNonStatinary[prob]
        df = IQR(df,prob)
        fig = plt.figure()
        fig.suptitle(prob)
        ax1 = plt.subplot(111)
        ax1.scatter(df['ages'], df[prob])
        plt.savefig('Images' + os.sep + prob + '.png')
        plt.tight_layout()

def chromosomXgraphStationary3plots():
    probsNonStatinary = ReadfCSV('probsNonStatinary')
    probs = probsNonStatinary.columns.values.tolist()
    info = ReadfPARQUET('HEALTHY_INFO')
    ages = info.loc[probsNonStatinary.index]['age']
    df = pd.DataFrame()
    for prob in probs:
        df['ages'] = ages
        df[prob] = probsNonStatinary[prob]
        df = IQR(df,prob)
        fig = plt.figure()
        fig.suptitle(prob)
        ax1 = plt.subplot(311)
        ax1.scatter(df['ages'], df[prob])
        ax2 = plt.subplot(312)
        means = df[prob].groupby(df['ages']).mean()
        ax2.scatter(means.index.values, means)
        ax3 = plt.subplot(313)
        std = df[prob].groupby(df['ages']).std()
        ax3.scatter(std.index.values, std)
        plt.savefig('Images/3Plots' + os.sep + prob + '.png')
        plt.tight_layout()


def chromosomXgraphStationary3plotsGender(cgstart:str, gender:str):
    probsNonStatinary = ReadfCSV('probsNonStatinary')
    probs = probsNonStatinary.columns.values.tolist()
    info = ReadfPARQUET('HEALTHY_INFO')
    merged = probsNonStatinary.merge(info, left_index=True, right_index=True)
    males_ages = merged[merged['gender'] == 'male']['age']
    male_gsm = merged[merged['gender'] == 'male'].index.values.tolist()
    female_ages = merged[merged['gender'] == 'female']['age']
    female_gsm = merged[merged['gender'] == 'female'].index.values.tolist()
    df = pd.DataFrame()
    if gender == 'male':
        for prob in tqdm(probs[probs.index(cgstart):]):
            df['ages'] = males_ages
            df[prob] = merged.loc[male_gsm][prob]
            df = IQR(df,prob)
            fig = plt.figure()
            fig.suptitle(prob)
            ax1 = plt.subplot(311)
            ax1.scatter(df['ages'], df[prob])
            ax2 = plt.subplot(312)
            means = df[prob].groupby(df['ages']).mean()
            ax2.scatter(means.index.values, means)
            ax3 = plt.subplot(313)
            std = df[prob].groupby(df['ages']).std()
            ax3.scatter(std.index.values, std)
            plt.savefig('Images/3Plots' + os.sep + prob + 'Male.png')
            plt.tight_layout()
    else:
        for prob in probs[probs.index(cgstart):]:
            df['ages'] = female_ages
            df[prob] = merged.loc[female_gsm][prob]
            df = IQR(df,prob)
            fig = plt.figure()
            fig.suptitle(prob)
            ax1 = plt.subplot(311)
            ax1.scatter(df['ages'], df[prob])
            ax2 = plt.subplot(312)
            means = df[prob].groupby(df['ages']).mean()
            ax2.scatter(means.index.values, means)
            ax3 = plt.subplot(313)
            std = df[prob].groupby(df['ages']).std()
            ax3.scatter(std.index.values, std)
            plt.savefig('Images/3Plots' + os.sep + prob + 'Female.png')
            plt.tight_layout()


chromosomXgraphStationary3plotsGender('cg00121904','female')