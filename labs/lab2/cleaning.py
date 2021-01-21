#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Lisa Korotkova, Mark Fishel

import os
import sys
import logging
from argparse import ArgumentParser

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def filter_lines(src_lines, tgt_lines):
    """
    Discard pairs with empty sentences
    and with sentence length ratio exceeding 9
    """
    # Check that files have the same length
    assert len(src_lines) == len(
        tgt_lines), 'Source and target side not parallel'

    raw_result = [sent_pair for sent_pair in zip(src_lines, tgt_lines) if
                  pair_ok(*sent_pair)]
    (src_result, tgt_result) = zip(*raw_result)

    return src_result, tgt_result


def pair_ok(src_sent, tgt_sent):
    """
    Returns False if either of the sentences is an empty string
    or if length ratio exceeds 9
    """
    # Check for empty strings
    if len(src_sent) == 0 or len(tgt_sent) == 0:
        return False

    # Calculate length ratio
    src_len, tgt_len = len(src_sent.split(" ")), len(tgt_sent.split(" "))
    ratio = src_len / tgt_len if src_len > tgt_len else tgt_len / src_len

    return src_len <= 100 and tgt_len <= 100 and ratio < 9


def filter_files(src_file, tgt_file, src_res, tgt_res):
    logging.info('Cleaning {} and {}'.format(src_file, tgt_file))

    # Read in source and target sentences
    with open(src_file, 'r', encoding='utf-8') as src_fh:
        src_lines = [line.strip() for line in src_fh.readlines()]
    with open(tgt_file, 'r', encoding='utf-8') as tgt_fh:
        tgt_lines = [line.strip() for line in tgt_fh.readlines()]
    # Filter out bad sentence pairs
    result = filter_lines(src_lines, tgt_lines)

    # Write result
    with open(src_res, 'w', encoding='utf-8') as src_r:
        src_r.writelines('\n'.join(result[0]))
    with open(tgt_res, 'w', encoding='utf-8') as tgt_r:
        tgt_r.writelines('\n'.join(result[1]))

    logging.info('Done')

if __name__ == '__main__':
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("--corpora", help="Input filenames prefix ")
    parser.add_argument("--output", help="Cleaned filenames prefix")
    parser.add_argument("--src_lang", help="Source language extension")
    parser.add_argument("--tgt_lang", help="Target language extension")

    args = parser.parse_args()

    # Generate file names
    src_in = '{}.{}'.format(args.corpora, args.src_lang)
    tgt_in = '{}.{}'.format(args.corpora, args.tgt_lang)
    src_out = '{}.{}'.format(args.output, args.src_lang)
    tgt_out = '{}.{}'.format(args.output, args.tgt_lang)

    # Clean the files
    filter_files(src_in, tgt_in, src_out, tgt_out)
