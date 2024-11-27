# PISpy ChangeLog

## 0.9.0

**Released: 2024-11-27**

- Updated for newer versions of Textual.
- Internal tweaks.

## 0.8.0

**Released: 2024-06-16**

- Updated Textual and fixed breakage.
- Added link-following support to the package description pane, when the
  description is seen as Markdown and the link can be reasonably followed.

## 0.7.0

**Released: 2024-04-22**

- The keywords display now allows for keywords that are space or comma
  separated. ([#21](https://github.com/davep/pispy/issues/21))
- The download count is now no longer shown (it is always `-1` anyway).
  ([#23](https://github.com/davep/pispy/pull/23))
- Requirements are now de-duplicated and sorted.
  ([#24](https://github.com/davep/pispy/pull/24))
- Made the UI a bit more minimal.
  ([#26](https://github.com/davep/pispy/pull/26))
- Switched to using
  [`Packaging`](https://packaging.pypa.io/en/stable/index.html) to parse
  dependency package details.

## 0.6.0

**Released: 2024-04-17**

- Add support for passing a package name on the command line.
- Show the package details inline in the terminal if the package name was
  passed on the command line.
- Big reworking of the whole UI.

## 0.5.0

**Released: 2024-04-12**

- Reworked the way the metadata is shown
  ([#2](https://github.com/davep/pispy/issues/2)).
- Clicking on URLs in the display now opens the default web browser
  ([#7](https://github.com/davep/pispy/issues/7)).

## 0.4.0

**Released: 2023-02-17**

- Updated to Textual v0.11.1, and started using the new Markdown widget to
  display markdown data.

## 0.3.0

**Released: 2023-01-07**

- Updated to the latest version of Textual, and make changes to take Textual
  changes into account. Also pinned the version of Textual (for now).

## 0.2.0

**Released: 2022-12-10**

- This release rounds out the data that is displayed when brought back from
  the JSON interface.

## 0.1.0

**Released: 2022-11-30**

- Initial release.

[//]: # (ChangeLog.md ends here)
