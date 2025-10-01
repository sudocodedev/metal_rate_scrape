import argparse

from src.db import create_collection, drop_collection_indexes, migrate_collection


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", choices=["create", "migrate", "dropindex"], type=str, required=True)
    parser.add_argument("-c", "--collection", type=str, required=False, default="")
    args = parser.parse_args()

    if args.action == "create":
        create_collection()
    elif args.action == "migrate":
        migrate_collection()
    elif args.action == "dropindex":
        if not args.collection or not args.collection.strip():
            raise ValueError("collection name can't be blank or empty.")
        drop_collection_indexes(args.collection)
    else:
        return


if __name__ == "__main__":
    main()
