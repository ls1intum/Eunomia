def generate_classification_prompt(subject, body):
    classification_prompt = [
        {"role": "system", "content":
            "You are an email classifier for a university study counseling service. Your task is to classify emails "
            "as 'sensitive' or 'non-sensitive' based on their content."
         },
        {"role": "user", "content": f"Email Subject: {subject}\n\nEmail Body:\n{body}"},
    ]
    return classification_prompt


def generate_study_program_classification_prompt(message, study_programs):
    prompt = [
        {"role": "system", "content": "You are an assistant that classifies questions based on study programs."},
        {"role": "user", "content": f"""
        Given the following question: "{message}", please determine if it is specific to any of the following study programs:
        {study_programs}.

        If the question is specific to one of the study programs, respond with the name of the program. If it is general and 
        not specific to any, respond with 'general'. 
        Do not explain or justify your decision. Respond with only the category. Return exactly one study program. 
        Answer with the name of the program exactly as written above. If the program is mentioned without specifying whether 
        it is a master's or bachelor's program, strip this specification from the name.

        Additionally, determine the language of the question and return both answers in the following JSON format:
        {{
            "language": "<language-of-question>",
            "study_program": "<study-program-of-question>"
        }}.
        """}
    ]
    return prompt
