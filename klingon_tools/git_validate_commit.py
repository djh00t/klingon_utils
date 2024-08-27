# klingon_tools/git_validate_commit.py
"""Module for validating Git commit messages.

This module provides functions to validate Git commit messages to ensure they
are signed off and follow the Conventional Commits standard.

Typical usage example:

    from klingon_tools.git_validate_commit import validate_commit_messages repo
    = Repo('/path/to/repo') is_valid = validate_commit_messages(repo)
"""

import re
from git import Repo


def is_commit_message_signed_off(commit_message: str) -> bool:
    """Check if the commit message is signed off.

    Args:
        commit_message (str): The commit message to check.

    Returns:
        bool: True if the commit message is signed off, False otherwise.
    """
    # Check for the "Signed-off-by:" string in the commit message
    return "Signed-off-by:" in commit_message.strip()


def is_conventional_commit(commit_message: str) -> bool:
    """Check if the commit message follows the Conventional Commits standard.

    Args:
        commit_message (str): The commit message to check.

    Returns:
        bool: True if the commit message follows the Conventional Commits
        standard, False otherwise.
    """
    # Split the message into lines
    lines = commit_message.strip().split("\n")

    # Check the first line (header)
    conventional_commit_pattern = (
        r"^(?:.{2})?"  # Optionally ignore first two characters
        r"(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert|wip)"
        r"\([\w\/-]+\): "  # Make the scope mandatory
        r".{10,}"  # Match at least 10 characters after the colon
    )

    if not re.match(conventional_commit_pattern, lines[0], re.UNICODE):
        return False

    # Check for the presence of a sign-off line
    sign_off_pattern = r"^Signed-off-by: .+ <.+@.+>$"
    if not any(re.match(sign_off_pattern, line.strip()) for line in lines):
        return False

    return True


def validate_commit_messages(repo: Repo) -> bool:
    """Validate all commit messages to ensure they are signed off and follow
    the Conventional Commits standard.

    Args:
        repo (Repo): The Git repository to validate commit messages for.

    Returns:
        bool: True if all commit messages are valid, False otherwise.
    """
    for commit in repo.iter_commits("HEAD"):
        if not validate_single_commit_message(commit.message):
            return False
    return True


def validate_single_commit_message(commit_message: str) -> bool:
    """Validate a single commit message.

    Args:
        commit_message (str): The commit message to validate.

    Returns:
        bool: True if the commit message is valid, False otherwise.
    """
    return is_commit_message_signed_off(
        commit_message
        ) and is_conventional_commit(
            commit_message)
