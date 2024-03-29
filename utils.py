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


def find(data: dict, keys: list) -> list:
    if not bool(keys):
        return data
    assert type(data) == dict, f'{data} is not dict'
    assert type(keys) in (tuple, list), f'invalid keys {keys}'
    for key in data:
        if unify_int(key) == keys[0]:
            return find(data[key], keys[1:])
    return None


def format_list(items: list) -> str:
    return '\n'.join(f'{i} -\t' + it.replace('\n', '\n\t')
                     for i, it in enumerate(items, 1)) + '\n'


class TodoHandler(object):
    def __init__(self):
        self._todos = json.loads(open(kFilenameTodo).read()) if os.path.isfile(
            kFilenameTodo) else dict()

    def get_on_day(self, target_time: datetime.datetime) -> list:
        keys = [
            str(i)
            for i in (target_time.year, target_time.month, target_time.day)
        ]
        return find(self._todos, keys)


def summarize_rules(time_attributes: dict) -> str:
    text = ''

    # summarize this day
    time_text = {t: str(time_attributes[t]) for t in time_attributes}
    time_even_odd = {
        t: 'odd' if time_attributes[t] % 2 == 1 else 'even'
        for t in time_attributes
    }

    # if file for rules is available, fine matches and print
    if os.path.isfile(kFilenameRule):
        rules = json.loads(open(kFilenameRule).read())
        for t in tuple(t for t in rules if t in time_attributes):
            for v in rules[t]:
                if v == time_text[t]:
                    text += f'Rule on {t} {v}\n' + format_list(
                        rules[t][v]) + '\n'
                if v == time_even_odd[t]:
                    text += f'Rule on {t} {v}\n' + format_list(
                        rules[t][v]) + '\n'

    return text


def summarize_day(target_time: datetime.datetime) -> str:
    text = 'On day ' + target_time.strftime(
        '%Y-%m-%d') + f' CW{target_time.isocalendar()[1]} \n\n'
    # summarize this day
    time_attributes = {
        'year': target_time.year,
        'month': target_time.month,
        'month-day': target_time.day,
        'week': target_time.isocalendar()[1],
        'week-day': target_time.isocalendar()[2],
    }
    text += summarize_rules(time_attributes)

    todo = TodoHandler().get_on_day(target_time)
    assert todo is None or type(todo) in (
        tuple, list), f'saved todo {todo} is not a list'
    if todo is not None:
        text += 'Todo is\n' + format_list(todo) + '\n'
    return text


def summarize_week(target_time: datetime.datetime) -> str:
    text = f'On CW{target_time.isocalendar()[1]} \n\n'
    # summarize this day
    time_attributes = {
        'year': target_time.year,
        'month': target_time.month,
        'week': target_time.isocalendar()[1],
    }
    text += summarize_rules(time_attributes)

    # if file for todos is available, fine matches and print
    if os.path.isfile(kFilenameTodo):
        todos = json.loads(open(kFilenameTodo).read())
        todo = find(todos,
                    tuple(str(time_attributes[k]) for k in ('year', 'month')))
        assert todo is None or type(
            todo) == dict, f'saved todo {todo} is not dict for a month'
        if todo is not None:
            todo_all = []
            isocalendar = target_time.isocalendar()
            days = tuple(
                str(
                    datetime.datetime.fromisocalendar(isocalendar[0],
                                                      isocalendar[1], d).day)
                for d in range(1, 8))
            for t in days:
                if t in todo and todo[t] not in todo_all:
                    todo_all += todo[t]
            text += 'Todo is\n' + format_list(todo_all) + '\n'
    return text


def is_date_format_correct(text: str) -> bool:
    try:
        datetime.datetime.fromisoformat(text)
    except:
        return False
    return True


def remove_old_todo():
    def clean_lower_entry(data: dict, bounds: list, removed=list):
        if bool(bounds):
            for key in tuple(data.keys()):
                num = int(key)
                if num < bounds[0]:
                    if len(bounds) == 1:
                        removed += data[key]
                    [
                        clean_lower_entry(elem, bounds[1:], removed)
                        for elem in data.values()
                    ]
                    data.pop(key)
                elif num == bounds[0]:
                    clean_lower_entry(data[key], bounds[1:], removed)
                    if not bool(data[key]):
                        data.pop(key)

    removed = []
    if os.path.isfile(kFilenameTodo):
        todos = json.loads(open(kFilenameTodo).read())
        now = datetime.datetime.now()
        clean_lower_entry(todos, (now.year, now.month, now.day), removed)
        open(kFilenameTodo, 'w').write(json.dumps(todos, indent=' '))

    return removed


