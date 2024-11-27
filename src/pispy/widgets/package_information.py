"""A window for showing information on a PyPI package."""

##############################################################################
# Python imports.
from functools import singledispatch
from typing import Any, Callable, Iterator
from urllib.parse import urlparse
from webbrowser import open as visit_url

##############################################################################
# Packing imports.
from packaging.requirements import Requirement

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label, Markdown, TabbedContent, TabPane, Tabs

##############################################################################
# Backward compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..data import Package, PackageURL


##############################################################################
class Title(Label):
    """A title for an item of package information."""

    DEFAULT_CSS = """
    Title {
        background: $panel-lighten-3;
        margin-right: 1;
        text-style: bold;
        width: 1fr;
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
        margin-right: 1;
        padding-bottom: 1;
        width: 1fr;
    }
    """


##############################################################################
class URL(Label):
    """A URL for an item of package information."""

    DEFAULT_CSS = """
    URL {
        margin-right: 1;
        padding-bottom: 1;
        width: 1fr;
    }
    """

    @staticmethod
    def looks_urlish(url: str) -> bool:
        """Test if a given string looks like an actual URL.

        Args:
            url: The URL to test.

        Returns:
            `True` if it really looks like a URL, `False` if not.
        """
        return bool(urlparse(url).scheme)

    def __init__(self, url: str) -> None:
        """Initialise the URL.

        Args:
            url: The URL.
        """
        super().__init__(
            f"[@click=visit('{url}')]{url}[/]" if self.looks_urlish(url) else url
        )

    def action_visit(self, url: str) -> None:
        """Visit the given URL.

        Args:
           url: The URL to visit.
        """
        visit_url(url)


##############################################################################
@singledispatch
def maybe_show(
    title: str, value: Any, widget: Callable[[Any], Widget]
) -> Iterator[Widget]:
    """Maybe show a value with a given title.

    Args:
        title: The title for the value to show.
        value: The value to show.
        widget: The type of widget to show the value.

    Yields:
        The widgets required to show the value.
    """
    yield Title(title)
    yield widget(value)


##############################################################################
@maybe_show.register
def _(title: str, value: None, widget: Callable[[Any], Widget]) -> Iterator[Widget]:
    """Show noting when the value is `None`."""
    del title, value, widget
    yield from ()


##############################################################################
@maybe_show.register
def _(title: str, value: str, widget: Callable[[Any], Widget]) -> Iterator[Widget]:
    """Maybe show a string value."""
    if value:
        yield Title(title)
        yield widget(value)


##############################################################################
def widgets_for(*values: tuple[str, Any, Callable[[Any], Widget]]) -> Iterator[Widget]:
    """Generate the widgets needed to show the given values.

    Args:
        values: The collection of values to show.

    Yields:
        The widgets required to show the values.
    """
    for title, value, display in values:
        yield from maybe_show(title, value, display)


##############################################################################
class TabContent(VerticalScroll):
    """A wrapper for the content of a package information tab."""

    class GoLeft(Message):
        """Message to request we move left in the tabs."""

    class GoRight(Message):
        """Message to request we move right in the tabs."""

    def action_scroll_left(self) -> None:
        """Handle a request to go left."""
        self.post_message(self.GoLeft())

    def action_scroll_right(self) -> None:
        """Handle a request to go right."""
        self.post_message(self.GoRight())


##############################################################################
class PackageURLDetails(TabPane):
    """Tab pane for showing details of a package URL."""

    def __init__(self, package_url: PackageURL) -> None:
        """Initialise the object.

        Args:
            package_url: The package URL to show.
        """
        super().__init__(package_url.filename)
        self._url = package_url

    def compose(self) -> ComposeResult:
        """Compose the package URL display.

        Returns:
            The package URL data layout.
        """
        with TabContent():
            yield from widgets_for(
                ("URL", self._url.url, URL),
                ("Package Type", self._url.packagetype, Value),
                ("Python Version", self._url.python_version, Value),
                ("Size", f"{self._url.size:,}", Value),
                ("MD5 Digest", self._url.md5_digest, Value),
                ("Uploaded", self._url.upload_time_iso_8601, Value),
                ("Has Signature", "Yes" if self._url.has_sig else "No", Value),
                ("Comments", self._url.comment_text, Value),
                *((name, value, Value) for name, value in self._url.digests.items()),
                ("Yanked", "Yes" if self._url.yanked else "No", Value),
                ("Yanked Reason", self._url.yanked_reason, Value),
            )


##############################################################################
class PackageDescription(TabPane):
    """A tab pane that shows the package description."""

    def __init__(self, package: Package):
        """Initialise the package description pane."""
        super().__init__("Description")
        self._package = package

    def compose(self) -> ComposeResult:
        with TabContent():
            yield (
                Markdown
                if self._package.description_content_type == "text/markdown"
                else Value
            )(self._package.description, id="description")

    @on(Markdown.LinkClicked)
    def maybe_handle_url(self, event: Markdown.LinkClicked) -> None:
        """Maybe handle a link coming from the `Markdown` widget.

        Args:
            event: The link click event.
        """
        if URL.looks_urlish(event.href):
            visit_url(event.href)


