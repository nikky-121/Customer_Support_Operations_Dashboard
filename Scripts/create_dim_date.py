import pandas as pd

# Read FactCalls
df = pd.read_excel(
    r"../Processed_Data/FactCalls/FactCalls.xlsx"
)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Extract unique dates (remove time)
dates = (
    df["Date"]
    .dt.normalize()
    .drop_duplicates()
    .sort_values()
)

# Create DimDate
dim_date = pd.DataFrame({
    "Date": dates
})

# Calendar attributes
dim_date["Day"] = dim_date["Date"].dt.day
dim_date["Month"] = dim_date["Date"].dt.month
dim_date["Month Name"] = dim_date["Date"].dt.strftime("%B")
dim_date["Quarter"] = "Q" + dim_date["Date"].dt.quarter.astype(str)
dim_date["Year"] = dim_date["Date"].dt.year
dim_date["Weekday"] = dim_date["Date"].dt.strftime("%A")
dim_date["Week Number"] = dim_date["Date"].dt.isocalendar().week.astype(int)

# Format Date
dim_date["Date"] = dim_date["Date"].dt.strftime("%d-%m-%Y")

# Reorder columns
dim_date = dim_date[
    [
        "Date",
        "Day",
        "Month",
        "Month Name",
        "Quarter",
        "Year",
        "Weekday",
        "Week Number",
    ]
]

# Save
dim_date.to_excel(
    r"../Processed_Data/DimDate/DimDate.xlsx",
    index=False
)

print(dim_date.head())
print("DimDate created successfully.")