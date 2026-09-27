from data_loader import load_portfolio_data


df = load_portfolio_data()

print("\n" + "=" * 60)
print("PORTFOLIO DATASET DETAILS")
print("=" * 60)

print("\nColumns:")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\nData Types:")
print(df.dtypes)

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 rows:")
print(df.head().to_string())