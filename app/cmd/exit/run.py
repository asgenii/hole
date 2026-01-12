import sys
from pathlib import Path
import importlib.util

def main(target, args):
    path = Path(target).resolve()
    folder = str(path.parent)

    if folder not in sys.path:
        sys.path.insert(0, folder)

    spec = importlib.util.spec_from_file_location('run module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, 'main'):
        return module.main(args)

    return None