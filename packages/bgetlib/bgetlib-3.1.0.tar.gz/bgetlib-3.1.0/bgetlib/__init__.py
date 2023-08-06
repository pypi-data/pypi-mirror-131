__title__ = "bgetlib"
__version__ = "3.1.0"
__description__ = "A BiliBili API library"
__source__ = "https://github.com/baobao1270/bgetlib"
__url__ = "https://bgetlib.josephcz.xyz/"
__author__ = "Joseph Chris"
__author_email__ = "joseph@josephcz.xyz"
__license__ = "MIT"

from ._api import BilibiliAPI, DownloadProgress
from ._codec import Codec
from ._utils import bv2av, av2bv
