import pandas as pd

# Create date range
dates = pd.date_range(
    start="2026-01-01",
    end="2030-12-31",
    freq="D"
)

dim_date = pd.DataFrame({
    "Date": dates
})

# Date attributes
dim_date["Year"] = dim_date["Date"].dt.year
dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
dim_date["Month Number"] = dim_date["Date"].dt.month
dim_date["Month Name"] = dim_date["Date"].dt.month_name()
dim_date["Year Month"] = dim_date["Date"].dt.strftime("%Y-%m")
dim_date["Week Number"] = dim_date["Date"].dt.isocalendar().week
dim_date["Day"] = dim_date["Date"].dt.day
dim_date["Day Name"] = dim_date["Date"].dt.day_name()
dim_date["Day Of Week"] = dim_date["Date"].dt.weekday + 1

# Weekend flag
dim_date["Is Weekend"] = dim_date["Day Name"].isin(
    ["Saturday", "Sunday"]
)

# Save
dim_date.to_csv(
    r"../Processed_Data/DimDate/DimDate.csv",
    index=False
)

print(dim_date.head())
print("\nRows:", len(dim_date))
print("\nDimDate created successfully")