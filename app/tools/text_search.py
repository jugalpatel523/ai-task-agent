async def text_search(args: dict) -> str:
    """
    Free stub tool: simulates search results.
    Replace later with real search API if needed.
    """
    query = (args.get("query") or "").strip()
    if not query:
        return "No query provided."

    canned = {
        "canada qa ai trends": "Trends: AI-assisted testing, Playwright automation, contract testing, LLM test generation, observability.",
        "redis best practices": "Use TTLs, avoid huge keys, monitor memory, choose right data structures, keep payload small."
    }
    key = query.lower()
    return canned.get(key, f"Simulated search results for: '{query}'.")
