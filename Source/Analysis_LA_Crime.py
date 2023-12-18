# %% [markdown]
#   # <center> ANALYSIS LOS ANGELES CRIME FROM 2020 TO PRESENT <center>
# 
#   **Team Members:**
# 
#    **Full Name** | **ID Number** | **Github**
#   --- | --- | ---
#   Nguyễn Phương Nam | 21120504 | https://github.com/Mr-Phuong-Nam
#   Võ Bá Hoàng Nhất | 21120516 | https://github.com/NhatUS03
#   Nguyễn Gia Phúc | 21120529 | https://github.com/ngphucdotpy
# 
# 

# %% [markdown]
#   ---

# %% [markdown]
#   ### Import libraries

# %%
import pandas as pd
import numpy as np


# %%
pd.set_option('display.max_columns', 500)


# %% [markdown]
#   ---

# %% [markdown]
#   # 1. Data collection

# %% [markdown]
#  - What subject is your data about? What is the source of your data?
#      - Our data is about crime, **detailedly** this dataset reflects incidents of crime in the City of Los Angeles from 2020 to now.
#      - The source of dataset is [data.gov](http://data.gov) .It has all the crimes reported and recorded by Los Angeles Police Department (LAPD).
#  - Do authors of this data allow you to use like this? You can check the data license.
#      - Authors of this data allow everyone use like, which based on CC0: Public Domain (No copyright), so we can collect, modify and distribute this dataset.
#  - How did authors collect data?
#      - The provided data, transcribed from original crime reports typed on paper, may contain inaccuracies due to the manual transcription process. Additionally, to safeguard privacy, some location fields are marked as (0°, 0°), and address details are limited to the nearest hundred block.

# %% [markdown]
#   # 2. Exploring data

# %% [markdown]
#   ## 2.1. Load the data

# %%
crime_df = pd.read_csv('../Data/Crime_Data_from_2020_to_Present.csv')
crime_df.head()


# %% [markdown]
#   ## 2.2 General

# %% [markdown]
#   ### How many rows and how many columns

# %%
crime_df.shape


# %% [markdown]
#   ### What is the meaning of each row?
#   Each row reflects a crime incident that occurred at a specific time and location in Los Angeles from 2020 to the present.

# %% [markdown]
#   ### Are there duplicated rows?

# %%
is_duplicated = np.any(crime_df.duplicated())
is_duplicated


# %% [markdown]
#   ### The meaning of each column

# %% [markdown]
#   - ``` DR_NO ```: Unique identification number for each reported crime.
#   - ``` Date Rptd ```: The date when the crime was reported.
#   - ``` DATE OCC ```: The date when the crime occurred.
#   - ``` TIME OCC ```: The time when the crime occurred.
#   - ``` AREA ```: The Los Angeles Police Department (LAPD) has 21 Community Police Stations referred to as Geographic Areas within the department. These Geographic Areas are sequentially numbered from 1-21.
#   - ``` AREA NAME ```: The 21 Geographic Areas or Patrol Divisions are also given a name designation that references a landmark or the surrounding community that it is responsible for.
#   - ```Rpt Dist No``` : Code that represents a sub-area within a Geographic Area.
#   - ```Part 1-2```: The code that categories the crime.
#       - 1 for part I crimes: also known as "Serious Crimes". Divided into two main categories:
#           - Violent Crimes: Offenses involving force or threat of force. Examples include murder, rape, robbery, and aggravated assault.
#           - Property Crimes: Offenses involving the taking or destruction of property but not force or threat of force. Examples include burglary, larceny-theft, motor vehicle theft, and arson.
#       - 2 for part II crimes: also known as "Less Serious Crimes". Examples include simple assault, fraud, embezzlement, drug offenses, and vandalism.
#   - ```Crm Cd```: The crime code, representing the type of crime.
#   - ```Crm Cd Desc```: The description of the crime.
#   - ```Mocodes```: Modus Operandi (MO) codes, which describe the method or pattern of operation used by the offender
#   - ```Vict Age```: The age of the victim.
#   - ```Vict Sex```: The gender of the victim (F: Female, M: Male, X: Unknown)
#   - ```Vict Descent```: Descent Code:
#       - A - Other Asian
#       - B - Black
#       - C - Chinese
#       - D - Cambodian
#       - F - Filipino
#       - G - Guamanian
#       - H - Hispanic/Latin/Mexican
#       - I - American Indian/Alaskan Native
#       - J - Japanese
#       - K - Korean
#       - L - Laotian
#       - O - Other
#       - P - Pacific Islander
#       - S - Samoan
#       - U - Hawaiian
#       - V - Vietnamese
#       - W - White
#       - X - Unknown
#       - Z - Asian Indian
#   - ```Premis Cd```: The type of structure, vehicle, or location where the crime took place.
#   - ```Premis Desc```: Defines the Premise Code provided.
#   - ```Weapon Used Cd```: The weapon code, representing the type of weapon used in the crime
#   - ```Weapon Desc```: Defines the Weapon Used Code provided.
#   - ```Status```: The status of the reported crime.
#   - ```Status Desc```: Defines the Status Code provided.
#       - AO: Adult Other
#       - AA: Adult Arrest
#       - IC: Invest Cont
#       - JA: Juv Arrest
#       - JO: Juv Other
#       - CC: Unknown
#   - ```Crm Cd 1```: Additional crime code information
#   - ```Crm Cd 2```: Additional crime code information
#   - ```Crm Cd 3```: Additional crime code information
#   - ```Crm Cd 4```: Additional crime code information
#   - ```LOCATION```: The location where the crime took place.
#   - ```Cross Street```: The cross street where the crime took place.
#   - ```LAT```: The latitude of the location
#   - ```LON```: The longitude of the location

