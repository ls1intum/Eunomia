def generate_classification_prompt(subject, body):
    classification_prompt = [
        {"role": "system", "content":
            "You are an email classifier for a university study counseling service. Your task is to classify emails "
            "as 'sensitive' or 'non-sensitive' based on their content."
         },
        {"role": "user", "content": f"Email Subject: {subject}\n\nEmail Body:\n{body}"},
    ]
    return classification_prompt


def generate_study_program_classification_prompt(message, study_prorgams):
    prompt = [
        {"role": "system", "content": "You are an assistant that classifies questions based on study programs."},
        {"role": "user", "content": f"""
        Given the following question: "{message}", please determine if it is specific to any of the following study programs:
        {study_prorgams}.

        If it is specific to one of the study programs, respond with the name of the program. If it is general and 
        not specific to any, respond with 'general'. 
        Do not explain your decision or try to justify it. Respond with only the category. Do not return multiple programs.
        Answer exactly with the name of the program as written above. If you can not specify whether it is master or bachelor, 
        strip the program of that specification. 
        """}

    ]
    return prompt
