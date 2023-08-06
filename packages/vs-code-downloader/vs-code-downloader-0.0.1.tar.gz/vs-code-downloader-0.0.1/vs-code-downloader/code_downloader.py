

import urllib.parse
import urllib.request
import urllib.error
import os
import sys
import platform
import subprocess


from typing import Callable
from http.client import HTTPResponse



class Conf:

    CDN_URL = "https://vscode.cdn.azure.cn"
    BUILD = 'stable'
    DOWNLOAD_URL = "https://code.visualstudio.com/sha/download"
    BUF_SIZE = 1024 * 1024


CONF = Conf()
SUPPORT_OS = ('darwin-universal', 'darwin', 'darwin-arm64',
              'win32', 'win32-x64', 'win32-arm64',
              'linux-deb-x64', 'linux-deb-arm64', 'linux-deb-armhf',
              'linux-rpm-x64', 'linux-rpm-arm64', 'linux-rpm-armhf',
              'linux-x64', 'linux-arm64', 'linux-armhf')
SUPPORT_BUILD = ('stable', 'insider')


def current_os():

    # mac
    if sys.platform == 'darwin':
        return 'darwin-universal'

    _machine = platform.machine().upper()

    # windows
    if sys.platform in ('win32', 'cygwin'):
        if _machine.find('ARM') >= 0:
            return 'win32-arm64'
        if _machine.find('64') >= 0:
            return 'win32-x64'
        else:
            return 'win32'
    with open(os.devnull, 'wb') as devnull:
        # ubuntu, debian
        if subprocess.call(['dpkg', '--version'], stderr=devnull, stdout=devnull) == 0:
            if _machine.find('ARM') >= 0:
                if _machine.find('64') >= 0:
                    return 'linux-deb-arm64'
                else:
                    return 'linux-deb-armhf'
            else:
                return 'linux-deb-x64'
        # centos, suse
        elif subprocess.call(['rpm', '--version'], stderr=devnull, stdout=devnull) == 0:
            if _machine.find('ARM') >= 0:
                if _machine.find('64') >= 0:
                    return 'linux-rpm-arm64'
                else:
                    return 'linux-rpm-armhf'
            else:
                return 'linux-rpm-x64'
        # other linux
        else:
            if _machine.find('ARM') >= 0:
                if _machine.find('64') >= 0:
                    return 'linux-arm64'
                else:
                    return 'linux-armhf'
            else:
                return 'linux-x64'


class DownloadException(Exception):

    def __init__(self, message, code: int = 500, body: str = ""):
        super(DownloadException, self).__init__(message)
        self.message = message
        self.code = code
        self.body = body


class CDNRedirector(urllib.request.HTTPRedirectHandler):

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        cdnUrl: str = newurl
        idx = cdnUrl.find(f'/{CONF.BUILD}/')
        if idx > 0:
            cdnUrl = CONF.CDN_URL + cdnUrl[idx:]

        return super().redirect_request(req, fp, code, msg, headers, cdnUrl)


def _encode_url(url: str) -> str:
    pr = urllib.parse.urlparse(url)
    path = urllib.parse.quote(pr.path, "/%")
    query = urllib.parse.quote(pr.query, "%=&")
    return urllib.parse.urlunparse((pr.scheme, pr.netloc, path, pr.params, query, pr.fragment))


def download(folder: str = "", filename: str = "", code_os: str = None, code_build: str = CONF.BUILD, cdn_url: str = CONF.CDN_URL, on_progress: Callable = None):
    _os = code_os or current_os()
    if _os not in SUPPORT_OS:
        raise DownloadException(f"{_os} is not supported, please selete one from {SUPPORT_OS}")
    _build = code_build or CONF.BUILD
    if _build not in SUPPORT_BUILD:
        raise DownloadException(f'{_build} is not supported, please selete one from {SUPPORT_BUILD}')
    _folder = folder or os.getcwd()
    CONF.CDN_URL = cdn_url or CONF.CDN_URL
    CONF.BUILD = _build
    url = f"{CONF.DOWNLOAD_URL}?build={_build}&os={_os}"
    dl_url = _encode_url(url)
    try:
        openner = urllib.request.build_opener(CDNRedirector)
        response: HTTPResponse = openner.open(dl_url, timeout=60)
        content_length = int(response.getheader("Content-Length"))
        total_download = 0
        real_url = response.geturl()
        fname = filename or os.path.basename(real_url)
        local_path = f"{_folder}/{fname}"
        with open(local_path, "wb") as local_file:
            for chunk in iter(lambda: response.read(CONF.BUF_SIZE), b''):
                total_download += len(chunk)
                if callable(on_progress):
                    on_progress(real_url, total_download, content_length)
                local_file.write(chunk)
        response.close()
        file_size = os.path.getsize(local_path)
        if content_length != file_size:
            raise DownloadException(f"download url from url {dl_url} error: file size not match")
    except DownloadException:
        raise
    except urllib.error.HTTPError as e:
        raise DownloadException(f"download url from url {dl_url}", e.code, e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise DownloadException(f"download url from url {dl_url}")
    except Exception as e:
        raise DownloadException(f"download url from url {dl_url} ")
