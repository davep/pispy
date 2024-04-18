"""Provides a class for getting data for a PyPI package."""

##############################################################################
# Python imports.
from functools import partial
from re import split
from typing import Any, NamedTuple

##############################################################################
# httpx imports.
import httpx


##############################################################################
def _get(
    payload: dict[str, dict[str, Any]], via: str, value: str, default: Any = ""
) -> Any:
    """Get some data, default if it isn't there or is `None`.

    Args:
        payload: The payload from the API.
        via: The child collection to get the value via.
        value: The value to get.
        default: The default to use.

    Returns:
        The value found, or the default.

    Note:
        The default is used if `value` can't be found, or if it is `None`.
    """
    return default if (result := payload.get(via, {}).get(value)) is None else result


##############################################################################
class PackageURL(NamedTuple):
    """A package's release URL data."""

    comment_text: str
    """The comment text for the URL."""

    digests: dict[str, str]
    """The digests for the URL."""

    downloads: int
    """The number of downloads for the URL."""

    filename: str
    """The filename for the URL."""

    has_sig: bool
    """Does the URL have a signature?"""

    md5_digest: str
    """The MD5 digest for the URL."""

    packagetype: str
    """The type of package."""

    python_version: str
    """The version of package for this URL."""

    size: int
    """The size of the download at this URL."""

    upload_time_iso_8601: str
    """The upload time of the URL in ISo 8601 format."""

    url: str
    """The URL itself."""

    yanked: bool
    """Has this URL been yanked?"""

    yanked_reason: str
    """The reason for the yank, if the URL has been yanked."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "PackageURL":
        """Get package URL information from the given data.

        Args:
            data: The URL data.

        Returns:
            An instance of a `PackageURL` class.
        """
        url = partial(_get, {"url": data}, "url")
        return cls(
            comment_text=url("comment_text"),
            digests=url("digests", {}),
            downloads=url("downloads", 0),
            filename=url("filename"),
            has_sig=url("has_sig", False),
            md5_digest=url("md5_digest"),
            packagetype=url("packagetype"),
            python_version=url("python_version"),
            size=url("size", 0),
            upload_time_iso_8601=url("upload_time_iso_8601"),
            url=url("url"),
            yanked=url("yanked", False),
            yanked_reason=url("yanked_reason"),
        )


##############################################################################
class Package(NamedTuple):
    """A Package in PyPI."""

    author: str
    """The author of the package."""

    author_email: str
    """The email address of the author."""

    bugtrack_url: str
    """The URL for the package's bug tracker."""

    classifiers: list[str]
    """The list of classifiers for the package."""

    description: str
    """The description for the package."""

    description_content_type: str
    """The content type of the description."""

    docs_url: str
    """The URL for the packages documentation."""

    download_url: str
    """The URL to download the package."""

    homepage: str
    """The homepage for the package."""

    keywords: list[str]
    """The keywords for the package."""

    license: str
    """The licence for the package."""

    maintainer: str
    """The name of the maintainer of the package."""

    maintainer_email: str
    """The email address of the maintainer of the package."""

    name: str
    """The name of the package."""

    package_url: str
    """The URL for the package."""

    platform: str
    """The platform for the package."""

    project_url: str
    """The URL of the project for the package."""

    project_urls: dict[str, str]
    """The URLs for the project associated with the package."""

    release_url: str
    """The URL of the latest release of the package."""

    requires_dist: list[str]
    """The requirements for the distribution of the package."""

    requires_python: str
    """The version of Python required for the package."""

    summary: str
    """The summary of the package."""

    version: str
    """The version of the package."""

    yanked: bool
    """Has the package been yanked?"""

    yanked_reason: str
    """The reason for the yank, if the package has been yanked."""

    urls: list[PackageURL]
    """The URLs for this package."""

    @classmethod
    async def from_pypi(cls, package: str) -> tuple[bool, "Package"]:
        """Get information on the given package from PyPI.

        Args:
            package: The name of the package to get data for.

        Returns:
            A flag to say if the package was found and package data.
        """

        async with httpx.AsyncClient() as client:
            # Get the package's data from the API.
            resp = await client.get(
                f"https://pypi.org/pypi/{package}/json", follow_redirects=True
            )

            # Extract the main payload data.
            data = resp.json()

            # Create the function to get the main package information.
            info = partial(_get, data, "info")

            # TODO: Do this in a less-monolothic way.
            return resp.status_code == httpx.codes.OK, cls(
                author=info("author"),
                author_email=info("author_email"),
                bugtrack_url=info("bugtrack_url"),
                classifiers=info("classifiers", []),
                description=info("description"),
                description_content_type=info("description_content_type"),
                docs_url=info("docs_url"),
                download_url=info("download_url"),
                homepage=info("home_page"),
                keywords=split("[ ,]+", info("keywords")),
                license=info("license"),
                maintainer=info("maintainer"),
                maintainer_email=info("maintainer_email"),
                name=info("name"),
                package_url=info("package_url"),
                platform=info("platform"),
                project_url=info("project_url"),
                project_urls=info("project_urls", {}),
                release_url=info("release_url"),
                requires_dist=info("requires_dist", []),
                requires_python=info("requires_python"),
                summary=info("summary"),
                version=info("version"),
                yanked=info("yanked", False),
                yanked_reason=info("yanked_reason"),
                urls=[PackageURL.from_json(url) for url in data.get("urls", [])],
            )


### package.py ends here
