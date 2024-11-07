#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint, choice
from subprocess import Popen, CalledProcessError
import sys


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    start_date = datetime(2024, 9, 9)  # Start date for commits
    end_date = datetime.now()  # End date is today

    # Set up commit frequency and range
    frequency = args.frequency
    max_commits = args.max_commits

    # Check if we are in an existing Git repository
    if not os.path.exists(".git"):
        print("Error: This script must be run inside an existing Git repository.")
        return

    # Loop through each day between the start and end date
    curr_date = start_date
    while curr_date <= end_date:
        # Determine if we should commit on this day
        if randint(0, 100) < frequency:
            # Randomize number of commits for this day
            num_commits = randint(15, max_commits)
            for _ in range(num_commits):
                # Randomize commit time within the day
                commit_time = curr_date + timedelta(minutes=randint(0, 1440))  # Random minute in the day
                make_commit(commit_time)
        curr_date += timedelta(days=1)  # Move to the next day

    print('\nRandomized commits \x1b[6;30;42mcompleted successfully\x1b[0m!')


def make_commit(commit_date):
    # Create or update testcommit.json file with each commit
    commit_message = random_message()
    with open("testcommit.json", "a") as file:
        file.write(f'{{"date": "{commit_date.strftime("%Y-%m-%d %H:%M:%S")}", "message": "{commit_message}"}}\n')

    # Stage changes and commit with the specific date
    run(["git", "add", "testcommit.json"])
    run(["git", "commit", "-m", commit_message, "--date", commit_date.strftime("%Y-%m-%d %H:%M:%S")])


def run(commands):
    try:
        process = Popen(commands)
        process.wait()
    except CalledProcessError as e:
        print(f"Error running command {commands}: {e}")


def random_message():
    messages = [
        "Refactor code for performance improvements",
        "Fix minor bug in logic",
        "Update test cases",
        "Add comments for clarity",
        "Code optimization",
        "Enhanced functionality",
        "Resolved merge conflicts",
        "Initial commit",
        "Bug fix and improvements",
        "Cleanup codebase",
        "Documentation updates",
        "Fix typos in comments",
        "Update dependencies"
    ]
    return choice(messages)


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-mc', '--max_commits', type=int, default=30,
                        required=False, help="""Defines the maximum amount of
                        commits a day the script can make. Accepts a number
                        from 15 to 30. The default value is 30.""")
    parser.add_argument('-fr', '--frequency', type=int, default=100,
                        required=False, help="""Percentage of days when the
                        script performs commits. The default value is 100.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()
