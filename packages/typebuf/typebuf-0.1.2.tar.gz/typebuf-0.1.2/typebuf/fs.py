import yaml


def load_from_yaml(filename) -> dict:
    with open(filename, 'r') as f:
        ret = yaml.safe_load(f.read())
    return ret
