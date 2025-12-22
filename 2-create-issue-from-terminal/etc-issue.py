#!/usr/bin/env python3

import os
import pdb
import requests
import sys
import time
import argparse
import pyperclip
from dotenv import load_dotenv
from datetime import date, datetime
from pprint import pprint
from typing import DefaultDict, List, Tuple, Optional
from collections import defaultdict

# print(sys.executable)
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = 'https://api.github.com'
OWNER = "pmpme"
REPO = "etc"
REPO_URL = f"{BASE_URL}/repos/{OWNER}/{REPO}"
ISSUES_URL = f"{REPO_URL}/issues?state=all"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

class Issues:

    def __init__(self):
        self.issues: dict[int, Tuple[str, str]] = {} # { number: (title, state) }
        self.issues_titles: DefaultDict[str, List[int]] = defaultdict(list) # { title: [number] }
        self._refresh_issues()


    def _refresh_issues(self, wait: int=1) -> None:
        self.issues.clear()
        self.issues_titles.clear()
        time.sleep(wait)
        issues_resp = requests.get(ISSUES_URL, headers=HEADERS)
        issues_resp.raise_for_status()
        issues_data = issues_resp.json()

        for raw_data in issues_data:
            if "pull_request" in raw_data:
                continue
            issue_num = raw_data.get('number')
            issue_title = raw_data.get('title')
            issue_state = raw_data.get('state')
            self.issues[issue_num] = (issue_title, issue_state)
            self.issues_titles[issue_title].append(issue_num)


    def get_issue(self, number: int) -> Tuple[str, str]:
        if number not in self.issues:
            raise KeyError(f"Issue #{number} not found")
        return self.issues[number]


    def get_numbers_for_title(self, title: str, state: Optional[str] = None) -> List[int]:
        if title not in self.issues_titles:
            raise KeyError(f"Issue with title '{title}' not found")

        issue_nums = self.issues_titles[title]
        if state:
            issue_nums = [num for num in issue_nums if self.issues[num][1] == state]
        return issue_nums


    def create_issue(self, title: str) -> int:
        data = { "title": title, "body": "WIP" }
        response = requests.post(ISSUES_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        issue_number = response.json().get("number")
        self._refresh_issues(3)
        print(f"[{datetime.now()}] Created #{issue_number} '{title}'")
        print(f"[{datetime.now()}] Reference: https://github.com/pmpme/etc/issues/{issue_number}")

        return issue_number

    def rename_issue(self, number:int, new_title:str) -> int:
        if number not in self.issues:
            raise KeyError(f"Issue #{number} not found")

        update_url = f"{REPO_URL}/issues/{number}"
        data = { "title": new_title }

        response = requests.patch(update_url, headers=HEADERS, json=data)
        response.raise_for_status()
        old_title, _ = self.issues[number]
        print(f"[{datetime.now()}] Renamed #{number}")
        print(f"\tOld title: '{old_title}'")
        print(f"\tNew title '{new_title}'")
        print(f"\tLink: https://github.com/{OWNER}/{REPO}/issues/{number}")

        return number


    def close_issues_not_planned(self, *args: int) -> None:
        to_close = set(args)

        for issue_num in args:
            close_url = f"{REPO_URL}/issues/{issue_num}"
            data = { "state": "closed", "state_reason": "not_planned" }
            response = requests.patch(close_url, headers=HEADERS, json=data)
            response.raise_for_status()

            if issue_num not in self.issues:
                raise KeyError(f"Issue #{issue_num} not found")

            if self.issues[issue_num][1] == "closed":
                print(f"[{datetime.now()}] Issue #{issue_num} already closed")
            else:
                response = requests.patch(close_url, headers=HEADERS, json=data)
                response.raise_for_status()
                print(f"[{datetime.now()}] Closed #{issue_num}")
            try:
                to_close.remove(issue_num)
            except:
                pdb.set_trace()

        self._refresh_issues(2)
        if to_close:
            print(f"[{datetime.now()}] Error closing {len(to_close)} / {len(args)} issues: {to_close}")
            return False
        return True

    def close_issues_not_planned_title(self, title:str, count: Optional[int] = None) -> None:
        issue_nums_all = self.get_numbers_for_title(title, "open")
        print(f"[{datetime.now()}] Total {len(issue_nums_all)} issues")
        count = count or len(issue_nums_all)
        if len(issue_nums_all) < count:
            raise Exception(f"No open tickets with title '{title}'")

        issue_nums = issue_nums_all[:count] if count else issue_nums_all[:]
        pdb.set_trace()
        return self.close_issues_not_planned(*issue_nums)


    def get_open_tickets(self) -> dict[int, Tuple[str, str]]:
        return {
            number: (title, state)
            for number, (title, state) in self.issues.items()
            if state == "open"
        }


    def print_table(self, exclude_closed: bool=True) -> None:
        issues = self.get_open_tickets() if exclude_closed else self.issues
        if not issues:
            print(f"[{datetime.now()}] No issues found.")
            return

        num_width = max(len(str(n)) for n in issues.keys())
        title_width = max(len(t[0]) for t in issues.values())
        state_width = max(len(t[1]) for t in issues.values())

        header = (
            f"{'#'.ljust(num_width)} | "
            f"{'TITLE'.ljust(title_width)} | "
            f"{'STATE'.ljust(state_width)}"
        )
        print(header)
        print("-" * len(header))

        for number, (title, state) in issues.items():
            print(
                f"{str(number).ljust(num_width)} | "
                f"{title.ljust(title_width)} | "
                f"{state.ljust(state_width)}"
            )


if __name__ == "__main__":
    # ---- Process arguments
    parser = argparse.ArgumentParser(
        description="Manage daily issues in Github repo pmpme/etc",
        prog="etc-issue"
    )

    subparsers = parser.add_subparsers(dest="command")

    # 1. Create command
    create_parser = subparsers.add_parser("create", help="Create a new issue")
    create_parser.add_argument("title", help="Title of new issue (in quotes)")

    # 2. Rename command
    rename_parser = subparsers.add_parser("rename", help="Rename an existing issue")
    rename_parser.add_argument("number", type=int, help="Issue number to rename")
    rename_parser.add_argument("new_title", help="New title for the issue")

    # 3. Link command
    link_parser = subparsers.add_parser("link", help="Print the Github URL for an issue")
    link_parser.add_argument("number", type=int, help="Issue number")


    # Default: If no arguments passed in, treat as --list
    args = parser.parse_args()

    # ---- Process commands
    issues = Issues()
    today_str = date.today().strftime("%m-%d-%Y")

    # Create new issue
    if args.command == "create":
        message = f"🚀 Creating new issue '{args.title}'"
        print(f"\n{message}\n")
        print("=" * len(message) + "\n")
        new_issue_num = issues.create_issue(args.title)
        print(f"\n🎉 #{new_issue_num} created")
    elif args.command == "rename":
        message = f"🔄 Renaming issue #{args.number} to '{args.new_title}'"
        print(f"\n{message}")
        print("=" * len(message) + "\n")
        updated_issue_num = issues.rename_issue(args.number, args.new_title)
        print(f"\n🎉 #{updated_issue_num} title renamed to '{args.new_title}'")
    elif args.command == "link":
        try:
            title, state = issues.get_issue(args.number)
            print(f"\nIssue #{args.number}: {title} ({state})")
            url = f"https://github.com/{OWNER}/{REPO}/issues/{args.number}"
            pyperclip.copy(url)
            print(f"Url: {url} (🎉 copied to clipboard!)")
        except KeyError:
            print(f"Error: Issue #{args.number} not found")
            sys.exit(1)
    else:
        message = f"[{datetime.now()}] Open Tickets in {OWNER}/{REPO}: {len(issues.get_open_tickets())}"
        print(f"\n{message}")
        print("=" * len(message) + "\n")
        issues.print_table()
        print("=" * len(message) + "\n")
        parser.print_usage()


"""
❯ cat ~/bin/etc-issue
#!/bin/bash
uv run $HOME/code/pmpme/etc/.venv/bin/python $HOME/code/pmpme/etc/2-create-issue-from-terminal/etc-issue.py "$@"
❯ 
"""

"""
Other stuff, archive for now

# ---- Close issues by numbers
# issues.close_issues_not_planned(11, 12)

# ---- Close issues with title
# issues.close_issues_not_planned_title(issue_title)
# issues.close_issues_not_planned_title(f"{today_str} | TBD")

# 🚫
"""