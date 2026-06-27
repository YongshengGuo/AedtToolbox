#--- coding:utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 2024-11-13
# refactor_utils.py
# Shared utilities for PyAEDT Windows installer (CPython-only, AEDT 2023.2+)

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union


def unzip_if_zip(path: Union[str, Path]) -> Path:
    """Unzip path if it is a ZIP file. Returns unzipped dir or original path."""
    import zipfile

    path = Path(path)
    if path.suffix.lower() != '.zip':
        return path

    unzipped_path = path.parent / path.stem
    if unzipped_path.exists():
        shutil.rmtree(unzipped_path, ignore_errors=True)

    try:
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(unzipped_path)
        return unzipped_path
    except Exception as e:
        raise RuntimeError(f"Failed to unzip {path}: {e}")


def create_venv(venv_dir: Union[str, Path], python_exe: str = sys.executable) -> None:
    """Create virtual environment using Python 3.10+ interpreter."""
    venv_dir = Path(venv_dir)
    venv_dir.parent.mkdir(parents=True, exist_ok=True)

    if venv_dir.exists() and (venv_dir/"3_10/Scripts/pip.exe").exists():
        return  # already exists

    print(f"Creating virtual environment at {venv_dir}...")
    result = subprocess.run([
        python_exe, "-m", "venv", str(venv_dir), "--clear"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to create venv: {result.stderr}")


def install_pyaedt_from_wheel(
    venv_dir: Union[str, Path],
    wheel_path: Union[str, Path],
    python_version: str = "3_10"
) -> None:
    """Install PyAEDT from local wheel (Windows, Python 3.10+, AEDT >= 2023.2)."""
    venv_dir = Path(venv_dir)
    wheel_path = Path(wheel_path)

    if not wheel_path.exists():
        raise FileNotFoundError(f"Wheel not found: {wheel_path}")

    # Resolve executables
    if os.name == "nt":
        pip_exe = venv_dir / "Scripts" / "pip.exe"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        pip_exe = venv_dir / "bin" / "pip"
        python_exe = venv_dir / "bin" / "python"

    if not pip_exe.exists():
        raise FileNotFoundError(f"pip not found in venv: {pip_exe}")

    # Unzip if needed
    unzipped_path = unzip_if_zip(wheel_path)

    # Install wheel
    print(f"Installing PyAEDT from {unzipped_path}...")
    result = subprocess.run([
        str(pip_exe),
        "install",
        "--no-cache-dir",
        "--no-index",
        f"--find-links={unzipped_path}",
        "pyaedt[all]"
    ], capture_output=False, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to install PyAEDT: {result.stderr}")


def add_pyaedt_to_aedt(
    personal_lib: Union[str, Path]
) -> None:
    """Run PyAEDT's AEDT panel installer script."""
    import tempfile
    from pathlib import Path

    personal_lib = Path(personal_lib)
    if not personal_lib.exists():
        # Create PersonalLib
        personal_lib.mkdir(parents=True, exist_ok=True)
        # raise FileNotFoundError(f"PersonalLib not found: {personal_lib}")

    # Resolve venv python.exe (cross-platform)
    if os.name == "nt":
        venv_root = Path(os.environ["APPDATA"]) / ".pyaedt_env" / "3_10"
        python_exe = venv_root / "Scripts" / "python.exe"
    else:
        venv_root = Path.home() / ".pyaedt_env" / "3_10"
        python_exe = venv_root / "bin" / "python"
    if not python_exe.exists():
        raise FileNotFoundError(f"python.exe not found in venv: {python_exe}")

    # Write installer script
    script_content = f'''
from ansys.aedt.core.extensions.installer.pyaedt_installer import add_pyaedt_to_aedt
add_pyaedt_to_aedt(personal_lib=r"{personal_lib}")
'''

    script_path = Path(tempfile.gettempdir()) / "configure_pyaedt.py"
    script_path.write_text(script_content)

    # Use venv's python.exe
    result = subprocess.run([
        str(python_exe), str(script_path)
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to register panels: {result.stderr}")

    # Cleanup
    script_path.unlink(missing_ok=True)


def install_pyaedt_online(
    venv_dir: Union[str, Path],
    python_version: str = "3_10"
) -> None:
    """Install PyAEDT online via pip (Windows, Python 3.10+, AEDT >= 2023.2)."""
    venv_dir = Path(venv_dir)

    # Resolve executables
    if os.name == "nt":
        pip_exe = venv_dir / "Scripts" / "pip.exe"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        pip_exe = venv_dir / "bin" / "pip"
        python_exe = venv_dir / "bin" / "python"

    if not pip_exe.exists():
        raise FileNotFoundError(f"pip not found in venv: {pip_exe}")

    # Install latest pyaedt[all]
    print("Installing PyAEDT online...")
    result = subprocess.run([
        str(pip_exe),
        "install",
        "--no-cache-dir",
        "pyaedt[all]"
    ], capture_output=False, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to install PyAEDT: {result.stderr}")
