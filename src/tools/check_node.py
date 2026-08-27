import shutil
import subprocess


def is_node_available(min_version: int = 18) -> bool:
    node = shutil.which("node")
    if node is None:
        return False

    try:
        version = subprocess.run(
            [node, "--version"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        major = int(version.removeprefix("v").split(".", 1)[0])
        return major >= min_version
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


if __name__ == "__main__":
    print(is_node_available())
