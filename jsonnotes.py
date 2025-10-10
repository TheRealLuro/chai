import json 


class user: 
    def __init__(self, user_id, username, roles):
        self.id = user_id
        self.name = username
        self.roles = roles
        self.is_active = True

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, roles={self.roles}, is_active={self.is_active})"


def demonstrate_json():
    user_data_dict = {
        "id": 101,
        "name": "Jason",
        "roles": ["viewer", "commenter"],
        "is_active": True
    }

    print(f"Original dictionary: {user_data_dict}")

    json_string = json.dumps(user_data_dict, indent=4)

    file_path = "user_data.json"

    with open(file_path, 'w') as file:
        file.write(json_string, file, indent=4)

    with open(file_path, 'r') as file:
        loaded_json = json.load(file)