import re


def strip_special_characters(some_string: str) -> str:
    """Remove all special characters, punctuation, and spaces from a string"""
    # Input: "Special $#! characters   spaces 888323"
    # Output: 'Specialcharactersspaces888323'
    result = ''.join(e for e in some_string if e.isalnum())
    return result


def chomp(string: str) -> str:
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", "")
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


def chomp_keep_single_spaces(string: str) -> str:
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    result = string.replace("\n", " ")  # Convert line ends to spaces
    result = re.sub(" [ ]*", " ", result)  # Truncate multiple spaces to single space
    result = result.replace(" ", " ")  # Replace weird spaces with regular spaces
    result = result.replace(u"\xa0", u" ")  # Remove non-breaking space
    result = re.sub("^[ ]*", "", result)  # Clean start
    return re.sub("[ ]*$", "", result)  # Clean end


def parse_text_for_url(string: str) -> str:
    return re.search("(?P<url>https?://[^\s'\"]+)", string).group("url")
