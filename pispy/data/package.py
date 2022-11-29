"""Provides a class for getting data for a PyPi package."""

##############################################################################
# Python imports.
from typing import NamedTuple, Any

##############################################################################
# httpx imports.
import httpx

##############################################################################
class Package( NamedTuple ):
    """A Package in PyPi."""

    author: str
    """str: The author of the package."""

    author_email: str
    """str: The email address of the author."""

    bugtrack_url: str
    """str: The URL for the package's bug tracker."""

    classifiers: list[ str ]
    """list[ str ]: The list of classifiers for the package."""

    description: str
    """str: The description for the package."""

    description_content_type: str
    """str: The content type of the description."""

    docs_url: str
    """str: The URL for the packages documentation."""

    download_url: str
    """str: The URL to download the package."""

    homepage: str
    """str: The homepage for the package."""

    keywords: list[ str ]
    """list[ str ]: The keywords for the package."""

    license: str
    """str: The licence for the package."""

    maintainer: str
    """str: The name of the maintainer of the package."""

    maintainer_email: str
    """str: The email address of the maintainer of the package."""

    name: str
    """str: The name of the package."""

    package_url: str
    """str: The URL for the package."""

    platform: str
    """str: The platform for the package."""

    project_url: str
    """str: The URL of the project for the package."""

    project_urls: dict[ str, str ]
    """dict[ str, str ]: The URLs for the project associated with the package."""

    release_url: str
    """str: The URL of the latest release of the package."""

    requires_dist: list[ str ]
    """list[ str ]: The requirements for the distribution of the package."""

    requires_python: str
    """str: The version of Python required for the package."""

    summary: str
    """str: The summary of the package."""

    version: str
    """str: The version of the package."""

    yanked: bool
    """bool: Has the package been yanked?"""

    yanked_reason: str
    """str: The reason for the yank, if the package has been yanked."""

    @classmethod
    async def from_pypi( cls, package: str ) -> tuple[ bool, "Package" ]:
        """Get information on the given package from PyPi.

        Args:
            package (str): The name of the package to get data for.

        Returns:
            tuple[ bool, Package ]: A flag to say if the package was found
                and package data.
        """

        async with httpx.AsyncClient() as client:

            resp = await client.get(
                f"https://pypi.org/pypi/{package}/json", follow_redirects=True
            )

            data = resp.json()
            def _info( value: str, default: Any ) -> Any:
                """Get some info, default if it isn't there or is `None`."""
                return default if (
                    result := data.get( "info", {} ).get( value )
                ) is None else result

            # TODO: Do this in a less-monolothic way.
            return resp.status_code == httpx.codes.OK, cls(
                author                   = _info( "author", "" ),
                author_email             = _info( "author_email", "" ),
                bugtrack_url             = _info( "bugtrack_url", "" ),
                classifiers              = _info( "classifiers", [] ),
                description              = _info( "description", "" ),
                description_content_type = _info( "description_content_type", "" ),
                docs_url                 = _info( "docs_url", "" ),
                download_url             = _info( "download_url", "" ),
                homepage                 = _info( "homepage", "" ),
                keywords                 = _info( "keywords", "" ).split(),
                license                  = _info( "licence", "" ),
                maintainer               = _info( "maintainer", "" ),
                maintainer_email         = _info( "maintainer_email", "" ),
                name                     = _info( "name", "" ),
                package_url              = _info( "package_url", "" ),
                platform                 = _info( "platform", "" ),
                project_url              = _info( "project_url", "" ),
                project_urls             = _info( "project_url", {} ),
                release_url              = _info( "release_url", {} ),
                requires_dist            = _info( "requires_dist", [] ),
                requires_python          = _info( "requires_python", "" ),
                summary                  = _info( "summary", "" ),
                version                  = _info( "version", "" ),
                yanked                   = _info( "yanked", False ),
                yanked_reason            = _info( "yanked_reason", "" )
            )

### package.py ends here
