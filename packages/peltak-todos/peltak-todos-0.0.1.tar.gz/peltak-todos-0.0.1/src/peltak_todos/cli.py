import itertools
import sys
import textwrap
from typing import List, Optional

from peltak.commands import click, root_cli, verbose_option
from peltak.core import context, git, log, shell

from . import parser
from .types import Todo


# TODO: Add date filter.
#  It should be possible to only search for todos that are newer than <data>.
#  It should accept '2020-01-15', '2020-01' and '2020'
# TODO: Add granular definition for git files checked
#  Allow passing --staged `--unstaged`, `--changed`, (staged + unstaged), `--untracked` to
#  define which git files should be checked
# TODO: Support passing directory via --file argument
#  Should check all files in the given directory.
@root_cli.command('todos')
@click.option('-u', '--untracked', is_flag=True, default=False)
@click.option(
    '-f', '--file', 'file_path',
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    default=None,
)
@click.option(
    '-a', '--author', 'authors',
    type=str,
    multiple=True,
    default=None,
)
@click.option(
    '--verify-complete',
    is_flag=True,
    default=False,
)
@verbose_option
def check_todos(
    untracked: bool,
    file_path: Optional[str],
    authors: List[str],
    verify_complete: bool,
) -> None:
    todos: List[Todo] = []

    if file_path:
        if file_path == ':commit':
            todos += parser.extract_from_files('staged', git.staged())
            todos += parser.extract_from_files('unstaged', git.unstaged())
        else:
            todos += parser.extract_from_files('', [file_path])
    else:
        branch_files = parser.get_changed_files(base_branch='master')
        todos += parser.extract_from_files('branch', branch_files)
        todos += parser.extract_from_files('staged', git.staged())
        todos += parser.extract_from_files('unstaged', git.unstaged())

    if untracked:
        todos += parser.extract_from_files('untracked', git.untracked())

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
