# Project Status Log

This tool provides a command-line interface to manage a project status log,
which is stored in a simple JSON file. It is designed to be used by both
humans and AI agents for tracking tasks, bugs, and other project items.

## Architecture

The tool is built in Python and follows a simple Command-Service-Repository
pattern. It uses only the Python standard library to ensure maximum
portability and ease of use in various environments.

-   **CLI:** `src/main.py` (using `argparse`)
-   **Business Logic:** `src/manager.py`
-   **Data Models:** `src/models.py` (using `dataclasses`)
-   **Storage:** `src/storage.py` (JSON file I/O)

## Usage

See the `plan.md` for detailed usage scenarios and the API contract.
