import os
from subprocess import CalledProcessError
from unittest.mock import Mock, call, patch

import pytest
import tornado

from jupyterlab_git.git import Git

from .testutils import FakeContentManager, maybe_future


@pytest.mark.asyncio
async def test_changed_files_invalid_input():
    with pytest.raises(tornado.web.HTTPError):
        await Git(FakeContentManager("/bin")).changed_files(
            base="64950a634cd11d1a01ddfedaeffed67b531cb11e"
        )


@pytest.mark.asyncio
async def test_changed_files_single_commit():

    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.return_value = maybe_future(
            (0, "file1.ipynb\x00file2.py\x00", "")
        )

        # When
        actual_response = await Git(FakeContentManager("/bin")).changed_files(
            single_commit="64950a634cd11d1a01ddfedaeffed67b531cb11e"
        )

        # Then
        mock_execute.assert_called_once_with(
            [
                "git",
                "diff",
                "64950a634cd11d1a01ddfedaeffed67b531cb11e^!",
                "--name-only",
                "-z",
            ],
            cwd="/bin",
        )
        assert {"code": 0, "files": ["file1.ipynb", "file2.py"]} == actual_response


@pytest.mark.asyncio
async def test_changed_files_working_tree():
    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.return_value = maybe_future(
            (0, "file1.ipynb\x00file2.py", "")
        )

        # When
        actual_response = await Git(FakeContentManager("/bin")).changed_files(
            base="WORKING", remote="HEAD"
        )

        # Then
        mock_execute.assert_called_once_with(
            ["git", "diff", "HEAD", "--name-only", "-z"], cwd="/bin"
        )
        assert {"code": 0, "files": ["file1.ipynb", "file2.py"]} == actual_response


@pytest.mark.asyncio
async def test_changed_files_index():
    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.return_value = maybe_future(
            (0, "file1.ipynb\x00file2.py", "")
        )

        # When
        actual_response = await Git(FakeContentManager("/bin")).changed_files(
            base="INDEX", remote="HEAD"
        )

        # Then
        mock_execute.assert_called_once_with(
            ["git", "diff", "--staged", "HEAD", "--name-only", "-z"], cwd="/bin"
        )
        assert {"code": 0, "files": ["file1.ipynb", "file2.py"]} == actual_response


@pytest.mark.asyncio
async def test_changed_files_two_commits():
    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.return_value = maybe_future(
            (0, "file1.ipynb\x00file2.py", "")
        )

        # When
        actual_response = await Git(FakeContentManager("/bin")).changed_files(
            base="HEAD", remote="origin/HEAD"
        )

        # Then
        mock_execute.assert_called_once_with(
            ["git", "diff", "HEAD", "origin/HEAD", "--name-only", "-z"], cwd="/bin"
        )
        assert {"code": 0, "files": ["file1.ipynb", "file2.py"]} == actual_response


@pytest.mark.asyncio
async def test_changed_files_git_diff_error():
    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.side_effect = CalledProcessError(128, b"cmd", b"error message")

        # When
        actual_response = await Git(FakeContentManager("/bin")).changed_files(
            base="HEAD", remote="origin/HEAD"
        )

        # Then
        mock_execute.assert_called_once_with(
            ["git", "diff", "HEAD", "origin/HEAD", "--name-only", "-z"], cwd="/bin"
        )
        assert {"code": 128, "message": "error message"} == actual_response


@pytest.mark.asyncio
@pytest.mark.parametrize("args, cli_result, cmd, expected", [
    (
        ("dummy.txt", "ar539ie5", "/bin"), 
        (0, "2\t1\tdummy.txt", ""), 
        ["git", "diff", "--numstat", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "ar539ie5", "--", "dummy.txt"],
        False
    ),
    (
        ("dummy.png", "ar539ie5", "/bin"), 
        (0, "-\t-\tdummy.png", ""), 
        ["git", "diff", "--numstat", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "ar539ie5", "--", "dummy.png"],
        True
    ),
    (
        ("dummy.txt", "INDEX", "/bin"), 
        (0, "2\t1\tdummy.txt", ""), 
        ["git", "diff", "--numstat", "--cached", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "--", "dummy.txt"],
        False
    ),
    (
        ("dummy.png", "INDEX", "/bin"), 
        (0, "-\t-\tdummy.png", ""), 
        ["git", "diff", "--numstat", "--cached", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "--", "dummy.png"],
        True
    ),
    (
        ("dummy.txt", "ar539ie5", "/bin"), 
        (128, "", "fatal: Git command failed"), 
        ["git", "diff", "--numstat", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "ar539ie5", "--", "dummy.txt"],
        tornado.web.HTTPError
    ),
    (
        ("dummy.txt", "ar539ie5", "/bin"), 
        (128, "", "fatal: Path 'dummy.txt' does not exist (neither on disk nor in the index)"), 
        ["git", "diff", "--numstat", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "ar539ie5", "--", "dummy.txt"],
        False
    ),
])
async def test_is_binary_file(args, cli_result, cmd, expected):
    with patch("jupyterlab_git.git.execute") as mock_execute:
        # Given
        mock_execute.return_value = maybe_future(cli_result)

        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                await Git(FakeContentManager("/bin"))._is_binary(*args)
        else:
            # When
            actual_response = await Git(FakeContentManager("/bin"))._is_binary(*args)

            # Then
            mock_execute.assert_called_once_with(cmd, cwd="/bin")

            assert actual_response == expected
