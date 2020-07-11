import sys
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('cmd', type=str)
    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit(0)

    if args.cmd == 'migrate':
        from manage import migrate
        migrate.main()


if __name__ == '__main__':
    main()
