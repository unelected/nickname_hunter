import importlib.util
import pyfiglet

from pathlib import Path
from importlib.machinery import ModuleSpec
from types import ModuleType


def get_info() -> None:
    logo: str = get_logo()
    module: ModuleType | None = get_version()
    print_data(logo, module)
    return None

def get_version() -> ModuleType | None:
    version_file = Path("./version.py")
    spec: ModuleSpec | None = importlib.util.spec_from_file_location("version", version_file)
    if isinstance(spec, ModuleSpec) and spec.loader:
        module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None

def get_logo() -> str:
    ascii_banner: str = pyfiglet.figlet_format("Nickname Hunter", font = "slant")
    return ascii_banner

def print_data(logo: str, module: ModuleType | None) -> None:
    if isinstance(module, ModuleType):
        print(f"{logo}\nversion: {module.__version__}")
    else:
        print(logo)
    print(f"\n")
    return None

