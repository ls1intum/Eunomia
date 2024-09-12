def generate_classification_prompt(subject, body):
    classification_prompt = [
        {"role": "system", "content": "You are a binary email classifier for a university study counseling service."},
        {"role": "user",
         "content": "Classify the following email from a student of the Technical University of Munich ("
                    "TUM) to the study counseling service into sensitive and non-sensitive categories. 'Sensitive' "
                    "emails include those that require a study counselor to take action, involve complex issues, "
                    "or contain personal/sensitive information. 'Non-sensitive' emails are those that can be "
                    "addressed through general information or do not require counselor intervention"
                    "Do not explain your decision or try to justify it. Respond with only the category"},
        {"role": "user", "content": f"Email Subject: {subject}\n\nEmail Body:\n{body}"},
        {"role": "assistant", "content": "Classify the email accordingly."}
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
