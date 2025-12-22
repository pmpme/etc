# Create Issue from Terminal

## Default: List open issues

```
❯ etc-issue

[2025-12-22 04:58:30.156224] Open Tickets in pmpme/etc: 6
=========================================================

#  | TITLE                                                                               | STATE
------------------------------------------------------------------------------------------------
42 | [etc-issue] option to only print open issues                                        | open
41 | [leet] increment existing prefix and take existin suffix if not otherwise specified | open
...
=========================================================

To create a new issue ➡️ $ etc-issue "title of your issue"
```

## Option `create`: Create new issue

```
❯ etc-issue create "[etc-issue] add option to get link to issue num"

🚀 Creating new issue '[etc-issue] add option to get link to issue num'

======================================================================

[2025-12-22 06:08:51.082629] Created #45 '[etc-issue] add option to get link to issue num'
[2025-12-22 06:08:51.082673] Reference: https://github.com/pmpme/etc/issues/45

🎉 #45 created
❯
```

## Option `rename`: Rename existing issue

```
❯ etc-issue rename 40 "rename existing issue by number"

🔄 Renaming issue #40 to 'rename existing issue by number'
=========================================================

[2025-12-22 05:42:01.094900] Renamed #40
        Old title: 'add option to rename existing issue'
        New title 'rename existing issue by number'
        Link: https://github.com/pmpme/etc/issues/40

🎉 #40 title renamed to 'rename existing issue by number'
```

## Option `link`: Get Link of existing issue

```
❯ etc-issue link 45

Issue #45: [etc-issue] add option to get link to issue num (open)
Url: https://github.com/pmpme/etc/issues/45 (🎉 copied to clipboard!)
```
