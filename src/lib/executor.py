from src.lib import loader
import platform

def exec(command, args):
    try:
        profile, module = loader.load(command)
    except TypeError:
        return None
    
    if module == None:
        return None
    
    if platform.platform() in profile['requirements']['os']:
        output = module.main(profile['venv']['entry'], args)
        return output
    
    return 'unmatched os'