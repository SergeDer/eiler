from flask import Flask, abort, jsonify, request

app = Flask(__name__)


def _extract_text_from_request() -> str:
    if request.is_json:
        data = request.get_json(silent=True) or {}
        text = data.get("text") if isinstance(data, dict) else None
    else:
        text = request.get_data(as_text=True)

    if text is None:
        abort(400, description="Request body must contain text content.")
    if not isinstance(text, str):
        abort(400, description="Provided text must be a string.")

    return text


def find_palindromes(text: str) -> list[str]:
    palindromes: list[str] = []
    seen: set[str] = set()
    n = len(text)

    for length in range(n, 1, -1):
        for start in range(0, n - length + 1):
            substring = text[start : start + length]
            if substring in seen:
                continue
            if substring == substring[::-1]:
                seen.add(substring)
                palindromes.append(substring)

    return palindromes


@app.post("/palindromes")
def palindromes_endpoint():
    text = _extract_text_from_request()
    if len(text) > 255:
        abort(400, description="Text must be 255 characters or fewer.")

    palindromes = find_palindromes(text)
    return jsonify(palindromes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
