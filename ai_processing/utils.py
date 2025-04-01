import re
import json



def parse_interview_data(results):
    """Extracts questions, ideal answers, strengths, and improvements from raw text."""
    questions = re.findall(r"\d+\.\s\*\*(.*?)\*\*", results)
    ideal_answers = re.findall(r"(?<=\*\*Ideal Response:\*\*\s)(.*?)(?=\n\n---|\n\n###|\Z)", results, re.DOTALL)
    strengths = re.findall(r"\*\*Strengths\*\*:\s*(.*?)\n", results)
    raw_improvements = re.findall(r"(?<=\*\*Improvements:\*\*\s)(.*?)(?=\n\n-|\n\n###|\Z)", results, re.DOTALL)

    # raw_improvements_text = str(raw_improvements) # "\n".join(raw_improvements)

    # Regex pattern to keep only the "Suggest" statements and remove "Ideal Response" parts
    pattern = r'^(Suggest.*?)(?:\s*- \*\*Ideal Response:\*\*.*)?$'

    cleaned_improvements = [re.sub(pattern, r'\1', text, flags=re.DOTALL) for text in raw_improvements]

    # # Print the cleaned list
    # print(cleaned_improvements[7])


    interview_data = []
    for i in range(len(questions)):
        interview_data.append({
            "question": questions[i].strip(),
            "ideal_answer": ideal_answers[i].strip() if i < len(ideal_answers) else None,
            "strengths": strengths[i].strip() if i < len(strengths) else None,
            "improvements": cleaned_improvements[i].strip() if i < len(cleaned_improvements) else None
        })
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
