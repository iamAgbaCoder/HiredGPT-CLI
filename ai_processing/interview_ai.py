from openai import OpenAI
import requests
from config import Client
import re
from decouple import config
import json

from .utils import parse_interview_data

# Function to extract questions
def extract_questions(text):
    pattern = r"\d+\.\s\*\*(.*?)\*\*\:\s(.*)"
    matches = re.findall(pattern, text)
    print(matches)
    return {q: desc for q, desc in matches}

def prompt(role, keywords, job_desc):

    # INTERVIEW_PROMPT = f"""
    # You are an AI-powered job interview simulator designed to assess candidates applying for the role of {role}.
    # Your job is to ask relevant interview questions, evaluate responses, and provide constructive feedback.
    #
    # 🔹 Context:
    # The job description for this role states:
    # '{job_desc}'
    #
    # 🔹 Instructions:
    # 1. Generate **5-7 interview questions** tailored to the role.
    #    - Include **behavioral** questions (STAR method: Situation, Task, Action, Result).
    #    - Include **technical** questions based on the required **skills and experience**.
    #    - Ensure relevance to the following **keywords**: {keywords}.
    #
    # 2. For each response, **evaluate the candidate** based on:
    #    - Clarity: How well they explain their answer.
    #    - Relevance: Whether their response aligns with the job role.
    #    - Depth: How detailed and insightful their response is.
    #    - Technical Accuracy: (if applicable) correctness of their explanation.
    #
    # 3. Provide AI-powered feedback:
    #    - Highlight strengths in the answer.
    #    - Suggest improvements for a better response.
    #    - If the response is weak, provide a **better example** of how to answer.
    #
    # """

    INTERVIEW_PROMPT = f"""
        You are an AI interview simulator assessing candidates for the role of {role}.
        Based on the job description: '{job_desc}' and keywords: {keywords}, generate **5-7 tailored questions**, including:
        - **Behavioral** (STAR method)
        - **Technical** (skills & experience)

        For each response, evaluate:
        - **Clarity** (well-explained?)
        - **Relevance** (aligned with role?)
        - **Depth** (insightful & detailed?)
        - **Technical Accuracy** (if applicable)

        Provide AI-powered feedback:
        - Highlight strengths
        - Suggest improvements
        - Offer an ideal response if needed
    """

    # INTERVIEW_PROMPT = f"""
    #     You are an AI interview simulator assessing candidates for the role of {role}.
    #     Based on the job description: '{job_desc}' and keywords: {keywords}, generate 5-7 tailored questions, including:
    #     - Behavioral (STAR method)
    #     - Technical (skills & experience)
    #
    #     For each response, evaluate:
    #     - Clarity (well-explained?)
    #     - Relevance (aligned with role?)
    #     - Depth (insightful & detailed?)
    #     - Technical Accuracy (if applicable)
    #
    #     Provide AI-powered feedback:
    #     - Highlight strengths
    #     - Suggest improvements
    #     - Offer an ideal response if needed
    # """
    import requests

    # Replace with your OpenRouter API key
    # API_KEY = 'your_openrouter_api_key'
    API_URL = 'https://openrouter.ai/api/v1/chat/completions'

    # Define the headers for the API request
    headers = {
        'Authorization': f'Bearer {config("OPENAI_SECRET_KEY")}',
        'Content-Type': 'application/json'
    }

    # Define the request payload (data)
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [{"role": "user", "content": INTERVIEW_PROMPT}]
    }

    # Send the POST request to the DeepSeek API
    response = requests.post(API_URL, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        body = response.json()
        print(body)
        with open("files/api_response.json", "w") as file:
            # file.write(str(body))
            # file.close()
            json.dump(body, file, indent=4)

        db = body["choices"][0]["message"]["content"]
        parsed_data = parse_interview_data(db)
        print("Parsed Data Below:")
        print(parsed_data)
        return parsed_data

    else:
        print("Failed to fetch data from API. Status Code:", response.status_code)
    #     try:
    #     completion = Client.chat.completions.create(
    #         model="gpt-4o",
    #         messages=[{"role": "system", "content": INTERVIEW_PROMPT}],
    #         max_tokens=500,
    #         temperature=0.7
    #     )
    #     # print(completion)
    #     result = completion.choices[0].message.content  # Extract response
    #     print(result)
    #     response = extract_questions(result)
    #     return response
    # except Exception as e:
    #     return f"⚠️ API Error: {str(e)}"
    #
    # # completion = Client.chat.completions.create(
    # #   model="openai/gpt-4o",
    # #   messages=[
    # #     {
    # #       "role": "user",
    # #       "content": INTERVIEW_PROMPT
    # #     }
    # #   ]
    # # )
    # # return (completion.choices[0].message.content)
