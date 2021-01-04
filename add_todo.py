import json
import re
import os

kFilenameTodo = 'todos.json'


def is_date_format_correct(text: str) -> bool:
    pattern = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
    return bool(re.findall(pattern, text))


assert not is_date_format_correct('abcd')
assert not is_date_format_correct('1234')
assert not is_date_format_correct('12345678')
assert not is_date_format_correct('1234/56/78')
assert not is_date_format_correct('12.34.5678')
assert is_date_format_correct('1234-56-78')

# load todos if available
todos = json.loads(
    open(kFilenameTodo).read()) if os.path.isfile(kFilenameTodo) else {}

# input date
date = input('write date in YYYY-MM-DD ')
assert is_date_format_correct(date), 'wrong format'
year, month, day = tuple(str(int(e)) for e in date.split('-'))
# prepare slot for today
if year not in todos:
    todos[year] = {}
if month not in todos[year]:
    todos[year][month] = {}
if day not in todos[year][month]:
    todos[year][month][day] = []

# add todo
todo_text = []
line = input('write todo, click another ENTER when finished ')
while bool(line):
    if not bool(line):
        break
    todo_text.append(line)
    line = input('')
assert bool(todo_text), 'empty input'
todos[year][month][day].append('\n'.join(todo_text))
open(kFilenameTodo, 'w').write(json.dumps(todos, indent=' '))