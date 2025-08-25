# `xum` - tmux session manager
Yes, it's another sessionizer using `tmux` and `fzf`.
Inspired by [ThePrimeagen's sessionizer](https://github.com/ThePrimeagen/tmux-sessionizer),
as most tmux sessionizers.

## Dependencies
- `tmux`
- `python` (at least 3.13)
- `zoxide`
- `fzf`

## Installation
Currently only `pipx`, maybe in the future I'll release a standalone binary.
```bash
pipx install xum
```

## Usage
`xum` is a simple Tmux session manager, it can be used to **create**, **attach to** and **delete** sessions.

There are four subcommands:
- `create`: list available directories among the ones provided (see below) and open a new window of a new session.
- `here`: create a new session in the current directory, for directory you visit less often.
- `switch`: list the currently open sessions and attach to the selected one.
- `close`: close selected session.

When creating new sessions `xum` uses *three* providers to generate a list of directories:
- `fd`: list all directories in a collection of watchdirs (see [Configuration] below).
- `zoxide`: list the directories in zoxide database.
- `custom_paths`: return manually specified entries (see [Configuration] below).

## Configuration
Configuration is performed by modifing the config file at `~/.config/xum/xum.toml`.

Here is an example configuration:
```toml
# search paths for fd
search_paths = ["~/projects"]
# additional manual entries
custom_paths = ["~/dotfiles"]
```

- `search_paths`
Define the directories on which to run `fd`. This will look for all directories contained therein.

- `custom_paths`
You can add individual directories to the list of available paths.
