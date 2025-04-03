# Author: Ho Wang Matthew Sung
# Title: dialect_typicality_calculation.py
# Version: 2
# Function: Counting characteristic features and dialect typicality of a particular dialect group per dialect
# Date of creation: 03-04-2025

import pandas as pd
import matplotlib.pyplot as plt

# dialect group name
group_name = str(input('What is the dialect group name?'))
num_of_feats = int(input('How many features?'))

# import typicality matrix
data = pd.read_excel(f"typicality_matrix_{group_name}_default.xlsx", index_col = 0)
# create list of localities
localities = list(data.columns.values)

### create a dataframe that matches the format of R
loc_list = []
score_list = []
iteration = []

# look at top 70 features
for i in range(10,num_of_feats+1,10): 
    df = data[:i]
    for j in range(len(localities)):
        name = str(localities[j])
        score = round((df[name].sum())/i, 2)
        no_of_items = str(i)
        loc_list.append(name)
        score_list.append(score)
        iteration.append(no_of_items)
        #print(name, score, no_of_items)

# get feature count intervals
features = []
for i in range(0, num_of_feats, 10):
    number = str(i+10)
    features.append(number)

# create dataframe for the typicality scores (per 10 features)
typicality = pd.DataFrame(zip(loc_list, score_list, iteration), columns = ['Localities', 'Typicality', 'Number of Features'])
typicality = typicality.pivot(index='Localities', columns='Number of Features', values='Typicality')
typicality = typicality[features].T

# create two subsets of locations (used in Sung 2025)
typicality_subset_Guangfu = typicality[['Foshan', 'Guangzhou', 'Hong Kong (Urban)', 'Macau', 'Panyu']]
typicality_subset_Siyi = typicality[['Guangzhou', 'Enping', 'Jiangmen', 'Doumen (Doumenzhen)', 'Taishan', 'Kaiping','Xinhui']]

# typicality score for selected Guangfu dialects
plot = typicality_subset_Guangfu.plot(title = f'Typicality of {group_name} Dialects by Number of Features')
plot.set_ylabel("Typicality")
lgd = plot.legend(fontsize = 10, loc = 'best', bbox_to_anchor = [1,1])#"upper right")
fig = plot.figure # created by Ho Wang Matthew Sung
fig.savefig(f'typicality_decay_plot_{group_name}_selected_Guangfu_dialects.jpg', dpi=600, bbox_inches='tight')

# typicality score for selected Siyi dialects
plot = typicality_subset_Siyi.plot(title = f'Typicality of {group_name} Dialects by Number of Features')
plot.set_ylabel("Typicality")
lgd = plot.legend(fontsize = 10, loc = 'best', bbox_to_anchor = [1,1])#"upper right")
fig = plot.figure
fig.savefig(f'typicality_decay_plot_{group_name}_selected_Siyi_dialects.jpg', dpi=600, bbox_inches='tight')