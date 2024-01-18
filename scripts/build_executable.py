#!/usr/bin/env python
"""Small script for building executables of the package.

Executables are built for every entrypoint defined in pyproject.toml.
"""

import tomllib
import PyInstaller.__main__


def get_entrypoints() -> dict[str, str]:
    """Fetches the entrypoints defined in pyproject.toml.

    Raises:
        FileNotFoundError: If the pyproject.toml file could not be found.

    Returns:
        dict[str, str]: The found entrypoints with name and function it points to.
    """
    try:
        with open("pyproject.toml", "rb") as f:
            return tomllib.load(f)["project"].get("scripts", {})
    except FileNotFoundError:
        raise FileNotFoundError(
            "Could not find the pyproject.toml file. Make sure to run this script from the project root directory."
        )


def build_executable(name: str, path: str) -> None:
    """Builds executable using PyInstaller.

    Args:
        name (str): Desired name of executable.
        path (str): Path to script from src directory.
    """
    print("=====")
    print(f"Building executable '{name}' from src/{path}..")
    print("=====")

    PyInstaller.__main__.run(
        [
            "--clean",
            "--noconfirm",
            "--add-data=README.md:.",
            f"--name={name}",
            f"src/{path}",
        ]
    )

    print("=====")
    print(f"Finished building executable '{name}' from src/{path}.")
    print("=====")


def main() -> None:
    """The main script where execution starts."""
    entrypoints = get_entrypoints()

    for name, function in entrypoints.items():
        path = function.split(":")[0].replace(".", "/") + ".py"

        build_executable(name, path)


if __name__ == "__main__":
    main()
