from pathlib import Path
from shutil import which
from platform import system
from subprocess import Popen, run
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