# %% [markdown]
#   ### General information about each column

# %%
crime_df.info()

# %% [markdown]
#   Some columns have the wrong data type:
#   - ```DR_Rptd```: object -> datetime
#   - ```DATE OCC```: object -> datetime
#   - ```TIME OCC```: int -> datetime
#   - ```Mocodes```: object -> list of mocodes

# %% [markdown]
# Crm Cd 2, 3, 4 have a lot of missing values

# %% [markdown]
#  ## 2.3 Exploring numerical and categorical columns

# %% [markdown]
#  Select the numerical and categorical columns.

# %%
num_cols = ['Vict Age', 'LAT', 'LON']
cat_cols = ['AREA', 'AREA NAME', 'Part 1-2', 'Crm Cd', 'Crm Cd Desc', 'Mocodes', 'Vict Sex', 'Vict Descent', 'Premis Cd', 'Premis Desc', \
            'Weapon Used Cd', 'Weapon Desc', 'Status', 'Status Desc', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street']


# %% [markdown]
#  ### Numerical columns

# %%
crime_df[num_cols].isnull().mean() * 100


# %% [markdown]
#  There is no missing value in these columns.

# %%
crime_df[num_cols].agg(['min', 'max'])


# %% [markdown]
#  The `LAT` and `LON` seem normal as well as they are coordinates.
# 
#  But the `Vict Age` is abnormal since there is existence of negative age (-3) and very old person (120).

# %% [markdown]
#  ### Categorical columns

# %%
crime_df[cat_cols].isnull().mean() * 100


# %% [markdown]
#  The overall missing value ratios are low except `Weapon Used Cd`, `Weapon Desc`, `Crm Cd 2`, `Crm Cd 3`, `Crm Cd 4` and `Cross Street`.

# %%
crime_df[cat_cols].nunique()


# %% [markdown]
#  `Mocodes` may contains the combinations of Mocode, then its unique values is high.
# 
#  The overall unique value of these columns is normal.

# %%
for col in cat_cols:
    print('-', col, ': ', end = '')
    print(crime_df[col].dropna().unique()[:5])


# %% [markdown]
#  Some unique values of these categorical columns are showed above.
# 
#  They are normal except the `Mocodes` is required to be split into list of Mocode.

# %% [markdown]
# # 3. Data cleaning

# %% [markdown]
# ### Drop Crime Cd 2, 3, 4 columns because they have a lot of missing values

# %%
crime_df = crime_df.drop(columns = ['Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4'])

# %% [markdown]
# ### Convert Date Rptd, DATE OCC, TIME OCC to datetime

# %% [markdown]
# - There is a redundant part in `DR_Rptd` and `DATE OCC` columns. That is the time part, which is always 12:00:00 AM. So we can drop it.

# %%
print(crime_df['Date Rptd'].str.split(' ').apply(lambda x: x[1] + ' ' + x[2]).unique())
print(crime_df['DATE OCC'].str.split(' ').apply(lambda x: x[1] + ' ' + x[2]).unique())

# %%
crime_df['Date Rptd'] = crime_df['Date Rptd'].str.split(' ').apply(lambda x: x[0])
crime_df['DATE OCC'] = crime_df['DATE OCC'].str.split(' ').apply(lambda x: x[0])

# %% [markdown]
# - The `TIME OCC` column is in integer format. First, we convert it to string format by adding zeros to the left of the number. Then, we convert it to datetime format.

# %%
crime_df['TIME OCC'] = crime_df['TIME OCC'].astype(str).str.zfill(4)

# %% [markdown]
# - Then we combine `DATE OCC` and `TIME OCC` to create a new column `Datetime OCC`. Finally, we convert Date Rptd and Datetime Occ to datetime format and drop the old columns.

# %%
crime_df['Datetime OCC'] = crime_df['DATE OCC'] + ' ' + crime_df['TIME OCC']
crime_df['Datetime OCC'] = pd.to_datetime(crime_df['Datetime OCC'], format = '%m/%d/%Y %H%M')
crime_df['Date Rptd'] = pd.to_datetime(crime_df['Date Rptd'], format = '%m/%d/%Y')

crime_df = crime_df.drop(columns = ['DATE OCC', 'TIME OCC'])
crime_df

# %% [markdown]
# # 4. Data visualization

# %% [markdown]
# # 5. Questions and answers

# %% [markdown]
# ### 5.1 Where is the location and what is the time happening of each type of crime?

# %% [markdown]
# First we need to know how many types of crime are there in this dataset.
# 

# %%
crime_df

# %% [markdown]
# There are 138 types of crime in this dataset. That's a lot. So we need to group them into some types of crime.
# 
# 
# 

# %%
crime_df['Crm Cd Desc'].unique()

# %% [markdown]
# # 6. Model to predict the time and location of the next crime

# %% [markdown]
# # 7. Conclusion

# %% [markdown]
# # 8. References


