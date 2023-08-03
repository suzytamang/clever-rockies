# This script removes tags that are subsets of another class. CLEVER already accounts
# for subsets that get tagged within the same class.
# coding: utf-8

import pandas as pd
import os
import re
import sys
import json
import csv
import argparse
import pattern
from os.path import exists
#import spacy

parser = argparse.ArgumentParser()
parser.add_argument('-t','--target', type = str, required = True, 
                    help = 'Path for TARGET class')
parser.add_argument('-d','--dictionary', type =str, required = True, 
                    help = 'Path and filename for the dictionary')
parser.add_argument('-c','--crossclass', type =str, required = True, 
                    help = 'File name of the cross_class_items list. This file is assumed to be in the same location as the dictionary')
args = parser.parse_args()

DICTIONARY_DATA = args.dictionary
NEG_DATA = os.path.join(args.target, "allNeg.txt")
POS_DATA = os.path.join(args.target, "allPos.txt")
CROSS_LIST = args.crossclass

cross_tagging_removed_POS=os.path.join(args.target, "allPos_cross_tag.txt")
cross_tagging_removed_NEG=os.path.join(args.target, "allNeg_cross_tag.txt")
output_POS=os.path.join(args.target, "allPos_cross_tag_removed.txt")
output_NEG=os.path.join(args.target, "allNeg_cross_tag_removed.txt")
dict_file =pd.read_csv(DICTIONARY_DATA, sep="|",header=0)

dict_file.columns =['dict_ID','TERM','CLASS','SUBCLASS']


def cross_tag_search(DATA,OUTPUT_DATA,REMOVED_DATA,cross_class):
    
    #DATA: either all_POS_patched.txt or all_NEG_patched.txt from step4
    #OUTPUT_DATA: results after removed cross class tag
    #REMOVED_DATA: removed tags
    if os.path.exists(DATA) and os.path.getsize(DATA)>0:
        all_data =pd.read_csv(DATA, sep="|", header = None, on_bad_lines = 'warn', keep_default_na = False)
        print("Processing "+ DATA +".....")
        to_be_dropped =[]
        for each_snippet_ID,each_dict_ID, each_snippet in zip(all_data[2], all_data[13],all_data[18]):
            if str(each_dict_ID) in cross_class:
                #if each_dict_ID == 8750:
                #    print(each_snippet_ID,each_dict_ID)
                for each_parent in cross_class[str(each_dict_ID)]:
                    if dict_file['TERM'].loc[dict_file["dict_ID"]==each_parent].to_string(index=False) in each_snippet:
                        to_be_dropped.append(each_snippet_ID) 
        after_cross_tags_removed = all_data[~all_data[2].isin(to_be_dropped)]
        removed_cross_tags = all_data[all_data[2].isin(to_be_dropped)]
        if not after_cross_tags_removed.empty:
            after_cross_tags_removed.to_csv(OUTPUT_DATA,sep='|',index= False, header = False)
        else:
            open(OUTPUT_DATA,'w').close()
        if not removed_cross_tags.empty:
            removed_cross_tags.to_csv(REMOVED_DATA,sep='|',index= False, header = False)
        else:
            open(REMOVED_DATA,'w').close()
    return

cross_class_sub_path= os.path.join(os.path.dirname(args.dictionary),CROSS_LIST)
if os.path.exists(cross_class_sub_path):
	with open(os.path.join(os.path.dirname(args.dictionary),CROSS_LIST)) as file:
		cross_class_items_data = file.read()
else:
	print("cross_class_items file in the dictionary folder does not exist. Use clever_dict_creator.py with the -g option to create one.")
cross_class_sub = json.loads(cross_class_items_data)
cross_tag_search(NEG_DATA,output_NEG,cross_tagging_removed_NEG, cross_class_sub)
cross_tag_search(POS_DATA,output_POS,cross_tagging_removed_POS, cross_class_sub)



##### TESTING #####
'''if os.path.exists(NEG_DATA) and os.path.getsize(NEG_DATA)>0:
    all_Neg =pd.read_csv(NEG_DATA, sep="|", header = None, on_bad_lines = 'warn', keep_default_na = False)

    print("Processing allNeg......")
    to_be_dropped =[]
    for each_snippet_ID,each_dict_ID, each_snippet in zip(all_Neg[2], all_Neg[13],all_Neg[18]):
        if each_dict_ID in cross_class:
            for each_parent in cross_class[each_dict_ID]:
                if dict_file['TERM'].loc[dict_file["dict_ID"]==each_parent].to_string(index=False) in each_snippet:
                    to_be_dropped.append(each_snippet_ID) 
    all_NEG = all_Neg[~all_Neg[2].isin(to_be_dropped)]
    new_all_NEG_removed = all_Neg[all_Neg[2].isin(to_be_dropped)]


    if not all_NEG.empty:
        all_NEG.to_csv(TEST_output_NEG,sep='|',index= False, header = False)
    else:
        open(TEST_output_NEG,'w').close()
    if not new_all_NEG_removed.empty:
        new_all_NEG_removed.to_csv(cross_tagging_removed_NEG,sep='|',index= False, header = False)
    else:
        open(cross_tagging_removed_NEG,'w').close()

if os.path.exists(POS_DATA) and os.path.getsize(POS_DATA)>0:
    print("Processing allPos ......")

    all_Pos =pd.read_csv(POS_DATA, sep="|", header = None, on_bad_lines = 'warn', keep_default_na = False)
    to_be_dropped =[]
    for each_snippet_ID,each_dict_ID, each_snippet in zip(all_Pos[2], all_Pos[13],all_Pos[18]):
        if each_dict_ID in cross_class:
            for each_parent in cross_class[each_dict_ID]:
                if dict_file['TERM'].loc[dict_file["dict_ID"]==each_parent].to_string(index=False) in each_snippet:
                    to_be_dropped.append(each_snippet_ID)
    all_POS = all_Pos[~all_Pos[2].isin(to_be_dropped)]
    new_all_POS_removed = all_Pos[all_Pos[2].isin(to_be_dropped)]
    if not all_POS.empty:
        all_POS.to_csv(TEST_output_POS,sep='|', index=False, header =False)
    else:
        open(TEST_output_POS,'w').close()
    if not new_all_POS_removed.empty:
        new_all_POS_removed.to_csv(cross_tagging_removed_POS,sep='|', index=False, header =False)
    else:
        open(cross_tagging_removed_POS,'w').close()
#TODO: cross_class_substrings() should be standalone function so that it will run only once for all classes.
def cross_class_substrings():
    cross_class = {}
    print("Searching for cross class substrings .....")
    for sub_str_id,sub_str_term, sub_str_class in zip(dict_file['dict_ID'],dict_file['TERM'],dict_file['CLASS']):
        for each_id,each_term, each_class in zip(dict_file['dict_ID'],dict_file['TERM'],dict_file['CLASS']):
            if sub_str_term in each_term.split() and sub_str_term!=each_term and (sub_str_class.startswith("HOPE") or sub_str_class.startswith("CONNECT") \
         or sub_str_class.startswith("CAPACITY") or sub_str_class.startswith("PPAIN"))\
         and   (each_class.startswith("HOPE") or each_class.startswith("CONNECT") \
         or each_class.startswith("CAPACITY") or each_class.startswith("PPAIN"))\
        and each_class!=sub_str_class:
                cross_class.setdefault(sub_str_id,[]).append(each_id)
    return cross_class
'''
