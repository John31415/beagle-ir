def hash_str(string: str) -> str:
    """Compute the md5 hash of a string. 

    Returns:
        str: Hexadecimal digits of the hash.
    """

    import hashlib

    return hashlib.md5(string.encode()).hexdigest()