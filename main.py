#! /usr/bin/env python

""" Put docstring here. """  # TODO

import json
import argparse

from vimeo_challenge.data import data_to_index, clips_to_dict
from vimeo_challenge.index import get_similar_clips, initialize_dsl


def main():
    """
    Usage: python main.py <clip id> [args]
    """
    parser = argparse.ArgumentParser(description='Find similar clips from clip id.',
                                     prefix_chars='-')
    parser.add_argument('clip_id', metavar='<clip id>')
    parser.add_argument('-f', '--fillIndex', action='store_true', default=False,
                        help='Fill ES index with staff pick data.', dest='fill')
    parser.add_argument('-p', '--dataPath', type=str, default='./data',
                        help='Set base path to staff picks directory.', dest='path')
    args = parser.parse_args()

    initialize_dsl()

    if args.fill:
        data_to_index(args.path)

    similar_clips = get_similar_clips(args.clip_id)
    clips_dict = clips_to_dict(similar_clips)
    print(json.dumps(clips_dict, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
