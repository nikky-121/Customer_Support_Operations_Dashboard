import pandas as pd

products = pd.DataFrame({
    "Product": ["ONT", "OLT"]
})

products.to_csv(
    r"../processed_data/DimProduct/DimProduct.csv",
    index=False
)

print(products)
print("\nDimProduct created successfully")