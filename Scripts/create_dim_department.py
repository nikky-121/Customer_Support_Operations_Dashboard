import pandas as pd

# Read FactDepartmentDaily
df = pd.read_excel(
    r"../Processed_Data/FactDepartmentDaily/FactDepartmentDaily.xlsx"
)

# Extract unique departments
departments = (
    df["Department"]
    .dropna()
    .astype(str)
    .str.strip()
    .drop_duplicates()
    .sort_values()
)

# Create DimDepartment
dim_department = pd.DataFrame({
    "Department Key": range(1, len(departments) + 1),
    "Department": departments.values
})

# Save
dim_department.to_excel(
    r"../Processed_Data/DimDepartment/DimDepartment.xlsx",
    index=False
)

print(dim_department)
print("DimDepartment created successfully.")