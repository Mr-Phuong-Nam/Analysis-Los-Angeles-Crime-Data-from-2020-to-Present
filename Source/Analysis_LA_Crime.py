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
# # 4. Data visualization

# %%
from Dashboard import app
app.run_server(debug=True)

# %% [markdown]
# From the dashboard, we can have some insights about the crime in Los Angeles from 2020 to present.

# %% [markdown]
# ## Take a look at the overall crime situation

# %% [markdown]
# <img src="../Data/Image/total_crime.png" style="height: 600px; width:1000px;"/>

# %% [markdown]
# Total number of crimes in Los Angeles from 2020 to october 2023 is 829778 with 2022 has the highest number of crimes.   
# 
# Central, 77th Street, and Pacific are the top 3 areas with the highest number of crimes.

# %% [markdown]
# <img src="../Data/Image/crime_number.png" style="height: 500px; width:1000px;"/>

# %% [markdown]
# There is no clear trend in the number of crimes over months. The crimes may be affected by many factors such as political, economic, social, etc. These factors are changing over time, so the number of crimes is not stable.
# 
# Most of the crimes are under investigation which means that most of the crimes are not solved.
# 
# Serious crimes are more than less serious crimes.

# %% [markdown]
# <img src="../Data/Image/crime_types.png" style="height: 400px; width:600px;"/>

# %% [markdown]
# In 10 types of crime, theft and robbery are the most common crimes, followed by assault and battery.

# %% [markdown]
# <img src="../Data/Image/theft_and_robbery.png" style="height: 500px; width:1000px;"/>

# %% [markdown]
# Theft and robbery crimes occur frequently in various areas. Perpetrators often employ strong arms and guns to threaten their victims, and these incidents typically take place in streets, parking lots, and even victims' homes.

# %% [markdown]
# <img src="../Data/Image/Assault_and_Battery.png" style="height: 500px; width:1000px;"/>

# %% [markdown]
# Assault and battery crimes occur frequently in various areas. Perpetrators often employ strong arms to attack their victims, and these incidents typically take place in single-family dwellings, multi-family dwellings, and streets. 

# %% [markdown]
# <img src="../Data/Image/victim.png" style="height: 400px; width:1200px;"/>

# %% [markdown]
# Most of the victim ages are in the range of 20-40. This is the age range when people are most active in society, so they are more likely to be victims of crime.
# 
# The porpotion between male and felame victims is almost equal.
# 
# Hispanic/Latin/Mexican is the most common descent of victims.

# %% [markdown]
# # 5. Questions and answers

# %% [markdown]
# ## 5.1 The time when criminals are most likely to be active ?

# %% [markdown]
# ### 5.1.1 Meanings:

# %% [markdown]
# - Help citizens in Los Angeles can know day in weeks and timestamp in day most likely to be active to limit going out.
# - This can help local law enforcement and security managers know when criminals are most active and take measures to tighten security at that time.

# %% [markdown]
# ### 5.1.2 How to answer questions:

# %% [markdown]
# - The team will create a 2-dimensional matrix to represent the number of crimes per hour of the day and each day of the week. 
# - Each column represents the number of cases for each hour of the year (select every 2 hours). And the rows represent the days of the week. Then use heatmap to visualize the results

# %%
def time_occurrence(df):

    """
    Function to create a matrix of the number of occurrences for each time interval and weekday
    Args:
        df: dataframe with the crime data
    Returns:
        time_matrix: matrix of the number of occurrences for each time interval and weekday
    """
    # Define time intervals and weekdays ,with time intervals of 2 hours
    bins = np.arange(0, 26, 2)
    weekdays = np.arange(7)
    
    # Create a matrix to store the number of occurrences for each time interval and weekday
    time_matrix = np.zeros((len(bins) - 1, len(weekdays)), dtype=int)

    # Iterate over time intervals
    for i in range(len(bins) - 1):
        # Create a boolean mask for the current time interval
        mask_hour = (df['datetime_occ'].dt.hour >= bins[i]) & (df['datetime_occ'].dt.hour < bins[i + 1])
        
        # Iterate over weekdays
        for j in range(len(weekdays)):
            # Create a boolean mask for the current weekday
            mask_weekday = df['datetime_occ'].dt.dayofweek == weekdays[j]

            # Count occurrences for the current time interval and weekday
            time_matrix[i, j] = np.sum(mask_hour & mask_weekday)

    return time_matrix


