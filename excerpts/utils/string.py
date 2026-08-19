import re


def slugify(string: str) -> str:
    """
    Convert a string into a URL-safe slug. The `string` param should be 200 or less chars.
    Example:
      "My initial string" -> "my-initial-string"
    """
    if len(string) > 200:
        raise ValueError("String must be less than 200 characters in length")

    slug = re.sub(pattern=r"[^a-z0-9]+", repl="-", string=string.strip().lower())
    return slug.strip("-")
