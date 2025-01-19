# create workflow agents as functions
# analyze_agent , surf_agent , response_agent
from src.utils import write_json
from src.templates import format_temp
import json

class Agent():
    def __init__(self, groq_client):
        self.__groq_client = groq_client

    def analyze_agent(self, query: str, prompt_temp='analysis_prompt'):
        # ip - formatted_prompt, op - 3 searching statements for surf agent
        prompt = format_temp(query, prompt_temp)
        llm_resp = self.__groq_client.chat.completions.create(
            messages=[{'role': 'system', 'content': f'{prompt}'}], model='llama-3.3-70b-versatile', temperature=0.8
        )
        statements = llm_resp.choices[0].message.content
        if statements:
            json_data = json.loads(statements)
            print("\n\n\n\nAGENT 1 DONE\n\n\n\n")
            write_json(r"C:\Users\harvi\Codebases\LLMOps\Agents\agents\analyze_agent.json", json_data)

    def surf_agent(self, query: str, url: str, web_content: str, prompt_temp='surf_prompt'):
        #ip - formatted_prompt, op - yes/no finally web information
        # print(web_content)
        # self.__prompt_temp = 'surf_summarize'
        # prompt_t = format_temp(self.__prompt_temp, web_content)
        # print("\n\n\n", prompt_t)
        # llm_resp = self.__groq_client.chat.completions.create(
        #     messages=[{'role': 'system', 'content': f'{prompt_t}'}], model='llama-3.3-70b-versatile', temperature=0.5
        # )
        # web_content = llm_resp.choices[0].message.content
        prompt = format_temp(query, prompt_temp, url, web_content)
        llm_resp = self.__groq_client.chat.completions.create(
            messages=[{'role': 'system', 'content': f'{prompt}'}], model='llama-3.3-70b-versatile', temperature=0.4
        )
        decision = llm_resp.choices[0].message.content
        if decision:
            json_data = json.loads(decision)
            print("\n\n\n\nAGENT 2 DONE\n\n\n\n")
            write_json(r"C:\Users\harvi\Codebases\LLMOps\Agents\agents\surf_agent.json", json_data)

    def response_agent(self, query: str, web_content, prompt_temp='response_prompt'):
        prompt = format_temp(query, prompt_temp, information=web_content)
        llm_resp = self.__groq_client.chat.completions.create(
            messages=[{'role': 'system', 'content': f'{prompt}'}], model='llama-3.3-70b-versatile', temperature=0.5
        )
        final_resp = llm_resp.choices[0].message.content
        print("\n\n\n\nAGENT 3 DONE\n\n\n\n")
        return final_resp