# to remind you of the regular rules and irregular todos

***todo*** make the code and document better, in a rush to make it working

## Files

- rules.json is for regular rules, that is to-be-done or permitted in some month, day, week, week-day, even-or-odd-number-of-them; example is rules-example.json
- todos.json is for one-time reminder, only trigger on one day by year-month-day; example is todos-examlpe.json

Each of them is skipped if not created

## Programs

- show_today.py shows the rules and todos for today
- show_next_day.py shows the rules and todos for the next working day (Saturday not included, you you need it, change the 5 to 6 in code)
- add_todo.py add one todo in file, it can create the file

They shall be executed in bash or Windows file browser directly without parameter.