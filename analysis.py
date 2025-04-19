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


# Mapping of local authorities to counties (only for England)
local_authority_to_county = {
    'County Durham': 'County Durham',
    'Darlington': 'County Durham',
    'Hartlepool': 'County Durham',
    'Middlesbrough': 'North Yorkshire',
    'Northumberland': 'Northumberland',
    'Redcar and Cleveland': 'North Yorkshire',
    'Stockton-on-Tees': 'North Yorkshire',
    'Gateshead': 'Tyne and Wear',
    'Newcastle upon Tyne': 'Tyne and Wear',
    'North Tyneside': 'Tyne and Wear',
    'South Tyneside': 'Tyne and Wear',
    'Sunderland': 'Tyne and Wear',
    'Blackburn with Darwen': 'Lancashire',
    'Blackpool': 'Lancashire',
    'Cheshire East': 'Cheshire',
    'Cheshire West and Chester': 'Cheshire',
    'Cumberland': 'Cumbria',
    'Halton': 'Cheshire',
    'Warrington': 'Cheshire',
    'Westmorland and Furness': 'Cumbria',
    'Bolton': 'Greater Manchester',
    'Bury': 'Greater Manchester',
    'Manchester': 'Greater Manchester',
    'Oldham': 'Greater Manchester',
    'Rochdale': 'Greater Manchester',
    'Salford': 'Greater Manchester',
    'Stockport': 'Greater Manchester',
    'Tameside': 'Greater Manchester',
    'Trafford': 'Greater Manchester',
    'Wigan': 'Greater Manchester',
    'Burnley': 'Lancashire',
    'Chorley': 'Lancashire',
    'Fylde': 'Lancashire',
    'Hyndburn': 'Lancashire',
    'Lancaster': 'Lancashire',
    'Pendle': 'Lancashire',
    'Preston': 'Lancashire',
    'Ribble Valley': 'Lancashire',
    'Rossendale': 'Lancashire',
    'South Ribble': 'Lancashire',
    'West Lancashire': 'Lancashire',
    'Wyre': 'Lancashire',
    'Knowsley': 'Merseyside',
    'Liverpool': 'Merseyside',
    'Sefton': 'Merseyside',
    'St. Helens': 'Merseyside',
    'Wirral': 'Merseyside',
    'East Riding of Yorkshire': 'East Riding of Yorkshire',
    'Kingston upon Hull, City of': 'East Riding of Yorkshire',
    'North East Lincolnshire': 'Lincolnshire',
    'North Lincolnshire': 'Lincolnshire',
    'North Yorkshire': 'North Yorkshire',
    'York': 'North Yorkshire',
    'Barnsley': 'South Yorkshire',
    'Doncaster': 'South Yorkshire',
    'Rotherham': 'South Yorkshire',
    'Sheffield': 'South Yorkshire',
    'Bradford': 'West Yorkshire',
    'Calderdale': 'West Yorkshire',
    'Kirklees': 'West Yorkshire',
    'Leeds': 'West Yorkshire',
    'Wakefield': 'West Yorkshire',
    'Derby': 'Derbyshire',
    'Leicester': 'Leicestershire',
    'North Northamptonshire': 'Northamptonshire',
    'Nottingham': 'Nottinghamshire',
    'Rutland': 'Rutland',
    'West Northamptonshire': 'Northamptonshire',
    'Amber Valley': 'Derbyshire',
    'Bolsover': 'Derbyshire',
    'Chesterfield': 'Derbyshire',
    'Derbyshire Dales': 'Derbyshire',
    'Erewash': 'Derbyshire',
    'High Peak': 'Derbyshire',
    'North East Derbyshire': 'Derbyshire',
    'South Derbyshire': 'Derbyshire',
    'Blaby': 'Leicestershire',
    'Charnwood': 'Leicestershire',
    'Harborough': 'Leicestershire',
    'Hinckley and Bosworth': 'Leicestershire',
    'Melton': 'Leicestershire',
    'North West Leicestershire': 'Leicestershire',
    'Oadby and Wigston': 'Leicestershire',
    'Boston': 'Lincolnshire',
    'East Lindsey': 'Lincolnshire',
    'Lincoln': 'Lincolnshire',
    'North Kesteven': 'Lincolnshire',
    'South Holland': 'Lincolnshire',
    'South Kesteven': 'Lincolnshire',
    'West Lindsey': 'Lincolnshire',
    'Ashfield': 'Nottinghamshire',
    'Bassetlaw': 'Nottinghamshire',
    'Broxtowe': 'Nottinghamshire',
    'Gedling': 'Nottinghamshire',
    'Mansfield': 'Nottinghamshire',
    'Newark and Sherwood': 'Nottinghamshire',
    'Rushcliffe': 'Nottinghamshire',
    'Herefordshire, County of': 'Herefordshire',
    'Shropshire': 'Shropshire',
    'Stoke-on-Trent': 'Staffordshire',
    'Telford and Wrekin': 'Shropshire',
    'Cannock Chase': 'Staffordshire',
    'East Staffordshire': 'Staffordshire',
    'Lichfield': 'Staffordshire',
    'Newcastle-under-Lyme': 'Staffordshire',
    'South Staffordshire': 'Staffordshire',
    'Stafford': 'Staffordshire',
    'Staffordshire Moorlands': 'Staffordshire',
    'Tamworth': 'Staffordshire',
    'North Warwickshire': 'Warwickshire',
    'Nuneaton and Bedworth': 'Warwickshire',
    'Rugby': 'Warwickshire',
    'Stratford-on-Avon': 'Warwickshire',
    'Warwick': 'Warwickshire',
    'Birmingham': 'West Midlands',
    'Coventry': 'West Midlands',
    'Dudley': 'West Midlands',
    'Sandwell': 'West Midlands',
    'Solihull': 'West Midlands',
    'Walsall': 'West Midlands',
    'Wolverhampton': 'West Midlands',
    'Bromsgrove': 'Worcestershire',
    'Malvern Hills': 'Worcestershire',
    'Redditch': 'Worcestershire',
    'Worcester': 'Worcestershire',
    'Wychavon': 'Worcestershire',
    'Wyre Forest': 'Worcestershire',
    'Bedford': 'Bedfordshire',
    'Central Bedfordshire': 'Bedfordshire',
    'Luton': 'Bedfordshire',
    'Peterborough': 'Cambridgeshire',
    'Southend-on-Sea': 'Essex',
    'Thurrock': 'Essex',
}

