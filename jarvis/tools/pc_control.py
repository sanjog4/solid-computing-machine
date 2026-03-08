from __future__ import annotations

import os
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import pyautogui
except Exception:  # pragma: no cover - optional dependency
    pyautogui = None  # type: ignore


class PCController:
    def __init__(self, screenshot_dir: str = "jarvis_screenshots") -> None:
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def open_application(self, app_path_or_name: str) -> str:
        try:
            if os.path.isfile(app_path_or_name):
                os.startfile(app_path_or_name)  # type: ignore[attr-defined]
            else:
                subprocess.Popen([app_path_or_name], shell=True)
            return f"Opened: {app_path_or_name}"
        except Exception as exc:
            return f"Failed to open '{app_path_or_name}': {exc}"

    def close_application(self, process_name: str) -> str:
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", process_name],
                check=True,
                capture_output=True,
                text=True,
            )
            return f"Closed: {process_name}"
        except subprocess.CalledProcessError as exc:
            return f"Failed to close '{process_name}': {exc.stderr.strip() or exc.stdout.strip()}"

    def take_screenshot(self, label: str = "screenshot") -> str:
        if pyautogui is None:
            return "pyautogui is not installed; screenshot unavailable."
        filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = self.screenshot_dir / filename
        image = pyautogui.screenshot()
        image.save(path)
        return str(path)

    def search_files(self, root_path: str, keyword: str, limit: int = 20) -> list[str]:
        matches: list[str] = []
        root = Path(root_path)
        if not root.exists():
            return [f"Path not found: {root_path}"]

        for file in root.rglob("*"):
            if file.is_file() and keyword.lower() in file.name.lower():
                matches.append(str(file))
                if len(matches) >= limit:
                    break
        return matches
