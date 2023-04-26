# %% [markdown]
# # RFM Segmentation with python (The Data analytics approach to gain customer insights.)

# %% [markdown]
# ## Import required libraries 

# %%
# importing required packages
import pandas as pd
import datetime as dt
from utils.config import config

# %% [markdown]
# ## Download or import transaction data and customer data

# %%

transact_data_file = config.get('INPUT','transaction_data',
                                 fallback='./data/input/customer_transaction_data.csv')

customer_data_file = config.get('INPUT','customer_data',
                                 fallback='./data/input/customer_data.csv')

df_customer = pd.read_csv(customer_data_file, on_bad_lines='skip')
df_transactions = pd.read_csv(transact_data_file, parse_dates=['transactionDate'], on_bad_lines='skip')

# %%
df_customer.info()
df_customer.describe()

# %%
df_transactions.info()
df_transactions.describe()

# %% [markdown]
# ## Data Preparation

# %%
df_customer[df_customer.duplicated()].any()

# %%
df_transactions[df_transactions.duplicated()].any()

# %% [markdown]
# ## Data Cleaning

# %%
#Data Cleaning for customers 

#Dropping Duplicates
df_customer.drop_duplicates(inplace=True)
generations = lambda age: 'Gen Z' if age <= 24 else 'Millennials' if age <= 40 else 'Gen X' if age <= 55 else 'Baby Boomers' if age <= 75 else 'Silent Generation'
df_customer['customerGeneration'] = df_customer['customerAge'].apply(generations)
state = lambda x: x.split(",")[-1].split()[0] if len(x.split(",")[-1].split()) == 2 else None
df_customer['customerState'] = df_customer['customerLocation'].apply(state)

#Data cleaning for transactions 
df_transactions.drop_duplicates(inplace=True)
df_transactions = df_transactions[df_transactions['customerID'].isin(df_customer['customerID'])]
df_transactions['amount'] = df_transactions['amount'].apply(abs)


# %%
#Checking if duplicates have been dropped
df_transactions[df_transactions.duplicated()].any()

# %%
#Checking for the number of unique Customers
df_transactions['customerID'].nunique()

# %%
# Checking for the total number of transaction records
df_transactions.shape

# %%
# Checking for the max and min InvoiceData inorder to calculate number of months of data available
print('Min:{}; max:{}'.format(min(df_transactions.transactionDate),max(df_transactions.transactionDate)))

# %% [markdown]
# # Cohort Analysis
# 
# Descriptive analytics tool used to group customers into mutually exclusive cohorts measured over time. Helps understand high level trends better by providing insight on metrics across products ans Customer life cycle.

# %% [markdown]
# ## Assign Acquisition Month Cohort to each Customer
# Assumption: Considert first transactionDate as acquisition date

# %%
# Define a function that will parse the date, it truncates given date obect to the first day of the month
def get_month(x): return dt.datetime(x.year, x.month, 1) 

