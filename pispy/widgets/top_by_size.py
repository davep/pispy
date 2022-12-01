"""Provides a widget that shows the top 100 packages by size."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.widgets    import Label, DataTable
from textual.containers import Container

##############################################################################
# Local imports.
from ..data.stats import Packages

##############################################################################
class TopBySize( Container ):
    """Widget for showing the top 100 packages."""

    DEFAULT_CSS = """
    TopBySize {
        layers: base label;
    }

    TopBySize Container {
        layer: base;
        border: solid $primary;
    }

    TopBySize Label {
        layer: label;
        width: auto;
        offset: 1 0;
        color: white;
        background: $primary;
    }

    TopBySize #top100 {
        margin: 1;
    }
    """

    def compose( self ) -> ComposeResult:
        """Compose the top 100 package display.

        Returns:
            ComposeResult: The top-by-size screen's layout.
        """
        self.top_100 = DataTable[ str ]( id="top100", zebra_stripes=True )
        yield Label( " Top 100 Packages by Size " )
        yield Container( self.top_100, classes="border" )

    async def get_top_100( self ) -> None:
        """Populate the main data grid with the top 100 packages."""
        self.top_100.add_columns( "Package", "Size" )
        for package in await Packages.top_100():
            self.top_100.add_row( package.name, f"{package.size:,}" )

    def on_mount( self ) -> None:
        """Start to populate the application on startup."""
        self.call_later( self.get_top_100 )

    def focus( self, scroll_visible: bool = True ) -> None:
        """Focus on the widget."""
        self.top_100.focus( scroll_visible )

### top_by_size.py ends here
