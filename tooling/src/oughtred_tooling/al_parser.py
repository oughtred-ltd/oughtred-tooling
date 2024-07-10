from functools import cache
import os
from pprint import pprint
import logging
import toml

def is_api_type(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'APIGroup =' in line:
                    return True
    except Exception as e:
        logging.debug(f"Error checking API type for file {file_path}: {e}")
    return False

def parse_al_file(file_path):
    details = {
        'APIGroup': '',
        'EntityName': '',
        'SourceTableView': '',
        'fields': []
    }
    in_layout = False
    in_repeater = False
    field_buffer = None  # Buffer to hold field information between lines

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            line = line.strip()

            # Capture APIGroup, EntityName, and SourceTable
            if 'APIGroup =' in line:
                details['APIGroup'] = line.split('=')[1].strip().strip("';")
            elif 'EntityName =' in line:
                details['EntityName'] = line.split('=')[1].strip().strip("';")
            elif 'SourceTableView =' in line:
                details['SourceTableView'] = line.split("=", 1)[1].strip()

            # Handle the layout and repeater sections
            if 'layout' in line:
                in_layout = True
            elif in_layout and 'repeater' in line:
                in_repeater = True
            elif in_layout and in_repeater and '}' in line:
                if 'repeater' in line:
                    in_repeater = False
                    field_buffer = None  # Clear buffer when leaving repeater
                elif 'area' in line or 'layout' in line:
                    in_layout = False

            # Process fields within repeater
            if in_layout and in_repeater:
                if 'field(' in line:
                    field_id = line.split(';')[0].split('(')[1].strip()
                    field_buffer = {'id': field_id}
                elif 'Caption =' in line and field_buffer:
                    field_caption = line.split('=')[1].strip().strip("';")
                    field_buffer['name'] = field_caption
                    details['fields'].append(field_buffer)
                    field_buffer = None  # Reset buffer after capturing complete field data

    except Exception as e:
        logging.debug(f"Error processing file {file_path}: {e}")

    return details

def process_directory(directory, print : bool = False, save : str = None):
    all_details = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.al'):
                full_path = os.path.join(root, file)
                file_name = os.path.basename(file).replace('.al', '')
                file_name = file_name[3:-5]
                if not is_api_type(full_path):
                    continue

                details = parse_al_file(full_path)
                all_details[file_name] = details
                
    if print:
        pprint(toml.dumps(all_details))
    
    if save:
        with open(save, 'w') as f:
            toml.dump(all_details, f)

    return all_details


@cache
def load_toml():
    try:
        with open("API_ENDPOINTS.toml") as f:
            apis = toml.load(f)
    except Exception as e:
        logging.debug(f"Error loading API_ENDPOINTS.toml: {e}")
        apis = {}
    return apis

def query_apis(query):
    for table, details in load_toml().items():
        if eval(query, {
            "table" : table.lower(), 
            "tableN" : table,
            **details
        }):
            yield table, details

