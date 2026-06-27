#--- coding:utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 2024-11-13
# install_pyaedt_gui.py
# PyAEDT Panel Installer — Standardized GUI (Windows-only, Python 3.10+)
# ⚠️ DO NOT MODIFY — GENERATED from ansys.aedt.core_pannel_plan_std.md v1.2

#检测oDesktop是否存在于运行环境，如果存在获取aedt的路径，使用aedt自带的python重新运行这个脚本,然后退出，需要兼容python2.7
import os
import sys
Module = sys.modules['__main__']
if hasattr(Module, "oDesktop"):
    import subprocess
    oDesktop = getattr(Module, "oDesktop")
    relaunched_flag = "PYAEDT_GUI_RELAUNCHED"

    # Always exit AEDT-side process after relaunch handling.
    if os.environ.get(relaunched_flag) != "1":
        script_path = os.path.abspath(__file__) if "__file__" in globals() else os.path.abspath(sys.argv[0])
        python_candidates = []

        try:
            exe_dir = os.path.normpath(oDesktop.GetExeDir())
            # Typical AEDT path: ...\v261\AnsysEM\Win64
            ansysem_dir = os.path.dirname(exe_dir)
            version_dir = os.path.dirname(ansysem_dir)

            python_candidates.append(os.path.join(
                ansysem_dir, "commonfiles", "CPython", "3_10", "winx64", "Release", "python", "python.exe"
            ))
            # Fallback when exe_dir depth is different.
            python_candidates.append(os.path.join(
                version_dir, "AnsysEM", "commonfiles", "CPython", "3_10", "winx64", "Release", "python", "python.exe"
            ))
        except Exception:
            python_candidates = []

        for py_exe in python_candidates:
            if os.path.exists(py_exe):
                env = os.environ.copy()
                env[relaunched_flag] = "1"
                return_code = subprocess.call([py_exe, script_path], env=env)
                raise SystemExit(return_code)

        raise RuntimeError("Detected AEDT environment, but AEDT bundled python.exe was not found.")

    raise SystemExit(0)


try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, StringVar, BooleanVar
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    from Tkinter import StringVar, BooleanVar

import threading
try:
    import queue
except ImportError:
    import Queue as queue
import time
import io

appPath = os.path.abspath(__file__) if "__file__" in globals() else os.path.abspath(sys.argv[0])
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)

# Import shared utilities
if sys.version_info[0] < 3:
    messagebox.showerror("Python Version Error", "Python 3.10 or newer is required outside AEDT bootstrap.")
    sys.exit(1)

try:
    from refactor_utils import create_venv, install_pyaedt_online, install_pyaedt_from_wheel, add_pyaedt_to_aedt
except ImportError as e:
    messagebox.showerror("Import Error", "Failed to import refactor_utils:\n{}\n\nMake sure this file is in the same folder as refactor_utils.py.".format(e))
    sys.exit(1)


# --- Utility Functions ---

def find_aedt_roots():
    """Scan os.environ for AnsysEM_ROOT* or ANSYSEM_ROOT* keys and return {version: path} dict.
    Matches both 'AnsysEM_ROOT241' and 'ANSYSEM_ROOT232' (case-insensitive).
    Extracts 3-digit version suffix from any key ending in \d{3}.
    Returns dict sorted by version descending (newest first)."""
    import re
    roots = {}
    for key, value in os.environ.items():
        # Match keys ending with exactly 3 digits: AnsysEM_ROOT241, ANSYSEM_ROOT232, etc.
        match = re.search(r'(AnsysEM_ROOT|ANSYSEM_ROOT|ansysEM_root|ansysem_root)(\d{3})$', key, re.IGNORECASE)
        if match:
            version = match.group(2)
            if os.path.isdir(value):
                roots[version] = value
    # Sort by version descending: '241' > '232'
    return dict(sorted(roots.items(), key=lambda x: x[0], reverse=True))


def get_personal_lib_path():
    """Returns Documents\\Ansoft\\PersonalLib path (Windows only)."""
    return os.path.join(os.path.expanduser("~"), "Documents", "Ansoft", "PersonalLib")


