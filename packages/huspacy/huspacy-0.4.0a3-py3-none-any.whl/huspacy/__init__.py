from spacy import load
from spacy.util import run_command as __run_command
import sys

__URL = "https://huggingface.co/huspacy/hu_core_news_lg/resolve/{version}/hu_core_news_lg-any-py3-none-any.whl"
__DEFAULT_VERSION = "main"


def download(version: str = __DEFAULT_VERSION):
    download_url = __URL.format(version=version)
    cmd = [sys.executable, "-m", "pip", "install"] + [download_url]
    __run_command(cmd)
