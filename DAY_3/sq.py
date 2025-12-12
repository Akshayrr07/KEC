import sqlite3
import pandas as pd

# -----------------------------
# 1. Read CSV
# -----------------------------
csv_file = "E:\\KEC\\CSV_Files\\Data\\2019.csv"
df = pd.read_csv(csv_file)

print(f"✔ Loaded CSV with shape: {df.shape}")

# -----------------------------
# 2. Create SQLite DB
# -----------------------------
db_name = "practice.db"
conn = sqlite3.connect(db_name)

# -----------------------------
# 3. Generate SQL table dynamically
# -----------------------------
# Convert pandas dtypes → SQLite types
dtype_mapping = {
    "int64": "INTEGER",
    "float64": "REAL",
    "object": "TEXT",
    "bool": "INTEGER",
    "datetime64[ns]": "TEXT"
}

columns_sql = []
for col, dtype in df.dtypes.items():
    sql_type = dtype_mapping.get(str(dtype), "TEXT")
    columns_sql.append(f'"{col}" {sql_type}')

create_sql = f"""
CREATE TABLE IF NOT EXISTS data_2019 (
    {", ".join(columns_sql)}
);
"""

conn.execute(create_sql)
print("✔ Table created based on CSV schema.")

# -----------------------------
# 4. Insert CSV rows
# -----------------------------
df.to_sql("data_2019", conn, if_exists="append", index=False)
conn.close()

print("✔ Data successfully loaded into practice.db → data_2019")
