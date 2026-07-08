import pandas as pd

df = pd.read_excel(
    r"../../Processed_Data/FactCalls/FactCalls.xlsx"
)

print("="*100)

sample_flows = (
    df["Call Flow"]
    .dropna()
    .sample(20, random_state=42)
)

for i, flow in enumerate(sample_flows, start=1):
    print(f"\nFLOW {i}")
    print("-"*80)
    print(flow)