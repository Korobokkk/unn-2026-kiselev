"""Fake class for testing purposes."""


class Fake:
    """A simple class that dynamically sets attributes based on a provided dictionary."""

    def __init__(self, dictionary: dict) -> None:
        """Initialize the Fake object with attributes from the provided dictionary."""
        for k, v in dictionary.items():
            setattr(self, k, v)
