# Author: Ho Wang Matthew Sung
# Title: dialect_typicality_calculation.py
# Function: Counting characteristic features and dialect typicality of a particular dialect group per dialect
# Date of creation: 03-04-2025

import pandas as pd
import numpy as np

def feat_count(no_of_feats, group_name):
    # import MSA data
    # data = pd.read_csv(r"Yue_full_ver1_no_NP_MSA.csv", sep=',', index_col = 'localities')
    data = pd.read_csv(r"C:\Users\Admin\Documents\Linguistics\PhD\Publications\Guangfu dialects\Typicality\Yue_full_ver1_no_NP_MSA_dialect_typicality.csv", sep=',', index_col = 'localities')

    # import nPMI score table from the nPMI calculation
    value = pd.read_csv(f"C:/Users/Admin/Documents/Linguistics/PhD/Publications/Guangfu dialects/CLIN paper/scripts and data/nPMI_feat_extraction_{group_name}.csv")
    # filter out features with nPMI lower than 0 (!!!!!! do we include 0??)
    value = value[value["nPMI"] > 0]

    ############## Set threshold for exclusivity and Representativeness #################
    # filter any features with exclusivity lower than ___
    value = value[value["Exclusivity"] > 0]
    # filter any features with proportion lower than ___
    value = value[value["Representativeness"] > 0]
    # reset index values ####### remember to turn this on when filters are used #########
    value = value.reset_index()

    ######## fill this in ########
    #get top X features; enter an integer or 'all' for all features (has to be a string)
    #number_of_features = 'all'
    number_of_features = no_of_feats

    if number_of_features == 'all':
        value = value
    else:
        value = value.head(number_of_features)

    # remember to replace ɮ back to 0 (this was changed because Gabmap does not recognise '0' as a category)

    # define a function which calculates the dialecthood (how much a dialect belongs to a cluster based on the nPMI score)

    # define a function which calculates the proportion of prototypical features that are present in each dialect # created by Ho Wang Matthew Sung
    ### require a string input
    def feature_proportion(dialect):    
        # subset the original dataset based on argument
        subset = pd.DataFrame(data.loc[dialect])
        # transform the subset dataframe so it is in row instead of column
        subset = subset.T
        
        # list of prototypical features in a dialect group
        feat_pool = list(value['Feature'])

        # empty list for storing number of items found in the subset data and for calculating the length of subset data
        feat_list = []
        
        # list of features present in the nPMI csv file (note: not variants!)
        trim_cols = list(value["Map"])
        #print('trimmed columns length', len(trim_cols))
        
        # convert list of features to string
        trim_cols_str = map(str, trim_cols)

        # reduce the subset dataset to only showing trimmed columns
        trim_data = subset[trim_cols_str]
        
        # set up temp empty list to store boolean results for the presence of features in a dialect
        temp = []
        
        # a for loop to interate finding the nPMI scores for each variant
        for i in range(0, trim_data.shape[1]):
            # find feature in the subset data
            feature = trim_data.columns[i]
            
            # find variant in the subset data
            variant = str(trim_data.iloc[0,i])
            
            # concatenate the variant and feature so that it matches the column in the nPMI csv file
            #concat = variant + '_' + feature
            concat = feature + '_' + variant
            
            # if statement to filter out variants which do not occur in the nPMI csv file (since they are not associated with the group)
            if value.at[i, 'Feature'] == concat:
                # append the variant to the feature list for the count of features in the dialect
                feat_list.append(concat)
                # append boolean item for the presence of the feature
                temp.append('Yes')
            else:
                # append boolean item for the absence of the feature
                temp.append('No')    
        # proportion of features: number of features present in dialect / number of features in the nPMI list (bigger than 0)
        prop_feats = round(len(feat_list)/len(feat_pool), 3)
        feat_count = len(feat_list)
        #print('Proportion of prototypical features', prop_feats)
        return prop_feats, feat_count

    # create empty lists to store calculated values for each dialect in the MSA file
    name_list2 = []
    dialect_proportion_list = []
    group_list2 = []
    excl_list2 = []
    prop_list2 = []
    feat_count_list = []

    # for loop to iterate function for the MSA file
    for i in range(0, len(data.index.values)):
        # define name of dialect/ locality
        name = str(data.index[i])
        # define dialecthood score
        dialect_proportion = feature_proportion(name)[0]
        # define feature count
        feature_count = feature_proportion(name)[1]
        #  define dialect group
        ##### remember to change out name ############
        group = group_name #str(input())
        # exclusivity threshold ############### set threshold ##################
        #excl = '>0.5'
        excl = 'default'
        # proportion threshold ############### set threshold ##################
        #prop = '>0.5'
        prop = 'default'
        # append all values to the list above
        name_list2.append(name)
        dialect_proportion_list.append(dialect_proportion)
        group_list2.append(group)
        excl_list2.append(excl)
        prop_list2.append(prop)
        feat_count_list.append(feature_count)
        print(name, feature_count, dialect_proportion)

    # create dataframe for the calculated values
    df_dialect_prop = pd.DataFrame({'Localities' : name_list2,
                                    'Number of Features': feat_count_list,
                                    f'Feat_prop_{number_of_features}' : dialect_proportion_list,
            'Group' : group_list2,
                                    'Exclusivity': excl_list2,
                                    'Reprsentativeness': prop_list2}, 
                                    columns=['Localities','Number of Features',f'Feat_prop_{number_of_features}', 'Group', 'Exclusivity', 'Representativeness'])

    df_dialect_prop.to_csv(f"Yue_dialect_feature_proportion_5_clusters_{group_name}_default_{number_of_features}feats.csv", index = False) # name based on Sung (2025)
    print('dialect proportion exported.')


# dialect group name
group_name = str(input('What is the dialect group name?'))
max_features = 70 # max feature is set as 70 following Sung (2025)

# for loop for extracting dialect typicality from a range of features
for i in range(10, (max_features + 10), 10): # python requires an addition of 10 to reach 70 in range()
    feat_count(i, group_name)