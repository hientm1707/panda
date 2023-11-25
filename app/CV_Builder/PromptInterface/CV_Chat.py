from openai import OpenAI 
import os
import re
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def generate_cv(old_cv, cv_template,job_description):
    client = OpenAI(api_key=api_key)
    system_prompt = f"You are an agent that can fill a CV template with the information from an user input old CV. You will strictly follow the format and style of the template, in other words, you should not change the layout of the template CV. Only extract relevant information from the old CV and do not add new sections, but try your best to include all existing sections in the template"
    user_prompt = f"\n\nOld CV:\n{old_cv}\n\nTemplate:\n{cv_template}, the output should only contains latex text. The style definition part of the template should be always included. Also, the wording, content selection and presentation order should be revised to better fit the job description, which is as follows: \n{job_description}\n "
    response = client.chat.completions.create(
    model="gpt-4",
    #response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    return response.choices[0].message.content

def generate_cl(job_description,cl_template,cl_instruct,old_cv):
    client = OpenAI(api_key=api_key)
    system_prompt = f"You are an agent that can write Cover letter based on the cv of an user and the job description. The format of the cover letter should be in a latex format. The template is as follows: \n{cl_template} \n The cover letter instruction is: \n{cl_instruct}"

    user_prompt = f"\n\nJob description:\n{job_description}\n\n the text extracted from the user's cv:\n{old_cv}, the output should only contains latex text. The style definition part of the template should be always included "
    response = client.chat.completions.create(
    model="gpt-4",
    #response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    return response.choices[0].message.content


def latex_verify(file_contents):
    
    pattern = r'\\documentclass.*?\\end{document}'
    match = re.search(pattern, file_contents, re.DOTALL)  # re.DOTALL allows . to match newline characters

    if match:
        return match.group()
    else:
        return None

