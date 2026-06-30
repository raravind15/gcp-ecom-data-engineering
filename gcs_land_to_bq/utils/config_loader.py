import yaml

def load_yaml_config(entity_name):

    config_file_path = f"{entity_name}.yaml"

    with open(config_file_path, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config