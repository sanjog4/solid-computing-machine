from __future__ import annotations

import os

from jarvis.brain.planner import TaskPlanner
from jarvis.tools.file_reader import FileReader
from jarvis.tools.pc_control import PCController
from jarvis.tools.trading import TradingAssistant
from jarvis.tools.voice import VoiceAssistant


class JarvisAgent:
    def __init__(self) -> None:
        self.voice = None
        self.pc = PCController()
        self.reader = FileReader()
        self.trading = TradingAssistant()
        self.planner = TaskPlanner(api_key=os.getenv("OPENAI_API_KEY"))

    def execute_command(self, command: str) -> str:
        cmd = command.strip()
        low = cmd.lower()

        if low.startswith("open "):
            return self.pc.open_application(cmd[5:].strip())
        if low.startswith("close "):
            process = cmd[6:].strip()
            if not process.lower().endswith(".exe"):
                process += ".exe"
            return self.pc.close_application(process)
        if low.startswith("screenshot"):
            label = cmd.replace("screenshot", "", 1).strip() or "screenshot"
            path = self.pc.take_screenshot(label=label.replace(" ", "_"))
            return f"Screenshot saved: {path}"
        if low.startswith("search files "):
            payload = cmd[len("search files "):]
            if "|" not in payload:
                return "Use: search files <root_path> | <keyword>"
            root_path, keyword = [p.strip() for p in payload.split("|", 1)]
            results = self.pc.search_files(root_path, keyword)
            return "\n".join(results) if results else "No matching files found."
        if low.startswith("read file "):
            return self.reader.read_file(cmd[len("read file "):].strip())
        if low.startswith("analyze journal "):
            return self.trading.analyze_journal(cmd[len("analyze journal "):].strip())
        if low.startswith("plan "):
            steps = self.planner.create_plan(cmd[len("plan "):].strip())
            return "\n".join(f"{s.id}. {s.action}" for s in steps)
        if low in {"help", "commands"}:
            return self.help_text()
        return "Unknown command. Say 'help' for supported commands."

    def run_voice_loop(self) -> None:
        if self.voice is None:
            self.voice = VoiceAssistant()
        self.voice.speak("JARVIS online. Say help for commands. Say exit to quit.")
        while True:
            try:
                spoken = self.voice.listen()
                if spoken.lower().strip() in {"exit", "quit", "stop"}:
                    self.voice.speak("Goodbye.")
                    break
                response = self.execute_command(spoken)
                self.voice.speak(response[:300])
            except Exception as exc:
                self.voice.speak(f"Error: {exc}")

    @staticmethod
    def help_text() -> str:
        return (
            "Commands:\n"
            "- open <app_or_path>\n"
            "- close <process_name>\n"
            "- screenshot [label]\n"
            "- search files <root_path> | <keyword>\n"
            "- read file <path>\n"
            "- analyze journal <csv_or_excel_path>\n"
            "- plan <goal>"
        )
