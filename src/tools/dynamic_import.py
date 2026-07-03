import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from src.translation import _

if TYPE_CHECKING:
    from src.tools import ColorfulConsole


def get_base_dir() -> Path:
    """
    获取基础目录
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.parent / "_internal"
    else:
        return Path(__file__).resolve().parent.parent.parent


def load_objects_from_external_py(
    file_name: str, object_names: list[str], console: "ColorfulConsole"
) -> dict:
    """
    从外部未打包的 .py 文件中读取多个指定对象，并以字典形式返回。
    :param file_name: 外部 .py 文件名 (例如 'other.py')
    :param object_names: 需要读取的对象名列表
    :param console: 彩色控制台输出实例，用于打印提示信息
    :return: 包含读取到的对象的字典 {对象名: 对象值}
    """
    base_dir = get_base_dir()
    file_path = base_dir / file_name

    if not file_path.exists():
        console.info(_("加密参数代码文件不存在！"))
        return {}

    # 1. 动态加载 .py 文件为模块
    spec = importlib.util.spec_from_file_location("external_dynamic_module", file_path)
    if spec is None or spec.loader is None:
        console.error(_("加密参数代码文件加载失败！"))
        return {}

    module = importlib.util.module_from_spec(spec)

    # 2. 执行模块代码
    spec.loader.exec_module(module)

    return {
        obj_name: getattr(module, obj_name)
        for obj_name in object_names
        if hasattr(module, obj_name)
    }


if __name__ == "__main__":
    from src.tools import ColorfulConsole

    print(
        load_objects_from_external_py(
            file_name="encipher.py",
            object_names=[
                "ABogus",
                "XBogus",
                "XGnarly",
            ],
            console=ColorfulConsole(),
        )
    )
