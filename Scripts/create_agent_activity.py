import pandas as pd
import re

# Read FactCalls
df = pd.read_excel(r"../Processed_Data/FactCalls/FactCalls.xlsx")

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

        dialed_agents = []
        answered_agents = []

        for agent, status in agents:

            agent = agent.strip()

            # Skip phone numbers
            if agent.isdigit():
                continue

            if status == "Dialed":
                if agent not in dialed_agents:
                    dialed_agents.append(agent)

            elif status == "Answered":
                if agent not in answered_agents:
                    answered_agents.append(agent)

        # Agents missed
        for agent in dialed_agents:

            if agent not in answered_agents:

                activity_rows.append({
                    "Call ID": row["Call ID"],
                    "Date": row["Date"],
                    "Product": row["Product"],
                    "Direction": row["Direction"],
                    "Department": row["Department"],
                    "Agent Name": agent,
                    "Activity": "Missed",
                    "Client Number": row["Client Number"],
                    "Call Duration": 0
                })

        # Agents answered
        for agent in dialed_agents:

            if agent in answered_agents:

                activity_rows.append({
                    "Call ID": row["Call ID"],
                    "Date": row["Date"],
                    "Product": row["Product"],
                    "Direction": row["Direction"],
                    "Department": row["Department"],
                    "Agent Name": agent,
                    "Activity": "Answered",
                    "Client Number": row["Client Number"],
                    "Call Duration": row["Call Duration"]
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
                "Agent Name": calling_agent,
                "Activity": "Answered",
                "Client Number": row["Client Number"],
                "Call Duration": row["Call Duration"]
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
                "Agent Name": calling_agent,
                "Activity": "Missed",
                "Client Number": row["Client Number"],
                "Call Duration": 0
            })


# Create dataframe
agent_df = pd.DataFrame(activity_rows)

agent_df["Date"] = pd.to_datetime(agent_df["Date"])
agent_df["Date"] = agent_df["Date"].dt.strftime("%d-%m-%Y %H:%M:%S")

print("Rows created:", len(agent_df))
print(agent_df.head())

# Save
agent_df.to_excel(
    r"../Processed_Data/FactAgentActivity/FactAgentActivity.xlsx",
    index=False
)

print("FactAgentActivity saved successfully")

print(agent_df["Direction"].value_counts())
print(agent_df["Activity"].value_counts())
print(agent_df["Agent Name"].nunique())