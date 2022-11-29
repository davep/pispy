"""The package information lookup screen."""

##############################################################################
# Python imports.
from typing import Any

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.screen     import Screen
from textual.widgets    import Header, Footer, Input, Button, Label
from textual.containers import Horizontal, Vertical
from textual.binding    import Binding

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
        super().__init__( Markdown( f"<{url}>" ) if url else "None" )

##############################################################################
class Lookup( Screen ):
    """The package lookup screen."""

    DEFAULT_CSS = """
    Lookup Input {
        width: 5fr;
    }

    Lookup Input {
        width: 1fr;
    }

    Lookup #input {
        height: 3;
    }

    Lookup #output {
        border: solid $primary;
        height: 1fr;
    }

    Label.error {
        color: red;
        text-style: bold;
    }

    Value.none {
        color: $text-muted;
    }
    """
    """The CSS for the screen."""

    BINDINGS = [
        Binding( "f2", "app.switch_screen( 'stats' )", "Package Stats" )
    ]
    """list[ Binding ]: The bindings for the stats screen."""

    def compose( self ) -> ComposeResult:
        """Compose the stats screen.

        Returns:
            ComposeResult: The stats screen's layout.
        """
        yield Header()
        yield Horizontal(
            Input( placeholder="Name of the package to look up in PyPi" ),
            Button( "Lookup" ),
            id="input"
        )
        yield Vertical(
            id="output"
        )
        yield Footer()

    def on_mount( self ) -> None:
        """Configure the screen once loaded up."""
        self.query_one( Input ).focus()

    async def lookup( self ) -> None:
        """Perform a lookup for a package."""

        if not self.query_one( Input ).value.strip():
            return

        # Clean out the output. We're going to build it up again.
        self.query( "#output > *" ).remove()

        # Download the data for the package.
        found, package = await Package.from_pypi( self.query_one( Input ).value )

        # If we found it...
        if found:
            # ...populate the output.
            self.query_one( "#output" ).mount(
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
                    else  package.description
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
                # TODO: Project URLs -- find a good example
                Title( "Release URL" ), URL( package.release_url ),
                Title( "Requires" ), Value( ", ".join( package.requires_dist ) ),
                # TODO: yanked
                # TODO: yanked_reason
            )
        else:
            # Report that we didn't find it.
            self.query_one( "#output" ).mount( Label( "Not found", classes="error" ) )

    async def on_input_submitted( self, _: Input.Submitted ) -> None:
        """React to the user hitting enter in the input field."""
        await self.lookup()

    async def on_button_pressed( self, _: Button.Pressed ) -> None:
        """React to the user pressing the lookup button."""
        await self.lookup()

### lookup.py ends here
