from __future__ import annotations

import argparse

from jarvis.brain.agent import JarvisAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="JARVIS-style local AI assistant for Windows")
    parser.add_argument("--mode", choices=["voice", "telegram", "cli"], default="cli")
    args = parser.parse_args()

    agent = JarvisAgent()

    if args.mode == "voice":
        agent.run_voice_loop()
    elif args.mode == "telegram":
        from jarvis.integrations.telegram_bot import JarvisTelegramBot

        JarvisTelegramBot(agent).run()
    else:
        print("JARVIS CLI mode. Type 'exit' to quit.")
        while True:
            cmd = input("jarvis> ").strip()
            if cmd.lower() in {"exit", "quit"}:
                break
            print(agent.execute_command(cmd))


if __name__ == "__main__":
    main()
