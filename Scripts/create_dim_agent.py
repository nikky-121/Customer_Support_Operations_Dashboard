import pandas as pd

# Read FactAgentActivity
df = pd.read_excel(
    r"../Processed_Data/FactAgentActivity/FactAgentActivity.xlsx"
)

# Extract unique agents
agents = (
    df["Agent Name"]
    .dropna()
    .astype(str)
    .str.strip()
    .drop_duplicates()
    .sort_values()
)

# Create DimAgent
dim_agent = pd.DataFrame({
    "Agent Key": range(1, len(agents) + 1),
    "Agent": agents.values
})

# Save
dim_agent.to_excel(
    r"../Processed_Data/DimAgent/DimAgent.xlsx",
    index=False
)

print(dim_agent)
print("DimAgent created successfully.")