import json
import os

def add_slug_field(file_path):
    try:
        # Load the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Add 'slug' field to each item
        for item in data:
            if "name" in item:
                item["slug"] = item["name"].replace(" ", "-").lower()

        # Save the updated JSON back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Slug fields added successfully to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the JSON file
file_name = "output.json"
file_path = os.path.join(os.getcwd(), file_name)

add_slug_field(file_path)
