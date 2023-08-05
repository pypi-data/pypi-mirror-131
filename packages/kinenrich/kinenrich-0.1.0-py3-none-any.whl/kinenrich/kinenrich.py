# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:48:07 2021

@author: gy199
"""
import pandas as pd
import random
import statistics
import scipy.stats
import numpy as np
import os


def read_modificationratio(file_source,output_dir,exp_label = "",output_label = ""):    
    file = open(file_source,"r")

    line = file.readline()
    headers = line.split('\t')
    if(exp_label==""):
        ratio_label = 'Ratio'
        norm_ratio_label = 'Ratio normalized'
    else:
        ratio_label = 'Ratio '+exp_label
        norm_ratio_label = 'Ratio '+exp_label+' normalized'        
    df = pd.DataFrame(columns=['id','position','siteratio','normsiteratio'])
    tempdict = {}
    idindex = 0   
    line = file.readline()
    while(line):
        contents = line.split('\t')
        for i in range(0,len(headers)):
            tempdict[headers[i]] = contents[i]
        if (tempdict["Reverse"]!= '+' and tempdict["Potential contaminant"]!='+' and float(tempdict["Localization prob"])>=0.75 and tempdict["Protein"]!='' and tempdict[ratio_label]!=''):
            
                proid =  tempdict['Protein']
                df.loc[idindex] = [proid,tempdict['Position'],tempdict[ratio_label],tempdict[norm_ratio_label]] 
                idindex = idindex+1

        else:
            pass
        tempdict = {}
        line = file.readline()
    df.to_csv( path_or_buf=output_dir+'site_'+str(output_label)+'.csv', sep=',', index=False, mode='w+')
    return()


def read_proteinratio(file_source,output_dir,exp_label = "",output_label = ""):    
    file = open(file_source,"r")
    line = file.readline()
    headers = line.split('\t')
    if(exp_label==""):
        ratio_label = 'Ratio'
    else:
        ratio_label = 'Ratio '+exp_label
    df = pd.DataFrame(columns=['id','ratio'])
    tempdict = {}
    idindex = 0   
    line = file.readline()
    while(line):
        contents = line.split('\t')
        for i in range(0,len(headers)):
            tempdict[headers[i]] = contents[i]
        if (tempdict["Reverse"]!= '+' and tempdict["Potential contaminant"]!='+' and tempdict[ratio_label]!='NaN'  ):
                proids = tempdict['Majority protein IDs'].strip('\t').split(';')
                for proid in proids:
                    try:
                        proid =  proid.split('|')[1]
                        df.loc[idindex] = [proid,tempdict[ratio_label]] 
                        idindex = idindex+1
                    except:
                        pass
        else:
            pass
        tempdict = {}
        line = file.readline()
    df.to_csv( path_or_buf=output_dir+'pro_'+str(output_label)+'.csv', sep=',', index=False, mode='w+')
    return()




def conv_MQtable(file_source,output_dir,siteorpro,exp_label="",output_label=""):
    if(siteorpro=='site'):
        read_modificationratio(file_source,output_dir,exp_label,output_label)
    elif(siteorpro=='pro' or siteorpro=='protein'):
        read_proteinratio(file_source,output_dir,exp_label,output_label)
    else:
        print('Unvalid file type parameter, input "site" for site ratio file, or input "protein" for protein ratio file')
    return()

        
#format  
#From	To
#Q92597	NDRG1
def read_uniprot2genename(file_source):
    file = open(file_source,"r")
    #line = file.readline()
    #headers = line.split('\t')
    linkdict = {}
    line = file.readline().strip('\n')
    while(line):
        contents = line.split(',') 
        linkdict[contents[0]] = contents[1]
        line = file.readline().strip('\n')   
    return(linkdict)

def read_kindict(file_source):
    file = open(file_source,"r")
    line = file.readline()
    line = line.split(',')#skip header
    linkdict = {}
    line = file.readline().strip('\n')
    while(line):
        contents = line.split(',')
        subs = contents[1].split(';')
        linkdict[contents[0]] = subs
        line = file.readline().strip('\n')   
    return(linkdict)

def read_protein_groups(file_source):    
    proratiodict = {}
    proratiodf = pd.read_csv(file_source, delimiter = ",",header = 0)
    proratiodf = proratiodf[pd.to_numeric(proratiodf['ratio'], errors='coerce').notnull()]
    proratiodf.dropna(subset = ["ratio"], inplace=True)
    for i in proratiodf.index: 
            proratiodict[proratiodf.loc[i,'id']] = float(proratiodf.loc[i,'ratio'])
    return(proratiodict)


def read_phospho_sites(file_source,proratiodict,unitogenedict,input_type,normbypro = False,log2trans = True):
    df = pd.read_csv(file_source, delimiter = ",",header = 0)
    

    if (normbypro==True):
        df.drop(columns=['normsiteratio'])
        df = df[pd.to_numeric(df['siteratio'], errors='coerce').notnull()]
        df.dropna(subset = ["siteratio"], inplace=True)
    else:
        df.drop(columns=['siteratio'])
        df.rename(columns={"normsiteratio": "siteratio"})
        df = df[pd.to_numeric(df['siteratio'], errors='coerce').notnull()]
        df.dropna(subset = ["siteratio"], inplace=True)
    
    if (normbypro==True):
        if(log2trans == True):
            for i in df.index:
                try:
                    proratio = proratiodict[df.loc[i,'id']]
                    normratio = float(df.loc[i,'siteratio'])/proratio
                    df.loc[i,'siteratio']= np.log2(normratio)
                except:
                    df.loc[i,'siteratio']= np.nan 
            
        else:
            for i in df.index:            
                try:
                    proratio = proratiodict[df.loc[i,'id']]
                    normratio = float(df.loc[i,'siteratio'])-proratio
                except:
                    df.loc[i,'siteratio']= np.nan 
            
                
    else:
        if(log2trans == True):
            for i in df.index:
                df.loc[i,'siteratio']= np.log2(df.loc[i,'siteratio'])
        else:
            pass
        
    df.dropna(subset = ["siteratio"], inplace=True)
    siteratiodf =  pd.DataFrame(columns = ['genename','proteinid','position','siteratio','uni_posi'])
    if (input_type=="p"):
        siteratiodf[['proteinid','position','siteratio']] = df[['id','position','siteratio']]
        for i in siteratiodf.index:    
            try:
                siteratiodf.loc[i,'genename']  = unitogenedict[siteratiodf.loc[i,'proteinid']]
            except:
                pass
            siteratiodf.loc[i,'id_posi']  = str(siteratiodf.loc[i,'proteinid'])+'_'+str(siteratiodf.loc[i,'position'])

    elif(input_type=="g"):
        siteratiodf[['genename','position','siteratio']] = df[['id','position','siteratio']]
        for i in siteratiodf.index:    
            siteratiodf.loc[i,'id_posi']  = str(siteratiodf.loc[i,'genename'])+'_'+str(siteratiodf.loc[i,'position'])
    else:
        return()
    

    
    return(siteratiodf)


def sitetoavgproratio(df,input_type):
    avgprodf = pd.DataFrame(columns=['genename','proteinid','positions','siteratio','siteratios'])
    avgprorownum = 0
    if (input_type == "p"):
        for i in df.index: 
            idx = avgprodf.index[avgprodf['proteinid'] == df.loc[i,'proteinid']]
            if (len(idx) >0):
                    idx = idx[0]
                    avgprodf.loc[idx, 'positions'].append(df.loc[i,'position'])
                    if(df.loc[i,'siteratio']!=None):
                        avgprodf.loc[idx, 'siteratios'].append(df.loc[i,'siteratio'])
    
            elif(df.loc[i,'proteinid']!=''):
                    avgprodf.loc[avgprorownum,'genename']=df.loc[i,'genename']
                    avgprodf.loc[avgprorownum,'proteinid']=df.loc[i,'proteinid']
                    avgprodf.loc[avgprorownum,'positions']=[df.loc[i,'position']]
                    avgprodf.loc[avgprorownum,'siteratios']=[df.loc[i,'siteratio']]
                    avgprorownum = avgprorownum+1
                
    else:
        for i in df.index:
            idx = avgprodf.index[avgprodf['genename'] == df.loc[i,'genename']]
            if (len(idx) >0):
                    idx = idx[0]
                    avgprodf.loc[idx, 'positions'].append(df.loc[i,'position'])
                    if(df.loc[i,'siteratio']!=None):
                        avgprodf.loc[idx, 'siteratios'].append(df.loc[i,'siteratio'])
            elif(df.loc[i,'genename']!='NaN'):
                    avgprodf.loc[avgprorownum,'genename']=df.loc[i,'genename']
                    avgprodf.loc[avgprorownum,'proteinid']=df.loc[i,'proteinid']
                    avgprodf.loc[avgprorownum,'positions']=[df.loc[i,'position']]
                    avgprodf.loc[avgprorownum,'siteratios']=[df.loc[i,'siteratio']]
                    avgprorownum = avgprorownum+1
    avgprodf['siteratio'] = pd.DataFrame(avgprodf['siteratios'].values.tolist()).mean(1) 
    
    return(avgprodf)


def kinase_enrichment(siteratiodf,unitogenedict,kindict,input_type):
    kinenrichdf =  pd.DataFrame(columns = ['kinase_genename','kinase','site_count','site_avg','sample_avg','sample_std','p_value','substrate_ratio'])
    idx = 0
    ratio_sample = siteratiodf['siteratio']
    try:
        ratio_sample = [x for x in ratio_sample if ~np.isnan(x)]
    except:
        ratio_sample = list(filter(None, ratio_sample))

    for kinase in kindict.keys():
        kinsubstrate = kindict[kinase]
        try:
            subdf = siteratiodf.loc[siteratiodf['id_posi'].isin(kinsubstrate)]
        except:
            continue
        sitecount = len(subdf)
        substrate_ratio_list = []
        # for i in subdf['genename'].values.tolist():
        #     if (i not in substrate_list):
        #         substrate_list.append(i)
        #         substrate_ratio_list.append(i+)

        for i in subdf.index:
            try:
                substrate_ratio_str = subdf.loc[i,'genename']+'_'+str(int(subdf.loc[i,'position']))
            except:
                substrate_ratio_str = subdf.loc[i,'genename']+'_'+"NaN"
            if (substrate_ratio_str not in substrate_ratio_list):
                 substrate_ratio_list.append(substrate_ratio_str+':'+str(subdf.loc[i,'siteratio']))
            
        if(sitecount<1):  #cannot calculate is there's no data points
            continue
        siteavg = statistics.mean(subdf['siteratio'])
        sampleavglist = []
        for i in range(0,10000):
            randsample = random.choices(ratio_sample, k=sitecount)
            sampleavglist.append(statistics.mean(randsample))
        sampleavg = statistics.mean(sampleavglist)
        samplestd = statistics.stdev(sampleavglist)
        zscore = abs(siteavg-sampleavg)/samplestd
        pvalue = scipy.stats.norm.sf(abs(zscore))*2
        if(input_type=='p'):
            try:
                kinase_gene  = unitogenedict[kinase]
            except:
                kinase_gene  = ''
            kinenrichdf.loc[idx] = [kinase_gene,kinase,sitecount,siteavg,sampleavg,samplestd,pvalue,substrate_ratio_list]
        else:
            kinenrichdf.loc[idx] = [kinase,'',sitecount,siteavg,sampleavg,samplestd,pvalue,substrate_ratio_list]
        idx = idx+1 

    return(kinenrichdf)



 
    
    
def kinenrich(siteratio_dir,input_type,output_dir,exp_label='',proratio_dir="None",ratio_output=False,log2trans=True):     
    #input_type: 'UniprotAC' or "genename"
    module_dir = os.path.abspath(os.path.dirname(__file__))
    unitogenedict = read_uniprot2genename(module_dir+'/unigenedict.csv') 

    
    
    #############################################################################################
    #input_type section, return() if input_type is invalid
    if (input_type=="UniprotAC" or input_type=="Uniprot" or input_type=="protein"):
        input_type = "p"
    elif (input_type=="gene symbol" or input_type=="gene name" or input_type=="gene"):
        input_type = 'g'
    else:
        print("Invalid input_type, please use one of the following strings")
        print("\"UniprotAC\"or \"protein\"  example:Q00987,P40337,Q9HAU4,O43791,Q7Z6Z7")
        print("\"gene symbol\"or \"gene\"  example:MDM2,VHL,SMUF2,SPOP,HUWE1")
        return()
   
    
    if(input_type =='p'):
        kindict = read_kindict(module_dir+'/kindictpro.csv') 
    else:
        kindict = read_kindict(module_dir+'/kindictgene.csv') 
    
    print("Analyzing data of experiment "+exp_label)
    #############################################################################################
    #gather ratios from input files and output ratio files 
    if(proratio_dir=="None"):
        normbypro = False
        proratiodict = {}
    else:
        normbypro = True
        proratiodict = read_protein_groups(proratio_dir)
    siteratiodf = read_phospho_sites(siteratio_dir,proratiodict,unitogenedict,input_type,normbypro,log2trans)
    #avgsiteratiodf = sitetoavgproratio(siteratiodf,input_type) #from site ratio to average protein ratio
    if(ratio_output==True):
        siteratiodf.to_csv(output_dir+'/site_level_ratio'+str(exp_label)+'.csv', sep=',',index = False, encoding='utf-8') 

     
        
    #############################################################################################

    sitekinenrichdf = kinase_enrichment(siteratiodf,unitogenedict,kindict,input_type)

    for i in sitekinenrichdf.index:  
        sitekinenrichdf.loc[i,'substrate_ratio'] = ';'.join(sitekinenrichdf.loc[i,'substrate_ratio'])
    if (normbypro == True):
            sitekinenrichdf.to_csv(output_dir+'/kinase_enrich_site_level_normalized_by_protein'+str(exp_label)+'.csv', sep=',',index = False, encoding='utf-8') 
    else:   
            sitekinenrichdf.to_csv(output_dir+'/kinase_enrich_site_level'+str(exp_label)+'.csv', sep=',',index = False, encoding='utf-8')    

    return()


conv_MQtable("C:/Users/gy199/OneDrive/Desktop/Kinase_enrichment/12072021Haiping/HCT116 SILAC Large scale Phospho (STY)Sites_addcontrol without proteasome inhibitor.txt","C:/Users/gy199/OneDrive/Desktop/Kinase_enrichment/",siteorpro='site',exp_label="H/L",output_label="HL")
conv_MQtable("C:/Users/gy199/OneDrive/Desktop/Kinase_enrichment/12072021Haiping/proteinGroups.txt","C:/Users/gy199/OneDrive/Desktop/Kinase_enrichment/",siteorpro='protein',exp_label="H/L",output_label="HL")

 