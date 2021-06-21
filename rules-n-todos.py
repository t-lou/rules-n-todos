import datetime
import json
import os
import tkinter
import tkinter.ttk
import tkinter.messagebox

import utils

# Height of buttons and other components.
kHeightButton = 5
# Width of buttons and other components.
kWidthButton = 80
# Whether Saturday is a working day.
kIsSaturdayWorkday = False
# Delatime of one day.
kOneDay = datetime.timedelta(days=1)
kParamButtonPack = {
    'expand': tkinter.YES,
    'fill': tkinter.X,
    'side': tkinter.TOP
}
kParamTextPack = {
    'expand': tkinter.YES,
    'fill': tkinter.BOTH,
    'side': tkinter.TOP
}
kParamPackLeft = {
    'expand': tkinter.YES,
    'fill': tkinter.BOTH,
    'side': tkinter.LEFT
}


def get_next_day() -> datetime.datetime:
    time = datetime.datetime.now() + kOneDay
    while time.isocalendar()[2] > (6 if kIsSaturdayWorkday else 5):
        time += kOneDay
    return time


def format_date(time: datetime.datetime) -> str:
    return str(time)[:10]


def update_text_this_day():
    text_this_day.config(state='normal')
    text_this_day.delete('1.0', tkinter.END)
    text_this_day.insert(tkinter.END,
                         utils.summarize_day(datetime.datetime.now()))
    text_this_day.config(state='disabled')


def update_next_next_day():
    text_next_day.config(state='normal')
    text_next_day.delete('1.0', tkinter.END)
    text_next_day.insert(tkinter.END, utils.summarize_day(get_next_day()))
    text_next_day.config(state='disabled')


def update_text_this_week():
    text_this_week.config(state='normal')
    text_this_week.delete('1.0', tkinter.END)
    text_this_week.insert(tkinter.END,
                          utils.summarize_week(datetime.datetime.now()))
    text_this_week.config(state='disabled')


def update_next_next_week():
    text_next_week.config(state='normal')
    text_next_week.delete('1.0', tkinter.END)
    text_next_week.insert(
        tkinter.END,
        utils.summarize_week(datetime.datetime.now() +
                             datetime.timedelta(days=7)))
    text_next_week.config(state='disabled')


def update_reminders():
    update_text_this_day()
    update_next_next_day()
    update_text_this_week()
    update_next_next_week()


def init_todo_addtion():
    text_todo_date.delete('1.0', tkinter.END)
    text_todo_content.delete('1.0', tkinter.END)
    text_todo_date.insert(tkinter.END, format_date(datetime.datetime.now()))


def add_todo():
    # load todos if available
    todos = json.loads(open(utils.kFilenameTodo).read()) if os.path.isfile(
        utils.kFilenameTodo) else {}

    date = text_todo_date.get('1.0', tkinter.END).strip()
    content = text_todo_content.get('1.0', tkinter.END).strip()

    if utils.is_date_format_correct(date) and bool(content):
        year, month, day = tuple(str(int(e)) for e in date.split('-'))
        utils.init_dict(todos, (year, month, day), [])

        todos[year][month][day].append(content)
        open(utils.kFilenameTodo, 'w').write(json.dumps(todos, indent=' '))

        init_todo_addtion()
        update_reminders()


def remove_old_todo():
    removed = utils.remove_old_todo()
    if bool(removed):
        text_todo_content.delete('1.0', tkinter.END)
        text_todo_content.insert(
            tkinter.END, 'removed todos\n' + utils.format_list(removed))


def display_rules():
    rules = utils.list_rules()
    text_rules.config(state='normal')
    text_rules.delete('1.0', tkinter.END)
    text_rules.insert(tkinter.END,
                      '\n'.join(', '.join(rule) for rule in rules))
    text_rules.config(state='disabled')


def clean_rule_text(text: str) -> list:
    elem_rules = tuple(line.strip().split(',') for line in text.split('\n')
                       if bool(line.strip()))
    assert all(len(elems) >= 3 for elems in elem_rules), 'not enough elements'
    rules = tuple(
        (elems[0].strip(), elems[1].strip(), ','.join(elems[2:]).strip())
        for elems in elem_rules)
    assert all(elems[0] in ('month', 'month-day', 'week', 'week-day') for elems in rules), \
        f'invalid first element, must be one of month, month-day, week, week-day'
    assert all(elems[1] in ('even', 'odd') or elems[1].isdigit() for elems in rules), \
        f'invalid second element, must be even, odd or a number'
    return rules


