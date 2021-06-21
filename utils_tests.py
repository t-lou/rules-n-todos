import utils

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
