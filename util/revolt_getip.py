#!/usr/bin/python3

import os
import argparse
from pathlib import Path


CONFIG_DIR = Path(Path.home(), 'revolt_config')
DATA_FILE = Path(CONFIG_DIR, 'ip_data.csv')


class DataItem:
    def __init__(self, *args):
        self.name = args[0] if len(args) > 0 else ''
        self.ip = args[1] if len(args) > 1 else ''
        self.mac = args[2] if len(args) > 2 else ''
        self.ports = args[3] if len(args) > 3 else ''

    def parse(self, _args: argparse.Namespace) -> None:
        for k in self.__dict__:
            val = getattr(_args, k)
            if val is not None:
                setattr(self, k, val)

    def get_line(self) -> str:
        return ';'.join([self.name, self.ip, self.mac, self.ports])


def parse_args():
    parser = argparse.ArgumentParser(
        description='revolt_getip utility',
        add_help=False
    )

    parser.add_argument('-g', '--get', nargs='?', default=False, const=True)
    parser.add_argument('-s', '--set', nargs='?', default=False, const=True)
    parser.add_argument('-d', '--delete', nargs='?', default=False, const=True)
    parser.add_argument('-n', '--name', required=False)
    parser.add_argument('-i', '--ip', required=False)
    parser.add_argument('-m', '--mac', required=False)
    parser.add_argument('-p', '--ports', required=False)
    parser.add_argument('-h', '--help', action='store_true')

    return parser.parse_args()


def read() -> dict:
    items = {}

    with open(DATA_FILE, 'r') as f:
        for line in f:
            item = DataItem(*[i.strip() for i in line.split(';')])
            items[item.name] = item

    return items


def write(items: dict) -> None:
    with open(DATA_FILE, 'w') as f:
        for item in items.values():
            f.write(f'{item.get_line()}\n')


def find(items: dict, **kwargs: dict) -> list:
    result = []

    keys = {k: kwargs[k] for k in ['name', 'ip', 'mac', 'ports'] if kwargs.get(k, None)}

    for item in items.values():
        if all([getattr(item, k).lowwer() == keys[k].lowwer() for k in keys]):
            result.append(item)

    return result


def get_cmd(_args: argparse.Namespace) -> None:
    params = _args.get.split() if isinstance(_args.get, str) else []
    item = DataItem(*params)
    item.parse(_args)

    items = read()

    _find = find(items, **item.__dict__)

    if len(_find):
        for i in _find:
            print(i.get_line())
    else:
        print('No items found')


def set_cmd(_args: argparse.Namespace) -> None:
    params = args.set.split() if isinstance(_args.set, str) else []
    item = DataItem(*params)
    item.parse(_args)

    if item.name is None:
        raise Exception('Name not found to set')

    items = read()
    items[item.name] = item
    write(items)

    print('Item set successfully')


def del_cmd(_args: argparse.Namespace) -> None:
    params = _args.get.split() if isinstance(_args.get, str) else []
    item = DataItem(*params)
    item.parse(_args)

    if item.name is None:
        raise Exception('Name not found to delete')

    items = read()

    if item.name in items:
        del items[item.name]
        write(items)
        print('Item deleted successfully')
    else:
        print('Item not found')


def help_cmd() -> None:
    msg = ['Usage: revolt_getip [OPTIONS]',
           '',
           'Options:',
           '-g, --get [SEARCH]              Show items, optionally filtered by SEARCH',
           '-s, --set [DATA]                Set item. To set item specify params "name ip mac ports" or set flags',
           '-d, --delete [DATA]             Delete item. To delete item specify params "name ip mac ports" or set flags',
           '-n, --name [NAME]               Set item name',
           '-i, --ip [IP]                   Set item ip',
           '-m, --mac [MAC]                 Set item mac',
           '-p, --ports [PORT1,PORT2, ...]  Set item ports']

    print('\n'.join(msg))


if __name__ == '__main__':
    try:
        if not os.path.isdir(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)

        if not DATA_FILE.exists():
            DATA_FILE.touch()

        args = parse_args()

        if args.get:
            get_cmd(args)
        elif args.set:
            set_cmd(args)
        elif args.delete:
            del_cmd(args)
        else:
            help_cmd()


    except Exception as e:
        print(e)
        exit(1)