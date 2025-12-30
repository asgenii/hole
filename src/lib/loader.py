import importlib, yaml, os

def load(command):

    if command == '':
        return None

    # profile.yml load
    found = False
    for _path in os.listdir('cmd'):
        with open(f'src/cmd/{_path}/profile.yml', 'r', encoding='utf-8') as file:
            profile = yaml.safe_load(file)
            
        if command == profile['command']['name']['general'] or command in profile['command']['name']['additional']:
            command = profile['command']['name']['general']
            found = True
            break

    # module load
    if found == False:
        return None
    
    spec = importlib.util.spec_from_file_location("run.py", f"cmd/{command}/run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return f'src/cmd/{command}/venv/{profile["venv"]["entry"]}', module