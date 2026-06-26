from collections import defaultdict

events: dict[str, dict[str, str | None]] = defaultdict(dict)

_EXPLICIT = {"relevant", "irrelevant"}
_PASSIVE = {"preview", "download"}


def add_event(event: dict) -> None:
    query_text = event.get("query_text", "")
    pdf_id = event.get("pdf_id", "")
    event_type = event.get("event_type", "")
    if not query_text or not pdf_id or not event_type:
        return
    current = events[query_text].get(pdf_id)
    if event_type == current and event_type in _EXPLICIT:
        events[query_text][pdf_id] = None
        return
    if event_type in _PASSIVE and current in _EXPLICIT:
        return
    events[query_text][pdf_id] = event_type


def get_events() -> dict[str, list[tuple[str, str]]]:
    return {
        query: [(pdf_id, action) for pdf_id, action in docs.items() if action]
        for query, docs in events.items()
        if any(action for action in docs.values())
    }
