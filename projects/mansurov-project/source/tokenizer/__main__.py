import click

from .tokenizer import tokenizer

@click.group()
def main():
    pass


@main.command()
@click.argument("text", type=str)
def label(text):
    if len("labels") == 0:
        print("No labels found for the given text")
    else:
        print(f"Provided text mentions")

if __name__ == "__main__":
    main()
