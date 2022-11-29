"""The main screen for the application."""

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.widgets import Header, Footer, DataTable

##############################################################################
# Local imports.
from ..data.stats import Packages

##############################################################################
class Main( Screen ):
    """The main screen for the application."""

    def compose( self ) -> ComposeResult:
        """Compose the main screen.

        Returns:
            ComposeResult: The main screen's layout.
        """
        yield Header()
        self.top_100 = DataTable[ str ]( id="top100", zebra_stripes=True )
        yield self.top_100
        yield Footer()

    async def get_top_100( self ) -> None:
        """Populate the main data grid with the top 100 packages."""
        self.top_100.add_columns( "Package", "Size" )
        for package in await Packages.top_100():
            self.top_100.add_row( package.name, f"{package.size:,}" )

    def on_mount( self ) -> None:
        """Start to populate the application on startup."""
        self.call_later( self.get_top_100 )

### main.py ends here
