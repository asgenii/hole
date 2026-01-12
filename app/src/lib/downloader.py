from pathlib import Path
from rich.console import Console
from rich.live import Live
from etc import loader
import subprocess, zipfile, time

def download_command(name: str):
    console = Console(force_terminal=True, color_system=None)

    config = loader.yml("config.yml")
    cmdpath = Path(config["paths"]["commands"])
    tmppath = Path(config["paths"]["temp"])
    tmppath.mkdir(parents=True, exist_ok=True)
    cmdpath.mkdir(parents=True, exist_ok=True)

    pathzip = tmppath / f"{name}.zip"
    target_dir = cmdpath / name
    target_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["scp", f"storage@158.220.126.85:~/cli/repo/{name}.zip", pathzip],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    with zipfile.ZipFile(pathzip) as z:
        infos = z.infolist()
        total = sum(i.file_size for i in infos)
        console.print(f"Extracting {name}.zip ({total/1024:.1f}KB)")

        done = 0
        start = time.time()

        with Live(console=console, refresh_per_second=10) as live:
            for info in infos:
                out = target_dir / Path(*Path(info.filename).parts[1:])
                if info.is_dir():
                    out.mkdir(parents=True, exist_ok=True)
                    continue
                out.parent.mkdir(parents=True, exist_ok=True)

                with z.open(info) as src, open(out, "wb") as dst:
                    while True:
                        chunk = src.read(64*1024)
                        if not chunk:
                            break
                        dst.write(chunk)
                        done += len(chunk)

                        width = 25
                        ratio = done / total if total else 1
                        fill = int(ratio * width)
                        if fill >= width:
                            bar_str = "=" * width
                        else:
                            bar_str = "=" * fill + ">" + "-" * (width - fill - 1)

                        elapsed = time.time() - start
                        speed = done / elapsed if elapsed else 0
                        eta = int((total - done) / speed) if speed else 0

                        live.update(
                            f"  [{bar_str}] "
                            f"{done/1024:.1f}KB/{total/1024:.1f}KB "
                            f"{speed/1024:.1f}KB/s "
                            f"{eta//60}:{eta%60:02d}"
                        )

    pathzip.unlink()