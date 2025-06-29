import json

def load_faq_data(file_path="faq_data.json"):
    with open(file_path, "r") as f:
        return json.load(f)
