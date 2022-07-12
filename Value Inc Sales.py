# -*- coding: utf-8 -*-
"""
Value Inc is a retail store that sells household items all over the world by bulk.
The Sales Manager has no sales reporting but he has a brief idea of current sales.
He also has no idea of the monthly cost, profit and top selling products. He wants a
dashboard on this and says the data is currently stored in an excel sheet.
"""
import pandas as pd

#Read CSV file and tell Python the separator is ; to properly recognize columns 
#are separate
df = pd.read_csv("transaction.csv", sep=';')

#Summary of data
df.info()

"""
Formulas
"""

#Cost per transaction formula = Cost * # of items purchased
df['Cost_Per_Transaction'] = df['CostPerItem'] * df['NumberOfItemsPurchased']

#Revenue per transaction = Price of item sold * # of items customer purchased
df['Revenue_Per_Transaction'] = df['SellingPricePerItem'] * df['NumberOfItemsPurchased']

#Profit per transaction = total revenue of transaction - cost of goods sold of transaction
df['Profit_Per_Transaction'] = df['Revenue_Per_Transaction'] - df['Cost_Per_Transaction']

#Markup = Gross profit per transaction / Cost [*100 if wanted in %]
df['Markup'] = df['Profit_Per_Transaction']/df['Cost_Per_Transaction'] * 100
#rounded to 2 decimal places
df['Markup'] = round(df['Markup'], 2)

#Profit Margin = profit per transaction / revenue per transaction [*100 if wanted in %]
df['Profit_Margin'] = df['Profit_Per_Transaction']/df['Revenue_Per_Transaction'] * 100
#round to 2 decimal places
df['Profit_Margin'] = round(df['Profit_Margin'], 2)

#Concatenate year month day into a DD-MM-YYYY format
day = df['Day'].astype(str)
year = df['Year'].astype(str)

day_month_year_format = day + '-' + df['Month'] + '-' + year
df['Date'] = day_month_year_format

#Viewing data using iloc, head, and tail
df.head(5)#quick basic view of first 5 rows
df.tail(10)#quick basic view of last 10 rows

df.iloc[0]#detailed view of first row 
df.iloc[:,17]#views all rows in 18th column which is profit margin 
df.iloc[:,[7,17]]#views all rows in 8th and 18th column which is item sold and profit margin, respectively

#Split client_keywords field into separate columns 
split_col = df['ClientKeywords'].str.split(',', expand=True)

df['Client_Age'] = split_col[0]
df['Client_Type'] = split_col[1]
df['Contract_Length'] = split_col[2]

#Clean up readability of new columns since hanging square bracket
df['Client_Age'] = df['Client_Age'].str.replace('[', '')
df['Contract_Length'] = df['Contract_Length'].str.replace(']', '')

#bringing in a new seasons dataset
df2 = pd.read_csv('value_inc_seasons.csv', sep = ';')

#merge new seasons dataset with transactions dataset
df = pd.merge(df, df2, on='Month')

#drop client keywords field since already split it
df = df.drop('ClientKeywords', axis=1)

#drop day year and month fields since already created Date column 
df = df.drop(['Day', 'Year', 'Month'], axis=1)

#export as CSV for internal consistency
df.to_csv('Value_Inc_Data_Cleaned.csv', index=False)