def get_aedt_python_exe(aedt_root):
    """Resolve AEDT bundled CPython path for venv creation."""
    aedt_root = os.path.normpath(str(aedt_root))

    # AnsysEM_ROOT* usually points to .../vXXX/AnsysEM, but keep fallback for .../vXXX.
    candidates = [
        os.path.join(aedt_root, "commonfiles", "CPython", "3_10", "winx64", "Release", "python", "python.exe"),
        os.path.join(aedt_root, "AnsysEM", "commonfiles", "CPython", "3_10", "winx64", "Release", "python", "python.exe"),
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    raise IOError(
        "AEDT bundled python.exe not found. Checked:\n- "
        + "\n- ".join(candidates)
    )


# --- Main GUI App ---
class PyAEDTInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyAEDT Installer v1.2")
        self.root.geometry("750x700")
        self.root.resizable(True, True)

        # --- Variables ---
        self.aedt_versions = find_aedt_roots()
        self.selected_version = StringVar()
        self.install_mode = StringVar(value="online")  # 'online' or 'offline'
        self.wheel_path = StringVar(value="")
        self.overwrite_venv = BooleanVar(value=True)  # default checked
        self.status_text = StringVar(value="Ready")
        self.progress_value = tk.DoubleVar(value=0.0)

        # Queue for thread-safe UI updates
        self.ui_queue = queue.Queue()
        self.log_queue = queue.Queue()

        # --- Build UI ---
        self._build_ui()
        self._start_ui_updater()
        self._start_log_updater()

    def _build_ui(self):
        # Main padding frame
        main_frame = ttk.Frame(self.root, padding="20")  # ✅ Optimized padding
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # ✅ Make columns 1 & 2 expandable
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        # ✅ Let log row (8) expand vertically
        main_frame.grid_rowconfigure(8, weight=1)

        # Title
        title = ttk.Label(
            main_frame,
            text="PyAEDT Panel Installer",
            font=("Segoe UI", 14, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 24))

        # AEDT Version Selection
        ttk.Label(
            main_frame,
            text="AEDT Version:",
            font=("Segoe UI", 10)
        ).grid(row=1, column=0, sticky=tk.W, pady=(0, 12))

        if self.aedt_versions:
            # Populate dropdown with sorted versions
            version_list = list(self.aedt_versions.keys())
            self.selected_version.set(version_list[0])  # default newest
            version_combo = ttk.Combobox(
                main_frame,
                textvariable=self.selected_version,
                values=version_list,
                state="readonly",
                width=10
            )
            version_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(0, 12))
        else:
            # Warning label
            warn_label = ttk.Label(
                main_frame,
                text="⚠ No AEDT installations detected via environment variables.",
                foreground="red",
                font=("Segoe UI", 10, "bold")
            )
            warn_label.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=(0, 12))

        # Installation Mode
        ttk.Label(
            main_frame,
            text="Installation Mode:",
            font=("Segoe UI", 10)
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 12))

        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=(0, 12))

        ttk.Radiobutton(
            mode_frame,
            text="Online Install (Internet)",
            variable=self.install_mode,
            value="online",
            command=self._on_mode_change
        ).pack(anchor=tk.W)

        ttk.Radiobutton(
            mode_frame,
            text="Offline Install (ZIP Package)",
            variable=self.install_mode,
            value="offline",
            command=self._on_mode_change
        ).pack(anchor=tk.W, pady=(5, 0))

        # ZIP File Selection (only for offline)
        zip_frame = ttk.Frame(main_frame)
        zip_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 12))

        ttk.Label(
            zip_frame,
            text="PyAEDT Wheel (.zip):",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W)

        self.zip_entry = ttk.Entry(
            zip_frame,
            textvariable=self.wheel_path,
            width=50,
            state="disabled"
        )
        self.zip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(5, 0))

        self.browse_btn = ttk.Button(
            zip_frame,
            text="Browse...",
            command=self._browse_wheel,
            state="disabled"
        )
        self.browse_btn.pack(side=tk.RIGHT, padx=(5, 0), pady=(5, 0))

        # PersonalLib Path Display
        ttk.Label(
            main_frame,
            text="PersonalLib Path:",
            font=("Segoe UI", 10)
        ).grid(row=4, column=0, sticky=tk.W, pady=(0, 12))

        personal_lib = get_personal_lib_path()
        lib_label = ttk.Label(
            main_frame,
            text=str(personal_lib),
            wraplength=550,
            anchor="w",
            justify="left",
            font=("Consolas", 9)
        )
        lib_label.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 12))

        # Checkbox: Overwrite Virtual Environment
        self.overwrite_check = ttk.Checkbutton(
            main_frame,
            text="Overwrite Virtual Environment (delete & rebuild in virtual environment root)",
            variable=self.overwrite_venv
        )
        self.overwrite_check.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 24))

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=(12, 0))

        ttk.Button(
            btn_frame,
            text="Cancel",
            width=12,
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=(12, 0))

        self.install_btn = ttk.Button(
            btn_frame,
            text="Install",
            width=12,
            command=self._start_install
        )
        self.install_btn.pack(side=tk.RIGHT)

        # Progress Bar
        ttk.Label(
            main_frame,
            text="Progress:",
            font=("Segoe UI", 10)
        ).grid(row=7, column=0, sticky=tk.W, pady=(24, 5))

        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_value,
            mode="determinate",
            length=590
        )
        self.progress_bar.grid(row=7, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(24, 5))

        # Log Window
        ttk.Label(
            main_frame,
            text="Log:",
            font=("Segoe UI", 10)
        ).grid(row=8, column=0, sticky=tk.W, pady=(24, 8))

        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(24, 8))
        # ✅ Make log frame expandable in both directions
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # ✅ Responsive Text widget — no fixed width, uses pack(fill=X, expand=True)
        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap=tk.NONE,
            font=("Consolas", 8),
            state="disabled"
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)

        # Status Bar
        status_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=1)
        status_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(12, 0))
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_text,
            padding=5
        )
        status_label.pack(anchor=tk.W)

        # Initialize mode UI
        self._on_mode_change()

        # Focus first interactive widget
        if self.aedt_versions:
            version_combo.focus()
        else:
            self.install_btn.focus()

    def _on_mode_change(self):
        """Enable/disable ZIP controls based on selected mode."""
        mode = self.install_mode.get()
        state = "normal" if mode == "offline" else "disabled"
        self.zip_entry.config(state=state)
        self.browse_btn.config(state=state)

    def _browse_wheel(self):
        """Open ZIP file dialog (only .zip files)."""
        path = filedialog.askopenfilename(
            title="Select PyAEDT Wheel (.zip)",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if path:
            self.wheel_path.set(path)

    def _validate_inputs(self):
        """Returns empty string on success, error message on failure."""
        if not self.aedt_versions:
            return "No AEDT installations found. Please set AnsysEM_ROOT* environment variables."

        ver = self.selected_version.get()
        if not ver or ver not in self.aedt_versions:
            return "Please select a valid AEDT version."

        if self.install_mode.get() == "offline":
            wheel = self.wheel_path.get().strip()
            if not wheel:
                return "Please select a PyAEDT wheel (.zip) file."
            if not os.path.exists(wheel):
                return "Wheel file not found: {}".format(wheel)
            if not wheel.lower().endswith(".zip"):
                return "Selected file must be a .zip archive."

        return ""  # OK

    def _start_install(self):
        """Start installation in background thread."""
        # Validate
        err = self._validate_inputs()
        if err:
            messagebox.showwarning("Validation Error", err)
            return

        # Disable UI
        # self.install_btn.config(state="disabled")
        # self.overwrite_check.config(state="disabled")
        self._set_status("Initializing...")

        # Start background thread
        self.install_thread = threading.Thread(target=self._run_install)
        self.install_thread.daemon = True
        self.install_thread.start()
        # self.install_btn.config(state="enabled")

    def _run_install(self):
        """Long-running install logic — runs in thread."""
        try:
            # --- Step 1: Prepare paths ---
            # Cross-platform venv root: ~/.pyaedt_env/3_10 (Linux/macOS), %APPDATA%\.pyaedt_env\3_10 (Windows)
            if os.name == "nt":
                venv_root = os.path.join(os.environ["APPDATA"], ".pyaedt_env", "3_10")
            else:
                venv_root = os.path.join(os.path.expanduser("~"), ".pyaedt_env", "3_10")
            personal_lib = get_personal_lib_path()
            aedt_ver = self.selected_version.get()
            aedt_root = self.aedt_versions[aedt_ver]
            aedt_python_exe = get_aedt_python_exe(aedt_root)

            # --- Step 2: Create virtual environment ---
            self._set_status("Creating virtual environment...")
            self._update_progress(10)
            self._log_append("[INFO] Creating virtual environment...")
            if self.overwrite_venv.get():
                if os.path.exists(venv_root):
                    import shutil
                    shutil.rmtree(venv_root, ignore_errors=True)
            # Use selected AEDT version bundled CPython to create .pyaedt_env.
            if not os.path.exists(os.path.join(venv_root, "Scripts", "python.exe")):
                self._log_append("[INFO] Using AEDT {} Python: {}".format(aedt_ver, aedt_python_exe))
                create_venv(venv_root, python_exe=str(aedt_python_exe))

            # --- Step 3: Install PyAEDT ---
            if self.install_mode.get() == "online":
                self._set_status("Installing PyAEDT online...")
                self._update_progress(40)
                self._log_append("[INFO] Installing PyAEDT online...")
                install_pyaedt_online(venv_root)
            else:
                wheel = self.wheel_path.get()
                self._set_status("Installing PyAEDT from {}...".format(os.path.basename(wheel)))
                self._update_progress(40)
                self._log_append("[INFO] Installing PyAEDT from {}...".format(os.path.basename(wheel)))
                install_pyaedt_from_wheel(venv_root, wheel)

            # --- Step 4: Register panels ---
            self._set_status("Registering PyAEDT panels...")
            self._update_progress(70)
            self._log_append("[INFO] Registering PyAEDT panels...")
            add_pyaedt_to_aedt(personal_lib=personal_lib)

            # --- Done ---
            self._set_status("✅ PyAEDT installed and registered")
            self._update_progress(100)
            self._log_append("[SUCCESS] PyAEDT installation completed successfully.")
            self.ui_queue.put(("success", "Success", "PyAEDT has been installed and registered for AEDT {}.\n\nTo use it:\n• Restart Ansys Electronics Desktop\n• Open any project → look for 'PyAEDT' tab in Automation panel".format(aedt_ver)))

        except Exception as e:
            error_msg = str(e)
            if "Failed to" in error_msg:
                error_msg = error_msg.split("Failed to", 1)[1].strip()
            self._set_status("❌ Error: {}".format(error_msg))
            self._update_progress(0)
            self._log_append("[ERROR] {}: {}".format(type(e).__name__, error_msg))
            self.ui_queue.put(("error", "Installation Failed", "{}: {}".format(type(e).__name__, error_msg)))

    def _start_ui_updater(self):
        """Poll UI queue and update widgets safely."""
        try:
            while True:
                msg = self.ui_queue.get_nowait()
                if msg[0] == "success":
                    _, title, body = msg
                    messagebox.showinfo(title, body)
                elif msg[0] == "error":
                    _, title, body = msg
                    messagebox.showerror(title, body)
                self.ui_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._start_ui_updater)

    def _start_log_updater(self):
        """Poll log queue and append to Text widget safely."""
        try:
            while True:
                line = self.log_queue.get_nowait()
                self.log_text.config(state="normal")
                self.log_text.insert(tk.END, line + "\n")
                self.log_text.see(tk.END)
                self.log_text.config(state="disabled")
                self.log_queue.task_done()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._start_log_updater)

    def _log_append(self, text):
        """Thread-safe log appender."""
        self.log_queue.put(text)

    def _set_status(self, text):
        """Thread-safe status setter."""
        self.status_text.set(text)
        self.root.update_idletasks()

    def _update_progress(self, value):
        """Thread-safe progress update."""
        self.progress_value.set(value)
        self.root.update_idletasks()

def main():
    # Python version guard
    if sys.version_info < (3, 10):
        messagebox.showerror("Python Version Error", "Python 3.10 or newer is required.")
        sys.exit(1)

    # Launch GUI
    root = tk.Tk()
    app = PyAEDTInstallerGUI(root)
    root.mainloop()


# --- Entry Point ---
if __name__ == "__main__":

    # Python version guard
    if sys.version_info < (3, 10):
        messagebox.showerror("Python Version Error", "Python 3.10 or newer is required.")
        sys.exit(1)

    # Launch GUI
    root = tk.Tk()
    app = PyAEDTInstallerGUI(root)
    root.mainloop()
