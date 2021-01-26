import json


def write_json_dict(input_dict, file_name):
    with open(file_name, 'w') as f:
        json.dump(input_dict, f, indent=2)
        f.close()


def read_json(file_path):
    with open(file_path, 'r') as f:
        val_dict = json.load(f)
        f.close()
        return val_dict


def write_file(file_path, input_text):
    with open(file_path, 'w') as f:
        f.write(input_text)
