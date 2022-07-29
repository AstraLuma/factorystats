import csv
import datetime
import re


def parse_time(text):
    text = re.sub(r'\.\d+', '', text)
    if text.endswith('Z'):
        return datetime.datetime.fromisoformat(text[:-1]).replace(tzinfo=datetime.timezone.utc)
    else:
        return datetime.datetime.fromisoformat(text)


TYPES = {
    'string': str,
    'long': int,
    'dateTime:RFC3339': parse_time,
}


def influx_parser(rows):
    casts = []
    columns = []
    looking_for_headers = True
    for row in rows:
        if not row:
            looking_for_headers = True
        elif row[0] == '#group':
            pass
        elif row[0] == '#datatype':
            casts = [TYPES[c]for c in row[1:]]
        elif row[0] == '#default':
            pass
        elif looking_for_headers:
            columns = row[1:]
            looking_for_headers = False
        else:
            yield {
                name: cast(value)
                for value, name, cast in zip(row[1:], columns, casts)
                if name not in ('_start', '_stop', 'result')
            }


if __name__ == '__main__':
    with open('dump.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in influx_parser(reader):
            print(row)
