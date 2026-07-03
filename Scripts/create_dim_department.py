import pandas as pd

df = pd.read_csv( r"../Processed_Data/FactDepartmentDaily/FactDepartmentDaily.csv")

dim_department = (
    df[["Product", "Department Name"]]
    .drop_duplicates()
    .sort_values(["Product", "Department Name"])
)

dim_department.columns = ["Product", "Department"]

dim_department.to_csv(
    "DimDepartment.csv",
    index=False
)

print("\nDimDepartment created sucessfully")