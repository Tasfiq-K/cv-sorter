from src.parsers.preprocess import clean_text


def test_multiple_spaces():
    assert clean_text("Python     Docker") == "Python Docker"


def test_blank_lines():
    assert clean_text("A\n\n\n\nB") == "A\n\nB"


def test_windows_newlines():
    assert clean_text("A\r\nB") == "A\nB"


def test_trailing_spaces():
    assert clean_text("Python   \nDocker   ") == "Python\nDocker"


if __name__ == "__main__":
    test_multiple_spaces()
    test_blank_lines()
    test_windows_newlines()
    test_trailing_spaces()