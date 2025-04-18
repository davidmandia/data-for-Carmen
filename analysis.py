## Look at comparison between 2018 and 2024 

## Check with Income / child poverty 


## compare with above and below average 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import openpyxl


# Load the data separately 2018 and 2024 
df_2018 = pd.read_csv('data/GCSE_data_English language_2018_Aged 17 to 19_4 and above_Grade outcomes.csv')
df_2024 = pd.read_csv('data/GCSE_data_English language_2024_Aged 17 to 19_4 and above_Grade outcomes.csv')

# Create a column in each dataframe with difference between county average and national ( last column)
df_2018['Difference_from_England_average_2018'] = df_2018.iloc[:, -2] - df_2018.iloc[:, -1]
df_2024['Difference_from_England_average_2024'] = df_2024.iloc[:, -2] - df_2024.iloc[:, -1]
 
## Merge dataframe on column County
df_merged_2018_vs_2024 = pd.merge(df_2018, df_2024, on='County', suffixes=('_2018', '_2024'))
# Check the first few rows of the merged dataframe
#print(df_merged_2018_vs_2024.head())

df_children = pd.read_excel('data/children_by_town.xlsx')


# Make sure the columns are strings before applying string filtering
df_children['Percentage_of_children_2018'] = df_children['Percentage_of_children_2018'].astype(str)
df_children['Percentage_of_children_2024'] = df_children['Percentage_of_children_2024'].astype(str)

# Now safely remove rows where the percentage columns contain '[x]'
df_children = df_children[~df_children['Percentage_of_children_2018'].str.contains(r'\[x\]', na=False)]
df_children = df_children[~df_children['Percentage_of_children_2024'].str.contains(r'\[x\]', na=False)]

# Strip % and convert to float
df_children['Percentage_of_children_2018'] = df_children['Percentage_of_children_2018'].str.rstrip('%').astype(float)
df_children['Percentage_of_children_2024'] = df_children['Percentage_of_children_2024'].str.rstrip('%').astype(float)

print(df_children.head())





# Group by county to compute totals and weighted averages
def weighted_avg(group, value_col, weight_col):
    total_weight = group[weight_col].sum()
    if total_weight == 0:
        return 0
    return (group[value_col] * group[weight_col]).sum() / total_weight


# Make sure number columns are numeric — convert strings to numbers
df_children['Number_ of_children_2018'] = pd.to_numeric(df_children['Number_ of_children_2018'], errors='coerce')
df_children['Number_ of_children_2024'] = pd.to_numeric(df_children['Number_ of_children_2024'], errors='coerce')



summary = df_children.groupby('County').apply(
    lambda g: pd.Series({
        'Total_children_2018': g['Number_ of_children_2018'].sum(),
        'Total_children_2024': g['Number_ of_children_2024'].sum(),
        'Weighted_percentage_2018': weighted_avg(g, 'Percentage_of_children_2018', 'Number_ of_children_2018'),
        'Weighted_percentage_2024': weighted_avg(g, 'Percentage_of_children_2024', 'Number_ of_children_2024'),
    })
).reset_index()

print(summary)

# save to csv
summary.to_csv('data/summary_by_county_2018_vs_2024.csv', index=False)

#print(df_merged_2018_vs_2024['County'].unique())
#print(summary['County'].unique())


replace_map = {
    'Bristol, City of': 'County of Bristol',
    'County Durham': 'Durham',
    'Herefordshire, County of': 'Herefordshire',
    'Cheshire East': 'Cheshire',
    'Cheshire West and Chester': 'Cheshire',
    'Bedford': 'Bedfordshire',
    'Central Bedfordshire': 'Bedfordshire',
    'West Berkshire': 'Berkshire',
    'Cumberland': 'Cumbria',
    
    
    # add more mappings as needed...
}

## Put the cambirdge together
## put together derbyshire 



# Apply replacements
summary['County'] = summary['County'].replace(replace_map)

# Now merge
merged_GCSE_poverty_2018_2024 = df_merged_2018_vs_2024.merge(summary, on='County', how='inner')

print(merged_GCSE_poverty_2018_2024.head())


# save to csv
merged_GCSE_poverty_2018_2024.to_csv('data/summary_by_county_2018_vs_2024.csv', index=False)


 ### A lot of the counties are not matching up but we can leave it for now 
 
 
 ## Questions: 
 
# 1. Has the percentage of children passing gone up and down in the counties?
# 2 Has the the difference from the national average gone up and down in the counties?
# Has the percentage of children passing gone down as the percentage of proverty has gone up


## Execute the code below to see the results 
print(merged_GCSE_poverty_2018_2024.columns)


# 1. Calculate change in percentage of children passing
merged_GCSE_poverty_2018_2024['Change_in_Pass_Percentage_2024_vs_2018'] = (
    merged_GCSE_poverty_2018_2024['PercentageResultsThresholdCounty_2024'] -
    merged_GCSE_poverty_2018_2024['PercentageResultsThresholdCounty_2018']
)

