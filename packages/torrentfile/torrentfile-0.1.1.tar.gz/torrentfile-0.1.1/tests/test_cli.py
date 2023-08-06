#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################
# THE SOFTWARE IS PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################
"""Testing functions for the command line interface."""

import datetime
import os
import sys
from pathlib import Path

import pyben
import pytest

from tests import dir1, dir2, rmpath
from torrentfile.cli import main


def test_cli_v1(dir1):
    """Basic create torrent cli command."""
    args = ["torrentfile", str(dir1)]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")  # nosec
    rmpath(str(dir1) + ".torrent")


def test_cli_v2(dir1):
    """Create torrent v2 cli command."""
    args = ["torrentfile", str(dir1), "--meta-version", "2"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")  # nosec
    rmpath(str(dir1) + ".torrent")


def test_cli_v3(dir1):
    """Create hybrid torrent cli command."""
    args = ["torrentfile", str(dir1), "--meta-version", "3"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")  # nosec
    rmpath(str(dir1) + ".torrent")


def test_cli_private(dir1):
    """Test private cli flag."""
    args = ["torrentfile", str(dir1), "--private"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert "private" in meta["info"]  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_piece_length(dir1, piece_length, version):
    """Test piece length cli flag."""
    # fmt: off
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version]
    # fmt: on
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["info"]["piece length"] == piece_length  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_announce(dir1, piece_length, version):
    """Test announce cli flag."""
    # fmt: off
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--tracker", "https://announce.org/tracker"]
    # fmt: on
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["announce"] == "https://announce.org/tracker"  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_announce_list(dir1, version):
    """Test announce list cli flag."""
    # fmt: off
    trackers = [
        "https://announce.org/tracker",
        "https://announce.net/tracker",
        "https://tracker.net/announce",
    ]
    args = [
        "torrentfile", str(dir1), "--meta-version", version, "--tracker"
    ] + trackers
    # fmt: on
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    for url in trackers:
        assert url in [j for i in meta["announce list"] for j in i]  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_comment(dir1, piece_length, version):
    """Test comment cli flag."""
    args = [
        "torrentfile",
        str(dir1),
        "--piece-length",
        str(piece_length),
        "--meta-version",
        version,
        "--comment",
        "this is a comment",
    ]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["info"]["comment"] == "this is a comment"  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_outfile(dir1, piece_length, version):
    """Test outfile cli flag."""
    outfile = str(dir1) + "test.torrent"
    args = [
        "torrentfile",
        str(dir1),
        "--piece-length",
        str(piece_length),
        "--meta-version",
        version,
        "-o",
        outfile,
    ]
    sys.argv = args
    main()
    assert os.path.exists(outfile)  # nosec
    rmpath(outfile)


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_creation_date(dir1, piece_length, version):
    """Test if torrents created get an accurate timestamp."""
    args = [
        "torrentfile",
        str(dir1),
        "--piece-length",
        str(piece_length),
        "--meta-version",
        version,
        "--comment",
        "this is a comment",
    ]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    num = float(meta["creation date"])
    date = datetime.datetime.fromtimestamp(num)
    now = datetime.datetime.now()
    assert date.day == now.day  # nosec
    assert date.year == now.year  # nosec
    assert date.month == now.month  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_created_by(dir1, piece_length, version):
    """Test if created torrents recieve a created by field in meta info."""
    args = [
        "torrentfile",
        str(dir1),
        "--piece-length",
        str(piece_length),
        "--meta-version",
        version,
        "--comment",
        "this is a comment",
    ]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert "TorrentFile" in meta["created by"]  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_web_seeds(dir1, piece_length, version):
    """Test if created torrents recieve a created by field in meta info."""
    # fmt: off
    args = ["torrentfile", str(dir1), "--piece-length", str(piece_length),
            "--meta-version", version, "-w", "https://webseed.url/1",
            "https://webseed.url/2", "https://webseed.url/3"]
    # fmt: on
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert "https://webseed.url/1" in meta["url-list"]  # nosec
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_with_debug(dir1, piece_length, version):
    """Test debug mode cli flag."""
    # fmt: off
    args = ["torrentfile", str(dir1), "--piece-length", str(piece_length),
            "--meta-version", version, "--comment", "this is a comment", "-d"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")  # nosec
    rmpath(str(dir1) + ".torrent")
    # fmt: on


@pytest.mark.parametrize("piece_length", [2 ** exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_with_source(dir1, piece_length, version):
    """Test source cli flag."""
    # fmt: off
    args = ["torrentfile", str(dir1), "--piece-length", str(piece_length),
            "--meta-version", version, "--source", "somesource"]
    # fmt: on
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["info"]["source"] == "somesource"  # nosec
    rmpath(str(dir1) + ".torrent")


def test_cli_help():
    """Test showing help notice cli flag."""
    args = ["-h"]
    sys.argv = args
    try:
        assert main()  # nosec
    except SystemExit:
        assert True  # nosec
        assert dir1  # nosec
        assert dir2  # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_empty_files(dir2, version):
    """Test creating torrent with empty files."""
    args = [
        "torrentfile",
        str(dir2),
        "--meta-version",
        version,
        "--source",
        "somesource",
    ]
    sys.argv = args
    for i, item in enumerate(Path(dir2).iterdir()):
        if i < 2:
            with open(item, "wb") as _:
                pass
        else:
            break
    main()
    assert os.path.exists(str(dir2) + ".torrent")  # nosec
    rmpath(str(dir2) + ".torrent")
