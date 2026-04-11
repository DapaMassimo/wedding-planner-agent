"""
Entry point for the wedding planner.

Builds the coordinator agent and starts a simple REPL loop. Each
turn is independent — no conversation memory yet (LangGraph supports
checkpointing, we'll add it when we need it).

Run with:
    uv run python -m wedding_planner.app.main
"""
import asyncio

from wedding_planner.app.coordinator import build_coordinator

async def _chat_loop() -> None:
    print("Building wedding planner... (this may take a moment to fetch MCP tools)")
    coordinator = await build_coordinator()
    print("Ready. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
    
        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            break

        result = await coordinator.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        reply = result["messages"][-1].content
        print(f"\nAssistant: {reply}\n")

def main() -> None:
    asyncio.run(_chat_loop())

if __name__ == "__main__":
    main()