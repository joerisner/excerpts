import pytest

from excerpts.utils.string import slugify


def test_slugify_success() -> None:
    string = "My 2nd Cool sTrInG!\n"
    slugified = slugify(string)

    assert slugified == "my-2nd-cool-string"


def test_slugify_raises_on_long_string() -> None:
    string_pass = str("a" * 200)
    string_fail = str("a" * 201)

    assert isinstance(slugify(string_pass), str)

    with pytest.raises(ValueError, match="String must be less than 200 characters in length"):
        slugify(string_fail)
