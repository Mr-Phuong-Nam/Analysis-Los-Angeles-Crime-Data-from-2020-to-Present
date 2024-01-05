# %% [markdown]
#  # <center> ANALYSIS LOS ANGELES CRIME FROM 2020 TO PRESENT <center>
# 
#  **Team Members:**
# 
#  **Full Name** | **ID Number** | **Github**
#  --- | --- | ---
#  Nguyễn Phương Nam | 21120504 | https://github.com/Mr-Phuong-Nam
#  Võ Bá Hoàng Nhất | 21120516 | https://github.com/NhatUS03
#  Nguyễn Gia Phúc | 21120529 | https://github.com/ngphucdotpy
# 
# 

# %% [markdown]
#  ---

# %% [markdown]
#  ### Import libraries

# %%
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

import os 
import sys

# %%
pd.set_option('display.max_columns', 500)

# %% [markdown]
#  ---

# %% [markdown]
#  # 1. Data collection

# %% [markdown]
#  - What subject is your data about? What is the source of your data?
#      - Our data is about crime, **detailedly** this dataset reflects incidents of crime in the City of Los Angeles from 2020 to now.
#      - The source of dataset is https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data
#      - It has all the crimes reported and recorded by Los Angeles Police Department (LAPD).
#  - Do authors of this data allow you to use like this?
#      - Authors of this data allow everyone use like, which based on CC0: Public Domain (No copyright), so we can collect, modify and distribute this dataset.
#  - How did we collect this data?
#      - We use the API of Socrata to collect this data. The API is https://data.lacity.org/resource/2nrs-mtv8.json. The instruction of using this API is https://dev.socrata.com/foundry/data.lacity.org/2nrs-mtv8
#      - We use the Python library `requests` to get the data from the API. And save it to a file named `crime_data_2020_present.csv`.

# %% [markdown]
#  # 2. Exploring data

# %% [markdown]
#  ## 2.1. Load the data

# %%
crime_df = pd.read_csv('../Data/Crime_Data_from_2020_to_Present.csv')
crime_df.head()

# %% [markdown]
# Normallizing the column names

# %%
#Lowercase all columns and replace spaces and "-" with underscores
crime_df.columns = crime_df.columns.str.lower()
crime_df.columns = crime_df.columns.str.replace(' ', '_')
crime_df.columns= crime_df.columns.str.replace('-', '_')

# %% [markdown]
#  ## 2.2 General

# %% [markdown]
#  ### How many rows and how many columns

# %%
crime_df.shape

# %% [markdown]
#  ### What is the meaning of each row?
#  Each row reflects a crime incident that occurred at a specific time and location in Los Angeles from 2020 to the present.

# %% [markdown]
#  ### Are there duplicated rows?

# %%
is_duplicated = np.any(crime_df.duplicated())
is_duplicated

# %% [markdown]
#  ### The meaning of each column

# %% [markdown]
#  - ``` dr_no ```: Unique identification number for each reported crime.
#  - ``` date_rptd ```: The date when the crime was reported.
#  - ``` date_occ ```: The date when the crime occurred.
#  - ``` time_occ ```: The time when the crime occurred.
#  - ``` area ```: The Los Angeles Police Department (LAPD) has 21 Community Police Stations referred to as Geographic Areas within the department. These Geographic Areas are sequentially numbered from 1-21.
#  - ``` area_name ```: The 21 Geographic Areas or Patrol Divisions are also given a name designation that references a landmark or the surrounding community that it is responsible for. For example 77th Street Division is located at the intersection of South Broadway and 77th Street, serving neighborhoods in South Los Angeles.
#  - ```rpt_dist_no``` : A four-digit code that represents a sub-area within a Geographic Area. All crime records reference the "RD" that it occurred in for statistical comparisons. Find LAPD Reporting Districts on the LA City GeoHub at http://geohub.lacity.org/datasets/c4f83909b81d4786aa8ba8a74
#  - ```part_1_2```: The code that categories the crime.
#      - 1 for part I crimes: also known as "Serious Crimes". Divided into two main categories:
#          - Violent Crimes: Offenses involving force or threat of force. Examples include murder, rape, robbery, and aggravated assault.
#          - Property Crimes: Offenses involving the taking or destruction of property but not force or threat of force. Examples include burglary, larceny-theft, motor vehicle theft, and arson.
#      - 2 for part II crimes: also known as "Less Serious Crimes". Examples include simple assault, fraud, embezzlement, drug offenses, and vandalism.
#  - ```crm_cd```: The crime code, representing the type of crime.
#  - ```crm_cd_desc```: The description of the crime.
#  - ```mocodes```: Modus Operandi (MO) codes, which describe the method or pattern of operation used by the offender
#  - ```vict_age```: The age of the victim.
#  - ```vict_sex```: The gender of the victim (F: Female, M: Male, X: Unknown)
#  - ```vict_descent```: Descent Code:
#      - A - Other Asian
#      - B - Black
#      - C - Chinese
#      - D - Cambodian
#      - F - Filipino
#      - G - Guamanian
#      - H - Hispanic/Latin/Mexican
#      - I - American Indian/Alaskan Native
#      - J - Japanese
#      - K - Korean
#      - L - Laotian
#      - O - Other
#      - P - Pacific Islander
#      - S - Samoan
#      - U - Hawaiian
#      - V - Vietnamese
#      - W - White
#      - X - Unknown
#      - Z - Asian Indian
#  - ```premis_cd```: The type of structure, vehicle, or location where the crime took place.
#  - ```premis_desc```: Defines the Premise Code provided.
#  - ```weapon_used_cd```: The weapon code, representing the type of weapon used in the crime
#  - ```weapon_desc```: Defines the Weapon Used Code provided.
#  - ```status```: The status of the reported crime.
#  - ```status_desc```: Defines the Status Code provided.
#      - AO: Adult Other
#      - AA: Adult Arrest
#      - IC: Invest Cont
#      - JA: Juv Arrest
#      - JO: Juv Other
#      - CC: Unknown
#  - ```crm_cd_1```: Additional crime code information
#  - ```crm_cd_2```: Additional crime code information
#  - ```crm_cd_3```: Additional crime code information
#  - ```crm_cd_4```: Additional crime code information
#  - ```location```: The location where the crime took place.
#  - ```cross_street```: The cross street where the crime took place.
#  - ```lat```: The latitude of the location
#  - ```lon```: The longitude of the location

