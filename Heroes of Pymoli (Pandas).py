#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

Data = "purchase_data.csv"


# In[2]:


purchase_df = pd.read_csv(Data)
purchase_df.head()


# In[3]:


#Username is easier for me to understand
purchase_df = purchase_df.rename(columns={"SN":"Username"})


# In[4]:


#Player Count
total_players = len(purchase_df['Username'].unique())
total_players_table = pd.DataFrame({"Total Players": [total_players]})

#Hide index
total_players_df = total_players_table.style.hide_index()
total_players_df


# In[5]:


#Purchasing Analysis (Total)
total_items = len(purchase_df['Item ID'].unique())
avg_price = purchase_df['Price'].mean()
total_purchases = purchase_df['Purchase ID'].count()
total_purchases_sum = purchase_df['Price'].sum()


# In[6]:


#Create a summary table to organize earlier data
purchasing_analysis_table = pd.DataFrame([{
    "Total Unique Items": total_items, 
    "Average Price": avg_price,
    "Number of Purchases": total_purchases,
    "Total Revenue": total_purchases_sum,
}], columns=["Total Unique Items", "Average Price", "Number of Purchases", "Total Revenue"])
purchasing_analysis_table

#Formating
purchasing_analysis_table["Average Price"] = purchasing_analysis_table["Average Price"].map("${0:.2f}".format)
purchasing_analysis_table["Total Revenue"] = purchasing_analysis_table["Total Revenue"].map("${0:,.2f}".format)
purchasing_analysis_table
Purchasing_Analysis_df = purchasing_analysis_table.style.hide_index()
Purchasing_Analysis_df 


# In[7]:


#Gender Demographics

#Creating 3 dataframes sorted by genders
male_df = purchase_df.loc[purchase_df["Gender"] == "Male", :]
female_df = purchase_df.loc[purchase_df["Gender"] == "Female", :]
other_df = purchase_df.loc[purchase_df["Gender"] == "Other / Non-Disclosed", :] 


# In[8]:


#Count Totals
total_male = len(male_df['Username'].unique())
total_female = len(female_df['Username'].unique())
total_other = len(other_df['Username'].unique())

#Percentages
male_percentage = total_male / total_players
female_percentage = total_female / total_players
other_percentage = total_other / total_players

#Formating
Male_Percentage = "{:.3%}".format(male_percentage)
Female_Percentage = "{:.3%}".format(female_percentage)
Other_Percentage = "{:.3%}".format(other_percentage)


# In[9]:


#Summary table for above data
gender_demographics_table = pd.DataFrame(
    [{"Gender": "Female", "Total Count": total_female, 
     "Percentage of Players": Female_Percentage},   
    {"Gender": "Male", "Total Count": total_male, 
    "Percentage of Players": Male_Percentage}, 
    {"Gender": "Other / Non-Disclosed", "Total Count": total_other, 
     "Percentage of Players": Other_Percentage
    }], columns=["Gender", "Total Count", "Percentage of Players"])

Gender_Demographics_df = gender_demographics_table.set_index('Gender')
Gender_Demographics_df


# In[10]:


#Purchasing Analysis (Gender)


# In[11]:


#Counting total purchases by genders
total_male_purchases = male_df['Purchase ID'].count()
total_female_purchases = female_df['Purchase ID'].count()
total_other_purchases = other_df['Purchase ID'].count()

#Average of gender prices
avg_male_price = male_df['Price'].mean()
avg_female_price = female_df['Price'].mean()
avg_other_price = other_df['Price'].mean()

#Sum of total male purchases
total_male_purchases_sum = male_df['Price'].sum()
total_female_purchases_sum = female_df['Price'].sum()
total_other_purchases_sum = other_df['Price'].sum()


# In[12]:


#Only use columns we need
Gender_2_df = purchase_df[["Username", "Gender", "Price"]]

#Group by gender
Gender_df = Gender_2_df.groupby(["Gender"])
Gender_comp_df = Gender_df.mean()
sum_gender_df = Gender_df.sum()

#Only use columns we need
Gender_count = purchase_df[["Gender" , "Purchase ID"]]

#Group by gender and count
gen_count = Gender_count.groupby(['Gender']).count() 


# In[13]:


# Merging columns

merge_df = pd.merge(sum_gender_df, Gender_comp_df, on="Gender", suffixes=(" (Total)", " (Avg)"))
merge_df_2 = pd.merge(merge_df, gen_count, on="Gender")


#Rename Purchase ID column
merge_df_2.rename(columns = {'Purchase ID':'Purchase Count'}, inplace = True)

#Create Avg Purchase Total Per Person column by dividing between dataframes
Avg_Purchase_Total_Per_Person = merge_df_2["Price (Total)"]/Gender_Demographics_df["Total Count"]

#Add new column
merge_df_2["Avg Purchase Total Per Person"] = Avg_Purchase_Total_Per_Person
merge_df_2

#Formating
merge_df_2["Price (Total)"] = merge_df_2["Price (Total)"].map("${0:.2f}".format)
merge_df_2["Price (Avg)"] = merge_df_2["Price (Avg)"].map("${0:.2f}".format)
merge_df_2["Avg Purchase Total Per Person"] = merge_df_2["Avg Purchase Total Per Person"].map("${0:,.2f}".format)
merge_df_2


# In[14]:


#Age Demographics


# In[15]:


#Lookup min and max to determin range
purchase_df['Age'].min()


# In[16]:


purchase_df['Age'].max()


# In[17]:


#Create a copy dataframe to find total count of users using bins
purchase_df_copy = purchase_df.copy()


# In[18]:


#Make bins
age_bins = [0, 9, 14, 19, 24, 29, 34, 39, 46]
labels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]


purchase_df_copy["Age Groups"] = pd.cut(purchase_df_copy["Age"], bins=age_bins, labels=labels)
age_group = purchase_df_copy.groupby("Age Groups")
total_count_age = age_group["Username"].nunique()

# Create Summary DataFrame
age_demographics_table = pd.DataFrame({
   "Total Count": total_count_age
})


# In[19]:


#Create bins for column added to dataframe
bins = [0, 9, 14, 19, 24, 29, 34, 39, 99]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

purchase_df["Age Bins"] = pd.cut(purchase_df["Age"], bins, labels=group_names, include_lowest=True)


# In[20]:


#Group by the bins made
Age_df = purchase_df.groupby(["Age Bins"])
Age_df_price = Age_df[["Price"]]


# In[21]:


#Find totals and averages
Age_Average_Purchase_Price = Age_df_price.mean()
Age_total = Age_df_price.sum()
Age_Purchase_Count = Age_df_price.count()


# In[22]:


#Merge columns and add suffixes
age_merge_df = pd.merge(Age_Average_Purchase_Price, Age_total, on="Age Bins", suffixes=(" (Avg)"," (Total)"))
age_merge_df_2 = pd.merge(age_merge_df, Age_Purchase_Count, on="Age Bins")
age_merge_df_2.rename(columns = {'Price':'Purchase Count'}, inplace = True)

#Create 'Average Purchase Total per Person' column by dividing from 'age_demographics_table'
age_merge_df_2['Average Purchase Total per Person'] = age_merge_df_2['Price (Total)'] / age_demographics_table['Total Count']
age_merge_df_2

#Formating
age_merge_df_2["Price (Avg)"] = age_merge_df_2["Price (Avg)"].astype(float).map("${:,.2f}".format)
age_merge_df_2["Price (Total)"] = age_merge_df_2["Price (Total)"].astype(float).map("${:,.2f}".format)
age_merge_df_2["Average Purchase Total per Person"] = age_merge_df_2["Average Purchase Total per Person"].astype(float).map("${:,.2f}".format)
age_merge_df_2


# In[23]:


#Top Spenders


# In[24]:


#Create new dataframe grouping by usernames
username_df = purchase_df.groupby(purchase_df['Username'])

#Find totals and averages
Username_purchase_count = username_df['Price'].count()
Username_average_purchase = username_df['Price'].mean()
Username_sum_purchase = username_df['Price'].sum()

# Create Summary DataFrame
Username_table = pd.DataFrame({ 
    "Purchase Count": Username_purchase_count,
    "Average Purchase Price": Username_average_purchase,
    "Total Purchase Value": Username_sum_purchase
})

#Identify top 5 spenders
Username_sorted = Username_table.sort_values(by=['Total Purchase Value'], ascending=False).head()

#Formating
Username_sorted["Average Purchase Price"] = Username_sorted["Average Purchase Price"].astype(float).map("${:,.2f}".format)
Username_sorted["Total Purchase Value"] = Username_sorted["Total Purchase Value"].astype(float).map("${:,.2f}".format)
Username_sorted


# In[25]:


#Most Popular Items


# In[26]:


#Create new dataframe for columns needed
item_df = purchase_df[["Item ID", "Item Name", "Price"]]
popular_item_df = item_df.groupby(["Item ID","Item Name"])

#Find totals and averages
item_purchase_count = popular_item_df['Price'].count()
item_sum_purchase = popular_item_df['Price'].sum()

#Create a variable and divide "Total Purchase Value" by "Purchase Count"
item_price = item_sum_purchase / item_purchase_count

#Summary table
most_popular_items = pd.DataFrame({
   "Purchase Count": item_purchase_count, 
   "Item Price": item_price,
   "Total Purchase Value": item_sum_purchase
})

#Formating
most_popular_item_df = most_popular_items.sort_values(by=['Purchase Count'], ascending=False).head()
most_popular_item_df

most_popular_item_df["Item Price"] = most_popular_item_df["Item Price"].astype(float).map("${:,.2f}".format)
most_popular_item_df["Total Purchase Value"] = most_popular_item_df["Total Purchase Value"].astype(float).map("${:,.2f}".format)
most_popular_item_df


# In[27]:


#Most Profitable Items


# In[28]:


#Sort by 
most_profitable_df = most_popular_items.sort_values(by=['Total Purchase Value'], ascending=False).head()

#Formating
most_profitable_df["Item Price"] = most_profitable_df["Item Price"].astype(float).map("${:,.2f}".format)
most_profitable_df["Total Purchase Value"] = most_profitable_df["Total Purchase Value"].astype(float).map("${:,.2f}".format)
most_profitable_df


# In[29]:


#Write up 


# In[30]:


# 1. The target demographic for marketing purposes should be males (84%) between the ages of 15 and 29 (77%).
# 2. On average all of the top 5 most popular items are also the most profitable.  The top five items' average price is $4.52 and the average price total of an item is 3.05. We can likley increase pricing on popular items.
# 3. While a smaller proportion of the demographics, females($4.47) and other/non-disclosed ($4.56) tend to spend more on purchases than males($4.07).


# In[ ]:





# In[ ]:




