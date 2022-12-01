"""Provides a class for getting data for a PyPi package."""

##############################################################################
# Python imports.
from typing    import NamedTuple, Any
from functools import partial

##############################################################################
# httpx imports.
import httpx

##############################################################################
def _get( payload: dict[ str, dict[ str, Any ] ], via: str, value: str, default: Any="" ) -> Any:
    """Get some data, default if it isn't there or is `None`.

    Args:
        payload (dict[ str, dict[ str, Any ] ]): The payload from the API.
        via (str): The child collection to get the value via.
        value (str): The value to get.
        default (Any, optional): The default to use.

    Returns:
        Any: The value found, or the default.

    Note:
        The default is used if `value` can't be found, or if it is `None`.
    """
    return default if (
        result := payload.get( via, {} ).get( value )
    ) is None else result

##############################################################################
class PackageURL( NamedTuple ):
    """A package's release URL data."""

    comment_text: str
    """str: The comment text for the URL."""

    digests: dict[ str, str]
    """dict[ str, str ]: The digests for the URL."""

    downloads: int
    """int: The number of downloads for the URL."""

    filename: str
    """str: The filename for the URL."""

    has_sig: bool
    """bool: Does the URL have a signature?"""

    md5_digest: str
    """str: The MD5 digest for the URL."""

    packagetype: str
    """str: The type of package."""

    python_version: str
    """str: The version of package for this URL."""

    size: int
    """int: The size of the download at this URL."""

    upload_time_iso_8601: str
    """str: The upload time of the URL in ISo 8601 format."""

    url: str
    """str: The URL itself."""

    yanked: bool
    """bool: Has this URL been yanked?"""

    yanked_reason: str
    """str: The reason for the yank, if the URL has been yanked."""

    @classmethod
    def from_json( cls, data: dict[ str, Any ] ) -> "PackageURL":
        """Get package URL information from the given data.

        Args:
            data (dict[ str, Any ]): The URL data.

        Returns:
            PackageURL: An instance of a `PackageURL` class.
        """
        url = partial( _get, { "url": data }, "url" )
        return cls(
            comment_text         = url( "comment_text" ),
            digests              = url( "digests", {} ),
            downloads            = url( "downloads", 0 ),
            filename             = url( "filename" ),
            has_sig              = url( "has_sig", False ),
            md5_digest           = url( "md5_digest" ),
            packagetype          = url( "packagetype" ),
            python_version       = url( "python_version" ),
            size                 = url( "size", 0 ),
            upload_time_iso_8601 = url( "upload_time_iso_8601" ),
            url                  = url( "url" ),
            yanked               = url( "yanked", False ),
            yanked_reason        = url( "yanked_reason" )
        )

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

    urls: list[ PackageURL ]
    """list[ URL ]: The URLs for this package."""

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

            # Get the package's data from the API.
            resp = await client.get(
                f"https://pypi.org/pypi/{package}/json", follow_redirects=True
            )

            # Extract the main payload data.
            data = resp.json()

            # Create the function to get the main package information.
            info = partial( _get, data, "info" )

            # TODO: Do this in a less-monolothic way.
            return resp.status_code == httpx.codes.OK, cls(
                author                   = info( "author" ),
                author_email             = info( "author_email" ),
                bugtrack_url             = info( "bugtrack_url" ),
                classifiers              = info( "classifiers", [] ),
                description              = info( "description" ),
                description_content_type = info( "description_content_type" ),
                docs_url                 = info( "docs_url" ),
                download_url             = info( "download_url" ),
                homepage                 = info( "homepage" ),
                keywords                 = info( "keywords" ).split(),
                license                  = info( "licence" ),
                maintainer               = info( "maintainer" ),
                maintainer_email         = info( "maintainer_email" ),
                name                     = info( "name" ),
                package_url              = info( "package_url" ),
                platform                 = info( "platform" ),
                project_url              = info( "project_url" ),
                project_urls             = info( "project_urls", {} ),
                release_url              = info( "release_url" ),
                requires_dist            = info( "requires_dist", [] ),
                requires_python          = info( "requires_python" ),
                summary                  = info( "summary" ),
                version                  = info( "version" ),
                yanked                   = info( "yanked", False ),
                yanked_reason            = info( "yanked_reason" ),
                urls                     = [
                    PackageURL.from_json( url ) for url in data.get( "urls", [] )
                ]
            )

### package.py ends here
