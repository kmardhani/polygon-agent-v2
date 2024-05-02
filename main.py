import sys
from polygon_agent_v2 import polygon_agent

agent = polygon_agent.PolygonAgent()

while True:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    question = input("Ask question or type q to quit> ")
    if question == "q" or question == "Q":
        sys.exit(0)

    summary = agent.initiate_session(question=question)
    print(f"Summary: {summary}")
