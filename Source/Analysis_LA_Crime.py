# %% [markdown]
# # <center> ANALYSIS LOS ANGELES CRIME FROM 2020 TO PRESENT <center>
# 
# **Team Members:**
# 
#  **Full Name** | **ID Number** | **Github**
# --- | --- | ---
# Nguyễn Phương Nam | 21120504 | https://github.com/Mr-Phuong-Nam
# 
# 

# %% [markdown]
# ---

# %% [markdown]
# ### Import libraries

# %%
import pandas as pd
import numpy as np

# %%
pd.set_option('display.max_columns', 500)

# %% [markdown]
# ---

# %% [markdown]
# # 1. Data collection

# %% [markdown]
# # 2. Exploring data

# %% [markdown]
# ## 2.1. Load the data

# %%
crime_df = pd.read_csv('../Data/Crime_Data_from_2020_to_Present.csv')
crime_df.head()

# %% [markdown]
# ## 2.2 General 

# %% [markdown]
# ### How many rows and how many columns

# %%
crime_df.shape

# %% [markdown]
# ### What is the meaning of each row?
# Each row reflects a crime incident that occurred at a specific time and location in Los Angeles from 2020 to the present.

# %% [markdown]
# ### Are there duplicated rows?

# %%
is_duplicated = np.any(crime_df.duplicated())
is_duplicated

# %% [markdown]
# ### The meaning of each column

# %% [markdown]
# - ``` DR_NO ```: Unique identification number for each reported crime.
# - ``` Date Rptd ```: The date when the crime was reported.
# - ``` DATE OCC ```: The date when the crime occurred.
# - ``` TIME OCC ```: The time when the crime occurred.
# - ``` AREA ```: The Los Angeles Police Department (LAPD) has 21 Community Police Stations referred to as Geographic Areas within the department. These Geographic Areas are sequentially numbered from 1-21.
# - ``` AREA NAME ```: The 21 Geographic Areas or Patrol Divisions are also given a name designation that references a landmark or the surrounding community that it is responsible for.
# - ```Rpt Dist No``` : Code that represents a sub-area within a Geographic Area.
# - ```Part 1-2```: The code that categories the crime. 
#     - 1 for part I crimes: also known as "Serious Crimes". Divided into two main categories:
#         - Violent Crimes: Offenses involving force or threat of force. Examples include murder, rape, robbery, and aggravated assault.
#         - Property Crimes: Offenses involving the taking or destruction of property but not force or threat of force. Examples include burglary, larceny-theft, motor vehicle theft, and arson.
#     - 2 for part II crimes: also known as "Less Serious Crimes". Examples include simple assault, fraud, embezzlement, drug offenses, and vandalism. 
# - ```Crm Cd```: The crime code, representing the type of crime.
# - ```Crm Cd Desc```: The description of the crime.
# - ```Mocodes```: Modus Operandi (MO) codes, which describe the method or pattern of operation used by the offender
# - ```Vict Age```: The age of the victim.
# - ```Vict Sex```: The gender of the victim (F: Female, M: Male, X: Unknown)
# - ```Vict Descent```: Descent Code: 
#     - A - Other Asian 
#     - B - Black 
#     - C - Chinese 
#     - D - Cambodian 
#     - F - Filipino 
#     - G - Guamanian 
#     - H - Hispanic/Latin/Mexican 
#     - I - American Indian/Alaskan Native 
#     - J - Japanese 
#     - K - Korean 
#     - L - Laotian 
#     - O - Other 
#     - P - Pacific Islander 
#     - S - Samoan 
#     - U - Hawaiian 
#     - V - Vietnamese 
#     - W - White 
#     - X - Unknown 
#     - Z - Asian Indian
# - ```Premis Cd```: The type of structure, vehicle, or location where the crime took place.
# - ```Premis Desc```: Defines the Premise Code provided.
# - ```Weapon Used Cd```: The weapon code, representing the type of weapon used in the crime
# - ```Weapon Desc```: Defines the Weapon Used Code provided.
# - ```Status```: The status of the reported crime.
# - ```Status Desc```: Defines the Status Code provided.
#     - AO: Adult Other
#     - AA: Adult Arrest
#     - IC: Invest Cont
#     - JA: Juv Arrest
#     - JO: Juv Other
#     - CC: Unknown 
# - ```Crm Cd 1```: Additional crime code information
# - ```Crm Cd 2```: Additional crime code information
# - ```Crm Cd 3```: Additional crime code information
# - ```Crm Cd 4```: Additional crime code information
# - ```LOCATION```: The location where the crime took place.
# - ```Cross Street```: The cross street where the crime took place.
# - ```LAT```: The latitude of the location
# - ```LON```: The longitude of the location

# %% [markdown]
# ### The current data type of each column

# %%
crime_df.dtypes 

# %% [markdown]
# Some columns have the wrong data type:
# - ```DATE OCC```: object -> datetime
# - ```TIME OCC```: int -> datetime
# - ```Mocodes```: object -> list of mocodes


