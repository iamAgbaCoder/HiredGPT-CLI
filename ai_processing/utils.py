import re
import json
import os
from datetime import datetime



def get_ordinal_suffix(day):
    """
    The get_ordinal_suffix() function is used to add the
    ordinal suffix (st, nd, rd, th) to the day of the month.
    """
    if day in [1, 21, 31]:
        return "st"
    elif day in [2, 22]:
        return "nd"
    elif day in [3, 23]:
        return "rd"
    else:
        return "th"

def custom_datetime_format():
    """Get the current date and format it as desired"""
    now = datetime.now()
    current_date = now.strftime("%A %d") + get_ordinal_suffix(now.day) + ", " + now.strftime("%B %Y")
    current_time = now.strftime("%I:%M %p")  # Get the time in 12-hour format
    return f"{current_date} at {current_time}"


def db_save(data: dict, filename="files/interview_results.json"):
    """Saves interview results to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_db(file_path="files/interview_results.json"):
    """Loads existing interview results to avoid overwriting."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}



def parse_interview_data(results):
    """Extracts questions, ideal answers, strengths, and improvements from raw text."""
    questions = re.findall(r"\d+\.\s\*\*(.*?)\*\*", results)
    ideal_answers = re.findall(r"(?<=\*\*Ideal Response:\*\*\s)(.*?)(?=\n\n---|\n\n###|\Z)", results, re.DOTALL)
    strengths = re.findall(r"\*\*Strengths\*\*:\s*(.*?)\n", results)
    raw_improvements = re.findall(r"(?<=\*\*Improvements:\*\*\s)(.*?)(?=\n\n-|\n\n###|\Z)", results, re.DOTALL)

    # raw_improvements_text = str(raw_improvements) # "\n".join(raw_improvements)
    print(ideal_answers)
    print("")
    print(raw_improvements)
    print("")
    # Regex pattern to keep only the "Suggest" statements and remove "Ideal Response" parts
    pattern = r'^(Suggest.*?)(?:\s*- \*\*Ideal Response:\*\*.*)?$'

    cleaned_improvements = [re.sub(pattern, r'\1', text, flags=re.DOTALL) for text in raw_improvements]
    print(cleaned_improvements)

    interview_data = []
    for i in range(len(questions)):
        interview_data.append({
            "question": questions[i].strip(),
            "ideal_answer": ideal_answers[i].strip() if i < len(ideal_answers) else None,
            "strengths": strengths[i].strip() if i < len(strengths) else None,
            "improvements": cleaned_improvements[i].strip() if i < len(cleaned_improvements) else None
        })
    # print(interview_data)
    return interview_data


# with open("../files/api_response.json", "r") as file:
#
#     try:
#         results = json.load(file)
#         # print(results, type(results))
#         # print(results["choices"][0]["message"]["content"])
#         parse_interview_data(results["choices"][0]["message"]["content"])  # Only call this if JSON decoding is successful
#     except json.JSONDecodeError as e:
#         print(f"JSON decoding error: {e}")
