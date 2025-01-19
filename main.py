from src.agents import Agent
from src.utils import groq_client, read_json, web_scrap

user_input = str(input("Enter your query: "))
Agent(groq_client).analyze_agent(user_input)
queries = read_json(r"C:\Users\harvi\Codebases\LLMOps\Agents\agents\analyze_agent.json")

for i in range(1, len(queries) + 1):
    query_key = f'q{i}'
    content = web_scrap(queries[query_key])
    url = content['url']
    web_content = content['content']
    Agent(groq_client).surf_agent(queries[query_key], url=url, web_content=web_content)
    
    decision = read_json(r"C:\Users\harvi\Codebases\LLMOps\Agents\agents\surf_agent.json")
    if decision['decision'] == 'yes':
        information = content['content']
        response = Agent(groq_client).response_agent(user_input, information)
        print("AI response: ", response)
        break
    elif decision['decision'] == 'no':
        continue
