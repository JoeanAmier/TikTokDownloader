from pathlib import Path
from shutil import which
from platform import system
from subprocess import Popen, run
from tempfile import NamedTemporaryFile
from textwrap import dedent

__all__ = ["FFMPEG"]


class FFMPEG:
    SYSTEM = system()

    # 常见终端及其执行模板
    linux_terminal_templates = {
        # GNOME Terminal (Ubuntu)
        "gnome-terminal": ["gnome-terminal", "--", "bash", "-c", "{cmd}; exec bash"],
        # Deepin Terminal
        "deepin-terminal": ["deepin-terminal", "--", "bash", "-c", "{cmd}; exec bash"],
        # XFCE4 Terminal (MX Linux 默认)
        "xfce4-terminal": [
            "xfce4-terminal",
            "--hold",
            "-e",
            'bash -c "{cmd}; exec bash"',
        ],
        # Konsole (KDE)
        "konsole": ["konsole", "-e", "bash", "-i", "-c", "{cmd}; bash"],
        # Terminator
        "terminator": ["terminator", "-x", "bash", "-c", "{cmd}; exec bash"],
    }

    def __init__(self, path: str):
        self.path = self.__check_ffmpeg_path(Path(path))
        self.support = {
            "Darwin": self.generate_command_darwin,
            "Linux": self.generate_command_linux,
            "Windows": self.generate_command_windows,
        }
        self.run_command = self.support.get(self.SYSTEM, None)
        self.state = bool(self.path) if self.run_command else False

    @staticmethod
    def generate_command_darwin(command: list) -> None:
        script = dedent(f"""
                tell application "Terminal"
                    do script "{" ".join(command).replace('"', '\\"')}"
                    activate
                end tell
                """)
        Popen(["osascript", "-e", script])

    @staticmethod
    def generate_command_windows(command: list) -> None:
        Popen(
            " ".join(
                [
                    "start",
                    "cmd",
                    "/k",
                ]
                + command
            ),
            shell=True,
        )

    @classmethod
    def generate_command_linux(cls, command: list) -> None:
        # TODO: Linux 系统尚未测试
        command = " ".join(command)
        print("ffmpeg command:", command)
        for term, template in cls.linux_terminal_templates.items():
            if which(term):
                # 填充命令并执行
                filled = [
                    part.format(cmd=command) if "{cmd}" in part else part
                    for part in template
                ]
                run(
                    filled,
                )

    def __check_ffmpeg_path(self, path: Path):
        return self.__check_system_ffmpeg() or self.__check_system_ffmpeg(path)

    def download(self, data: list[tuple], proxy, user_agent):
        for u, p in data:
            command = self.__generate_command(
                u,
                p,
                proxy,
                user_agent,
            )
            self.run_command(command)

    def merge_audio(
        self,
        video: str,
        music: str,
        output: str,
    ) -> tuple[bool, str]:
        """将背景音乐合并到视频文件中，音乐时长超过视频时自动截断音乐

        :param video: 视频文件路径
        :param music: 背景音乐文件路径
        :param output: 输出文件路径
        :return: (是否合并成功, 失败原因)
        """
        command = [
            self.path,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            video,
            "-i",
            music,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-af",
            "apad",
            "-shortest",
            "-movflags",
            "+faststart",
            "-f",
            "mp4",
            output,
        ]
        return self.__run_command(command)

    def __run_command(self, command: list[str]) -> tuple[bool, str]:
        try:
            result = run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError as e:
            return False, str(e)
        return result.returncode == 0, result.stderr.strip()

    def merge_music_videos(
        self,
        videos: list[str],
        music: str,
        output: str,
    ) -> tuple[bool, str]:
        """将多个视频拼接为单个视频后合并背景音乐，音乐时长超过视频时自动截断音乐

        优先使用 concat demuxer 无损拼接，视频参数不一致时回退为 concat filter 重新编码

        :param videos: 视频文件路径列表
        :param music: 背景音乐文件路径
        :param output: 输出文件路径
        :return: (是否合并成功, 失败原因)
        """
        if result := self.__merge_music_videos_concat(videos, music, output):
            return result
        return self.__merge_music_videos_filter(videos, music, output)

    def __merge_music_videos_concat(
        self,
        videos: list[str],
        music: str,
        output: str,
    ) -> tuple[bool, str] | None:
        """使用 concat demuxer 无损拼接视频并合并背景音乐

        :return: 成功返回 (True, "")；失败返回 None 以尝试其他方案
        """
        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            suffix=".txt",
            delete=False,
        ) as f:
            f.write("".join(f"file '{Path(v).as_posix()}'\n" for v in videos))
            list_file = f.name
        try:
            command = [
                self.path,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file,
                "-i",
                music,
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-af",
                "apad",
                "-shortest",
                "-movflags",
                "+faststart",
                "-f",
                "mp4",
                output,
            ]
            result = run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            return None
        finally:
            Path(list_file).unlink(missing_ok=True)
        if result.returncode == 0:
            return True, ""
        return None

    def __merge_music_videos_filter(
        self,
        videos: list[str],
        music: str,
        output: str,
    ) -> tuple[bool, str]:
        """使用 concat filter 重新编码拼接视频并合并背景音乐"""
        inputs = []
        for video in videos:
            inputs.extend(("-i", video))
        inputs.extend(("-i", music))
        command = [
            self.path,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            *inputs,
            "-filter_complex",
            "".join(f"[{i}:v]" for i in range(len(videos)))
            + f"concat=n={len(videos)}:v=1:a=0[v]",
            "-map",
            "[v]",
            "-map",
            f"{len(videos)}:a:0",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-af",
            "apad",
            "-shortest",
            "-movflags",
            "+faststart",
            "-f",
            "mp4",
            output,
        ]
        return self.__run_command(command)

    def __generate_command(
        self,
        url,
        file,
        proxy,
        user_agent,
    ) -> list:
        command = [
            self.path,
            "-hide_banner",
            "-rw_timeout",
            f"{30 * 1000 * 1000}",
            "-loglevel",
            "info",
            "-protocol_whitelist",
            "rtmp,crypto,file,http,https,tcp,tls,udp,rtp,httpproxy",
            "-analyzeduration",
            f"{10 * 1000 * 1000}",
            "-probesize",
            f"{10 * 1000 * 1000}",
            "-fflags",
            "+discardcorrupt",
            "-user_agent",
            f'"{user_agent}"',
            "-i",
            f'"{url}"',
            "-bufsize",
            "10240k",
            "-map",
            "0",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-sn",
            "-dn",
            "-reconnect_delay_max",
            "60",
            "-reconnect_streamed",
            "-reconnect_at_eof",
            "-max_muxing_queue_size",
            "128",
            "-correct_ts_overflow",
            "1",
            "-f",
            "mp4",
        ]
        if proxy:
            for insert_index, item in enumerate(("-http_proxy", proxy), start=2):
                command.insert(insert_index, item)
        command.append(f'"{file}"')
        return command

    @staticmethod
    def __check_system_ffmpeg(path: Path = None):
        return which(path or "ffmpeg")
