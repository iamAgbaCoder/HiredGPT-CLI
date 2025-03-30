from openai import OpenAI
import requests
from config import Client

def prompt(role, keywords, job_desc):

    INTERVIEW_PROMPT = f"""
    You are an AI-powered job interview simulator designed to assess candidates applying for the role of {role}.
    Your job is to ask relevant interview questions, evaluate responses, and provide constructive feedback.

    🔹 Context:
    The job description for this role states:
    '{job_desc}'

    🔹 Instructions:
    1. Generate **5-7 interview questions** tailored to the role.
       - Include **behavioral** questions (STAR method: Situation, Task, Action, Result).
       - Include **technical** questions based on the required **skills and experience**.
       - Ensure relevance to the following **keywords**: {keywords}.

    2. For each response, **evaluate the candidate** based on:
       - Clarity: How well they explain their answer.
       - Relevance: Whether their response aligns with the job role.
       - Depth: How detailed and insightful their response is.
       - Technical Accuracy: (if applicable) correctness of their explanation.

    3. Provide AI-powered feedback:
       - Highlight strengths in the answer.
       - Suggest improvements for a better response.
       - If the response is weak, provide a **better example** of how to answer.

    """

    completion = Client.chat.completions.create(
      model="openai/gpt-4o",
      messages=[
        {
          "role": "user",
          "content": INTERVIEW_PROMPT
        }
      ]
    )
    return (completion.choices[0].message.content)
