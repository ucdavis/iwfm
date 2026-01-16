# main.py
# Unified Command Line Interface entry point for iwfm
# Copyright (C) 2026 University of California
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------



"""
Unified CLI entry point for IWFM.

This module defines:
- Root Typer app
- Global flags (--power, --dev)
- Logging configuration
- Registration of command groups

Existing scripts remain directly runnable.
"""

from __future__ import annotations

import sys
import typer
from typing import Optional
from iwfm.debug.logger_setup import logger

# Root Typer app
app = typer.Typer(
    name="iwfm",
    help="Integrated Water Flow Model utilities",
    add_completion=True,
    no_args_is_help=True,
)

# ---- CLI Context -------------------------------------------------------------

class CLIContext:
    """
    Holds global CLI state shared across commands.
    """
    def __init__(self):
        self.power: bool = False
        self.dev: bool = False


def get_context() -> CLIContext:
    ctx = typer.get_current_context()
    if ctx.obj is None:
        ctx.obj = CLIContext()
    return ctx.obj


# ---- Logging ----------------------------------------------------------------

def configure_logging(power: bool, dev: bool) -> None:
    """
    Configure logging once, based on CLI mode using loguru logger.
    """
    if dev:
        level = "DEBUG"
    elif power:
        level = "INFO"
    else:
        level = "WARNING"

    logger.remove()  # Remove default loguru logger
    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.debug(f"Logging configured: level={level}")


# ---- Root Callback -----------------------------------------------------------

@app.callback()
def main(
    ctx: typer.Context,
    power: bool = typer.Option(
        False,
        "--power",
        help="Enable power-user commands and INFO-level logging",
    ),
    dev: bool = typer.Option(
        False,
        "--dev",
        help="Enable developer/debug commands and DEBUG-level logging",
    ),
):
    """
    IWFM unified command-line interface.
    """
    ctx.ensure_object(CLIContext)
    ctx.obj.power = power
    ctx.obj.dev = dev

    configure_logging(power=power, dev=dev)  # Use loguru-based logging setup


# ---- Subcommand Registration -------------------------------------------------
# Importing here avoids circular imports and keeps startup predictable

def _register_commands():
    """
    Register all command groups.
    Power/dev visibility is handled inside each group.
    """
    from iwfm.calib import calib
    from iwfm.gis import gis
    from iwfm.xls import xls
    from iwfm.debug import debug

    app.add_typer(calib.app, name="calib", help="Model calibration commands")
    app.add_typer(gis.app, name="gis", help="GIS-related utilities")
    app.add_typer(xls.app, name="xls", help="Excel import/export utilities")
    app.add_typer(debug.app, name="debug", help="Developer and diagnostic commands",
         hidden=not get_context().dev,
     )


_register_commands()


# ---- Entry Point -------------------------------------------------------------

def run():
    """
    Console script entry point.
    """
    app()


if __name__ == "__main__":
    run()
