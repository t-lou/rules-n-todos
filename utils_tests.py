import utils
import os
import datetime

assert utils.unify_int('1') == '1'
assert utils.unify_int('01') == '1'
assert utils.unify_int('001') == '1'
assert utils.unify_int('10') == '10'
assert utils.unify_int('day-1') == 'day-1'
assert utils.unify_int('day') == 'day'
assert utils.unify_int('') == ''

assert utils.find('1', []) == '1'
assert utils.find({'1': 3}, []) == {'1': 3}
assert utils.find({'1': 3}, ['1']) == 3
assert utils.find({'01': 3}, ['1']) == 3
assert utils.find({'001': 3}, ['1']) == 3
assert utils.find({'1': 3}, ['2']) is None
assert utils.find({'1': {'2': 3}}, ['1', '2']) == 3
assert utils.find({'1': {'2': 3}}, ['1', '1']) is None

assert not utils.is_date_format_correct('')
assert not utils.is_date_format_correct('abcd')
assert not utils.is_date_format_correct('1234')
assert not utils.is_date_format_correct('12345678')
assert not utils.is_date_format_correct('1234/56/78')
assert not utils.is_date_format_correct('12.34.5678')
assert not utils.is_date_format_correct('1234-56-78')
assert utils.is_date_format_correct('1992-01-15')


def test_progress():
    path_file = '.progress.json'
    path_back = '.progress.json.back'
    if os.path.isfile(path_file):
        os.rename(path_file, path_back)

    handler = utils.ProgressHandler()
    assert handler.get_names() == tuple()

    handler.add_progress('t1', datetime.datetime(1991, 5, 22),
                         datetime.datetime(1992, 1, 15))
    assert handler.get_names() == ('t1', )
    assert handler.get_details('t1') == {
        'start': datetime.datetime(1991, 5, 22),
        'end': datetime.datetime(1992, 1, 15),
        'progress': -1
    }
    assert handler.get_details('t2') == None

    handler.save_progress()
    handler1 = utils.ProgressHandler()
    assert handler1.get_names() == ('t1', )
    assert handler1.get_details('t1') == {
        'start': datetime.datetime(1991, 5, 22),
        'end': datetime.datetime(1992, 1, 15),
        'progress': -1
    }
    assert handler1.get_details('t2') == None

    assert handler.get_progress('t2', datetime.datetime(1992, 1, 15)) == None
    assert handler.get_progress('t1') == 100
    assert handler.get_progress('t1', datetime.datetime(1992, 1, 15)) == 100
    assert handler.get_progress('t1', datetime.datetime(1991, 5, 22)) == 0
    assert 0 < handler.get_progress('t1', datetime.datetime(1992, 1, 1)) < 100

    if os.path.isfile(path_back):
        os.rename(path_back, path_file)


test_progress()
