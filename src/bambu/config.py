import tomllib

def read_config(fname: str):
    with open(fname, 'rb') as f:
        return tomllib.load(f)
