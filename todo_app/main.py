import argparse
import json
import os
from datetime import datetime

TODO_FILE = "todos.json"

# ANSI-Farben
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)

def save_todos(todos: list):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=4)

def add_todo(title: str, category: str, priority: str):
    todos = load_todos()

    todo = {
        "title": title,
        "category": category,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    todos.append(todo)
    save_todos(todos)
    print(f"{GREEN}Added:{RESET} {title}")

def list_todos(sort_by: str | None = None):
    todos = load_todos()

    if not todos:
        print(f"{YELLOW}No todos yet.{RESET}")
        return

    if sort_by == "priority":
        todos.sort(key=lambda t: t["priority"])
    elif sort_by == "created":
        todos.sort(key=lambda t: t["created_at"])

    for i, t in enumerate(todos, start=1):
        status = f"{GREEN}✓{RESET}" if t["done"] else " "
        print(f"{i}. [{status}] {t['title']} ({t['category']} | {t['priority']})")

def mark_done(index: int):
    todos = load_todos()

    if index < 1 or index > len(todos):
        print(f"{RED}Invalid index.{RESET}")
        return

    todos[index - 1]["done"] = True
    save_todos(todos)
    print(f"{GREEN}Marked as done:{RESET} {todos[index - 1]['title']}")

def delete_todo(index: int):
    todos = load_todos()

    if index < 1 or index > len(todos):
        print(f"{RED}Invalid index.{RESET}")
        return

    removed = todos.pop(index - 1)
    save_todos(todos)
    print(f"{RED}Deleted:{RESET} {removed['title']}")

def filter_todos(by: str, value: str):
    todos = load_todos()

    if not todos:
        print(f"{YELLOW}No todos yet.{RESET}")
        return

    if by == "category":
        filtered = [t for t in todos if t["category"] == value]
    elif by == "priority":
        filtered = [t for t in todos if t["priority"] == value]
    else:
        print(f"{RED}Unknown filter type.{RESET}")
        return

    if not filtered:
        print(f"{YELLOW}No matching todos.{RESET}")
        return

    for i, t in enumerate(filtered, start=1):
        status = f"{GREEN}✓{RESET}" if t["done"] else " "
        print(f"{i}. [{status}] {t['title']} ({t['category']} | {t['priority']})")

def main():
    parser = argparse.ArgumentParser(description="Todo Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("title")
    add_parser.add_argument("category")
    add_parser.add_argument("priority")

    # list
    list_parser = subparsers.add_parser("list", help="List all todos")
    list_parser.add_argument(
        "--sort",
        choices=["priority", "created"],
        help="Sort by priority or created time"
    )

    # done
    done_parser = subparsers.add_parser("done", help="Mark a todo as done")
    done_parser.add_argument("index", type=int, help="Index of the todo")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("index", type=int, help="Index of the todo")

    # filter
    filter_parser = subparsers.add_parser("filter", help="Filter todos")
    filter_parser.add_argument("by", choices=["category", "priority"])
    filter_parser.add_argument("value")

    args = parser.parse_args()

    if args.command == "add":
        add_todo(args.title, args.category, args.priority)

    elif args.command == "list":
        list_todos(args.sort)

    elif args.command == "done":
        mark_done(args.index)

    elif args.command == "delete":
        delete_todo(args.index)

    elif args.command == "filter":
        filter_todos(args.by, args.value)

if __name__ == "__main__":
    main()
