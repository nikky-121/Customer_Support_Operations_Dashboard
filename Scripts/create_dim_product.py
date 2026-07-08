import pandas as pd

# Read FactCalls
df = pd.read_excel(
    r"../Processed_Data/FactCalls/FactCalls.xlsx"
)

# Extract unique products
products = (
    df["Product"]
    .dropna()
    .astype(str)
    .str.strip()
    .drop_duplicates()
    .sort_values()
)

# Create Product Key
dim_product = pd.DataFrame({
    "Product Key": range(1, len(products) + 1),
    "Product": products.values
})

# Save
dim_product.to_excel(
    r"../Processed_Data/DimProduct/DimProduct.xlsx",
    index=False
)

print(dim_product)
print("DimProduct created successfully.")