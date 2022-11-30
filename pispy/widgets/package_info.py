"""Provides a widget that shows package information."""

##############################################################################
# Python imports.
from typing        import Any, Iterator
from pkg_resources import parse_requirements

##############################################################################
# Textual imports.
from textual.containers import Vertical
from textual.widgets    import Label

##############################################################################
# Rich imports.
from rich.markdown import Markdown
from rich.console  import RenderableType

##############################################################################
# Local imports.
from ..data import Package

##############################################################################
class Title( Label ):
    """A title for an item of package information."""

    DEFAULT_CSS = """
    Title {
        background: $panel-lighten-3;
        text-style: bold;
    }
    """
    """str: The defaults styles."""

    def __init__( self, text: str ) -> None:
        """Initialise the title.

        Args:
            text (str): The title.
        """
        super().__init__( f"{text}:" )

##############################################################################
class Value( Label ):
    """A value for an item of package information."""

    DEFAULT_CSS = """
    Value {
        background: $panel;
        padding-bottom: 1;
    }

    Value.none {
        color: $text-muted;
    }
    """
    """str: The default styles."""

    def __init__( self, value: RenderableType, *args: Any, **kwargs: Any ) -> None:
        """Initialise the value.

        Args:
            value (RenderableType): The value.
        """
        super().__init__(
            value or "None",
            *args,
            classes=( "none" if not value else "" ),
            **kwargs
        )

##############################################################################
class URL( Value ):
    """A URL for an item of package information."""

    def __init__( self, url: str ) -> None:
        """Initialise the URL.

        Args:
            value (RenderableType): The value.
        """
        super().__init__( Markdown( f"<{url}>" ) if url else "" )

##############################################################################
class PackageInfo( Vertical, can_focus=True ):
    """Widget for displaying package information."""

    DEFAULT_CSS = """
    PackageInfo {
        border: tall $primary;
        height: 1fr;
    }

    PackageInfo:focus {
        border: tall $accent;
    }

    PackageInfo Label.error {
        color: red;
        text-style: bold;
    }
    """

    async def clear( self ) -> None:
        """Clear the content of the widget."""
        await self.query( "PackageInfo > * ").remove()

    @staticmethod
    def project_urls( urls: dict[ str, str ] ) -> Iterator[ Title | URL ]:
        """Generate title/URL widgets from the project's URLs.

        Args:
            urls (dict[ str, str]): The project URLs.

        Yields:
            Title | URL: A title or a URL.
        """
        for title, url in urls.items():
            yield Title( title )
            yield URL( url )

    async def show( self, package_name: str ) -> None:
        """Show the package information for the given package.

        Args:
            package_name (str): The name of the package to lookup and show
        """

        # Clear any previous content.
        await self.clear()

        # Don't bother trying to do anything if there isn't actually a name.
        if not package_name.strip():
            return

        # Download the data for the package.
        found, package = await Package.from_pypi( package_name )

        # If we found it...
        if found:
            # ...populate the output.
            await self.query_one( PackageInfo ).mount(
                Title( "Name"), Value( package.name ),
                Title( "Version"), Value( package.version ),
                Title( "Summary"), Value( package.summary ),
                Title( "URL" ), URL( package.package_url ),
                Title( "Author" ), Value( package.author ),
                Title( "Email" ), Value( package.author_email ),
                Title( "Bug Track URL" ), URL( package.bugtrack_url ),
                Title( "Classifiers" ), Value( "\n".join( package.classifiers ) ),
                Title( "Description" ), Value(
                    Markdown( package.description )
                    if package.description_content_type == "text/markdown"
                    else package.description
                ),
                Title( "Documentation URL" ), URL( package.docs_url ),
                Title( "Download URL" ), URL( package.download_url ),
                Title( "Homepage" ), URL( package.homepage ),
                Title( "Keywords" ), Value( ", ".join( package.keywords ) ),
                Title( "License" ), Value( package.license ),
                Title( "Maintainer" ), Value( package.maintainer ),
                Title( "Email" ), Value( package.maintainer_email ),
                Title( "Platform" ), Value( package.platform ),
                Title( "Project URL" ), URL( package.project_url ),
                *self.project_urls( package.project_urls ),
                Title( "Release URL" ), URL( package.release_url ),
                Title( "Requires" ),Value(
                    ", ".join(
                        f"[@click=screen.lookup('{pkg.project_name}')]{pkg.project_name}[/]"
                        for pkg in parse_requirements( package.requires_dist )
                    )
                ),
                # TODO: yanked
                # TODO: yanked_reason
            )
        else:
            # Report that we didn't find it.
            await self.query_one( PackageInfo ).mount( Label( "Not found", classes="error" ) )

### package_info.py ends here
