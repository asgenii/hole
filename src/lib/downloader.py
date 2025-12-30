from pathlib import Path
from tqdm import tqdm
from etc import loader
import subprocess, zipfile

def download_command(name: str):
    config = loader.yml('config.yml')
    cmdpath = Path(config['paths']['commands'])
    tmppath = Path(config['paths']['temp'])
    tmppath.mkdir(parents=True, exist_ok=True)
    cmdpath.mkdir(parents=True, exist_ok=True)

    pathzip = tmppath / f"{name}.zip"
    target_dir = cmdpath / name
    target_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "scp",
        f"storage@158.220.126.85:~/cli/repo/{name}.zip",
        str(pathzip)
    ], check=True)

    with zipfile.ZipFile(pathzip, "r") as z:
        members = z.namelist()
        with tqdm(total=len(members), desc=f"Extracting {name}") as pbar:
            for member in members:
                member_path = Path(member)
                if member_path.parts:
                    target_path = target_dir.joinpath(*member_path.parts[1:])
                    if member.endswith("/"):
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with z.open(member) as source, open(target_path, "wb") as target_file:
                            target_file.write(source.read())
                pbar.update(1)

    pathzip.unlink()