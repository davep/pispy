"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer
from textual.binding import Binding

##############################################################################
# Local imports.
from ..widgets import TopBySize

##############################################################################
class Stats( Screen ):
    """The stats screen for the application."""

    BINDINGS = [
        Binding( "f2", "switch_screen( 'lookup' )", "Package Lookup" )
    ]
    """list[ Binding ]: The bindings for the stats screen."""

    def compose( self ) -> ComposeResult:
        """Compose the stats screen.

        Returns:
            ComposeResult: The stats screen's layout.
        """
        yield Header()
        yield TopBySize()
        yield Footer()

    def on_mount( self ) -> None:
        """Set the main screen up on load."""
        self.query_one( TopBySize ).focus()

### main.py ends here
