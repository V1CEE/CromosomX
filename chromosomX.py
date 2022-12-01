import pandas as pd

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


def cromosomXGenderMapper():
    probs = ReadfCSV('Probs')
    refbase = ReadfPARQUET('Healthy_REFBASE')
    info = ReadfPARQUET('HEALTHY_INFO')
    flag = 0
    probDict = {}
    for i,prob in enumerate(probs['cg']):
        data = refbase.loc[prob]
        dict = {}
        probDict = {}
        for obj in refbase.columns.values:
            dict[obj] = info.loc[obj]['gender']
        data.rename(index=dict, inplace = True)
        if flag == 0:
            df = data.copy()
            flag = 1
        elif flag == 1:
            df = pd.concat([df,data],axis=1)
    Savedf2CSV(df, 'ProbsGeder')

cromosomXGenderMapper()