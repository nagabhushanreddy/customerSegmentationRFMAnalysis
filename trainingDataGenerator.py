# %% [markdown]
# # Use this script to generate sample data that can be used to evaluate and understand prototype.
# 
# * In real world case please use actual data from your banking transacgtion data. 
# * This tool is only meant for understanding the prototype by generating sample data-set and does not reflect any real-world data. 

# %% [markdown]
# # Import required libraries

# %%
from faker import Faker
import pandas as pd
import random
from utils.config import config

# %% [markdown]
# # Download template data

# %%

category_data_file = config.get('META','category_data',
                                 fallback='./data/DSME-Categories.csv')

transaction_codes_data_file = config.get('META','transaction_codes_data',
                                 fallback='./data/DSME-Transaction-codes.csv')

category_data = pd.read_csv(category_data_file)
transaction_codes = pd.read_csv(transaction_codes_data_file)
# Define some rules 
category_data['indicator'] = category_data['Category2'].apply(lambda x: 'CR' if any (cat2 in x.strip().lower() for cat2 in ['revenue', 'incom']) else 'DB')

# %% [markdown]
# # Create supporting functions

# %%
from faker.providers import BaseProvider, company
from faker import Faker
import fnmatch
fake = Faker()

# create new provider class
class TranNotesProvider(BaseProvider):
    def transaction_notes(self, transaction_type="") -> str:
        my_list = ['', ' ']
        transaction_type = transaction_type.lower()
        if fnmatch.fnmatch(transaction_type, '*supply chain costs*'.lower()):
            my_list = ['transport goods', 'send goods',
                       'supply-chain', 'supply', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*transportation costs*'.lower()):
            my_list = ['travel', 'transport', 'bus',
                       'flight', 'cab', 'car', '', ' ']
        elif fnmatch.fnmatch(transaction_type,  '*employee salaries and benefits*'.lower()):
            my_list = ['wage', 'bonus', 'salary', 'pay',
                       'incentive', 'perk for employee', 'Tips', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*business travel*'.lower()):
            my_list = ['air line', 'business trip', 'trip', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*rent*'.lower()):
            my_list = ['shop rent', 'office rent',
                       'monthly rental', 'rent', 'lease', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*IT expenses*'.lower()):
            my_list = ['IT rental', 'Pay software', 's/w',
                       'license', 'billing', 'software', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Utilities*'.lower()):
            my_list = ['gas', 'electicity', 'phone bill', 'telephone bill',
                       'internet bill payment', 'cleaning', 'town council', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*electricity*'.lower()):
            my_list = ['electicity', 'power bill', 'Energy bill' ,'', ' ']        
        elif fnmatch.fnmatch(transaction_type, '*gas*'.lower()):
            my_list = ['gas bill', 'Energy bill', 'cooking', 'heating','', ' ']        
        elif fnmatch.fnmatch(transaction_type, '*internet*'.lower()):
            my_list = ['phone bill', 'internet bill', 'broadband', 'communication','', ' ']                    
        elif fnmatch.fnmatch(transaction_type, '*Licenses and insurance*'.lower()):
            my_list = ['license fee', 'business insurance',
                       'insurance', 'accounting', 'royalty', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Employee training*'.lower()):
            my_list = ['training', 'education', 'skill development', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Marketing*'.lower()):
            my_list = ['ads', 'marketing', 'capaign',
                       'tv advertisement', 'newspapaer advertisement', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*COGS*'.lower()):
            my_list = ['raw material', 'fruits',
                       'vegetables', 'cloth', 'garment', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Meals and entertainment *'.lower()):
            my_list = ['food', 'meal', 'coffee', 'tv', 'outing', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Consulting*'.lower()):
            my_list = ['accounting', 'legal payment', 'taxing', 'digital',
                       'website', 'mobile app', 'search engine', 'seo', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Inventory*'.lower()):
            my_list = ['goods purchased', 'inventory billing', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Machinery*'.lower()):
            my_list = ['gas', 'electicity', 'phone bill', 'telephone bill',
                       'internet bill payment', 'cleaning', 'town council', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Real Estate*'.lower()):
            my_list = ['gardening bill', 'landscaping bill',
                       'interior design', 'showcase', 'painting bill', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Other Outgoing*'.lower()):
            my_list = ['pay', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Sales Revenue*'.lower()):
            my_list = ['Payment Received', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Interest Income*'.lower()):
            my_list = ['intertest paid for period', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Rental Income*'.lower()):
            my_list = ['rent', 'paying rent', 'pay', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Services Income*'.lower()):
            my_list = ['service provided', '', ' ']
        elif fnmatch.fnmatch(transaction_type, '*Other Income*'.lower()):
            my_list = ['other', 'any', 'miscellaneous', '', ' ']
        else:
            my_list = my_list
        return self.random_element(elements=my_list)


class CustomCompanyProvider(company.Provider):
    # Define your custom method to generate company names
    def custom_company_name(self, transaction_type=""):
        industries = {
            "Supply chain costs": [
                "Logistics",
                "Transportation",
                "Warehousing",
                "Distribution",
                "Freight",
                "Supply Chain Management",
                "Inventory Management",
                "Procurement",
                "Shipping",
                "Freight Forwarding",
                ''
            ],
            "Transportation costs": [
                "Transportation",
                "Ride-hailing",
                "Taxi",
                "Delivery",
                "Logistics",
                "Courier",
                "Shipping",
                "Freight",
                "Freight Forwarding",
                "Warehousing",
                "Transportation Network",
                "Express",
                "Transport",
                "Dispatch",
                "Shipment",
                "Fleet",
                "Distribution",
                "Last-mile",
                "On-demand",
                "Transportation Management"
            ],
            "Employee salaries and benefits": [],
            "Business travel": [
                "Airways",
                "Airlines",
                "Aviation",
                "Airline Services",
                "Business Travel",
                "Corporate Travel",
                "Travel Management",
                "Travel Solutions",
                "Travel Services",
                "Business Air Travel",
                "Travel Management Solutions",
                "Travel Agency",
                "Corporate Air Travel",
                "Business Travel Solutions",
                "Business Airline Services",
                "Corporate Travel Services",
                "Travel Management Company",
                "Corporate Airline Services",
                "Business Travel Agency",
                "Travel Management Solutions",
                "Corporate Travel Management"
            ],
            "Rent": [
                "Properties",
                "Estates",
                "Rentals",
                "Realty",
                "Leasing",
                "Lettings",
                "Homes",
                "Apartments",
                "Residences",
                "Accommodations",
                "Spaces",
                "Dwellings",
                "Tenements",
                "Lodgings",
                "Villas"
            ],
            "IT expenses": [
                "Solutions",
                "Technologies",
                "Systems",
                "Software",
                "Services",
                "Consulting",
                "Development",
                "Solutions",
                "Innovations",
                "Digital",
                "Solutions",
                "Information",
                "Management",
                "Technologies",
                "Applications"
            ],
            "Utilities": [
                "Power",
                "Energy",
                "Utilities",
                "Group",
                "Solutions",
                "Services",
                "Resources",
                "Electric",
                "Water",
                "Gas",
                "Renewable",
                "Provider"
            ],
            "Electricity": [
                "Power",
                "Energy",
                "Electric",
                "Renewable",
                "Provider"
            ],
            "Gas": [
                "Gas",
                "Renewable",
                "Energy"
            ],
            "Internet": [
                "TeleCommunications",
                "communication",
                "fiber",
                "internet services",
                "broadband services",
                "4G Services"
            ],
            "Licenses and insurance": [
                "Insurance",
                "Assurance",
                "Licensing",
                "Licensing & Insurance",
                "Underwriters",
                "Brokers",
                "Agency",
                "Coverage",
                "Risk Management",
                "Insurers",
                "License Services",
                "License Solutions",
                "License Providers",
                "License Brokers",
                "License Consultants"
            ],
            "Employee training": [
                "Training",
                "Learning",
                "Development",
                "Education",
                "Solutions",
                "Academy",
                "Institute",
                "Consulting",
                "Professional Development",
                "Corporate Training",
                "Skills Development",
                "Human Resources Development",
                "Talent Development",
                "Leadership Training",
                "Workplace Training"
            ],
            "Marketing": [
                "Marketing",
                "Advertising",
                "Digital",
                "Media",
                "Communications",
                "Strategy",
                "Solutions",
                "Agency",
                "Creative",
                "Branding",
                "Social",
                "Public Relations",
                "Content",
                "Analytics",
                "Campaigns"
            ],
            "COGS": [
                "Wholesale",
                "Distributors",
                "Suppliers",
                "Traders",
                "Wholesalers",
                "Merchants",
                "Suppliers",
                "Providers",
                "B2B (Business-to-Business)",
                "Trade",
                "Bulk",
                "Resellers",
                "Exporters",
                "Importers",
                "Agents"
            ],
            "Meals and entertainment": [
                "Restaurants",
                "Catering",
                "Dining",
                "Hospitality",
                "Food",
                "Beverages",
                "Caterers",
                "Events",
                "Banquets",
                "Hospitality",
                "Entertainment",
                "Dining",
                "Culinary",
                "Dining",
                "Bistro"
            ],
            "Consulting": [
                "Consulting",
                "Advisory",
                "Solutions",
                "Services",
                "Strategies",
                "Partners",
                "Group",
                "Advisors",
                "Management",
                "Associates",
                "Experts",
                "Consultants",
                "Professional",
                "Advisory",
                "Business"
            ],
            "Inventory": [
                "Wholesale",
                "Distributors",
                "Suppliers",
                "Wholesale Distributors",
                "Wholesalers",
                "Suppliers",
                "Distributors",
                "Resellers",
                "Wholesalers",
                "Bulk",
                "Retailers",
                "Merchandise",
                "Inventory",
                "Products",
                "Goods"
            ],
            "Machinery": [
                "Machinery",
                "Equipment",
                "Tools",
                "Industrial",
                "Solutions",
                "Systems",
                "Technologies",
                "Manufacturing",
                "Automation",
                "Engineering",
                "Innovations",
                "Supplies",
                "Machineries",
                "Services",
                "Components"
            ],
            "Real Estate": [
                "Interiors",
                "Landscaping",
                "Property",
                "Realty",
                "Development",
                "Construction",
                "Design",
                "Architecture"
            ],
            "Sales Revenue": [''],
            "Interest Income": [''],
            "Investment Income": [''],
            "Rental Income": [''],
            "Services Income": [''],
            "Other Income": [''],
            "Other Incoming": [''],
            "Other Outgoing": ['']
        }
        industry = ""
        for industry_type in list(industries.keys()):
            if fnmatch.fnmatch(transaction_type.lower(),  f'*{industry_type}*'.lower()):
                industry_list = industries[industry_type]
                industry = self.random_element(elements=industry_list)
        company_name_with_industry = f"{self.company()} {industry} {self.company_suffix()}"
        return company_name_with_industry

employeeList = []

# %%
# then add new provider to faker instance
fake.add_provider(TranNotesProvider)
fake.add_provider(CustomCompanyProvider)


# %%
import uuid

def make_employeelist(n):
    salaries = list(range(2000, 5000 + 1, 500))
    global employeeList
    for i in range(n):
        employeeList.append({
            "name": fake.name(),
            "salary": fake.random_element(elements=salaries),
            "accountNumber": fake.random_number(digits=10)
        })
    
def get_customer():
    sampleTransaction = {
    'customerID': '',
    'customerName':'',
    'customerAge': '',
    'customerGender': '',
    'customerLocation': '',
    'customerEducation': '',
    'customerIndustry': '',
    'customerAuthorizedSignatories': ''
    }
    sampleTransaction['customerID'] = fake.random_number(digits=8, fix_len=True)
    sampleTransaction['customerName'] = fake.random_element(elements=[fake.name(),fake.name(),fake.name(),fake.name(), fake.company()])
    sampleTransaction['customerAge'] = fake.random_int(min=20, max=80)
    sampleTransaction['customerGender'] = fake.random_element(elements=('Male', 'Female', 'Other'))
    sampleTransaction['customerLocation'] = fake.address()
    sampleTransaction['customerEducation'] = fake.random_element(elements=('High School', 'Bachelor', 'Master', 'PhD'))
    sampleTransaction['customerIndustry'] = fake.random_element(elements=('Textiles and Garments', 'Food and Beverage', 'Furniture', 'Tourism', 'Automotive' , 'Manufacturing', 'Retail', 'Healthcare', 'Hospitality', 'Finance', 'IT', 'Education'))
    anotherAuthSignatory = random.choice([None, fake.name()])
    sampleTransaction['customerAuthorizedSignatories'] = [signatory for signatory in [sampleTransaction['customerName'],anotherAuthSignatory] if signatory]
    return sampleTransaction

def get_transaction(row):
    sampleTransaction = {
    'transactionReference': '',
    'transactionDate': '',
    'payeeAccountNumber': "",
    'payeeName': '',
    'payeeIndustry': '',
    'transactionCode': '',
    'amount': 0,
    'indicator': '',
    'transferNotes': ''
    }
    
    utility_list = ["gas", "electricity", "internet"]

    category = row['Category1']
    level_down_category = fake.random_element(elements=utility_list) if fnmatch.fnmatch(
             category.lower(),  '*Utilities*'.lower()) else category
    if category.strip():
        transferNotes = fake.transaction_notes(level_down_category) 
    else:
        transferNotes = ""
    
    sampleTransaction['transactionReference'] = uuid.uuid4().hex
    sampleTransaction['transactionDate'] = fake.date_between(start_date='-3y', end_date='today')
    sampleTransaction['indicator'] = row['indicator']
    sampleTransaction['transactionCategory'] = category
    sampleTransaction['transferNotes'] = transferNotes
    random_int = random.randint(1, 9)
    sampleTransaction['transactionCode'] = transaction_codes.iloc[random_int]['Trx Code']
    
    if fnmatch.fnmatch((row['Category1']).lower(),  '*employee salaries and benefits*'.lower()):
        employee = fake.random_element(elements=employeeList)
        sampleTransaction['payeeAccountNumber'] = employee.get("accountNumber")
        sampleTransaction['payeeName'] = employee.get("name")
        sampleTransaction['amount'] = employee.get("salary")
    else:
        sampleTransaction['payeeAccountNumber'] = fake.random_number(digits=10)
        payeeName = fake.name() if row['indicator'] == 'CR' else fake.custom_company_name(transaction_type=level_down_category)
        sampleTransaction['payeeName'] = payeeName
        amount = fake.pyfloat(left_digits=3, right_digits=2, min_value=100, max_value=999) if row['indicator'] == 'CR' else  fake.pyfloat(left_digits=4, right_digits=2, min_value=1000, max_value=9999)
        sampleTransaction['amount'] = amount 
    return sampleTransaction


# %%
print(get_customer())

# %% [markdown]
# # Generate training data
# 
# 1. Simulate customers so they fall into various segments 
#     - Most Valued Customers 
#     - Loyal Customers
#     - Potential Loyal Customers
#     - Need Attention 
#     - Churned Folk
# 2. Simulate to have transactions of different types and different amount. 
# 3. Spread acorss a period of 2 years
# 

# %%
# Create customers 

import pandas as pd 

number_of_customers = 2000
customers=[]
for i in range(number_of_customers):
    customers.append(get_customer())

df_customers = pd.DataFrame(customers)

df_customers.info()

df_customers.head()

# %%
def split_list(numbers, ratios):
    # Calculate the total length of the sublists
    total_length = sum(ratios)
    
    # Calculate the length of each sublist
    lengths = [int(len(numbers) * r / total_length) for r in ratios]
    
    # Add any remaining elements to the first sublist
    lengths[0] += len(numbers) - sum(lengths)
    
    # Use list slicing to split the original list into sublists
    sublists = [numbers[sum(lengths[:i]):sum(lengths[:i+1])] for i in range(len(ratios))]
    
    return sublists

# %%
segments_to_split = {
    0 : {
        "label" : "MVC",
        "description": "Most Valued Customer",
        "ratio" : 15,
        "transactionsPerMonth" : 8
    },
    1 : {
        "label" : "LOY",
        "description": "Loyal Customer",
        "ratio" : 35,
        "transactionsPerMonth" : 4
    },
    2 : {
        "label" : "POT",
        "description": "Potential Loyal Customer",
        "ratio" : 15,
        "transactionsPerMonth" : 2
    },
    3 : {
        "label" : "AN",
        "description": "Attention Needed Customer",
        "ratio" : 18,
        "transactionsPerMonth" : 0.5
    },
    4 : {
        "label" : "LS",
        "description": "Churned Folk",
        "ratio" : 17,
        "transactionsPerMonth" : 0.002
    } 
}

df_customers['segment_key'] = pd.NA

ratio_list = list(map(lambda x : x.get('ratio'), segments_to_split.values()))

segment_index_list = split_list(range(len(df_customers)), ratio_list)

for key in segments_to_split.keys():
    index_list = segment_index_list[key]
    df_customers.loc[index_list, 'segment_key'] = key 
    # Handling customer data 
    if key == 0:
        #Add logic for MVC
        None 
    elif key == 1: 
        #Add logic for LOY 
        None
    elif key == 2: 
        #Add logic for POT
        None
    elif key == 3: 
        #Add logic for AN
        df_customers.loc[index_list, 'customerEducation'] = df_customers.loc[index_list, 'customerEducation'].apply(lambda x: fake.random_element(elements=('High School', 'Bachelor',x)))
        df_customers.loc[index_list, 'customerAge'] = df_customers.loc[index_list, 'customerAge'].apply(lambda x: fake.random_element(elements=range(40,70)))
        df_customers.loc[index_list, 'customerIndustry'] = df_customers.loc[index_list, 'customerAge'].apply(lambda x: fake.random_element(elements=('Textiles and Garments', 'Food and Beverage', 'Furniture',x)))
    elif key == 4:
        #Add logic for LS
        df_customers.loc[index_list, 'customerEducation'] = df_customers.loc[index_list, 'customerEducation'].apply(lambda x: fake.random_element(elements=('High School',x)))
        df_customers.loc[index_list, 'customerAge'] = df_customers.loc[index_list, 'customerAge'].apply(lambda x: fake.random_element(elements=range(50,81)))
        df_customers.loc[index_list, 'customerIndustry'] = df_customers.loc[index_list, 'customerAge'].apply(lambda x: fake.random_element(elements=('Textiles and Garments', 'Food and Beverage', 'Furniture',x)))
    else:
        print("Unknown segment no action performed.")





df_customers['segment_key'].value_counts()


# %%
# Create transactions for each segment as per the rules 
import datetime
number_of_months_data = 24
number_of_years = number_of_months_data/12
start_date=datetime.date.today() - datetime.timedelta(days=1*number_of_years*365)
end_date=datetime.date.today()
get_transaction_date = lambda x : fake.date_between(start_date=start_date, end_date=end_date)
df_transactions = pd.DataFrame()
for index, row in df_customers.iterrows():
    make_employeelist(1)
    transactionsPerMonth = 1
    segment_key = row['segment_key']
    transactionsPerMonth = segments_to_split[segment_key].get('transactionsPerMonth')
    number_of_transactions = number_of_months_data * transactionsPerMonth
    transactions = []
    while number_of_transactions > 0:
        category_row = category_data.sample(n=1, axis=0).to_dict('records')[0]
        transactions.append(get_transaction(category_row))
        number_of_transactions = number_of_transactions - 1 
    if transactions:
        df_transactions_customer = pd.DataFrame(transactions)
        df_transactions_customer['customerID'] = row['customerID']
        # Add logic to change any data in df_transactions_customer 
        # Dates should be adjusted for recency 
        if segment_key == 0:
            #Add logic for MVC
            start_date=datetime.date.today() - datetime.timedelta(days=1*number_of_years*365)
            end_date=datetime.date.today()
            df_transactions_customer['transactionDate'] = df_transactions_customer['transactionDate'].apply(get_transaction_date)
        elif segment_key == 1: 
            #Add logic for LOY 
            start_date=datetime.date.today() - datetime.timedelta(days=0.9*number_of_years*365)
            end_date=datetime.date.today()
            df_transactions_customer['transactionDate'] = df_transactions_customer['transactionDate'].apply(get_transaction_date)
        elif segment_key == 2: 
            #Add logic for POT
            start_date=datetime.date.today() - datetime.timedelta(days=0.75*number_of_years*365)
            end_date=datetime.date.today()
            df_transactions_customer['transactionDate'] = df_transactions_customer['transactionDate'].apply(get_transaction_date)
        elif segment_key == 3: 
            #Add logic for AN
            start_date=datetime.date.today() - datetime.timedelta(days=1*number_of_years*365)
            end_date=datetime.date.today() - datetime.timedelta(days=0.75*number_of_years*365)
            df_transactions_customer['transactionDate'] = df_transactions_customer['transactionDate'].apply(get_transaction_date)
        elif segment_key == 4:
            #Add logic for LS
            start_date=datetime.date.today() - datetime.timedelta(days=1*number_of_years*365)
            end_date=datetime.date.today() - datetime.timedelta(days=0.5*number_of_years*365)
            df_transactions_customer['transactionDate'] = df_transactions_customer['transactionDate'].apply(get_transaction_date)
        else:
            print("Unknown segment no action performed.")
        df_transactions = pd.concat([df_transactions, df_transactions_customer]) 
df_transactions['customerID'].value_counts()

# %%
(pd.merge(df_transactions, df_customers, on='customerID', how='inner') ).groupby('segment_key').agg({'customerID': 'max', 'segment_key': 'size'})

# %%
#Remove unwanted columns
df_customers.drop(columns=['segment_key'], inplace=True)

# %% [markdown]
# # Save Training data

# %%
import os

transact_data_file = config.get('INPUT','transaction_data',
                                 fallback='./data/input/customer_transaction_data.csv')

customer_data_file = config.get('INPUT','customer_data',
                                 fallback='./data/input/customer_data.csv')

os.makedirs(os.path.dirname(transact_data_file),exist_ok=True)
os.makedirs(os.path.dirname(customer_data_file),exist_ok=True)

df_transactions.to_csv(transact_data_file, index=False)
df_customers.to_csv(customer_data_file, index=False)

print(f"Data is saved to files\n{customer_data_file}\n{transact_data_file}\n")


