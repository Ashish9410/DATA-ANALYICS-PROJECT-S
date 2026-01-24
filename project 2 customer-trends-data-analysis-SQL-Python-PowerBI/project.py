# CUSTOMER SHOPPING BEHAVIOR
# EDA + MYSQL (DIRECT CONNECTOR)

import pandas as pd
import numpy as np
import mysql.connector

# STEP 1: LOAD DATASET
FILE_PATH = "customer_shopping_behavior.csv"

df = pd.read_csv(FILE_PATH)

print("\n✅ Dataset Loaded Successfully")
print("Shape:", df.shape)
print(df.head())

# STEP 2: BASIC EDA
print("\n📊 Dataset Info")
print(df.info())

print("\n❓ Missing Values")
print(df.isnull().sum())

print("\n📈 Statistical Summary")
print(df.describe())

# STEP 3: DATA CLEANING
df.drop_duplicates(inplace=True)

num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

df[num_cols] = df[num_cols].fillna(df[num_cols].median())

for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

print("\n✅ Data Cleaning Completed")
print("New Shape:", df.shape)

# STEP 4: MYSQL CREDENTIALS
HOST = "127.0.0.1"
USER = "root"
PASSWORD = "YOUR MYSQL PASS"   # original password
DATABASE = "customer_behavior"

# STEP 5: CONNECT TO MYSQL (NO DATABASE)
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)

cursor = conn.cursor()

# STEP 6: CREATE DATABASE IF NOT EXISTS
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
conn.commit()
print(f"✅ Database '{DATABASE}' ready")

# STEP 7: CONNECT TO DATABASE
conn.database = DATABASE
print("✅ Connected to MySQL Database")

# STEP 8: CREATE TABLE
columns_sql = []
for col, dtype in df.dtypes.items():
    if "int" in str(dtype):
        columns_sql.append(f"`{col}` INT")
    elif "float" in str(dtype):
        columns_sql.append(f"`{col}` FLOAT")
    else:
        columns_sql.append(f"`{col}` VARCHAR(255)")

create_table_query = f"""
CREATE TABLE IF NOT EXISTS customer_shopping_cleaned (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {", ".join(columns_sql)}
)
"""

cursor.execute(create_table_query)
conn.commit()
print("✅ Table created / verified")

# STEP 9: INSERT DATA
placeholders = ", ".join(["%s"] * len(df.columns))
columns = ", ".join([f"`{col}`" for col in df.columns])

insert_query = f"""
INSERT INTO customer_shopping_cleaned ({columns})
VALUES ({placeholders})
"""

data_tuples = [tuple(row) for row in df.to_numpy()]

cursor.executemany(insert_query, data_tuples)
conn.commit()

print("✅ Data inserted into MySQL table: customer_shopping_cleaned")

# STEP 10: CLOSE CONNECTION
cursor.close()
conn.close()

print("\n🎉 EDA + MYSQL PIPELINE COMPLETED SUCCESSFULLY")
