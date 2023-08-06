import os.path
import shutil
import uuid
from subprocess import CompletedProcess
from typing import Union, Optional


class _hndl:
    def __init__(self, source: Optional[bytes] = None, extension: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.path = self.id + ".bgetlibtmp"
        if extension is not None:
            self.path += "." + extension
        if source is not None:
            with open(self.path, "wb+") as f:
                f.write(source)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def copy(self, dest: str):
        shutil.copy(self.path, dest)

    # noinspection PyBroadException
    def close(self):
        try:
            os.remove(self.path)
        except:
            pass


class Codec:
    def __init__(self, ffmpeg_location: str = "ffmpeg") -> None:
        self.ffmpeg = ffmpeg_location

    def _run(self, args: str) -> CompletedProcess:
        cmd = '"{ffmpeg}" -y -hide_banner {args}'.format(ffmpeg=self.ffmpeg, args=args)
        import subprocess
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise Exception("ffmpeg failed with code {}".format(result.returncode))
        return result

    def merge_video(self, audio_stream: bytes, video_stream: bytes, dest: str) -> None:
        with _hndl(extension="mp4") as output, _hndl(audio_stream) as audio, _hndl(video_stream) as video:
            args = '-i "{}" -i "{}" -c copy "{}"'.format(audio.path, video.path, output.path)
            self._run(args)
            output.copy(dest)

    def copy_audio(self, audio_stream: bytes, dest: str) -> None:
        with _hndl(extension="aac") as output, _hndl(audio_stream) as audio:
            args = '-i "{}" -vn -c copy "{}"'.format(audio.path, output.path)
            self._run(args)
            output.copy(dest)

    def convert_video(self, audio_stream: bytes, video_stream: bytes, dest: str, codec: str = "mp4") -> None:
        with _hndl(extension=codec) as output, _hndl(audio_stream) as audio, _hndl(video_stream) as video:
            args = '-i "{}" -i "{}" "{}"'.format(audio.path, video.path, output.path)
            self._run(args)
            output.copy(dest)

    def convert_audio(self, audio_stream: bytes, dest: str, codec: str = "aac",
                      bitrate: Optional[int] = None, sample_rate: Optional[int] = None) -> None:
        args = " -vn"
        if bitrate is not None:
            args = " -ab {}".format(bitrate)
        if sample_rate is not None:
            args = " -ar {}".format(sample_rate)
        with _hndl(extension=codec) as output, _hndl(audio_stream) as audio:
            args = '-i "{}" {} "{}"'.format(audio.path, args, output.path)
            self._run(args)
            output.copy(dest)
