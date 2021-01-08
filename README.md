# to remind you of the regular rules and irregular todos

## Run

`python3 rules-n-todos.py` or Wdouble click rules-n-todos.py on Windows.

## Files

- rules.json is for regular rules, that is to-be-done or permitted in some month, day, week, week-day, even-or-odd-number-of-them; example is rules-example.json
- todos.json is for one-time reminder, only trigger on one day by year-month-day; example is todos-examlpe.json

Each of them is skipped if not created

## Functions

- show the todos and rules for today, the next workday, this week and next week
- add and remove rules, each line is one rule, for example *week-day,1,team round*
- add one todo for one day or remove the outdated todos

- reminders for the next workday

![image](https://github.com/t-lou/rules-n-todos/blob/master/screenshots/show-next-day.png)

- reminders for the next week

![image](https://github.com/t-lou/rules-n-todos/blob/master/screenshots/show-next-week.png)

- dialogue for adding and removing rules

![image](https://github.com/t-lou/rules-n-todos/blob/master/screenshots/rules-handling.png)

- window for adding todo and removing old todos

![image](https://github.com/t-lou/rules-n-todos/blob/master/screenshots/todos-handling.png)