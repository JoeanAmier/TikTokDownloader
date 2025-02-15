from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def find_python_files(dir_, file):
    with open(file, "w", encoding="utf-8") as f:
        for py_file in dir_.rglob("*.py"):  # 递归查找所有 .py 文件
            f.write(str(py_file) + "\n")  # 写入文件路径


# 设置源目录和输出文件
source_directory = ROOT.joinpath("src")  # 源目录
output_file = "py_files.txt"  # 输出文件名

find_python_files(source_directory, output_file)
print(f"所有 .py 文件路径已保存到 {output_file}")
