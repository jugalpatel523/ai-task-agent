async def db_lookup(args: dict) -> str:
    """
    Free stub tool: simulates internal DB lookups.
    Replace later with real Postgres queries if desired.
    """
    entity = (args.get("entity") or "").strip().lower()
    if not entity:
        return "No entity provided."
    demo = {
        "pricing": "Doc: Pricing module uses caching and GraphQL to reduce redundant DB calls.",
        "etl": "Doc: ETL runs nightly; incremental loads rely on timestamps + auditing."
    }
    return demo.get(entity, f"No record found for '{entity}'.")
