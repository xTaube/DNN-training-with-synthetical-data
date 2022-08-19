from collections import namedtuple


def enum(*values) -> namedtuple:
    """custom enum type"""
    return namedtuple("Enum", values)(*values)


Range = namedtuple("Range", ("min", "max"))
