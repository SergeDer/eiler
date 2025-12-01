# eiler

Простой веб-сервис на Flask с одним POST-эндпойнтом `/palindromes`, который принимает строку (до 255 символов) и возвращает список её непустых подстрок-палиндромов длиной два символа и больше.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Сервис запустится на `http://localhost:5000`.

## Пример запроса

Отправка сырого текстового тела или JSON с ключом `text`:

```bash
curl -X POST http://localhost:5000/palindromes \
  -H "Content-Type: text/plain" \
  --data "анна"
```

Успешный ответ:

```json
["анна", "нн"]
```