def get_quarter_start(x):
    quarter_start_month = ((x.month - 1) // 3) * 3 + 1
    return dt.datetime(x.year, quarter_start_month, 1)

def get_cohort_start_date(x):
    cohort = config.get('GROUPING','cohort',
                                 fallback='MONTHLY')
    x = get_month(x) if cohort == 'MONTHLY' else get_quarter_start(x) if cohort == 'QUARTERLY' else x 
    return x 

# Apply get_month method to transactionDate and create acquisitionDate Column
df_transactions['acquisitionDate'] = df_transactions['transactionDate'].apply(get_cohort_start_date) 

# Create groupby Obj with customerID & use acquisitionDate column for further Manipulation
grouping = df_transactions.groupby('customerID')['acquisitionDate'] 

# Finally Transform with min function to assign the smallest acquisitionDate Value to each Customer in the DataSet
df_transactions['cohort'] = grouping.transform('min')

# %%
#Extract integer values from the data
def get_date_int(data,column):
    year=data[column].dt.year
    month=data[column].dt.month
    day=data[column].dt.day
    return year, month, day

# %%
# Assign Time Offset Value
invoice_year, invoice_month, _=get_date_int(df_transactions,'acquisitionDate')
cohort_year, cohort_month,_=get_date_int(df_transactions,'cohort')
year_diff= invoice_year-cohort_year
month_diff=invoice_month-cohort_month
#+1 for first month to be marked as one instead of 0 for better interpretetation
df_transactions['CohortIndex']= (year_diff*12) + (month_diff+1)
#check if the new column has been added. CohortIndex
df_transactions.head()

# %%
grouping = df_transactions.groupby(['cohort', 'CohortIndex'])

cohort_data = grouping['customerID'].apply(pd.Series.nunique)

cohort_data = cohort_data.reset_index()

cohort_counts = cohort_data.pivot(index='cohort',
                                 columns='CohortIndex',
                                 values='customerID')
print(cohort_counts)

# %%
cohort_sizes = cohort_counts.iloc[:,0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
retention.index=retention.index.date
retention.round(3)*100

# %%
import plotly.express as px

values = retention.fillna(0).applymap(lambda x: round(x*100)).values

fig = px.imshow(values,
                title='Retention Rates',
                x=list(retention.columns),
                y=list(retention.index),
                color_continuous_scale='ylgn',
                text_auto=True,
                height=400,
                width=800
                )

fig.update_layout(xaxis_title='Number of months', yaxis_title='Cohort',
                  coloraxis_colorbar=dict(title='% Activity'),
                  height=500, width=800)

fig.show()



# %% [markdown]
# # RFM Segmentation 
# 
# Recency (R) : Days Since Last Customer Transaction
# Frequency (F): Number of transacations in the last 12 months
# Monetary Value (M) : Total Spend in the last 12 months
# 
# # RFM Data Preperation
# 
#  Pandas built-in function #qcut will be used to calculate percentiles
#  
# To implement RFM Segmentation, we need to further process the data set in by the following steps:
# 
# Recency : For each customer ID, calculate the days since the last transaction. Create a hypothetical date maximum Date +1 to make it seem as though we are working on the most recent data substract the max Date of transaction(Most recent date of transation) of the customer. However, usually the data used is Real time data and using the present date would be ideal. 
# Frequency: Count the number of invoices per customer to derive the frequency and 
# Monetary Data: Sum the amount of money a customer transacted and divide it by Frequency, to get the amount per transaction on average, that is the Monetary data.

# %%
# create hypothetical snapshot_day as if anlysisng the most recent data
snapshot=max(df_transactions.transactionDate)+dt.timedelta(days=1)

# %%
datamart=df_transactions.groupby(['customerID']).agg({
    'transactionDate':lambda x:(snapshot-x.max()).days,
    'transactionReference':'count',
    'amount':'sum'
})

# %%
# Rename columns for easy interpretation
datamart.rename(columns={'transactionDate':'Recency',
                         'transactionReference': 'Frequency',
                         'amount': 'MonetaryValue'},inplace=True

)

# %%
#View of The RFM table
datamart.tail()

# %%
# Create Lables for Each RFM Metric:Create generator of values for labels with range function
r_labels=list(range(5,0,-1))
m_labels=range(1,6)
f_labels=range(1,5)

# %%
#Create quartile Values using qcut function
r_quartiles=pd.qcut(datamart['Recency'],5,labels=r_labels)
m_quartiles=pd.qcut(datamart['MonetaryValue'],5,labels=m_labels)
f_quartiles=pd.qcut(datamart['Frequency'],4,labels=f_labels)

# %%
#Assign R,F,M quartile values to customers
datamart=datamart.assign(R=r_quartiles.values)
datamart=datamart.assign(F=f_quartiles.values,M=m_quartiles.values)

# %%
#snealpeak of the added column-R
datamart.head()

# %%
# Sneakpeak of the new datamart
datamart.head()

# %%
# deriving RFM-Segment column
def join_rfm(x) : return str(x['R'])+str(x['F'])+str(x['M'])
datamart['RFM_Segment']=datamart.apply(join_rfm,axis=1)
# Deriving RFM Score column
datamart['RFM_Score']=datamart[['R','F','M']].sum(axis=1)

# %%
# snakpeak of  datamart 
datamart.head()

# %%
datamart.groupby('RFM_Segment').size().sort_values(ascending=False)[:10]

# %%
# Summary metrics per RFM Score
datamart.groupby('RFM_Score').agg({
  'Recency':'mean',
  'MonetaryValue' :'mean',
  'Frequency':['mean','count']
}).round(1)

# %% [markdown]
# ## Grouping Customers into Named Segments
# Now that we have competed the RFM segmentation, users can be groups into named categories for marketing and profiling purpsoses.
# 1. MVC (Most Valuable customer): RFM_Score >=12
# 2. Loyal Customers: RFM_Score between 9 and 11
# 3. Potentially Loyal: RFM_Score between 7 and 9
# 4. Need Attention : RFM Score between 5 and 6
# 5. Churned Folk : RFM_Score < 5
# 

# %%
def segment_me(datamart):
    if datamart['RFM_Score']>=12 :
        return 'MVC'
    if(datamart['RFM_Score']>=9) and datamart['RFM_Score']<11:
        return 'Loyal '
    if(datamart['RFM_Score']>=7) and datamart['RFM_Score']<9:
        return 'Potentially Loyal'
    elif(datamart['RFM_Score']>=4) and datamart['RFM_Score']<6:
        return 'Churned Folk'
    else:
        return  'Need Attention'

# %%
datamart['General_Segment']=datamart.apply(segment_me,axis=1)    
datamart.groupby('General_Segment').agg({
  'Recency':'mean',
  'MonetaryValue' :'mean',
  'Frequency':['mean','count']
    
    }).round(1)

# %%
datamart.head()

# %%
datamart.describe()

# %% [markdown]
# ## Display as chart for high-level segment

# %%
import plotly.express as px

# count the number of occurrences of each General_Segment value
segment_counts = datamart['General_Segment'].value_counts()

fig = px.treemap(
    title= "RFM Customer Segmentation",
    names=[f"{x}<br>{y}" for x, y in zip(segment_counts.index.to_list(), segment_counts.to_list())],
    parents=["Customer Segments"]*segment_counts.size,
    values=segment_counts.to_list(),
    labels=segment_counts.to_list()
)
fig.show()

# %% [markdown]
# ## Further Analysis using customer demographic information

# %%
df_customer_datamart = pd.merge(df_customer, datamart, on='customerID', how='inner')
df_customer_datamart.head()

# %% [markdown]
# ## Show drill-down data or sub-segments
# 
# Feel free to add more entries to list variable `sub_segment_columns=['customerEducation', 'customerIndustry', 'customerGeneration']`

# %%
import plotly.express as px
import pandas as pd

segment_groups = df_customer_datamart.groupby('General_Segment')
for segment, segment_data in segment_groups:
    sub_segment_columns=['customerEducation', 'customerIndustry', 'customerGeneration']
    group_data = segment_data.groupby(sub_segment_columns).size().reset_index(name='count')
    group_data["all"] = segment # in order to have a single root node
    fig = px.treemap(group_data,path=sub_segment_columns, values='count', title=segment)
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()
    
for segment, segment_data in segment_groups:
    sub_segment_columns=['customerState']
    group_data = segment_data.groupby(sub_segment_columns).size().reset_index(name='count')
    group_data["all"] = segment # in order to have a single root node
    fig = px.treemap(group_data,path=sub_segment_columns, values='count', title=segment)
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    fig.show()

# %% [markdown]
# ## Save data for further evaluation and action.

# %%
import os


transaction_data_file = config.get('OUTPUT','transaction_data',
                                 fallback='./data/output/customer_transaction_data.csv')

customer_data_file = config.get('OUTPUT','customer_data',
                                 fallback='./data/output/customer_data.csv')

os.makedirs(os.path.dirname(transaction_data_file),exist_ok=True)
os.makedirs(os.path.dirname(customer_data_file),exist_ok=True)

df_transactions.to_csv(transaction_data_file, index=False)
df_customer_datamart.to_csv(customer_data_file, index=False)

print(f"Data is saved to files\n{customer_data_file}\n{transaction_data_file}\n")


