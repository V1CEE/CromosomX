import select
import os
from tqdm import tqdm
import pandas as pd
from DataMgmt import *
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from CrawlSettings import SeleniumUtils
from selenium.webdriver.common.by import By
from System import InsidePath as ip
from chromosomX import chromosomXprobsExtract, chromosomXgraphGender


def main_run():
    call = input("enter Read/Create/concat/chromosomXprobsExtract/chromosomXprobsgraghGender\n").lower()
    if call == 'create':
        seleniumCls = SeleniumUtils(r'https://www.metabolomicsworkbench.org/databases/proteome/MGP.php')
        main_df(seleniumCls)
    elif call == 'read':
        seleniumCls = SeleniumUtils(r'https://www.metabolomicsworkbench.org/databases/proteome/MGP.php')
        main_df_read(seleniumCls)
    elif call == 'concat':
        df = pd.concat([ReadfCSV('main_df'), ReadfCSV('MGPdf')], axis=1)
        Savedf2CSV(df, 'CromosomXgenes')
    elif call == 'chromosomxprobsextract':
        chromosomXprobsExtract()
    elif call == 'chromosomxprobsgraghgender':
        cgStart = input('enter cg to start graph from\n')
        if cgStart.isascii():
            chromosomXgraphGender(cgStart)
        elif cgStart == 0:
            chromosomXgraphGender(str(0))
        else:
            print('try again\n')
            main_run()
    else:
        print('try again\n')
        main_run()

def main_df(seleniumCls:SeleniumUtils):
    seleniumCls.OpenWebsite()
    dropDown = Select(seleniumCls.FindElementByXPATH('//select[@name="SMP_PATHWAY_ID"]'))
    count = Select(seleniumCls.FindElementByXPATH('//select[@name="nums"]'))
    df_list = []
    for i in tqdm(range(1, len(dropDown.options))):
        dropDown.select_by_index(i)
        count.select_by_visible_text("All")
        pathway_name = dropDown.first_selected_option.text
        button = seleniumCls.FindElementByXPATH("//input[@type='Submit']").click()
        df_list.append(pd.read_html(seleniumCls.driver.page_source)[2])
        df_list[-1]['pathway_name'] = pathway_name
        seleniumCls.OpenWebsite()
        count = Select(seleniumCls.FindElementByXPATH('//select[@name="nums"]'))
        dropDown = Select(seleniumCls.FindElementByXPATH('//select[@name="SMP_PATHWAY_ID"]'))
    df = pd.concat(df_list, ignore_index = True)
    df.drop('Enzyme/Reactants', axis=1, inplace=True)
    Savedf2CSV(df, 'main_df')

def main_df_read(seleniumCls:SeleniumUtils):
    df = ReadfCSV('main_df')
    Savedf2CSV(pd.concat(MGPdf(seleniumCls, df['MGP ID'].tolist()), ignore_index = True), 'MGPdf')


def MGPdf(seleniumCls:SeleniumUtils, mgp_num_list:list):
    df_list = []
    for i in tqdm(range(len(mgp_num_list))):
        pageurl = 'https://www.metabolomicsworkbench.org/databases/proteome/MGP_detail.php?MGP_ID=' + mgp_num_list[i]
        seleniumCls.driver.get(pageurl)
        seleniumCls.WaitElement(xpath="//*[@id='content']/table/tbody/tr/td/fieldset/table[1]")
        geneSymbol = seleniumCls.FindElementByXPATH("//a[@title='HGNC Gene symbol']").get_attribute('href')
        map_loc = seleniumCls.FindElementByXPATH("//th[text()='Map Location']/parent::tr/td").text
        chromosome = seleniumCls.FindElementByXPATH("//th[text()='Chromosome']/parent::tr/td").text
        try:
            synonyms = seleniumCls.FindElementByXPATH("//th[text()='Synonyms']/parent::tr/td").text
        except:
            synonyms = ''
        try:
            summary = seleniumCls.FindElementByXPATH("//th[text()='Summary']/parent::tr/td").text
        except:            summary = ''



        df_list.append(pd.DataFrame(data={ 'geneSymbol': mgp_num_list[i],'geneSymbol_link':geneSymbol, 'map_loc': map_loc, 'chromosome': chromosome, 'synonyms': synonyms, 'summary': summary}, index=[0]))
    return df_list


main_run()