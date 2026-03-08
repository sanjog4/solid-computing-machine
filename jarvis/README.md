# JARVIS (Windows Local AI Assistant)

## Features
- Voice assistant using `speechrecognition` + `pyttsx3`
- PC control tools:
  - Open applications
  - Close applications
  - Take screenshots
  - Search files
- Telegram bot control with `python-telegram-bot`
- Autonomous task planning via OpenAI (with fallback planner)
- Read PDF, image, and text files
- Trading journal analytics via `pandas`

## Run
```bash
python -m jarvis.main --mode cli
python -m jarvis.main --mode voice
python -m jarvis.main --mode telegram
```

## Environment variables
- `OPENAI_API_KEY` for autonomous planning
- `TELEGRAM_BOT_TOKEN` for Telegram mode
- `TELEGRAM_CHAT_ID` optional allowlist for a specific chat

## Command examples
- `open notepad`
- `close notepad.exe`
- `screenshot desktop`
- `search files C:\\Users\\Me\\Documents | invoice`
- `read file C:\\Users\\Me\\Documents\\notes.txt`
- `analyze journal C:\\Users\\Me\\Documents\\trading_journal.csv`
- `plan Build me a Python dashboard for portfolio risk`