def add_rule():
    def add_rule_impl():
        rules = clean_rule_text(text_new_rules.get('1.0', tkinter.END))
        utils.add_rules(rules)
        text_new_rules.delete('1.0', tkinter.END)
        display_rules()
        update_reminders()

    window_add = tkinter.Tk()
    window_add.title('add rules')

    explanation = ('add rules in text field, each line for one rule:', '',
                   'month, even, rule for even months',
                   'week-day, 1, rule for monday')
    tkinter.Label(window_add,
                  text='\n'.join(explanation),
                  width=kWidthButton,
                  height=kHeightButton,
                  justify=tkinter.LEFT).pack()

    text_new_rules = tkinter.Text(window_add,
                                  width=kWidthButton,
                                  height=kHeightButton * 3)
    text_new_rules.pack(**kParamTextPack)

    tkinter.Button(window_add,
                   text='add',
                   height=kHeightButton,
                   width=kWidthButton,
                   command=add_rule_impl).pack(**kParamButtonPack)


def remove_rule():
    def remove_rule_impl():
        rules = clean_rule_text(text_new_rules.get('1.0', tkinter.END))
        utils.remove_rules(rules)
        text_new_rules.delete('1.0', tkinter.END)
        display_rules()
        update_reminders()

    window_remove_rule = tkinter.Tk()
    window_remove_rule.title('remove rules')

    explanation = ('remove rules in text field, each line for one rule:',
                   '(action will take place when all at exact matches)',
                   'month, even, rule for even months',
                   'week-day, 1, rule for monday')
    tkinter.Label(window_remove_rule,
                  text='\n'.join(explanation),
                  width=kWidthButton,
                  height=kHeightButton,
                  justify=tkinter.LEFT).pack()

    text_new_rules = tkinter.Text(window_remove_rule,
                                  width=kWidthButton,
                                  height=kHeightButton * 3)
    text_new_rules.pack(**kParamTextPack)

    tkinter.Button(window_remove_rule,
                   text='remove',
                   height=kHeightButton,
                   width=kWidthButton,
                   command=remove_rule_impl).pack(**kParamButtonPack)


def set_todo_date_next_day():
    text_todo_date.delete('1.0', tkinter.END)
    text_todo_date.insert(tkinter.END, format_date(get_next_day()))


def set_todo_date_next_week():
    text_todo_date.delete('1.0', tkinter.END)
    text_todo_date.insert(
        tkinter.END,
        format_date(datetime.datetime.now() + datetime.timedelta(days=7)))


base_window = tkinter.Tk()
base_window.title('rules-n-todos')

tab_container = tkinter.ttk.Notebook(base_window)
frame_this_day = tkinter.Frame(tab_container)
frame_next_day = tkinter.Frame(tab_container)
frame_this_week = tkinter.Frame(tab_container)
frame_next_week = tkinter.Frame(tab_container)
frame_handle_rule = tkinter.Frame(tab_container)
frame_handle_todo = tkinter.Frame(tab_container)
frame_calendar = tkinter.Frame(tab_container)

# for tab this day
text_this_day = tkinter.Text(frame_this_day,
                             width=kWidthButton,
                             height=kHeightButton * 5,
                             state=tkinter.DISABLED)
text_this_day.bind('<1>', lambda event: text_this_day.focus_set())
update_text_this_day()
text_this_day.pack(**kParamTextPack)

tkinter.Button(frame_this_day,
               text='refresh',
               height=kHeightButton,
               width=kWidthButton,
               command=update_text_this_day).pack(**kParamButtonPack)

# for tab next day
text_next_day = tkinter.Text(frame_next_day,
                             width=kWidthButton,
                             height=kHeightButton * 5,
                             state=tkinter.DISABLED)
text_next_day.bind('<1>', lambda event: text_next_day.focus_set())
update_next_next_day()
text_next_day.pack(**kParamTextPack)

tkinter.Button(frame_next_day,
               text='refresh',
               height=kHeightButton,
               width=kWidthButton,
               command=update_next_next_day).pack(**kParamButtonPack)

# for tab this week
text_this_week = tkinter.Text(frame_this_week,
                              width=kWidthButton,
                              height=kHeightButton * 5,
                              state=tkinter.DISABLED)
text_this_week.bind('<1>', lambda event: text_this_week.focus_set())
update_text_this_week()
text_this_week.pack(**kParamTextPack)

tkinter.Button(frame_this_week,
               text='refresh',
               height=kHeightButton,
               width=kWidthButton,
               command=update_text_this_week).pack(**kParamButtonPack)

# for tab next week
text_next_week = tkinter.Text(frame_next_week,
                              width=kWidthButton,
                              height=kHeightButton * 5,
                              state=tkinter.DISABLED)
text_next_week.bind('<1>', lambda event: text_next_week.focus_set())
update_next_next_week()
text_next_week.pack(**kParamTextPack)

tkinter.Button(frame_next_week,
               text='refresh',
               height=kHeightButton,
               width=kWidthButton,
               command=update_next_next_week).pack(**kParamButtonPack)

