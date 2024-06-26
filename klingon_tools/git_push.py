"""Module for pushing changes to a remote Git repository.

This module provides functionality to push changes to a remote Git repository
after performing several checks and operations such as validating commit messages,
stashing unstaged changes, rebasing, and applying stashed changes back.

Typical usage example:

    import git
    from klingon_tools.git_push import git_push

    repo = git.Repo('/path/to/repo')
    git_push(repo)
"""

import git
from git import GitCommandError
from klingon_tools.logger import logger
import subprocess
from klingon_tools.git_validate_commit import validate_commit_messages
from klingon_tools.openai_tools import OpenAITools


def git_push(repo: git.Repo) -> None:
    """Pushes changes to the remote repository.

    This function performs several steps to ensure that the local repository
    is in sync with the remote repository before pushing changes. It validates
    commit messages, stashes any unstaged changes, rebases the current branch
    on top of the remote branch, and then pushes the changes. If there were
    any stashed changes, it attempts to apply them back.

    Args:
        repo (git.Repo): The Git repository object.

    Raises:
        GitCommandError: If any git command fails.
        Exception: For any unexpected errors.
    """
    try:
        # Handle file deletions
        deleted_files = subprocess.run(
            ["git", "ls-files", "--deleted"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()

        if deleted_files:
            for file in deleted_files:
                try:
                    # Stage the deleted file
                    repo.git.add(file)
                    # Commit the deletion with a specific message
                    commit_message = f"chore({file}): Handle deletions"
                    repo.index.commit(commit_message)
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to handle deletion for {file}: {e}")
                    continue
        openai_tools = OpenAITools()
        openai_tools = OpenAITools()
        if not validate_commit_messages(repo, openai_tools):
            logger.error(
                message="Commit message validation failed. Aborting push.", status="❌"
            )
            return

        # Fetch the latest changes from the remote repository
        repo.remotes.origin.fetch()

        # Get the current branch name
        current_branch = repo.active_branch.name

        # Check for unstaged changes and stash them if any
        stash_needed = repo.is_dirty(untracked_files=True)
        if stash_needed:
            repo.git.stash("save", "--include-untracked", "Auto stash before rebase")

        # Rebase the current branch on top of the remote branch
        repo.git.rebase(f"origin/{current_branch}")

        # Push the changes to the remote repository
        repo.remotes.origin.push()

        # Apply the stashed changes back if they were stashed
        if stash_needed:
            try:
                repo.git.stash("pop")
            except GitCommandError as e:
                logger.error(
                    message="Failed to apply stashed changes",
                    status="❌",
                    reason=str(e),
                )
                # If there are conflicts, you can handle them here or manually resolve them

        logger.info(message="Pushed changes to remote repository", status="✅")
    except GitCommandError as e:
        logger.error(
            message="Failed to push changes to remote repository",
            status="❌",
            reason=str(e),
        )
    except Exception as e:
        logger.error(
            message="An unexpected error occurred",
            status="❌",
            reason=str(e),
        )
