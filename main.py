#!/usr/bin/env python3

import camelot
import click
import PyPDF2

from pipetools import pipe


def get_interesting_pdf_pages(pdf):
    with open(pdf, "rb") as f:
        pdf = PyPDF2.PdfFileReader(f)
        n_pages = pdf.getNumPages()

    if n_pages == 3:
        raise ValueError("There are no interesting pages in {}".format(pdf))

    # yikes
    page_range = range(3, n_pages - 1) if n_pages != 4 else [3]

    return [str(page) for page in page_range]


def filter_out_header_and_trailer(table):
    return table[3:-1]


def normalise_characters(rows):
    return [[col.replace("\n", "") for col in row] for row in rows]


def fixup_empty_columns(rows):
    # TODO: implement this
    return rows


process_table = (
    pipe | filter_out_header_and_trailer | normalise_characters | fixup_empty_columns
)


def do_the_thing(pdf):
    print(pdf)
    interesting_pages = get_interesting_pdf_pages(pdf)

    tables = camelot.read_pdf(pdf, pages=",".join(interesting_pages), flavor="stream")
    tables = [process_table(table.data) for table in tables]

    print(tables)


@click.command()
@click.argument("pdf", nargs=-1)
def main(pdf):
    print([do_the_thing(pdf) for pdf in pdf])


if __name__ == "__main__":
    main()
