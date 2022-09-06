import click

from .tokenizer import tokenize
from .reader import read_emoji_to_label_mapping


@click.group()
def main():
    pass


@main.command()
@click.argument("text", type=str)
def label(text):
    labels = read_emoji_to_label_mapping("assets/emoji-to-label.yml").classify(text)

    if len(labels) == 0:
        print("No labels found for the given text")
    else:
        print(f"Provided text mentions {', '.join(labels)}")

if __name__ == "__main__":
    main()
