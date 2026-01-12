from src.lib import loader
import platform

def exec(command, args):
    try:
        profile, module = loader.load(command)
    except TypeError:
        return None
    
    if module == None:
        return None
    
    if platform.system() in profile['requirements']['os']:
        output = module.main(f"cmd/{profile['command']['name']['general']}/venv/{profile['venv']['entry']}", args)
        return output
    
    return 'unmatched os'