# for tab handle rule
text_rules = tkinter.Text(frame_handle_rule,
                          height=kHeightButton * 3,
                          width=kWidthButton,
                          state=tkinter.DISABLED)
text_rules.bind('<1>', lambda event: text_rules.focus_set())
display_rules()
text_rules.pack(**kParamTextPack)

tkinter.Button(frame_handle_rule,
               text='add',
               height=kHeightButton,
               width=kWidthButton,
               command=add_rule).pack(**kParamButtonPack)
tkinter.Button(frame_handle_rule,
               text='remove',
               height=kHeightButton,
               width=kWidthButton,
               command=remove_rule).pack(**kParamButtonPack)

# for tab handle todo
frame_todo_date = tkinter.Frame(frame_handle_todo)
text_todo_date = tkinter.Text(frame_todo_date,
                              height=3,
                              width=kWidthButton // 4)
text_todo_date.pack(**kParamPackLeft)
tkinter.Button(frame_todo_date,
               height=3,
               width=kWidthButton // 4,
               text='next day',
               command=set_todo_date_next_day).pack(**kParamPackLeft)
tkinter.Button(frame_todo_date,
               height=3,
               width=kWidthButton // 4,
               text='same day next week',
               command=set_todo_date_next_week).pack(**kParamPackLeft)
text_todo_content = tkinter.Text(frame_handle_todo,
                                 height=kHeightButton * 3,
                                 width=kWidthButton)
frame_todo_date.pack(**kParamTextPack)
text_todo_content.pack(**kParamTextPack)
tkinter.Button(frame_handle_todo,
               text='add',
               height=kHeightButton,
               width=kWidthButton,
               command=add_todo).pack(**kParamButtonPack)
tkinter.Button(frame_handle_todo,
               text='remove old',
               height=kHeightButton,
               width=kWidthButton,
               command=remove_old_todo).pack(**kParamButtonPack)
init_todo_addtion()


# for table calendar
def update_calendar():
    today = datetime.datetime.now()
    date = today - datetime.timedelta(days=(
        today.isocalendar()[2] - 1)) + datetime.timedelta(days=(7 * w_offset))
    for w in range(n_week):
        for d in range(7):
            buttons_cw[w].configure(text=f'CW{date.isocalendar()[1]}')
            buttons_calendar[w][d].configure(text=f'{date.month}-{date.day}')
            is_today = today.year == date.year and today.month == date.month and today.day == date.day
            buttons_calendar[w][d].configure(
                bg='grey' if is_today else 'white')
            buttons_calendar[w][d].configure(
                fg='white' if is_today else 'black')
            date += kOneDay


def navi_week(row: int):
    global w_offset
    w_offset += row - (n_week // 2)
    update_calendar()


def disp_date(row: int, col: int):
    today = datetime.datetime.now()
    date = today - datetime.timedelta(days=(
        today.isocalendar()[2] - 1)) + datetime.timedelta(days=(7 * w_offset))
    date += datetime.timedelta(days=(7 * row + col))

    display = tkinter.Tk()
    display.title(str(date)[:10])
    text_display = tkinter.Text(display,
                                width=kWidthButton,
                                height=kHeightButton * 5)
    text_display.insert(tkinter.END, utils.summarize_day(date))

    text_display.config(state='disabled')
    text_display.bind('<1>', lambda event: text_next_day.focus_set())
    text_display.pack(**kParamTextPack)


n_week = 9
w_offset = -(n_week // 2)
width_calendar_item = kWidthButton // 11
height_calendar_item = 2
buttons_calendar = tuple(
    tuple(
        tkinter.Button(frame_calendar,
                       height=height_calendar_item,
                       width=width_calendar_item,
                       command=lambda x=r, y=c: disp_date(x, y))
        for c in range(7)) for r in range(n_week))
buttons_cw = tuple(
    tkinter.Button(frame_calendar,
                   height=height_calendar_item,
                   width=width_calendar_item,
                   command=lambda x=r: navi_week(x)) for r in range(n_week))
for w in range(n_week):
    for d in range(7):
        buttons_cw[w].grid(column=0, row=(w + 1))
        buttons_cw[w].configure(text=f'CW{w}')
        buttons_calendar[w][d].grid(column=(d + 1), row=(w + 1))
        buttons_calendar[w][d].configure(text=f'{w}-{d}')

update_calendar()

tab_container.add(frame_this_day, text='this day')
tab_container.add(frame_next_day, text='next day')
tab_container.add(frame_this_week, text='this week')
tab_container.add(frame_next_week, text='next week')
tab_container.add(frame_handle_rule, text='handle rule')
tab_container.add(frame_handle_todo, text='handle todo')
tab_container.add(frame_calendar, text='calendar')

tab_container.pack(**kParamTextPack)

tkinter.mainloop()
