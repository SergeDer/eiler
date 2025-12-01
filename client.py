"""Простой CLI-клиент для palindrome-сервиса."""

import argparse
import sys
from typing import Iterable

import requests

DEFAULT_URL = "http://localhost:5000/palindromes"


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Отправить строку в palindrome-сервис и получить список палиндромов.",
    )
    parser.add_argument(
        "text",
        help="Строка (до 255 символов), которую нужно отправить.",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Полный URL эндпойнта (по умолчанию {DEFAULT_URL}).",
    )
    return parser.parse_args(argv)


def send_request(text: str, url: str) -> list[str]:
    response = requests.post(url, data=text.encode("utf-8"), headers={"Content-Type": "text/plain"}, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        raise ValueError("Unexpected response format: expected JSON array")
    return payload


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    if len(args.text) > 255:
        print("Ошибка: длина строки должна быть не более 255 символов.", file=sys.stderr)
        return 1

    try:
        palindromes = send_request(args.text, args.url)
    except requests.RequestException as exc:
        print(f"Не удалось выполнить запрос: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("Ответ сервера:")
    for item in palindromes:
        print(f"- {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
