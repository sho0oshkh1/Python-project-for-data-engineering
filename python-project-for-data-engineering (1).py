#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0221ENSkillsNetwork23455645-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 

# # Peer Review Assignment - Data Engineer - ETL
# 

# Estimated time needed: **20** minutes
# 

# ## Objectives
# 
# In this final part you will:
# 
# *   Run the ETL process
# *   Extract bank and market cap data from the JSON file `bank_market_cap.json`
# *   Transform the market cap currency using the exchange rate data
# *   Load the transformed data into a seperate CSV
# 

# For this lab, we are going to be using Python and several Python libraries. Some of these libraries might be installed in your lab environment or in SN Labs. Others may need to be installed by you. The cells below will install these libraries when executed.
# 

# In[ ]:


#!mamba install pandas==1.3.3 -y
#!mamba install requests==2.26.0 -y


# ## Imports
# 
# Import any additional libraries you may need here.
# 

# In[1]:


import glob
import pandas as pd
from datetime import datetime


# As the exchange rate fluctuates, we will download the same dataset to make marking simpler. This will be in the same format as the dataset you used in the last section
# 

# In[2]:


get_ipython().system('wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/bank_market_cap_1.json')
get_ipython().system('wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/bank_market_cap_2.json')
get_ipython().system('wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Final%20Assignment/exchange_rates.csv')


# ## Extract
# 

# ### JSON Extract Function
# 
# This function will extract JSON files.
# 

# In[3]:


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe


# ## Extract Function
# 
# Define the extract function that finds JSON file `bank_market_cap_1.json` and calls the function created above to extract data from them. Store the data in a `pandas` dataframe. Use the following list for the columns.
# 

# In[4]:


columns=['Name','Market Cap (US$ Billion)']


# In[8]:


def extract():
    # Write your code here
    fname = "bank_market_cap_1.json"
    df = extract_from_json(fname)
    df2 = df[columns]
    return df2


# <b>Question 1</b> Load the file <code>exchange_rates.csv</code> as a dataframe and find the exchange rate for British pounds with the symbol <code>GBP</code>, store it in the variable  <code>exchange_rate</code>, you will be asked for the number. Hint: set the parameter  <code>index_col</code> to 0.
# 

# In[9]:


# Write your code here
df_exr = pd.read_csv("exchange_rates.csv", index_col=0)
exchange_rate = df_exr.loc["GBP", "Rates"]
print(df_exr.head())
print()
print("exchange_rate = ", exchange_rate)


# ## Transform
# 
# Using <code>exchange_rate</code> and the `exchange_rates.csv` file find the exchange rate of USD to GBP. Write a transform function that
# 
# 1.  Changes the `Market Cap (US$ Billion)` column from USD to GBP
# 2.  Rounds the Market Cap (US$ Billion)\` column to 3 decimal places
# 3.  Rename `Market Cap (US$ Billion)` to `Market Cap (GBP$ Billion)`
# 

# In[11]:


def transform(dataFrame, ex_rate):
    # Write your code here
    usd2gbp = dataFrame.loc["USD", "Rates"] / ex_rate
    df_usd = extract()
    df_usd.loc[:, "Market Cap (GBP$ Billion)"] = round(df_usd.iloc[:, 1] / usd2gbp, 3)
    df_gbp = df_usd.drop("Market Cap (US$ Billion)", axis=1)
    return df_gbp, usd2gbp
    


# ## Load
# 
# Create a function that takes a dataframe and load it to a csv named `bank_market_cap_gbp.csv`. Make sure to set `index` to `False`.
# 

# In[ ]:

targetfile="bank_matket_cap_gbp.csv"
def load(targetfile,datatoload):
    # Write your code here
    datatoload.to_csv(targetfile, index=False)
    


# ## Logging Function
# 

# Write the logging function <code>log</code> to log your data:
# 

# In[13]:


def log(msg):
    # Write your code here
    with open("log.txt", "a") as f:
        dt = datetime.today().strftime("%Y-%m-%d %H:%M-%S")
        f.write(str(dt) + "   " + str(msg) + "\n")


# ## Running the ETL Process
# 

# Log the process accordingly using the following <code>"ETL Job Started"</code> and <code>"Extract phase Started"</code>
# 

# In[14]:


# Write your code here
log("ETL Job Started")
log("Extract phase Started")


# ### Extract
# 

# <code>Question 2</code> Use the function <code>extract</code>, and print the first 5 rows, take a screen shot:
# 

# In[15]:


# Call the function here
df0 = extract()
# Print the rows here
df0.head()


# Log the data as <code>"Extract phase Ended"</code>
# 

# In[16]:


# Write your code here
log("Extract phase Ended")


# ### Transform
# 

# Log the following  <code>"Transform phase Started"</code>
# 

# In[17]:


# Write your code here
log("Transform phase Started")


# <code>Question 3</code> Use the function <code>transform</code> and print the first 5 rows of the output, take a screen shot:
# 

# In[18]:


# Call the function here
df_gbp, usd2gbp = transform(df_exr, exchange_rate)    
# Print the first 5 rows here
print(df_gbp.head())


# Log your data <code>"Transform phase Ended"</code>
# 

# In[19]:


# Write your code here
log("Transform phase Ended")


# ### Load
# 

# Log the following `"Load phase Started"`.
# 

# In[20]:


# Write your code here
log("Load phase Started")


# Call the load function
# 

# In[23]:


# Write your code here
load(df_gbp, "bank_market_cap_1.json") 


# Log the following `"Load phase Ended"`.
# 

# In[24]:


# Write your code here
log("Load phase Ended")

