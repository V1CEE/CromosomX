import pandas as pd
from matplotlib import pyplot as plt
from DataMgmt import *
from tqdm import tqdm

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


def chromosomXgraphGender():
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
    for prob in probs['cg']:
        fig = plt.figure()
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        valuesMalecurr = valuesMale.loc[prob]
        valuesFemalecurr = valuesFemale.loc[prob]
        ax1.scatter(ageMalelist, valuesMalecurr)
        ax1.set_title('Male ' + prob)
        ax1.set_xlabel('Age')
        ax1.set_ylabel('beta value')
        ax2.scatter(ageFemalelist, valuesFemalecurr)
        ax2.set_title('Female ' + prob)
        ax2.set_xlabel('Age')
        ax2.set_ylabel('beta value')
        fig.tight_layout()
        plt.show()

chromosomXgraphGender()