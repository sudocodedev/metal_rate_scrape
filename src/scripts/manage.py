import argparse

from src.db import create_collection, migrate_collection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", choices=["create", "migrate"], type=str, required=True)
    args = parser.parse_args()

    if args.action == "create":
        create_collection()
    elif args.action == "migrate":
        migrate_collection()
    else:
        return


if __name__ == "__main__":
    main()
