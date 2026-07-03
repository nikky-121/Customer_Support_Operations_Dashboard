import pandas as pd
import re

# Read FactCalls
df = pd.read_csv(r"../Processed_Data/FactCalls/FactCalls.csv")

activity_rows = []

for _, row in df.iterrows():

    call_flow = str(row["Call Flow"])
    direction = str(row["Direction"]).strip()

    # Extract all Agent events
    agents = re.findall(
        r'Agent:\s*(.*?)\((Dialed|Answered)\)',
        call_flow
    )

    # ==========================
    # INBOUND LOGIC
    # ==========================
    if direction == "Inbound":

        dialed_agents = set()
        answered_agents = set()

        for agent, status in agents:

            agent = agent.strip()

            # Skip phone numbers
            if agent.isdigit():
                continue

            if status == "Dialed":
                dialed_agents.add(agent)

            elif status == "Answered":
                answered_agents.add(agent)

        # Answered records
        for agent in answered_agents:

            activity_rows.append({
                "Call ID": row["Call ID"],
                "Date": row["Date"],
                "Product": row["Product"],
                "Direction": row["Direction"],
                "Department": row["Department"],
                "Agent": agent,
                "Activity": "Answered"
            })

        # Missed records
        for agent in (dialed_agents - answered_agents):

            activity_rows.append({
                "Call ID": row["Call ID"],
                "Date": row["Date"],
                "Product": row["Product"],
                "Direction": row["Direction"],
                "Department": row["Department"],
                "Agent": agent,
                "Activity": "Missed"
            })

    # ==========================
    # OUTBOUND LOGIC
    # ==========================
    elif direction == "Outbound":

        dialed_agents = []
        answered_agents = []
        answered_numbers = []

        for agent, status in agents:

            agent = agent.strip()

            if status == "Dialed":

                # Real agent names only
                if not agent.isdigit():
                    dialed_agents.append(agent)

            elif status == "Answered":

                if agent.isdigit():
                    answered_numbers.append(agent)
                else:
                    answered_agents.append(agent)

        # No calling agent found
        if len(dialed_agents) == 0:
            continue

        calling_agent = dialed_agents[0]

        # Customer answered
        if len(answered_numbers) > 0:

            activity_rows.append({
                "Call ID": row["Call ID"],
                "Date": row["Date"],
                "Product": row["Product"],
                "Direction": row["Direction"],
                "Department": row["Department"],
                "Agent": calling_agent,
                "Activity": "Answered"
            })

        # Agent-to-agent test call
        elif len(answered_agents) > 0:
            continue

        # Customer missed
        else:

            activity_rows.append({
                "Call ID": row["Call ID"],
                "Date": row["Date"],
                "Product": row["Product"],
                "Direction": row["Direction"],
                "Department": row["Department"],
                "Agent": calling_agent,
                "Activity": "Missed"
            })


# Create dataframe
agent_df = pd.DataFrame(activity_rows)

print("Rows created:", len(agent_df))
print(agent_df.head())

# Save
agent_df.to_csv(
    r"../Processed_Data/FactAgentActivity/FactAgentActivity.csv",
    index=False
)

print("FactAgentActivity saved successfully")

print(agent_df["Direction"].value_counts())
print(agent_df["Activity"].value_counts())
print(agent_df["Agent"].nunique())