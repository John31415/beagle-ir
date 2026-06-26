def action_to_score(action: str) -> float:
    """Return the numeric relevance score for a given action string.

    Args:
        action: One of 'relevant', 'irrelevant', 'download', 'preview'.

    Returns:
        A float score. Unknown actions return 0.0.
    """

    action_scores: dict[str, float] = {
        "relevant": +1.0,
        "irrelevant": -1.0,
        "download": +0.5,
        "preview": +0.3,
    }

    return action_scores.get(action, 0.0)
