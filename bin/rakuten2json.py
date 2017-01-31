#!/usr/bin/python3

import json
import multiprocessing
import os
import os.path

import gargparse
from gargparse import ARGS
import langdetect
import nltokeniz


gargparse.add_argument('--train_data_size', type=int, required=True)
gargparse.add_argument('--develop_data_size', type=int, required=True)
gargparse.add_argument('--test_data_size', type=int, required=True)
gargparse.add_argument('example_filename')
gargparse.add_argument('output_dirname', default='.', nargs='?')


def write_json_file(line, data_dir):
    records = line.split('\t')
    assert len(records) == 9

    try:
        document = nltokeniz.tokenize(records[-1])
    except langdetect.lang_detect_exception.LangDetectException as e:
        document = [[records[-1]]]

    example = {
        'id': int(records[0]),
        'document': document,
        'label': {
            'multi': [int(label) for label in records[1:-1]],
        },
    }

    with open(os.path.join(data_dir, str(example['id'])) + '.json', 'w') \
            as phile:
        json.dump(example, phile, ensure_ascii=False, indent='\t')


def repeat(x):
    while True:
        yield x


def main():
    with open(ARGS.example_filename) as phile:
        lines = phile.readlines()

    for data_use in ['train', 'develop', 'test']:
        data_dir = os.path.join(ARGS.output_dirname, data_use)
        os.makedirs(data_dir, exist_ok=True)

        data_size = getattr(ARGS, data_use + '_data_size')
        lines_for_me, lines = lines[:data_size], lines[data_size:]

        multiprocessing.Pool().starmap(write_json_file,
                                       zip(lines_for_me, repeat(data_dir)))


if __name__ == '__main__':
    main()
