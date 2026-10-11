
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# random.seed(42)

# Sample data
salespersons = [
    "Aarav Sharma",
    "Priya Reddy",
    "Rahul Verma",
    "Sneha Patel",
    "Amit Kumar",
    "Ananya Singh",
    "Kiran Rao",
    "Pooja Gupta",
    "Arjun Reddy",
    "Neha Sharma",
    "Rohit Mishra",
    "Kavya Nair",
    "Sanjay Patel",
    "Divya Menon",
    "Vikram Singh",
    "Meera Iyer",
    "Akash Verma",
    "Riya Kapoor",
    "Suresh Reddy",
    "Nisha Kumari",
    "Varun Joshi",
    "Aishwarya Rao",
    "Deepak Yadav",
    "Tanvi Shah",
    "Manish Gupta",
    "Shreya Das",
    "Nikhil Jain",
    "Lakshmi Menon",
    "Rajesh Kumar",
    "Simran Kaur",
    "Pranav Shah",
    "Ishita Roy",
    "Abhishek Mishra",
    "Swati Agarwal",
    "Gaurav Malhotra",
    "Sahana Murthy",
    "Naveen Reddy",
    "Ritika Sinha",
    "Ajay Thakur",
    "Pallavi Desai",
    "Karthik Iyer",
    "Monika Sethi",
    "Vikas Chauhan",
    "Gayatri Joshi",
    "Tarun Mehta",
    "Bhavana Rao",
    "Siddharth Jain",
    "Radhika Pillai",
    "Yash Bansal",
    "Shalini Kapoor",
    "Rohan Kulkarni",
    "Ananya Sinha",
    "Vikram Joshi",
    "Meera Nair",
    "Sandeep Yadav",
    "Kavya Rao",
    "Arjun Mehta",
    "Divya Pillai",
    "Manish Tiwari",
    "Ishita Das",
    "Abhishek Jain",
    "Swati Chawla",
    "Nikhil Bansal",
    "Tanvi Deshmukh",
    "Akash Malhotra",
    "Ritu Agarwal",
    "Varun Shetty",
    "Shreya Ghosh",
    "Deepak Chauhan",
    "Aditi Saxena",
    "Mohan Babu",
    "Nandini Roy",
    "Siddharth Khanna",
    "Lakshmi Krishnan",
    "Rajesh Pawar",
    "Simran Kaur",
    "Pranav Kulkarni",
    "Padmini Rao",
    "Harish Chandra",
    "Bhavana Reddy",
    "Tarun Kapoor",
    "Komal Sharma",
    "Gaurav Tripathi",
    "Sahana Murthy",
    "Naveen Kumar",
    "Ritika Singh",
    "Ajay Patel",
    "Pallavi Desai",
    "Karthik Subramanian",
    "Monika Verma",
    "Vikas Sharma",
    "Gayatri Joshi",
    "Rahul Choudhary",
    "Preeti Nair",
    "Siddhi Patil",
    "Anil Reddy",
    "Radhika Menon",
    "Yash Agarwal",
    "Shalini Gupta",
    "Aditya Deshmukh"
]


regions = ["North", "South", "East", "West"]

products = {
    "Laptop": 45000,
    "Mobile": 20000,
    "Keyboard": 1200,
    "Mouse": 600,
    "Monitor": 12000,
    "Headphones": 2500,
    "Printer": 8000,
    "Tablet": 15000,
    "Smartwatch": 10000,
    "Camera": 18000,
    "Speakers": 3000,
    "External Hard Drive": 5000
}

data = []
start_date = datetime(2026, 1, 1)

# Generate 200 sales transactions
for i in range(1, 10001):
    product = random.choice(list(products.keys()))

    row = {
        "Order ID": f"ORD{i:04d}",
        "Date": (
            start_date + timedelta(days=random.randint(0, 89))
        ).strftime("%Y-%m-%d"),
        "Salesperson": random.choice(salespersons),
        "Region": random.choice(regions),
        "Product": product,
        "Quantity": random.randint(1, 10),
        "Unit Price": products[product]
    }

    data.append(row)

df = pd.DataFrame(data)

# 1. Add duplicate records
duplicates = df.sample(10, random_state=1)
df = pd.concat([df, duplicates], ignore_index=True)

# 2. Introduce null values
for col in ["Date", "Salesperson", "Region", "Product"]:
    indexes = random.sample(list(df.index), 5)
    df.loc[indexes, col] = None

# 3. Introduce missing quantities
indexes = random.sample(list(df.index), 5)
df.loc[indexes, "Quantity"] = None

# 4. Introduce missing unit prices
indexes = random.sample(list(df.index), 5)
df.loc[indexes, "Unit Price"] = None

# 5. Introduce invalid dates
indexes = random.sample(list(df.index), 3)
for idx in indexes:
    df.loc[idx, "Date"] = "invalid-date"

# 6. Introduce negative quantities
indexes = random.sample(list(df.index), 3)
df.loc[indexes, "Quantity"] = -random.randint(1, 5)

# 7. Introduce zero unit prices
indexes = random.sample(list(df.index), 3)
df.loc[indexes, "Unit Price"] = 0

# 8. Introduce inconsistent text
df.loc[df.sample(3, random_state=10).index, "Region"] = " south "
df.loc[df.sample(3, random_state=20).index, "Product"] = "laptop"

# 9. Add blank strings
indexes = random.sample(list(df.index), 3)
df.loc[indexes, "Salesperson"] = ""

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)



df.to_csv("C:\\Users\\Admin\\Desktop\\Final Project\\Data_sets\\messy_sales_data.csv", index=False)
df.to_excel("C:\\Users\\Admin\\Desktop\\Final Project\\Data_sets\\messy_sales_data.xlsx", index=False)

print("Messy sales dataset generated!")
print("Total rows:", len(df))
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nExact duplicate rows:", df.duplicated().sum())
print("\nFirst 10 rows:")
print(df.head(10))