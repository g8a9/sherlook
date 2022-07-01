"""Console script for sherlook."""
import sys
import click
from sentence_transformers import SentenceTransformer, util
import torch
from . import bibtex
from pathlib import Path
import os


ANTHOLOGY_PATH = os.path.join(Path.home(), "anthology.bib")
ANTHOLOGY_EMBEDDINGS_PATH = os.path.join(Path.home(), "acltitle_embeds.pt")


def find_topk(query, embeddings, model, k=3):
    query_emb = model.encode(query, device="cpu")
    cos_scores = util.cos_sim(query_emb, embeddings)
    top_results = torch.topk(cos_scores, k=k)
    return top_results.indices[0]


@click.command()
def main(args=None):
    """Console script for sherlook."""

    click.echo("Loading model...")
    model = SentenceTransformer("all-mpnet-base-v2")
    click.echo("Loading embeddings...")
    anth_embeds = torch.load(ANTHOLOGY_EMBEDDINGS_PATH).cpu()

    anthology = bibtex.read_bibtex(ANTHOLOGY_PATH)
    key2title = {k: v.fields["title"] for k, v in anthology.entries.items()}
    titles = list(key2title.values())

    idx2persons = {
        idx: v.persons for idx, (_, v) in enumerate(anthology.entries.items())
    }
    idx2bibkey = {idx: k for idx, (k, _) in enumerate(anthology.entries.items())}
    idx2title = {k: v for k, v in enumerate(titles)}

    click.echo("Insert queries to search the ACL Anthology")

    try:
        while True:
            query = input(">> ")
            if query == "exit":
                break

            top_results = find_topk(query, anth_embeds, model)

            click.echo("")
            click.echo("")

            for idx in top_results:
                click.echo(f"Bibkey: {idx2bibkey[idx.item()]}")
                click.echo(f"Title: {idx2title[idx.item()]}")
                click.echo(f"Persons: {idx2persons[idx.item()]}")

                click.echo("---" * 4)

            click.echo("")
            click.echo("")

    except KeyboardInterrupt:
        return

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