# %% [markdown]
#  ### General information about each column

# %%
crime_df.info()

# %% [markdown]
#  Some columns have the wrong data type:
#  - ```date_rptd```: object -> datetime
#  - ```date_occ```: object -> datetime
#  - ```time_occ```: int -> datetime
#  - ```mocodes```: object -> list of mocodes

# %% [markdown]
#  crm_cd 2, 3, 4 have a lot of missing values

# %% [markdown]
# ## 2.3 Exploring numerical and categorical columns

# %% [markdown]
# Select the numerical and categorical columns.

# %%
num_cols = ['vict_age', 'lat', 'lon']

cat_cols = ['area', 'area_name', 'part_1_2', 'crm_cd', 'crm_cd_desc', 'mocodes', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc', 'weapon_used_cd', 'weapon_desc', 'status', 'status_desc', 'crm_cd_1', 'crm_cd_2', 'crm_cd_3', 'crm_cd_4', 'cross_street']

# %% [markdown]
# ### Numerical columns

# %%
crime_df[num_cols].isnull().mean() * 100

# %% [markdown]
# These columns have no missing values.

# %%
crime_df[num_cols].agg(['min', 'max'])

# %% [markdown]
#   Both the `lat` and `lon` appear normal as expected for coordinates. However, the `vict_age` value is unusual. It includes negative ages (-3) and exceptionally high values (120), suggesting inconsistencies or potential errors.

# %% [markdown]
# ### Categorical columns

# %%
crime_df[cat_cols].isnull().mean() * 100

# %% [markdown]
#  The overall missing value ratios are low except `weapon_used_cd`, `weapon_desc`, `crm_cd_2`, `crm_cd_3`, `crm_cd_4` and `cross_street`.

# %%
crime_df[cat_cols].nunique()

# %% [markdown]
#   The `mocodes` column may contain combinations of Mocodes, leading to a high number of unique values. However, the overall number of unique values in the other columns is within a normal range.

# %%
crime_df['mocodes'].str.split().explode().nunique()

# %% [markdown]
# `mocodes`' unique values after splitting are shown above.

# %%
for col in cat_cols:
    print('-', col, ': ', end = '')
    print(crime_df[col].dropna().unique()[:5])

# %% [markdown]
#   Some unique values of these categorical columns are shown above. All appear normal except for the `mocodes` column, which requires splitting into a list of individual Mocodes during the data pre-processing phase.

# %% [markdown]
#    # 3. Data cleaning

# %% [markdown]
#    ### Drop columns

# %% [markdown]
#  Columns `crm_cd_2`, `crm_cd_3`, `crm_cd_4`, `cross_street` are dropped because they have too many missing values.

# %%
crime_df = crime_df.drop(columns=['crm_cd_2', 'crm_cd_3', 'crm_cd_4', 'cross_street'])

# %% [markdown]
#  Drop `dr_no`, `area`, `premis_cd`, `status`, `weapon_used_cd` because they are not useful.

# %%
crime_df = crime_df.drop(['dr_no', 'area', 'premis_cd', 'status', 'weapon_used_cd'], axis=1)

# %% [markdown]
#  ### Convert `date_rptd,` `date_occ`, `time_occ` to datetime

# %% [markdown]
#  `date_rptd` and `date_occ` are floating timestamp data. They are something like this: 2020-01-08T00:00:00.000.

# %% [markdown]
#  We only need the date in the front, the time is always 00:00:00.000 so we can drop it.

# %%
def convert_to_datetime(col):
    """
    Converts a column with format like '2020-01-01T00:00:00.000' to datetime
    
    Parameters
    ----------
    col : string series

    Returns
    -------
    date series
    """

    return pd.to_datetime(col.str.split('T').str[0])

crime_df['date_occ'] = convert_to_datetime(crime_df['date_occ'])
crime_df['date_rptd'] = convert_to_datetime(crime_df['date_rptd'])


# %% [markdown]
#    The `time_occ` column is in integer format. First, we convert it to string format by adding zeros to the left of the number. Then, we convert it to datetime format.

# %%
crime_df['time_occ'] = crime_df['time_occ'].astype(str).str.zfill(4)

# %% [markdown]
#  Then we combine `date_occ` and `time_occ` to create a new column `datetime_occ`. 

# %%
crime_df['datetime_occ'] = pd.to_datetime(crime_df['date_occ'].astype(str) + ' ' + crime_df['time_occ'].astype(str), format='%Y-%m-%d %H%M', errors='coerce')

crime_df[['date_occ', 'time_occ', 'datetime_occ']].head()


# %% [markdown]
#  Now we can drop `date_occ`, `time_occ`.

# %%
crime_df = crime_df.drop(['date_occ', 'time_occ'], axis=1)


# %% [markdown]
#    ### Handle missing values

# %% [markdown]
#  `vict_age` has a lot of values that less than 1. By checking the 'Crm Cd Desc' column, we can see that these rows do not have any relation with babies. So we can consider them as missing values.

# %%
crime_df.loc[crime_df['vict_age'] <= 0, 'crm_cd_desc'].unique()[:10]

# %%
crime_df.loc[crime_df['vict_age'] <= 0, 'vict_age'] = np.nan

# %% [markdown]
# `vict_sex` has some different values that are not F, M. We can consider them as missing values. Then we can fill them with X (Unknown).

# %%
crime_df['vict_sex'].unique()

# %%
crime_df.loc[(crime_df['vict_sex'] != 'F') & (crime_df['vict_sex'] != 'M'), 'vict_sex'] = 'X'

# %% [markdown]
#  Similarly for `vict_descent` and `status_desc` columns.

# %%
crime_df['vict_descent'].unique()

# %%
crime_df.loc[crime_df['vict_descent'] == '-', 'vict_descent'] = 'X'
crime_df.loc[crime_df['vict_descent'].isna(), 'vict_descent'] = 'X'

# %%
crime_df['status_desc'].unique()

# %% [markdown]
#  ### Convert numerical mocodes to categorical mocodes

# %% [markdown]
#  Load the description for each mocode.

# %%
meanings = json.load(open('../Data/meanings.json', 'r'))
mocodes_dict = meanings['mocodes']
list(mocodes_dict.items())[:5]


# %% [markdown]
#  Create `mocodes_desc` to store the description of each mocode.

# %%

def convert_mocodes(MC_string):
    """
    Convert the string of numerical mocodes to a list of their meanings
    
    Parameters:
    -----------
    MC_string: str
        The string of numerical mocodes

    Returns:
    --------
    MC_list: list
        The list of mocodes' meanings

    """

    if pd.notna(MC_string):
        MC_list = MC_string.split(' ')
        # Ignore the codes that are not in the dictionary
        MC_list = [mocodes_dict[MC] for MC in MC_list if MC in mocodes_dict]
        return MC_list
    
    return np.nan

crime_df['mocodes_desc'] = crime_df['mocodes'].agg(convert_mocodes)


# %%
crime_df[['mocodes', 'mocodes_desc']].head()


# %% [markdown]
# ### Add crime type column

# %% [markdown]
# As we observed, there are 138 different crime codes. They are too many to analyze. So we will group them into 10 types of crime: 
# 1. Assault and Battery
# 2. Theft and Robbery
# 3. Property Damage and Vandalism
# 4. Sexual Offenses
# 5. Threats and Harassment
# 6. Fraud and Forgery
# 7. Traffic Offenses
# 8. Juvenile Offenses
# 9. Weapons Offenses
# 10. Other Miscellaneous Crimes

# %%
crime_types = json.load(open('../Data/crime_types.json', 'r'))
crime_types['Assault and Battery']

# %%
# Reverse the dictionary
crime_types_dict = {}
for key, value in crime_types.items():
    for v in value:
        crime_types_dict[v] = key

crime_df['crm_type'] = crime_df['crm_cd_desc'].map(crime_types_dict)
crime_df['crm_type'].unique()

# %% [markdown]
# ### Save the cleaned data

# %%
crime_df.shape

# %%
crime_df.head()

# %%
crime_df.to_csv('../Data/crime_data_cleaned.csv', index = False)


# %% [markdown]
#    # 4. Data visualization

# %%
# from Dashboard import app

# app.run_server(debug=True)

# %% [markdown]
#    # 5. Questions and answers

# %% [markdown]
#    ### 5.1 Where is the location and what is the time happening of each type of crime?

# %% [markdown]
#    First we need to know how many types of crime are there in this dataset.
# 

# %% [markdown]
#    There are 138 types of crime in this dataset. That's a lot. So we need to group them into some types of crime.
# 
# 
# 

# %% [markdown]
#    # 6. Model to predict the time and location of the next crime

# %% [markdown]
#    # 7. Conclusion

# %% [markdown]
#    # 8. References


