# PISpy

## Introduction

PISpy aims to be a simple but useful [PyPi](https://pypi.org/) lookup client
for the Terminal, built with [Textual](https://textual.textualize.io/).

## Installation

### pipx

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install pispy-client
```

### Homebrew

The package can be installed using Homebrew. Use the following commands to
install:

```sh
$ brew tap davep/homebrew
$ brew install pispy
```

## Running

Once installed, just run `pispy` from your shell.

![PISpy lookup up Textual](https://raw.githubusercontent.com/davep/pispy/main/img/pispy.png)

## Naming

> Wait! What? Is this pispy or pispy-client? Why the two names?

Well... when I started hacking this together I went to check if PyPi had a
package called `pispy` and it didn't, so I steamed ahead with that. Only
when I came to add the package to PyPi did it say it wouldn't let me because
it was too similar to another package.

So... package name is `pispy-client` but the content is `pispy`.

## Work in progress

PISpy is currently a work in progress. I'm still figuring out what it should
do and how; but for now it provides a simple package lookup interface.

[//]: # (README.md ends here)
