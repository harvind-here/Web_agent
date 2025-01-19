#load every template from the templates folder
import os
from langchain.prompts import PromptTemplate

templates_dir = r"src\templates"
templates = {}
for filename in os.listdir(templates_dir):
    file_path = os.path.join(templates_dir, filename)
    
    with open(file_path, 'r') as file:
        template_name = os.path.splitext(filename)[0]
        templates[template_name] = file.read()

def get_temp(template_name):
    if template_name in templates:
        return templates[template_name]
    else:
        print(f'{template_name} not found')
        return None

def format_temp(user_query, template_name, url='', web_content='', information=''):
    if template_name=='analysis_prompt':
        prompt = PromptTemplate(input_variables=["user_query"], template = get_temp(template_name))
        formatted_prompt = prompt.format(user_query=user_query)
        return formatted_prompt
    elif template_name=='surf_prompt' and url and web_content:
        prompt = PromptTemplate(input_variables=["user_query", "url", "web_content"], template = get_temp(template_name))
        formatted_prompt = prompt.format(user_query=user_query, url=url, web_content=web_content)
        return formatted_prompt
    elif template_name=='response_prompt' and information:
        print('template getting loaded...')
        prompt = PromptTemplate(input_variables=["user_query", "information"], template = get_temp(template_name))
        print('template file identified')
        print('info: ', information)
        formatted_prompt = prompt.format(user_query=user_query, information=information or 'no info provided')
        print("template loaded!")
        return formatted_prompt
    else:
        print(f'{template_name} not found')
    # elif template_name=='surf_summarize' and web_content:
    #     prompt = PromptTemplate(input_variables=["information"], template = get_temp(template_name))
    #     formatted_prompt = prompt.format(information=web_content)