# 2. Calculate change in gap to national average
merged_GCSE_poverty_2018_2024['Change_from_National_Difference_of_passing_2024_vs_2024'] = (
    merged_GCSE_poverty_2018_2024['Difference_from_England_average_2024'] -
    merged_GCSE_poverty_2018_2024['Difference_from_England_average_2018']
)

# 3. Look at poverty and pass rate relationship
merged_GCSE_poverty_2018_2024['Change_in_Poverty_2024_2018'] = (
    merged_GCSE_poverty_2018_2024['Weighted_percentage_2024'] -
    merged_GCSE_poverty_2018_2024['Weighted_percentage_2018']
)


# Calculate direction labels
merged_GCSE_poverty_2018_2024['Pass_Percentage_Change_Direction'] = merged_GCSE_poverty_2018_2024['Change_in_Pass_Percentage_2024_vs_2018']\
    .apply(lambda x: 'UP' if x > 0 else ('DOWN' if x < 0 else 'NO CHANGE'))

merged_GCSE_poverty_2018_2024['National_Diff_Change_Direction'] = merged_GCSE_poverty_2018_2024['Change_from_National_Difference_of_passing_2024_vs_2024']\
    .apply(lambda x: 'UP' if x > 0 else ('DOWN' if x < 0 else 'NO CHANGE'))

merged_GCSE_poverty_2018_2024['Poverty_Change_Direction'] = merged_GCSE_poverty_2018_2024['Change_in_Poverty_2024_2018']\
    .apply(lambda x: 'UP' if x > 0 else ('DOWN' if x < 0 else 'NO CHANGE'))
    
## save to csv
merged_GCSE_poverty_2018_2024.to_csv('data/merged_GCSE_poverty_2018_vs_2024.csv', index=False)

# Create your final summary DataFrame
summary_stats = merged_GCSE_poverty_2018_2024[[
    'County',
    'Change_in_Pass_Percentage_2024_vs_2018', 'Pass_Percentage_Change_Direction',
    'Change_from_National_Difference_of_passing_2024_vs_2024', 'National_Diff_Change_Direction',
    'Change_in_Poverty_2024_2018', 'Poverty_Change_Direction'
]]

# Save to CSV
summary_stats.to_csv('data/summary_stats_2018_vs_2024.csv', index=False)



# If you want to check directly for your 3rd question:
# Cases where poverty increased but pass rate decreased


### 

import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for a clean plot
sns.set(style="whitegrid")

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=merged_GCSE_poverty_2018_2024,
    x='Weighted_percentage_2024',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    hue='National_Diff_Change_Direction',  # <- your column uses 'UP', 'DOWN', 'NO CHANGE'
    palette={
        'UP': 'green',
        'DOWN': 'red',
        'NO CHANGE': 'gray'
    }
)

plt.title('2024 Child Poverty vs Change in Pass Rate Relative to National Average')
plt.xlabel('Child Poverty Percentage (2024)')
plt.ylabel('Change from National Average (2024 vs 2018)')

plt.legend(title='Pass Rate Change vs National Avg')
plt.grid(True)
plt.tight_layout()
plt.show()
# Save the plot
plt.savefig('data/2024_Child_Poverty_vs_Change_in_Pass_Rate.png', dpi=300)


## Change in direcion and change of poverty in relation to inital poverty ## 2018

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=merged_GCSE_poverty_2018_2024,
    x='Change_in_Poverty_2024_2018',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    size='Total_children_2024',  # optional, gives you the sense of population
    hue='Weighted_percentage_2018',  # starting poverty
    palette='coolwarm',  # or try 'viridis'
    sizes=(20, 200),
    alpha=0.7
)

plt.title('Change in Poverty vs. Change in GCSE Pass Rate Gap\n(Color = Initial Poverty in 2018)')
plt.xlabel('Change in Child Poverty (2024 vs 2018)')
plt.ylabel('Change in GCSE Pass Rate Gap vs National (2024 vs 2018)')

plt.axhline(0, color='black', linestyle='--', linewidth=0.7)  # no change in pass rate
plt.axvline(0, color='black', linestyle='--', linewidth=0.7)  # no change in poverty

plt.grid(True)
plt.tight_layout()
plt.show()
# Save the plot
plt.savefig('data/Change_in_Poverty_vs_Change_in_Pass_Rate.png', dpi=300)


sns.lmplot(
    data=merged_GCSE_poverty_2018_2024,
    x='Change_in_Poverty_2024_2018',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    hue='Poverty_Change_Direction',  # or bin the starting poverty into high/low
    scatter_kws={'alpha':0.6},
    height=6,
    aspect=1.2
)
plt.axhline(0, color='black', linestyle='--', linewidth=0.7)
plt.axvline(0, color='black', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()
# Save the plot
plt.savefig('data/Change_in_Poverty_vs_Change_in_Pass_Rate_with_LM.png', dpi=300)


### partial correlation 

import pingouin as pg

# Compute partial correlation: change in pass rate vs change in poverty, controlling for initial poverty
partial_corr = pg.partial_corr(
    data=merged_GCSE_poverty_2018_2024,
    x='Change_in_Poverty_2024_2018',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    covar='Weighted_percentage_2018',
    method='pearson'
)

print(partial_corr)
