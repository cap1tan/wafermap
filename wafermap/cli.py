"""Console script for wafermap."""

import fire


def help():
    print("wafermap")
    print("=" * len("wafermap"))
    print("A python package to plot maps of semiconductor wafers.")


def main():
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