def list_rules() -> tuple:
    rules = []
    if os.path.isfile(kFilenameRule):
        saved_rules = json.loads(open(kFilenameRule).read())
        for interval in saved_rules:
            for occurrence in saved_rules[interval]:
                for rule in saved_rules[interval][occurrence]:
                    rules.append((interval, occurrence, rule))
    return rules


def init_dict(data: dict, keys: tuple, init_value):
    if bool(keys):
        if keys[0] not in data:
            data[keys[0]] = {} if len(keys) > 1 else init_value
        init_dict(data[keys[0]], keys[1:], init_value)


def add_rules(rules: list):
    defined_rules = json.loads(
        open(kFilenameRule).read()) if os.path.isfile(kFilenameRule) else {}
    for rule in rules:
        init_dict(defined_rules, rule[:2], [])
        defined_rules[rule[0]][rule[1]].append(rule[2])
    open(kFilenameRule, 'w').write(json.dumps(defined_rules, indent=' '))


def remove_rules(rules: list):
    defined_rules = json.loads(
        open(kFilenameRule).read()) if os.path.isfile(kFilenameRule) else {}
    assert all(rule[0] in defined_rules \
                and rule[1] in defined_rules[rule[0]] \
                and rule[2] in defined_rules[rule[0]][rule[1]] \
            for rule in rules), \
        'at least one rule is not found'
    for rule in rules:
        defined_rules[rule[0]][rule[1]] = [
            content for content in defined_rules[rule[0]][rule[1]]
            if content != rule[2]
        ]
    open(kFilenameRule, 'w').write(json.dumps(defined_rules, indent=' '))


class ProgressHandler(object):
    def __init__(self):
        self._path = '.progress.json'
        self._date_format = '%Y-%m-%d'
        self._progresses = self.load_progress()

    def get_names(self) -> tuple:
        return tuple(self._progresses.keys())

    def get_details(self, name: str) -> dict:
        return self._progresses[name] if name in self._progresses else None

    def load_progress(self) -> dict:
        progresses = json.loads(open(self._path).read()) if os.path.isfile(
            self._path) else {}
        return {
            name: {
                'start':
                datetime.datetime.strptime(progresses[name]['start'],
                                           self._date_format),
                'end':
                datetime.datetime.strptime(progresses[name]['end'],
                                           self._date_format),
                'progress':
                progresses[name]['progress'],
            }
            for name in progresses
        }

    def _get_date(self, date_start: datetime.datetime) -> datetime.datetime:
        return datetime.datetime(year=date_start.year,
                                 month=date_start.month,
                                 day=date_start.day)

    def add_progress(self,
                     name: str,
                     date_start: datetime.datetime,
                     date_end: datetime.datetime,
                     progress: int = -1):
        date_end = self._get_date(date_end)
        date_start = self._get_date(date_start)
        assert date_end >= date_start, 'end before start'
        self._progresses[name] = {
            'start': date_start,
            'end': date_end,
            'progress': progress,
        }

    def get_progress(self, name: str, date: datetime.datetime = None) -> int:
        if name not in self._progresses:
            return None
        detail = self._progresses[name]
        if detail['progress'] >= 0:
            return detail['progress']
        date = self._get_date(
            date if date is not None else datetime.datetime.now())
        return max(
            0,
            min(
                100,
                int(100.0 * (date - detail['start']).days /
                    (detail['end'] - detail['start']).days)))

    def save_progress(self):
        open(self._path, 'w').write(
            json.dumps(
                {
                    name: {
                        'start':
                        self._progresses[name]['start'].strftime(
                            self._date_format),
                        'end':
                        self._progresses[name]['end'].strftime(
                            self._date_format),
                        'progress':
                        self._progresses[name]['progress'],
                    }
                    for name in self._progresses
                },
                indent=' '))
