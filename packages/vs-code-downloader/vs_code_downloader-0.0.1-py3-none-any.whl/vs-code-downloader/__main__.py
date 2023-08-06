
# -*- coding: utf-8 -*-
import sys
import getopt
from .code_downloader import download, CONF, DownloadException


VERSION = '0.0.1'


def print_help():
    print(f"""
    python3 -m vs-code-downloader [options]

    Options:
    -h    --help        Print this message.
    -o    --os          One of the following, if not present, will check you system and find a most suitable one.
                            Mac 10.11+:                         darwin-universal
                            Mac 10.11+ Intel Chip:              darwin
                            Mac 10.11+ Apple Silicon:           darwin-arm64

                            Windwos 32bit:                      win32
                            Windows X64:                        win32-x64
                            Windows ARM:                        win32-arm64

                            Ubuntu/Debian X64:                  linux-deb-x64
                            Ubuntu/Debian ARM64:                linux-deb-arm64
                            Ubuntu/Debian ARM:                  linux-deb-armhf

                            Red Hat/Fedora/SUSE/CentOS X64:     linux-rpm-x64
                            Red Hat/Fedora/SUSE/CentOS ARM64:   linux-rpm-arm64
                            Red Hat/Fedora/SUSE/CentOS ARM:     linux-rpm-armhf

                            .tar.gz X64:                        linux-x64
                            .tar.gz ARM64:                      linux-arm64
                            .tar.gz ARM:                        linux-armhf
    -b    --build       Accept `stable` or `insider`, default is `stable`
    -d    --dir         Which folder you want to save the file, default is the current work directory
    -n    --filename    If you want to save his file in a specified name, default the filename in server is used
    -c    --cdn         Wich cdn you want to use, default is {CONF.CDN_URL}
    """)


def update_progress(real_url, downloaded, total):
    progress = float(downloaded) / float(total)
    text = f"Downloading code from [{real_url}]: {round(progress * 100)}%({downloaded}/{total})\r"
    print(text, end='')


def main(argv):
    try:
        opts = getopt.getopt(argv, "v:h:o:b:c:d:n:",
                             ["version=", "help=", "os=", "build=", "cdn=", "dir=", "filename="])[0]
        vscode_os = None
        vscode_build = None
        cdn_url = None
        dir = None
        filename = None
        for opt, val in opts:
            if opt in ('-o', '--os'):
                vscode_os = val
            elif opt in ('-b', '--build'):
                vscode_build = val
            elif opt in ('-c', '--cdn'):
                cdn_url = val
            elif opt in ('-d', '--dir'):
                dir = val
            elif opt in ('-n', '--filename'):
                filename = val

        try:
            download(folder=dir, filename=filename, code_os=vscode_os, code_build=vscode_build, cdn_url=cdn_url, on_progress=update_progress)
            print("")
        except DownloadException as e:
            print(f"Download error!: {e}")
    except Exception:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
