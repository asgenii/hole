def main(args):
    from src.lib import downloader
    if args[0] in ['recieve', 'rcv']:
        downloader.download_command(args[1])