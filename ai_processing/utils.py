import re
import json



def parse_interview_data(results):
    """Extracts questions, ideal answers, strengths, and improvements from raw text."""
    questions = re.findall(r"\d+\.\s\*\*(.*?)\*\*", results)
    # ideal_answers = re.findall(r"\*\*Ideal Response\*\*:\s*\"(.*?)\"", results)
    ideal_answers = re.findall(r"(?<=\*\*Ideal Response:\*\*\s)(.*?)(?=\n\n---|\n\n###|\Z)", results, re.DOTALL)
    strengths = re.findall(r"\*\*Strengths\*\*:\s*(.*?)\n", results)
    improvements = re.findall(r"(?<=\*\*Improvements:\*\*\s)(.*?)(?=\n\n-|\n\n###|\Z)", results, re.DOTALL)

    # print(questions)
    # print()
    # print(ideal_answers)
    # print()
    # print(strengths)
    # print(improvements)

    # Regex pattern
    pattern = r"(?<=\*\*Improvements:\*\*\s)(.*?)(?=\n\s*\*\*Ideal Response:|\n\n-|\n\n###|\Z)" 

    # Extracting improvements
    improvements = re.findall(pattern, results, re.DOTALL)

    # Printing all extracted improvements
    for i, improvement in enumerate(improvements, 1):
        print(f"Improvement {i}: {improvement.strip()}\n")


    interview_data = []
    for i in range(len(questions)):
        interview_data.append({
            "question": questions[i].strip(),
            "ideal_answer": ideal_answers[i].strip() if i < len(ideal_answers) else None,
            "strengths": strengths[i].strip() if i < len(strengths) else None,
            "improvements": improvements[i].strip() if i < len(improvements) else None
        })

    return interview_data

with open("../files/api_response.json", "r") as file:

    try:
        results = json.load(file)
        # print(results, type(results))
        # print(results["choices"][0]["message"]["content"])
        parse_interview_data(results["choices"][0]["message"]["content"])  # Only call this if JSON decoding is successful
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
