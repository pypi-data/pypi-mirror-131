"""
###################
peltak TODOs plugin
###################


Overview
========

This plugin allows you to quickly scan your files for TODO comments and track
them across commits. This makes it easy to leave yourself todos while working on
a branch and then resolve them either before commiting or before finishing the PR.

"""
from .cli import check_todos  # noqa: F401


__version__ = "0.0.1"
