import os
import json
import datetime

kFilenameRule = 'rules.json'
kFilenameTodo = 'todos.json'


def unify_int(text: str) -> str:
    try:
        text = str(int(text))
    except:
        pass
    return text


if __name__ == '__main__':
    assert unify_int('1') == '1'
    assert unify_int('01') == '1'
    assert unify_int('001') == '1'
    assert unify_int('10') == '10'
    assert unify_int('day-1') == 'day-1'
    assert unify_int('day') == 'day'
    assert unify_int('') == ''


def find(data: dict, keys: list) -> list:
    if not bool(keys):
        return data
    assert type(data) == dict, f'{data} is not dict'
    assert type(keys) in (tuple, list), f'invalid keys {keys}'
    for key in data:
        if unify_int(key) == keys[0]:
            return find(data[key], keys[1:])
    return None


if __name__ == '__main__':
    assert find('1', []) == '1'
    assert find({'1': 3}, []) == {'1': 3}
    assert find({'1': 3}, ['1']) == 3
    assert find({'01': 3}, ['1']) == 3
    assert find({'001': 3}, ['1']) == 3
    assert find({'1': 3}, ['2']) is None
    assert find({'1': {'2': 3}}, ['1', '2']) == 3
    assert find({'1': {'2': 3}}, ['1', '1']) is None


def display(items: list):
    for i, it in enumerate(items, 1):
        print(f'{i} -\t' + it.replace('\n', '\n\t'))


def show(target_time: datetime.datetime):
    print('On day ' + target_time.strftime('%Y-%m-%d'))
    # summarize this day
    time_text = {
        'year': str(target_time.year),
        'month': str(target_time.month),
        'month-day': str(target_time.day),
        'week': str(target_time.isocalendar()[1]),
        'week-day': str(target_time.isocalendar()[2]),
    }
    time_even_odd = {
        t: 'odd' if int(time_text[t]) % 2 == 1 else 'even'
        for t in time_text
    }

    # if file for rules is available, fine matches and print
    if os.path.isfile(kFilenameRule):
        rules = json.loads(open(kFilenameRule).read())
        for t in rules:
            for v in rules[t]:
                if v == time_text[t]:
                    print(f'Rule on {t} {v}')
                    display(rules[t][v])

    # if file for todos is available, fine matches and print
    if os.path.isfile(kFilenameTodo):
        todos = json.loads(open(kFilenameTodo).read())
        todo = find(
            todos, tuple(time_text[k] for k in ('year', 'month', 'month-day')))
        assert todo is None or type(todo) in (
            tuple, list), f'saved todo {todo} is not a list'
        if todo is not None:
            print('Todo for today is')
            display(todo)
