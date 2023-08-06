# torrentfile

![torrentfile](https://github.com/alexpdev/torrentfile/blob/master/assets/torrentfile.png?raw=true)

------

## Bittorrent File Creator (.torrent)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/202440df15224535b5358503e6235c88)](https://www.codacy.com/gh/alexpdev/TorrentFile/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alexpdev/TorrentFile&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/alexpdev/TorrentFile/branch/master/graph/badge.svg?token=PXFsxXVAHW)](https://codecov.io/gh/alexpdev/TorrentFile)
![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/TorrentFile)
![GitHub License](https://img.shields.io/github/license/alexpdev/TorrentFile)
[![CI](https://github.com/alexpdev/TorrentFile/actions/workflows/python_workflow.yml/badge.svg?branch=master&event=push)](https://github.com/alexpdev/TorrentFile/actions/workflows/python_workflow.yml)
[![DeepSource](https://deepsource.io/gh/alexpdev/TorrentFile.svg/?label=active+issues&token=16Sl_dF7nTU8YgPilcqhvHm8)](https://deepsource.io/gh/alexpdev/TorrentFile/)

_TorrentFile_ can create torrent files, Check content for accuracy and completeness with a
.torrent file, and display detailed information contained in a .torrent file.

## Features

- Create meta files for Bittorrent v1, v2 and hybrid torrent files.
- Display detailed information contained in torrent file.
- Check/ReCheck content and torrent file for download completion details and data integrity.
- Supports all .torrent files.
- GUI project can be found at [https://github.com/alexpdev/TorrentfileQt](https://github.com/alexpdev/TorrentfileQt)
- Flexible API can be used as a library or easily integrate into larger codebase

## Documentation

Documentation can be found in the `./docs` directory, or online at [https://alexpdev.github.io/torrentfile](https://alexpdev.github.io/torrentfile).

## Installation

### via PyPi

`pip install torrentfile`

### via Git

```bash:
git clone https://github.com/alexpdev/torrentfile.git
python setup.py install
```

### download

Or download the latest release from the Release page on github.
[https://github.com/alexpdev/torrentfile/releases](https://github.com/alexpdev/torrentfile/releases)

## CLI Help Message

```bash:
usage: TorrentFile [-h] [-v] [-d] [-p] [-s <source>] [-c <comment>]
                   [-o <path>] [--meta-version <int>] [-l <int>]
                   [-t <url> [<url> ...]] [-w <url> [<url> ...]]
                   [-r <.torrent>]
                   <content>

Terminal based tool for creating, checking, or editing Bittorrent
meta(.torrent) files. TorrentFile supports all meta file versions including
hybrid files.

positional arguments:
  <content>                             path to content file or directory

optional arguments:
  -h, --help                            show this help message and exit
  -v, --version                         show program version and exit
  -d, --debug                           output debug information
  -p, --private                         create file for private tracker
  -s <source>, --source <source>        specify source tracker
  -c <comment>, --comment <comment>     include a comment in file metadata
  -o <path>, --out <path>               output path for created .torrent file
  --meta-version <int>                  Bittorrent metafile version.
                                        Options = 1, 2 or 3.
                                        (1) = Bittorrent v1 (Default)
                                        (2) = Bittorrent v2
                                        (3) = Bittorrent v1 & v2 hybrid

  -l <int>, --piece-length <int>        Fixed amount of bytes for each chunk of data. (Default: None)
                                        Acceptable input values include integers 14-24, which
                                        will be interpreted as the exponent for 2^n, or any perfect
                                        power of two integer between 16Kib and 16MiB (inclusive).
                                        Examples:: [--piece-length 14] [-l 20] [-l 16777216]

  -t <url> [<url> ...], --tracker <url> [<url> ...]
                                        One or more Bittorrent tracker announce url(s).
                                        Examples:: [-a url1 url2 url3]  [--anounce url1]

  -w <url> [<url> ...], --web-seed <url> [<url> ...]
                                        One or more url(s) linking to a http server hosting
                                        the torrent contents.  This is useful if the torrent
                                        tracker is ever unreachable. Example:: [-w url1 [url2 [url3]]]

  -r <.torrent>, --check <.torrent>, --recheck <.torrent>
                                        Activates the torrent checker mode.
                                        <.torrent> is the path to a torrent meta file.
                                        Check <content> data integrity with <.torrent> file.
                                        If this is active, all other options are ignored (except --debug)
                                        Ex:: :~$ torrentfile -r path/to/file.torrent path/to/contents
```

## License

Distributed under the GNU LGPL v3. See `LICENSE` for more information.

[https://github.com/alexpdev](https://github.com/alexpdev/)

## Issues

If you encounter any bugs or would like to request a new feature please open a new issue.

[https://github.com/alexpdev/TorrentFile/issues](https://github.com/alexpdev/TorrentFile/issues)
