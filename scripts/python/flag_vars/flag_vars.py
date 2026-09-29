#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""
Find files under a directory and flag them by inserting _ref before
the file extension (e.g. filename.yml -> filename_ref.yml):

  1. Any file named vars.yml (at any depth)
  2. Any file named main.yml inside a "vars" directory (at any depth)
  3. All *.yml files inside the "scripts" directory (default: <root>/scripts)
  4. All files inside the top-level "templates" directory (default: <root>/templates)
  5. All files inside any roles/<ROLENAME>/templates directory (at any depth)

If --sole-directory is given, all normal rules are skipped and only the
files under that one directory are flagged.

Dry-run by default; pass --apply to actually rename the files.

NOTES:
'pip3 install argcomplete' # (if not installed already)
'activate-global-python-argcomplete --user' to activate argcomplete, then restart your shell.
"""

import argparse
from pathlib import Path

try:
    import argcomplete
except ImportError:
    argcomplete = None

__version__ = "1.0.0"

def display(path: Path) -> str:
    """Show paths relative to the current directory when possible."""
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def find_target_vars_files(root: Path):
    """Yield paths for vars.yml and vars/main.yml at any depth under root."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if name == "vars.yml":
            yield path
        elif name == "main.yml" and path.parent.name.lower() == "vars":
            yield path


def find_scripts_yml_files(scripts_dir: Path):
    """Yield all *.yml files in the scripts directory (recursive)."""
    if not scripts_dir.is_dir():
        return
    for path in scripts_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() == ".yml":
            yield path


def find_all_files(directory: Path):
    """Yield every file in the given directory (recursive)."""
    if not directory.is_dir():
        return
    for path in directory.rglob("*"):
        if path.is_file():
            yield path


def find_role_template_files(root: Path):
    """Yield every file inside any roles/<ROLENAME>/templates directory."""
    for path in root.rglob("*"):
        if not path.is_dir() or path.name.lower() != "templates":
            continue
        rel_parts = path.relative_to(root).parts
        # Matches roles/<ROLENAME>/templates and any templates dir
        # nested somewhere under a "roles" directory.
        if "roles" in rel_parts[:-1]:
            yield from find_all_files(path)


def flag_file(path: Path, apply: bool) -> bool:
    """Insert _ref before the file extension. Returns True if flagged."""
    if path.stem.lower().endswith("_ref"):
        return False  # already flagged
    new_path = path.with_name(path.stem + "_ref" + path.suffix)
    if new_path.exists():
        print(f"[SKIPPED] {display(new_path)} already exists")
        return False
    if apply:
        path.rename(new_path)
        print(f"[RENAMED] {display(path)} -> {display(new_path)}")
    else:
        print(f"[WOULD RENAME] {display(path)} -> {display(new_path)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Rename vars.yml, vars/main.yml, scripts/*.yml, and template files by inserting _ref before the extension."
    )
    directory_arg = parser.add_argument(
        "directory", nargs="?", default=".",
        help="Directory to search (default: current directory)")
    parser.add_argument("--scripts-dir", default="scripts",
                        help="Name of the scripts directory relative to the search directory (default: scripts)")
    parser.add_argument("--templates-dir", default="templates",
                        help="Name of the top-level templates directory relative to the search directory (default: templates)")
    sole_dir_arg = parser.add_argument(
        "--sole-directory", default=None,
        help="Skip all rules and only flag files under this directory. "
             "Relative paths are resolved from your current location, e.g. ../templates")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename the files (default is dry-run)")

    if argcomplete:
        directory_arg.completer = argcomplete.completers.DirectoriesCompleter()
        sole_dir_arg.completer = argcomplete.completers.DirectoriesCompleter()
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if not root.is_dir():
        parser.error(f"Not a directory: {root}")

    if args.sole_directory:
        sole_dir = Path(args.sole_directory).resolve()
        if not sole_dir.is_dir():
            parser.error(f"Not a directory: {args.sole_directory}")
        targets = set(find_all_files(sole_dir))
    else:
        scripts_dir = root / args.scripts_dir
        templates_dir = root / args.templates_dir

        # Use a set so a file matching several rules is only processed once
        targets = set(find_target_vars_files(root))
        targets.update(find_scripts_yml_files(scripts_dir))
        targets.update(find_all_files(templates_dir))
        targets.update(find_role_template_files(root))

    flagged = 0
    for path in sorted(targets):
        if flag_file(path, args.apply):
            flagged += 1

    mode = "Renamed" if args.apply else "Found (dry-run)"
    print(f"\n{mode} {flagged} file(s).")
    if not args.apply and flagged:
        print("Run again with --apply to perform the renames.")


if __name__ == "__main__":
    main()
