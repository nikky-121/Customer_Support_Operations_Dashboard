import pandas as pd

# Read files
agent_activity = pd.read_csv(
    r"../Processed_Data/FactAgentActivity/FactAgentActivity.csv"
)

agent_daily = pd.read_csv(
    r"../Processed_Data/FactAgentDaily/FactAgentDaily.csv"
)

# Collect agent names
agents = pd.concat([
    agent_activity["Agent"],
    agent_daily["Agent Name"]
])

# Clean
agents = (
    agents
    .dropna()
    .astype(str)
    .str.strip()
)

# Remove blanks
agents = agents[agents != ""]

# Create dimension
dim_agent = pd.DataFrame({
    "Agent": sorted(agents.unique())
})

# Reset index
dim_agent = dim_agent.reset_index(drop=True)

# Save
dim_agent.to_csv(
    r"../Processed_Data/DimAgent/DimAgent.csv",
    index=False
)

print(dim_agent.head(20))
print("\nTotal Agents:", len(dim_agent))
print("\nDimAgent created successfully")