"""Main entry point for running the application."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace

##############################################################################
# Local imports.
from . import __version__
from .app import PISpy


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The parsed command line arguments.
    """
    parser = ArgumentParser(
        prog="pispy",
        description="Look up package information on PyPI.",
        epilog=f"v{__version__}",
    )

    # Add the package argument.
    parser.add_argument(
        "package",
        nargs="?",
        help="A package to look up",
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information.",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Return the arguments.
    return parser.parse_args()


##############################################################################
def run() -> None:
    """Run the application."""
    arguments = get_args()
    PISpy(arguments.package).run(inline=arguments.package is not None)


##############################################################################
# Run the app if we're being called on as the main entry point.
if __name__ == "__main__":
    run()

### __main__.py ends here
