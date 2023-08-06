from . import constants


def parse(art: str) -> str:
    """Parse ASCII art and return the message.

    Args:
        art (str): ASCII art to parse

    Returns:
        str: message

    Examples:
        .. code:: python

            >>> parse(".##..\n#..#.\n#..#.\n####.\n#..#.\n#..#.")
            'A'
    """
    message = ""
    ncol = len(art.splitlines()[1])
    nchar = ncol // 5
    for i in range(nchar):
        s = "\n".join(
            "".join(c for c in line.strip()[i * 5 : (i * 5 + 5)])
            for line in art.splitlines()
        )
        for k, v in constants.ASCII_LETTERS.items():
            if s == v:
                message += k
    return message
