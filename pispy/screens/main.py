"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer

##############################################################################
class Main( Screen ):
    """The main screen for the application."""

    def compose( self ) -> ComposeResult:
        """Compose the main screen.

        Returns:
            ComposeResult: The main screen's layout.
        """
        yield Header()
        yield Footer()

### main.py ends here
