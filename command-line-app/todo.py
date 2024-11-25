#!/usr/bin/env python

import argparse
import os

TASK_FILE = os.path.expanduser("~/.tasks.txt")

def create_parser():
    parser = argparse.ArgumentParser(description="Command-line Todo List App")
    parser.add_argument("-a", "--add", metavar="", help="Add a new task")
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
    parser.add_argument("-r", "--remove", metavar="", help="Remove a task by index")
    return parser

def add_task(task):
    with open(TASK_FILE, "a") as file:
        file.write(task + "\n")
    print(f"Task added: {task}")

def list_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            tasks = file.readlines()
            if tasks:
                print("Your tasks:")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task.strip()}")
            else:
                print("No tasks found.")
    else:
        print("No tasks found.")

def remove_task(index):
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            tasks = file.readlines()
        if 0 < index <= len(tasks):
            removed_task = tasks.pop(index - 1).strip()
            with open(TASK_FILE, "w") as file:
                file.writelines(tasks)
            print(f"Task removed: {removed_task}")
        else:
            print("Invalid task index.")
    else:
        print("No tasks found.")

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.add:
        add_task(args.add)
    elif args.list:
        list_tasks()
    elif args.remove:
        try:
            remove_task(int(args.remove))
        except ValueError:
            print("Please provide a valid task index.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
