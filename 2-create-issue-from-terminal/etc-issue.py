#!/usr/bin/env python3

import os
import pdb
import requests
import sys
import time
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
    issues = Issues()
    today_str = date.today().strftime("%m-%d-%Y")

    # [PRINT OPEN ISSUES] if no args or too many args provided
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        message = f"[{datetime.now()}] Open Tickets in {OWNER}/{REPO}: {len(issues.get_open_tickets())}"
        print(f"\n{message}")
        print("=" * len(message) + "\n")
        issues.print_table()
        print("=" * len(message) + "\n")
        print("To create a new issue ➡️ $ etc-issue \"title of your issue (in quotes)\"\n")
        sys.exit(0)

    # [CREATE NEW ISSUE] if title provided
    if len(sys.argv) == 2:
        issue_title = sys.argv[1]
        print(f"\n🚀 Starting [etc-issue] {today_str} '{issue_title}'")
        print("===================================================\n")
        new_issue_num = issues.create_issue(issue_title)
        sys.exit(0)    

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
"""