# Apply replacements
summary['County'] = summary['County'].replace(local_authority_to_county)


# Function to calculate weighted average for poverty percentage
def weighted_avg(group, value_col, weight_col):
    total_weight = group[weight_col].sum()
    if total_weight == 0:
        return 0
    return (group[value_col] * group[weight_col]).sum() / total_weight

summary = df_children.groupby('County').apply(
    lambda g: pd.Series({
        'Total_children_2018': g['Number_ of_children_2018'].sum(),
        'Total_children_2024': g['Number_ of_children_2024'].sum(),
        'Weighted_percentage_2018': weighted_avg(g, 'Percentage_of_children_2018', 'Number_ of_children_2018'),
        'Weighted_percentage_2024': weighted_avg(g, 'Percentage_of_children_2024', 'Number_ of_children_2024'),
    })
).reset_index()

print(summary)



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
from adjustText import adjust_text

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=merged_GCSE_poverty_2018_2024,
    x='Change_in_Poverty_2024_2018',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    size='Total_children_2024',
    hue='Weighted_percentage_2018',
    palette='coolwarm',
    sizes=(20, 200),
    alpha=0.7
)

# Create label objects
texts = []
for i, row in merged_GCSE_poverty_2018_2024.iterrows():
    texts.append(
        plt.text(
            row['Change_in_Poverty_2024_2018'],
            row['Change_from_National_Difference_of_passing_2024_vs_2024'],
            row['County'],
            fontsize=8
        )
    )

# Adjust labels with a minimum distance from points to avoid overlap with bubbles
adjust_text(
    texts,
    arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5),
    force_text=0.2,        # Allow text to move further from points
    force_points=0.4,      # Allow points to move slightly to make space
    only_move={'points': 'y', 'text': 'xy'},  # Move the labels freely in both directions
    lim=100,               # Increase iterations to improve placement
    add_textprops={'verticalalignment': 'bottom', 'horizontalalignment': 'left'},  # Adjust label alignment
    expand_points=(1.5, 1.5),  # Expand the area in which points can move, giving them more space
)

plt.title('Change in Poverty vs. Change in Pass Rate Gap\n(Labels Adjusted for Clarity)')
plt.xlabel('Change in Child Poverty (2024 vs 2018)')
plt.ylabel('Change in Pass Rate Gap to National Average (2024 vs 2018)')
plt.axhline(0, color='black', linestyle='--', linewidth=0.7)
plt.axvline(0, color='black', linestyle='--', linewidth=0.7)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.savefig('data/2024_Child_Poverty_vs_Change_in_Pass_Rate.png', dpi=300)


## Change in direcion and change of poverty in relation to inital poverty ## 2018

from adjustText import adjust_text

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    data=merged_GCSE_poverty_2018_2024,
    x='Change_in_Poverty_2024_2018',
    y='Change_from_National_Difference_of_passing_2024_vs_2024',
    size='Total_children_2024',
    hue='Weighted_percentage_2018',
    palette='coolwarm',
    sizes=(20, 200),
    alpha=0.7
)

# Create label objects for each county
texts = []
for i, row in merged_GCSE_poverty_2018_2024.iterrows():
    texts.append(
        plt.text(
            row['Change_in_Poverty_2024_2018'],
            row['Change_from_National_Difference_of_passing_2024_vs_2024'],
            row['County'],
            fontsize=8
        )
    )

# Adjust labels with a minimum distance from points to avoid overlap with bubbles
adjust_text(
    texts,
    arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5),
    force_text=0.2,        # Allow text to move further from points
    force_points=0.4,      # Allow points to move slightly to make space
    only_move={'points': 'y', 'text': 'xy'},  # Move the labels freely in both directions
    lim=100,               # Increase iterations to improve placement
    add_textprops={'verticalalignment': 'bottom', 'horizontalalignment': 'left'},  # Adjust label alignment
    expand_points=(1.5, 1.5),  # Expand the area in which points can move, giving them more space
)

plt.title('Change in Poverty vs. Change in Pass Rate Gap\n(Labels Adjusted for Clarity)')
plt.xlabel('Change in Child Poverty (2024 vs 2018)')
plt.ylabel('Change in Pass Rate Gap vs National (2024 vs 2018)')

plt.axhline(0, color='black', linestyle='--', linewidth=0.7)  # reference line for pass rate
plt.axvline(0, color='black', linestyle='--', linewidth=0.7)  # reference line for poverty

plt.grid(True)
plt.tight_layout()
plt.show()

# Save the plot
plt.savefig('data/Change_in_Poverty_vs_Change_in_Pass_Rate.png', dpi=300)