# %%
#Call the function to create the matrix
time_matrix=time_occurrence(crime_df)

#Initialize the columns and index of the matrix
columns=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
indexs=['12am-2am','2am-4am','4am-6am','6am-8am','8am-10am','10am-12pm','12pm-2pm','2pm-4pm','4pm-6pm','6pm-8pm','8pm-10pm','10pm-12am']

#Create a dataframe with the matrix
time_df=pd.DataFrame(time_matrix,columns=columns,index=indexs)

# %%
#Plot the heatmap to visualize the time of occurrence

#Set the size of the figure
plt.figure(figsize=(8,6))

#Plot the heatmap
sns.heatmap(time_df,cmap='YlGnBu')

#Set the title, x and y labels
plt.title('Time of Occurrence')
plt.xticks(rotation=45)
plt.xlabel('Day of Week')
plt.ylabel('Time')
plt.show()

# %% [markdown]
# ### 5.1.3 Answer

# %% [markdown]
# - Comment:
#     - According to the time of day, time from 2am to 4am has the smallest number of crimes .Meanwhile, time 12am to 2pm and 4pm to 8pm are the time when the number of criminals is most active.
#     - Regarding weekdays, we see that Friday has a lot of criminal activity.
# 
# - Conclusion: 
#     - Regarding early morning time, it can be explained simply by saying that at that time, the number of people going out is very small, so criminals do not have many opportunities to perform actions.
#     - You can see, in the period from 4 to 8 pm, the number of crimes is extremely high, the explanation is because this is the time of the weekend just starting, so there are a lot of outside activities, crime. Access to more people. At the same time, everyone leaves the house more, creating more conditions for criminals to rob.
# 

# %% [markdown]
# ## 5.2 Do criminal groups operate depending on the season (cold or hot weather) ?

# %% [markdown]
# ### 5.2.1 Meanings

# %% [markdown]
# - Help people improvise to reduce the possibility of facing dangerous situations according to the seasons of the year.
# - If the results of this question differ between groups, this is an interesting result for everyone to understand better about *criminal psychology*.
# 

# %% [markdown]
# ### 5.2.2 How to answer questions

# %% [markdown]
# - Firstly, let's find out what types of crimes happen the most.

# %%
#Count the number of each type of crime
crime_counts = crime_df['crm_type'].value_counts()

#Sort the number of each type of crime
crime_counts = crime_counts.sort_values(ascending=False)

#Set style
sns.set(style="whitegrid")

#Set size of figure and plot bar chart
plt.figure(figsize=(10, 6))
bars = plt.barh(crime_counts.index, crime_counts, color='salmon')

#Set value of each ba

#Set title and label
plt.title('Distribution of Crime Types')
plt.xlabel('Number of Crimes')

#Save figure
plt.show()

# %% [markdown]
# - Through this we can see that 3 types *Theft and Robbery*, *Assauld and Battery* and *Property Damage and Vandalism* are at the top in terms of the number of crimes that occur.
# - And these 3 crime groups can be groups that directly affect residents.
# - Therefore, the main analysis is Weaknesses for these three groups seem more useful to people in general and the city of Los Angeles in particular.

# %%
#Create a new dataframe to store important types of crime needed to this question
effect_president_col=['Theft and Robbery','Assault and Battery','Property Damage and Vandalism']
effect_president_crime_df=crime_df[crime_df['crm_type'].isin(effect_president_col)]

# %% [markdown]
# - Secondly, we need to see what our data looks like for each year, is there any missing or oulier in a certain month?

# %%
#Load image of the viaualization of the crime each month ,which is saved from the dashboard
import imageio

def plot_image_from_png(file_path):
    # Read image from file_path
    image = imageio.imread(file_path)

    # Plot the image
    plt.imshow(image)
    plt.axis('off')  # clear x- and y-axes
    plt.show()

# Đường dẫn đến file PNG của bạn
file_path = '../Data/NumberOfCrimesEachMonth.png'
# Gọi hàm để plot ảnh
plot_image_from_png(file_path)


# %% [markdown]
# - We can see that the year 2023 is missing November and December data. Maybe the agencies have not yet completed the report and added it to the dataset. 
# - So we can delete the 2023 data so that the assessments will be accurate than.

