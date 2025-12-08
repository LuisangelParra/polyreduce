from typing import Any, Dict


class ProblemInstance:
    """
    Represents an instance of a decision problem.

    This base class does NOT use @dataclass to avoid field ordering issues
    in subclasses (dataclasses cannot have non-default fields after default ones).

    Subclasses are free to use @dataclass and define their own fields. 
    They should populate `self.data` inside their __post_init__() or __init__().
    """

    def __init__(self, name: str):
        self.name = name
        self.data = {}

    def __repr__(self):
        return f"ProblemInstance(name={self.name!r}, keys={list(self.data.keys())})"
