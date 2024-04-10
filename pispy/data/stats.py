"""Provides the code for getting the main PyPi stats."""

##############################################################################
# Python imports.
from typing import NamedTuple, Iterator

##############################################################################
# httpx imports.
import httpx


##############################################################################
class Package(NamedTuple):
    """Class that holds the details of a specific package."""

    name: str
    """The name of the package."""

    size: int
    """The size of the package."""


##############################################################################
class Packages:
    """A collection of packages from the PyPi stats API."""

    def __init__(self, data: dict[str, dict[str, int]]) -> None:
        """Initialise the packages collection from the API data.

        Args:
            data: The data from the API.
        """
        self._packages = sorted(
            [Package(k, v["size"]) for k, v in data.items()],
            key=lambda package: package.size,
            reverse=True,
        )

    def __iter__(self) -> Iterator[Package]:
        """Get an iterator of all the packages.

        Yields:
            A package from PyPi.
        """
        return iter(self._packages)


### stats.py ends here
