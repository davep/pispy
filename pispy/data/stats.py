"""Provides the code for getting the main PyPi stats."""

##############################################################################
# Python imports.
from typing import NamedTuple, Iterator

##############################################################################
# httpx imports.
import httpx

##############################################################################
class Package( NamedTuple ):
    """Class that holds the details of a specific package."""

    name: str
    """str: The name of the package."""

    size: int
    """int: The size of the package."""

##############################################################################
class Packages:
    """A collection of packages from the PyPi stats API."""

    def __init__( self, data: dict[ str, dict[ str, int ] ] ) -> None:
        """Initialise the packages collection from the API data.

        Args:
            data (dict[ str, dict[ str, int ] ]): The data from the API.
        """
        self._packages = sorted(
            [ Package( k, v[ "size" ] ) for k,v in data.items() ],
            key=lambda package: package.size,
            reverse=True
        )

    def __iter__( self ) -> Iterator[ Package ]:
        """Get an iterator of all the packages.

        Yields:
            Package: A package from PyPi.
        """
        return iter( self._packages )

    @classmethod
    async def top_100( cls ) -> "Packages":
        """Get the top 100 packages by size on PyPi.

        Returns:
            Packages: The package collection.
        """
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://pypi.org/stats/",
                follow_redirects = True,
                headers          = { "accept": "application/json" }
            )
            return cls( resp.json()[ "top_packages" ] )

### stats.py ends here
