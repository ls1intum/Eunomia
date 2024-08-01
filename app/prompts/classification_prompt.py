def generate_classification_prompt(subject, body):
    classification_prompt = [
        {"role": "system", "content": "You are a binary classifier."},
        {"role": "user",
         "content": "Classify the following email from a student of the Technical University of Munich ("
                    "TUM) to the study counseling service into sensitive and non-sensitive categories. "
                    "Provide the classification and the confidence level in percentage in JSON format."
                    "Do not explain your decision or try to justify it. Adhere to the response json format that is "
                    "shown as in the example of the ResponseFormat below:"},
        {"role": "user", "content": f"""
    Email:
    {body}
    Example ResponseFormat:
    {{
      "classification": "sensitive" or "non-sensitive",
      "confidence_level": "20%"
    }}
        """}
    ]
    return classification_prompt
