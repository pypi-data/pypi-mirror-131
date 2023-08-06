import os.path
import time
import requests
from dataclasses import dataclass, field
from typing import Tuple, Optional, Callable, List


@dataclass
class DownloadProgress:
    total_bytes: int
    finished_bytes: int = field(init=False)
    left_bytes: int = field(init=False)
    percentage: float = field(init=False)
    start_at: float = field(init=False)
    finished: bool = field(init=False)

    def __post_init__(self):
        self.finished_bytes = 0
        self.left_bytes = self.total_bytes
        self.percentage = 0
        self.start_at = time.time()
        self._ticks = [self.start_at]
        self._tick_bytes = [0]
        self.finished = False

    def _update(self, finished: int) -> None:
        self.finished_bytes = finished
        self.left_bytes = self.total_bytes - finished
        self.percentage = finished / self.total_bytes
        self._ticks.append(time.time())
        self._tick_bytes.append(self.finished_bytes)

    def average_speed(self) -> float:
        total_time = self._ticks[-1] - self.start_at
        if total_time <= 0:
            return 0
        return self.finished_bytes / total_time

    def difference_speed(self) -> float:
        if len(self._ticks) < 2:
            return 0
        t = self._ticks[-1] - self._ticks[-2]
        d = self._tick_bytes[-1] - self._tick_bytes[-2]
        if t <= 0:
            return 0
        return d / t

    def smoothed_speed(self, window: int = 4) -> float:
        if len(self._ticks) < 2:
            return 0
        slice_t = self._ticks[-window:]
        slice_d = self._tick_bytes[-window:]
        sum_speed = 0
        number = len(slice_t) - 1
        for i in range(number):
            dt = slice_t[i + 1] - slice_t[i]
            dd = slice_d[i + 1] - slice_d[i]
            sum_speed += (dd / dt) if (dt > 0) else 0
        return sum_speed / number


