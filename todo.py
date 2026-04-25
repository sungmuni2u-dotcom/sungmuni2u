#!/usr/bin/env python3
"""Simple CLI TODO app."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

DEFAULT_DB_PATH = Path(".todo.json")


@dataclass
class TodoItem:
    id: int
    title: str
    done: bool = False


class TodoStore:
    def __init__(self, path: Path = DEFAULT_DB_PATH):
        self.path = path

    def load(self) -> List[TodoItem]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [TodoItem(**item) for item in raw]

    def save(self, items: List[TodoItem]) -> None:
        payload = [asdict(item) for item in items]
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )


class TodoApp:
    def __init__(self, store: TodoStore):
        self.store = store

    def add(self, title: str) -> TodoItem:
        items = self.store.load()
        next_id = max((item.id for item in items), default=0) + 1
        todo = TodoItem(id=next_id, title=title)
        items.append(todo)
        self.store.save(items)
        return todo

    def list_items(self, show_all: bool = True) -> List[TodoItem]:
        items = self.store.load()
        if show_all:
            return items
        return [item for item in items if not item.done]

    def mark_done(self, item_id: int) -> TodoItem:
        items = self.store.load()
        for item in items:
            if item.id == item_id:
                item.done = True
                self.store.save(items)
                return item
        raise ValueError(f"ID {item_id} 항목을 찾을 수 없습니다.")

    def delete(self, item_id: int) -> TodoItem:
        items = self.store.load()
        for idx, item in enumerate(items):
            if item.id == item_id:
                removed = items.pop(idx)
                self.store.save(items)
                return removed
        raise ValueError(f"ID {item_id} 항목을 찾을 수 없습니다.")

    def clear_done(self) -> int:
        items = self.store.load()
        remaining = [item for item in items if not item.done]
        removed_count = len(items) - len(remaining)
        self.store.save(remaining)
        return removed_count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="TODO 관리 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="할 일 추가")
    add_p.add_argument("title", help="할 일 제목")

    list_p = sub.add_parser("list", help="할 일 목록 보기")
    list_p.add_argument("--open", action="store_true", help="미완료 항목만 보기")

    done_p = sub.add_parser("done", help="할 일 완료 처리")
    done_p.add_argument("id", type=int, help="완료 처리할 ID")

    del_p = sub.add_parser("delete", help="할 일 삭제")
    del_p.add_argument("id", type=int, help="삭제할 ID")

    sub.add_parser("clear-done", help="완료 항목 모두 삭제")

    return parser


def print_items(items: List[TodoItem]) -> None:
    if not items:
        print("할 일이 없습니다.")
        return

    for item in items:
        status = "✅" if item.done else "⬜"
        print(f"{item.id:>3}. {status} {item.title}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    app = TodoApp(TodoStore())

    try:
        if args.command == "add":
            item = app.add(args.title)
            print(f"추가됨: [{item.id}] {item.title}")
            return 0

        if args.command == "list":
            print_items(app.list_items(show_all=not args.open))
            return 0

        if args.command == "done":
            item = app.mark_done(args.id)
            print(f"완료됨: [{item.id}] {item.title}")
            return 0

        if args.command == "delete":
            item = app.delete(args.id)
            print(f"삭제됨: [{item.id}] {item.title}")
            return 0

        if args.command == "clear-done":
            count = app.clear_done()
            print(f"완료 항목 {count}개 삭제")
            return 0

    except ValueError as error:
        print(f"오류: {error}")
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