##############################################################################
class PackageUnknown(TabPane):
    """Tab pane used to show that the package was unknown."""

    DEFAULT_CSS = """
    PackageUnknown {
        height: 1fr;
        align: center middle;
        Label {
            background: $error;
            border: round $boost;
            text-style: bold;
            content-align: center middle;
            width: 75%;
            height: 50%;
        }
    }
    """

    def __init__(self, package_name: str):
        """Initialise the package unknown pane."""
        super().__init__("[red]Unknown[/]")
        self._package_name = package_name

    def compose(self) -> ComposeResult:
        yield Label(f"Package '{self._package_name}' is not available on PyPI")


##############################################################################
class PackageDetails(TabPane):
    """A tab pane that shows the details of the package."""

    def __init__(self, package: Package):
        """Initialise the package details pane."""
        super().__init__("Details")
        self._package = package

    def compose(self) -> ComposeResult:
        """Compose the package details display.

        Returns:
            The package URL data layout.
        """
        with TabContent():
            yield from widgets_for(
                ("Name", self._package.name, Value),
                ("Version", self._package.version, Value),
                ("Summary", self._package.summary, Value),
                ("URL", self._package.package_url, URL),
                ("Author", self._package.author, Value),
                ("Email", self._package.author_email, Value),
                ("Bug Track URL", self._package.bugtrack_url, URL),
                ("Classifiers", "\n".join(self._package.classifiers), Value),
                ("Documentation URL", self._package.docs_url, URL),
                ("Download URL", self._package.download_url, URL),
                ("Homepage", self._package.homepage, URL),
                ("Keywords", ", ".join(self._package.keywords), Value),
                ("License", self._package.license, Value),
                ("Maintainer", self._package.maintainer, Value),
                ("Email", self._package.maintainer_email, Value),
                ("Platform", self._package.platform, Value),
                ("Project URL", self._package.project_url, URL),
                *(
                    (title, value, URL)
                    for title, value in self._package.project_urls.items()
                ),
                ("Release URL", self._package.release_url, URL),
                (
                    "Requires",
                    ", ".join(
                        sorted(
                            set(
                                f"[@click=app.lookup('{pkg.name}')]{pkg.name}[/]"
                                for pkg in (
                                    Requirement(requirement)
                                    for requirement in self._package.requires_dist
                                )
                            )
                        )
                    ),
                    Value,
                ),
                ("Yanked", "Yes" if self._package.yanked else "No", Value),
                ("Yanked Reason", self._package.yanked_reason, Value),
            )


##############################################################################
class PackageInformation(TabbedContent):
    """A widget for showing information about a PyPI package."""

    DEFAULT_CSS = """
    PackageInformation {
        Tab {
            padding: 0;
            margin: 0 1;
        }
        background: $panel;
        height: 1fr;
        &> * {
            visibility: hidden;
        }
        &.content > * {
            visibility: visible;
        }
    }
    """

    BINDINGS = [
        ("up, down, home, end, pageup, pagedown", "focus_details"),
    ]

    @work(exclusive=True)
    async def show(self, package_name: str) -> bool:
        """Show the package information for the given package.

        Args:
            package_name: The name of the package to lookup and show

        Returns:
            `True` if the package was found, `False` if not.
        """

        # Don't bother trying to do anything if there isn't actually a name.
        if not package_name.strip():
            return False

        # Mark that there's content now.
        self.set_class(True, "content")

        # Show we're loading.
        self.loading = True

        # Clear any existing content.
        self.clear_panes()

        # Download the data for the package.
        found, package = await Package.from_pypi(package_name)

        if found:
            self.add_pane(PackageDetails(package))
            if package.description.strip():
                self.add_pane(PackageDescription(package))
            for url in package.urls:
                self.add_pane(PackageURLDetails(url))
        else:
            self.add_pane(PackageUnknown(package_name))

        # We're all done now.
        self.loading = False

        return found

    @on(TabContent.GoLeft)
    async def tab_leftward(self) -> None:
        """Handle a request to move leftward."""
        await self.query_one(Tabs).focus().run_action("previous_tab")

    @on(TabContent.GoRight)
    async def tab_righttward(self) -> None:
        """Handle a request to move rightward."""
        await self.query_one(Tabs).focus().run_action("next_tab")

    def action_focus_details(self) -> None:
        """Handle a request to ensure the content is focused."""
        if self.active_pane is not None and self.screen.focused == self.query_one(Tabs):
            try:
                self.active_pane.query_one(TabContent).focus()
            except NoMatches:
                pass

    def focus(self, scroll_visible: bool = True) -> Self:
        self.query_one(Tabs).focus(scroll_visible)
        return self


### package_information.py ends here
