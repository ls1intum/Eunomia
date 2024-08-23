def generate_classification_prompt(subject, body):
    classification_prompt = [
        {"role": "system", "content": "You are a binary classifier."},
        {"role": "user",
         "content": "Classify the following email from a student of the Technical University of Munich ("
                    "TUM) to the study counseling service into sensitive and non-sensitive categories. 'Sensitive' "
                    "emails include those that require a study counselor to take action, involve complex issues, "
                    "or contain personal/sensitive information. 'Non-sensitive' emails are those that can be "
                    "addressed through general information or do not require counselor intervention"
                    "Do not explain your decision or try to justify it. Respond with only the category"},
        {"role": "user", "content": f"""
    Email:
    {body}
        """}
    ]
    return classification_prompt
