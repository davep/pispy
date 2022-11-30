"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app     import App
from textual.binding import Binding

##############################################################################
# Local imports.
from .        import __version__
from .screens import Stats, Lookup

##############################################################################
class PISpy( App[ None ] ):
    """The main application class."""

    TITLE = "PISpy"
    """str: The title of the application."""

    SUB_TITLE = f"The Terminal PyPi Viewer - v{__version__}"
    """str: The subtitle of the application."""

    SCREENS = {
        "stats": Stats,
        "lookup": Lookup
    }
    """dict[ str, Screen ]: The screen collection for the application."""

    BINDINGS = [
        Binding( "ctrl+q", "quit", "Quit" )
    ]
    """list[ Binding ]: The main application bindings."""

    def on_mount( self ) -> None:
        """Configure the application on startup."""
        self.push_screen( "lookup" )

##############################################################################
def run() -> None:
    """Run the application."""
    PISpy().run()

### app.py ends here
