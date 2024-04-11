"""Provides a widget that shows package information."""

##############################################################################
# Python imports.
from typing import Any, Iterator
from pkg_resources import parse_requirements

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Markdown

##############################################################################
# Rich imports.
from rich.console import RenderableType

##############################################################################
# Local imports.
from ..data import Package, PackageURL


##############################################################################
class Title(Label):
    """A title for an item of package information."""

    DEFAULT_CSS = """
    Title {
        background: $panel-lighten-3;
        text-style: bold;
        width: 100%;
    }
    """
    """The defaults styles."""

    def __init__(self, text: str) -> None:
        """Initialise the title.

        Args:
            text: The title.
        """
        super().__init__(f"{text}:")


##############################################################################
class Value(Label):
    """A value for an item of package information."""

    DEFAULT_CSS = """
    Value {
        background: $panel;
        padding-bottom: 1;
        width: 100%;

        &.none {
            color: $text-muted;
        }
    }

    """
    """The default styles."""

    def __init__(self, value: RenderableType, *args: Any, **kwargs: Any) -> None:
        """Initialise the value.

        Args:
            value: The value.
        """
        super().__init__(
            value or "None", *args, classes=("none" if not value else ""), **kwargs
        )


##############################################################################
class URL(Markdown):
    """A URL for an item of package information."""

    DEFAULT_CSS = """
    URL {
        background: $panel;
        margin: 0;
    }
    """

    def __init__(self, url: str) -> None:
        """Initialise the URL.

        Args:
            url: The URL.
        """
        super().__init__(f"<{url}>" if url else "*None*")


##############################################################################
class PackageURLData(Vertical):
    """Widget for displaying data about a package URL."""

    DEFAULT_CSS = """
    PackageURLData {
        height: auto;
        border: solid $accent;
        background: $panel;
    }
    """

    def __init__(self, url: PackageURL, *args: Any, **kwargs: Any) -> None:
        """Initialise the package URL widget.

        Args:
            url: The package URL to display the data for.
        """
        super().__init__(*args, **kwargs)
        self._url = url

    @staticmethod
    def digests(digest_data: dict[str, str]) -> Iterator[Title | Value]:
        """Generate the widgets for displaying digest items.

        Args:
            digest_data: The digest data for the URL.

        Yields:
            The widgets for displaying the data.
        """
        for name, value in digest_data.items():
            yield Title(name)
            yield Value(value)

    def compose(self) -> ComposeResult:
        """Compose the package URL display.

        Returns:
            The package URL data layout.
        """
        yield Title("URL")
        yield URL(self._url.url)
        yield Title("Package Type")
        yield Value(self._url.packagetype)
        yield Title("Python Version")
        yield Value(self._url.python_version)
        yield Title("Size")
        yield Value(f"{self._url.size:,}")
        yield Title("MD5 Digest")
        yield Value(self._url.md5_digest)
        yield Title("Uploaded")
        yield Value(self._url.upload_time_iso_8601)
        yield Title("Has Signature")
        yield Value("Yes" if self._url.has_sig else "No")
        yield Title("Downloads")
        yield Value(f"{self._url.downloads:,}")
        yield Title("Comments")
        yield Value(self._url.comment_text)
        yield from self.digests(self._url.digests)
        yield Title("Yanked")
        yield Value("Yes" if self._url.yanked else "No")
        yield Title("Yanked Reason")
        yield Value(self._url.yanked_reason)


##############################################################################
class PackageInfo(VerticalScroll):
    """Widget for displaying package information."""

    DEFAULT_CSS = """
    PackageInfo {
        border: tall $background;
        height: 1fr;
        padding: 0 1;

        &:focus {
            border: tall $accent;
        }

        Label.error {
            color: red;
            text-style: bold;
        }
    }
    """

    @staticmethod
    def project_urls(urls: dict[str, str]) -> Iterator[Title | URL]:
        """Generate title/URL widgets from the project's URLs.

        Args:
            urls: The project URLs.

        Yields:
            A title or a URL.
        """
        for title, url in urls.items():
            yield Title(title)
            yield URL(url)

    @staticmethod
    def package_urls(urls: list[PackageURL]) -> Iterator[Title | PackageURLData]:
        """Create the display of the given URLs.

        Args:
           urls: The URLs to display.

        Yields:
           Title and PackageURLData widgets.
        """
        for package in urls:
            yield Title(package.filename)
            yield PackageURLData(package)

    @staticmethod
    def _perhaps_include(title: str, value: Any, widget: type[Value] | type[URL] | type[Markdown] | type[PackageURLData]):
        if value is None or (isinstance(value, str) and not value):
            return
        yield Title(title)
        yield widget(value)     # TODO: Clean up typing.

    async def show(self, package_name: str) -> None:
        """Show the package information for the given package.

        Args:
            package_name: The name of the package to lookup and show
        """

        # Don't bother trying to do anything if there isn't actually a name.
        if not package_name.strip():
            return

        # Clear any previous content.
        await self.remove_children()

        # Download the data for the package.
        found, package = await Package.from_pypi(package_name)

        # If we found it...
        if found:
            widgets: list[Widget] = []
            for title, value, display in (
                    ("Name", package.name, Value),
                    ("Version", package.version, Value),
                    ("Summary", package.summary, Value),
                    ("URL", package.package_url, URL),
                    ("Author", package.author, Value),
                    ("Email", package.author_email, Value),
                    ("Bug Track URL",package.bugtrack_url, URL),
                    ("Classifiers", "\n".join(package.classifiers), Value),
                    (
                        "Description",
                        package.description,
                        Markdown
                        if package.description_content_type == "text/markdown"
                        else Value
                    ),
                    ("Documentation URL", package.docs_url, URL),
                    ("Download URL", package.download_url, URL),
                    ("Homepage", package.homepage, URL),
                    ("Keywords", ", ".join(package.keywords), Value),
                    ("License", package.license, Value),
                    ("Maintainer", package.maintainer, Value),
                    ("Email", package.maintainer_email, Value),
                    ("Platform", package.platform, Value),
                    ("Project URL", package.project_url, URL),
                    *(
                        (title, value, URL) for title, value in package.project_urls.items()
                    ),
                    ("Release URL", package.release_url, URL),
                    (
                        "Requires",
                        ", ".join(
                            f"[@click=screen.lookup('{pkg.project_name}')]{pkg.project_name}[/]"
                            for pkg in parse_requirements(package.requires_dist)
                        ),
                        Value
                    ),
                    ("Yanked", "Yes" if package.yanked else "No", Value),
                    ("Yanked Reason", package.yanked_reason, Value),
                    *(
                        (package.filename, package, PackageURLData)
                        for package in package.urls
                    )
            ):
                widgets.extend(list(self._perhaps_include(title, value, display)))
            await self.mount(*widgets)
        else:
            # Report that we didn't find it.
            await self.mount(Label("Not found", classes="error"))


### package_info.py ends here
