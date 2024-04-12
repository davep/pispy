"""Provides the main application class."""

##############################################################################
# Python imports.
import sys

##############################################################################
# Textual imports.
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input

##############################################################################
# Local imports.
from .widgets import PackageInfo


##############################################################################
class PISpy(App[None]):
    """The main application class."""

    CSS = """
    Header {
        HeaderIcon {
            visibility: hidden;
        }

        &.-tall {
            height: 1;
        }
    }
    """

    BINDINGS = [("escape", "quit", "Quit")]
    """The main application bindings."""

    ENABLE_COMMAND_PALETTE = False
    """Disable the command palette."""

    def compose(self) -> ComposeResult:
        """Compose the stats screen.

        Returns:
            The stats screen's layout.
        """
        yield Input(placeholder="Name of the package to look up in PyPI")
        yield PackageInfo()

    async def on_mount(self) -> None:
        """Pre-fill the display if a package is passed on the command line."""
        try:
            # TODO: doing it via argv is icky, but it's handy for a quick
            # hack. Once I've revamped the UI I'll switch to argparse, and
            # probably add an inline switch.
            self.query_one(Input).value = sys.argv[1]
        except IndexError:
            return
        await self.lookup_package()

    @on(Input.Submitted)
    async def lookup_package(self) -> None:
        """React to the user hitting enter in the input field."""
        await self.query_one(PackageInfo).show(self.query_one(Input).value)

    async def action_lookup(self, package: str) -> None:
        """React to a hyperlink of a project being clicked on.

        Args:
            package: The name of the package to look up.
        """
        self.query_one(Input).value = package
        self.query_one(Input).cursor_position = len(package)
        await self.lookup_package()


##############################################################################
def run() -> None:
    """Run the application."""
    PISpy().run()


### app.py ends here