# %%
#Just 2022 under 
effect_president_crime_df=effect_president_crime_df[effect_president_crime_df['datetime_occ'].dt.year<=2022]

# %%
#Change datetime_occ to month
def change_date_to_month(date):
    return date.month
effect_president_crime_df['datetime_occ']=effect_president_crime_df['datetime_occ'].apply(change_date_to_month)

# %%
#Create a new dataframe to store the number of each type of crime each month
temp_df=effect_president_crime_df.groupby(['datetime_occ','crm_type']).size().to_frame('count').reset_index()

#Create a new dataframe to store the average number of each type 
average_df=temp_df.groupby(['crm_type']).mean().reset_index().drop(['datetime_occ'],axis=1)

# %%
#create standard deviation dataframe by take count in each month of each type of 
#crime minus average of that type of crime and then divide by average of that type of crime
standard_deviation_df=temp_df.merge(average_df,on='crm_type')
standard_deviation_df.columns=['datetime_occ','crm_type','count','average']
standard_deviation_df['standard_deviation']=standard_deviation_df['count']-standard_deviation_df['average']

#Divide standard deviation by average and then multiply by 100 to get the percentage
standard_deviation_df['standard_deviation']=round((standard_deviation_df['standard_deviation']/standard_deviation_df['average'])*100,1)
standard_deviation_df=standard_deviation_df.drop(['count','average'],axis=1)


# %% [markdown]
# - According to online sources, we can know that the cold season months in Los Angeles start from November to March (next month) and the hot season from May to October. We can draw more straight lines representing these two seasons by month to make it easier to visualize.
# 

# %%
import matplotlib.pyplot as plt
import pandas as pd

# Pivot the DataFrame to have each type_crime as a separate column
pivot_df = standard_deviation_df.pivot(index='datetime_occ', columns='crm_type', values='standard_deviation')

# Create a grouped bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each type_crime as a separate set of bars
pivot_df.plot(kind='bar', stacked=False, ax=ax)

#Plot hot and cold season
#value of x and y for hot and cold season is x-axis and y-axis of the plot not is the value of month
cold_season_1_x=[10,11.5]
cold_season_2_x=[-0.5,2]
cold_season_y=[10,10]
hot_season_1=[4,9]
hot_season_y=[-10,-10]
plt.plot(cold_season_1_x,cold_season_y,color='blue')
plt.plot(cold_season_2_x,cold_season_y,color='blue')
plt.plot(hot_season_1,hot_season_y,color='red')


# Add labels and title for each line
plt.text( 6, -10+0.5, 'Hot Season', color='red')
plt.text( 0, 10+0.5, 'Cold Season', color='blue')



# Add labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Deviation from average (%)')
ax.set_title('Seasonal structure of crime types')
# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')
# Show the legend
plt.legend(title='Type of Crime',loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Show the plot
plt.tight_layout()
plt.show()


# %% [markdown]
# - Comment:
#     - Overall, crime groups saw a decrease in incidents from February to April.
#     - As for the *Assault and Battery* and *Property Damage and Vasndalism* groups, criminals prefer to operate from May to October.This is also a hot time of year in Los Angeles.
#     - The *Theft and Robbery* group prefers to operate from October to January of the next year.This is also a cold time of year in Los Angeles.
# - Conclusion:
#     - The fact that crime groups *Assault and Battery* and *Property Damage and Vasndalism* are high in the hot season can be explained by the fact that this is the summer vacation where many community activities take place, so criminals who commit crimes and crimes have many opportunities to approach criminals. more target audience.
#     - In the cold season, more types of robberies occur because the cold season can have very limited passersby on the streets, so criminals have many opportunities to commit theft without being detected.
# 
# 

# %% [markdown]
# ### 5.1 Where is the location and what is the time happening of each type of crime?

# %% [markdown]
# First we need to know how many types of crime are there in this dataset.
# 

# %% [markdown]
# There are 138 types of crime in this dataset. That's a lot. So we need to group them into some types of crime.
# 
# 
# 

# %% [markdown]
# # 6. Model to predict the time and location of the next crime.

# %% [markdown]
# # 7. Conclusion

# %% [markdown]
# # 8. References

