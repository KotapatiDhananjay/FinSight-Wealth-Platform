import pandas as pd


def load_portfolio_data():
    file_path = "data/finsight_portfolio_data.csv"

    df = pd.read_csv(file_path)

    print("Portfolio Dataset Loaded Successfully")
    print("--------------------------------------")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    return df


def load_risk_profiles():
    file_path = "data/finsight_risk_profiles.csv"

    df = pd.read_csv(file_path)

    print("\nRisk Profile Dataset Loaded Successfully")
    print("----------------------------------------")
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    return df


if __name__ == "__main__":
    portfolio_data = load_portfolio_data()
    risk_profiles = load_risk_profiles()