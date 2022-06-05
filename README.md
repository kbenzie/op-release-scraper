# `op` release scraper

Grabs the HTML https://app-updates.agilebits.com/product_history/CLI2 and
scrapes the release version, release date, and download links into the
`op-releases.json` file. This is intended to facilitate automatic installation
and upgrade of the `op` 1Password command line tool on platforms where package
manager support is not already provided.

## Usage

Grab the latest list of `op` releases:

```console
$ curl -s https://raw.githubusercontent.com/kbenzie/op-release-scraper/main/op-releases.json
```
