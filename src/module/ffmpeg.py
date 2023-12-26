from pathlib import Path
from platform import system
from shutil import which
from subprocess import Popen

__all__ = ["FFMPEG"]


class FFMPEG:
    def __init__(self, path: str):
        self.path = self.__check_ffmpeg_path(Path(path))
        self.state = bool(self.path)
        self.command, self.shell = self._check_system_type()

    @staticmethod
    def _check_system_type():
        if (s := system()) == "Darwin":  # macOS
            return ['open', '-a', 'Terminal'], False
        elif s == "Windows":  # Windows
            return ['start', 'cmd', '/k'], True
        elif s == "Linux":  # Linux
            return ['x-terminal-emulator'], False

    def __check_ffmpeg_path(self, path: Path):
        # return None  # 调试使用
        return self.__check_system_ffmpeg() or self.__check_system_ffmpeg(path)

    def download(self, data: list[tuple], proxies, timeout, user_agent):
        for u, p in data:
            command = self.__generate_command(
                u, p, proxies, timeout, user_agent)
            Popen(command, shell=self.shell)

    def __generate_command(
            self,
            url,
            file,
            proxies,
            timeout,
            user_agent) -> str:
        command = self.command.copy()
        command.extend([
            self.path,
            "-hide_banner",
            "-log_level", "error",
            "-protocol_whitelist", "rtmp,crypto,file,http,https,tcp,tls,udp,rtp",
            "-fflags", "+discardcorrupt",
            "-timeout", f"{timeout * 1000 * 1000}",
            "-user_agent", f'"{user_agent}"',
            "-i", f'"{url}"',
            "-bufsize", "5120k",
            "-map", "0",
            "-c:v", "copy",
            "-c:a", "copy",
            "-sn", "-dn",
            "-reconnect_delay_max", "15",
            "-reconnect_streamed", "-reconnect_at_eof",
            "-max_muxing_queue_size", "64",
            "-correct_ts_overflow", "1",
        ])
        if proxies:
            for insert_index, item in enumerate(
                    ("-http_proxy", proxies), start=len(self.command) + 2):
                command.insert(insert_index, item)
        command.append(f'"{file}"')
        # print(" ".join(command))  # 调试使用
        return " ".join(command)

    @staticmethod
    def __check_system_ffmpeg(path: Path = None):
        return which(path or "ffmpeg")