class BilibiliAPI:
    def __init__(self, cookie_filename: Optional[str] = None) -> None:
        if cookie_filename is not None:
            import http.cookiejar as cookiejar
            self.cookies = cookiejar.MozillaCookieJar()
            self.cookies.load(cookie_filename, ignore_discard=True, ignore_expires=True)
        else:
            self.cookies = None

    def _request(self, url: str, **kwargs) -> requests.Response:
        if self.cookies is not None:
            kwargs["cookies"] = self.cookies
        return requests.get(url, **kwargs)

    def _interface_request(self, path, **kwargs) -> dict:
        return self._request("https://api.bilibili.com" + path, **kwargs).json()

    def get_favorites(self, favorite_id: int, page: int = 1) -> list:
        path = "/x/v3/fav/resource/list?media_id={}&pn={}&ps=20&order=mtime".format(favorite_id, page)
        favourites = self._interface_request(path)["data"]["medias"]
        return favourites or []

    def get_favorites_all(self, favorite_id: int) -> List[dict]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            favorites += page_favorites
            page += 1
        return favorites

    def get_favorites_since(self, favorite_id: int, from_timestamp: int) -> List[dict]:
        page = 1
        favorites = []
        while True:
            page_favorites = self.get_favorites(favorite_id, page)
            if len(page_favorites) == 0:
                break
            for v in page_favorites:
                if v.favorite_at < from_timestamp:
                    break
                favorites.append(v)
            page += 1
        return favorites

    def list_user_favourite_folders(self, uid: int) -> List[dict]:
        path = "/x/v3/fav/folder/created/list-all?up_mid={}".format(uid)
        folders = self._interface_request(path)["data"]["list"]
        return folders or []

    def get_video(self, aid: int) -> dict:
        path = "/x/web-interface/view?aid={}".format(aid)
        return self._interface_request(path)["data"]

    def get_live_danmaku(self, cid: int) -> str:
        url = "https://comment.bilibili.com/{}.xml".format(cid)
        return self._request(url).text

    def get_archive(self, category_id: int, tag_id: Optional[int] = None, page: int = 1) -> Tuple[int, List[dict]]:
        if tag_id is not None:
            path = "/x/tag/ranking/archives?ps=20&pn={}&rid={}&tag_id={}".format(page, category_id, tag_id)
        else:
            path = "/x/web-interface/newlist?ps=20&pn={}&rid={}".format(page, category_id)
        response = self._interface_request(path)
        videos = response["data"]["archives"]
        count = response["data"]["page"]["count"]
        return count, videos

    def list_stickers(self) -> List[dict]:
        path = "/x/emote/setting/panel?business=reply"
        packages = self._interface_request(path)["data"]["all_packages"]
        return packages or []

    def get_sticker(self, sticker_id: int) -> dict:
        url = "/x/emote/package?business=reply&ids={}".format(sticker_id)
        sticker = self._interface_request(url)["data"]["packages"]
        return sticker or sticker

    def get_cover_picture(self, aid) -> Tuple[str, bytes]:
        url = self.get_video(aid)["pic"]
        basename = os.path.basename(url)
        stream = requests.get(url).content
        return basename, stream

    def get_stream_url(self, aid: int, cid: int, enable_h265=True, enable_hdr=True, enable_dolby=True) -> dict:
        quality_flag = 16 | 64  # dash + 4k
        if enable_hdr:
            quality_flag = quality_flag | 64
        if enable_dolby:
            quality_flag = quality_flag | 256
        if enable_hdr or enable_dolby:
            enable_h265 = True

        path = "/x/player/playurl?avid={}&cid={}&fnver=0&fnval={}&fourk=1".format(aid, cid, quality_flag)
        stream_urls = self._interface_request(path)["data"]["dash"]
        audio_url = stream_urls["audio"][0]["baseUrl"]
        video_url = stream_urls["video"][0]["baseUrl"]
        if enable_h265:
            h265_streams = list(filter(lambda stream: stream["codecid"] == 12, stream_urls["video"]))
            if len(h265_streams) > 0:
                video_url = h265_streams[0]["baseUrl"]
        return {"audio": audio_url, "video": video_url}

    def _download(self, url: str, chunk_size: int = 8192,
                  progress_callback: Optional[Callable[[DownloadProgress], None]] = None) -> bytes:
        headers = {
            "User-Agent": "Bilibili Freedoooooom/MarkII",
            "Referer": "https://www.bilibili.com/",
            "Accept": "*/*",
            "Icy-MetaData": "1"
        }
        stream = self._request(url, headers=headers, stream=True)
        progress = DownloadProgress(total_bytes=int(stream.headers['content-length']))
        binary = bytes()
        for chunk in stream.iter_content(chunk_size=chunk_size):
            if chunk:
                binary += chunk
                progress._update(len(binary))
                if progress_callback is not None:
                    progress_callback(progress)
        progress.finished = True
        if progress_callback is not None:
            progress_callback(progress)
        return binary

    def get_audio_stream(self, aid: int, cid: int, trunk_size: Optional[int] = 8192,
                         progress_update: Optional[Callable[[DownloadProgress], None]] = None) -> bytes:
        url = self.get_stream_url(aid, cid)["audio"]
        return self._download(url, trunk_size, progress_callback=progress_update)

    def get_video_stream(self, aid: int, cid: int,
                         enable_h265=True, enable_hdr=True, enable_dolby=True, trunk_size: Optional[int] = 8192,
                         progress_update: Optional[Callable[[DownloadProgress], None]] = None) -> Tuple[bytes, bytes]:
        url = self.get_stream_url(aid, cid, enable_h265, enable_hdr, enable_dolby)
        audio = self._download(url["audio"], trunk_size, progress_callback=progress_update)
        video = self._download(url["video"], trunk_size, progress_callback=progress_update)
        return audio, video

    def audio_stream_to_file(self, aid: int, cid: int, dest: str, ffmpeg: str = "ffmpeg",
                             progress_update: Optional[Callable[[DownloadProgress], None]] = None) -> None:
        audio = self.get_audio_stream(aid, cid, progress_update=progress_update)
        from ._codec import Codec
        codec = Codec(ffmpeg)
        codec.copy_audio(audio, dest)

    def video_stream_to_file(self, aid: int, cid: int, dest: str, ffmpeg: str = "ffmpeg",
                             enable_h265=True, enable_hdr=True, enable_dolby=True,
                             progress_update: Optional[Callable[[DownloadProgress], None]] = None) -> None:
        audio, video = self.get_video_stream(aid, cid, enable_h265, enable_hdr, enable_dolby,
                                             progress_update=progress_update)
        from ._codec import Codec
        codec = Codec(ffmpeg)
        codec.merge_video(audio, video, dest)
