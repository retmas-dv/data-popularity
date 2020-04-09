__author__ = 'Dmitry Golubkov'

import datetime
import argparse
from datasets import get_dataset_popularity_by_tasks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--connection', dest='connection_string', type=str, default=None, required=True)
    parser.add_argument(
        '--from', dest='from_date', type=lambda s: datetime.datetime.strptime(s, '%d-%m-%Y'), default=None,
        required=True)
    parser.add_argument(
        '--to', dest='to_date', type=lambda s: datetime.datetime.strptime(s, '%d-%m-%Y'), default=None,
        required=True)
    parser.add_argument('--ignore-tid', dest='ignore_tid', action='store_true', default=False)
    parser.add_argument('--max-length', dest='max_length', type=int, default=None)
    parser.add_argument('--min-value', dest='min_value', type=int, default=None)
    args = parser.parse_args()
    _ = get_dataset_popularity_by_tasks(args.connection_string,
                                        args.from_date,
                                        args.to_date,
                                        args.ignore_tid,
                                        args.max_length,
                                        args.min_value)


if __name__ == "__main__":
    main()
