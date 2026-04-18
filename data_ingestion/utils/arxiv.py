def valid_query_arxiv(k: int) -> int:
    """Returns the lowest value greater than k that is valid for requests in arXiv.
    """
    valid_values = [25, 50, 100, 250, 500, 1000, 2000]
    for vv in valid_values:
        if k <= vv:
            return vv
    return valid_values[-1]