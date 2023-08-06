import itertools
import sys
import textwrap
from pathlib import Path
from typing import List, Optional

from peltak.core import context, git, log, shell

from . import parser
from .types import Todo


def check_todos(
    untracked: bool,
    file_path: Optional[str],
    authors: List[str],
    verify_complete: bool,
) -> None:
    repo_path = Path(
        shell.run("git rev-parse --show-toplevel", capture=True).stdout.strip()
    )

    if file_path:
        if file_path != ':commit':
            input_files = frozenset([file_path])
        else:
            input_files = frozenset([
                repo_path / fpath
                for fpath in (git.staged() + git.unstaged())
            ])
    else:
        input_files = frozenset(
            repo_path / fpath
            for fpath in (
                parser.get_changed_files(base_branch='master')
                + git.staged()
                + git.unstaged()
            )
        )

    if untracked:
        input_files |= frozenset([
            (repo_path / fpath) for fpath in git.untracked()
        ])

    todos = parser.extract_from_files(list(input_files))

    filtered_todos = [
        t for t in todos
        if not authors or any(
            a.lower() in t.author.lower() for a in authors
        )
    ]
    _render_todos(filtered_todos)

    if verify_complete and len(filtered_todos) > 0:
        sys.exit(127)


def _render_todos(todos: List[Todo]) -> None:
    print('\n')
    for file_path, file_todos in itertools.groupby(todos, key=lambda x: x.file):
        shell.cprint(f"<92>{file_path}\n")
        for todo in sorted(file_todos, key=lambda x: x.lines.start):
            if context.get('verbose') >= 1:
                shell.cprint(
                    f"<36>{todo.pretty_timestamp}  <33>{todo.author}<0>\n"
                    f"<95>{todo.file}:{todo.lines}  <90>{todo.sha1}<0>\n\n"
                    f"{textwrap.indent(todo.color_text, '  ')}\n\n"
                )
            else:
                shell.cprint(
                    f"    <95>:{todo.lines}  <36>{todo.pretty_timestamp}  "
                    f"<33>{todo.author_email}  <90>{todo.sha1}<0><0>\n\n"
                    f"{textwrap.indent(todo.color_text, '        ')}\n"
                )
        print()

    log.info(f"Found <33>{len(todos)}<32> TODOs")
