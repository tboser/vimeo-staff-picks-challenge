#! /usr/bin/env python

""" Command line access to vimeo_challenge. """

import json
import argparse
import warnings

from vimeo_challenge.data import data_to_index, clips_to_list
import vimeo_challenge.index as index

# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


def main():
    """
    Usage: python main.py <clip id> [args]
    For complete information: python main.py -h
    """
    parser = argparse.ArgumentParser(description='Find clips similar to clip_id.',
                                     prefix_chars='-')
    parser.add_argument('clip_id', metavar='<clip id>', default=None, nargs='?')
    parser.add_argument('-f', '--fillIndex', action='store_true', default=False,
                        help='Fill ES index with staff pick data.', dest='fill')
    parser.add_argument('-p', '--dataPath', type=str, default='./data',
                        help='Set base path to staff picks directory.', dest='path')
    parser.add_argument('-s', '--saveModel', action='store_true', default=False,
                        help='Create snapshot of clips index.', dest='save')
    parser.add_argument('-n', '--modelName', type=str, default='clips_snapshot',
                        help='Specify snapshot name when saving/loading.', dest='model_name')
    parser.add_argument('-l', '--loadModel', action='store_true', default=False,
                        help='Restore a snapshot of clips index.', dest='load')
    parser.add_argument('-o', '--hostName', type=str, default='localhost',
                        help='Set elasticsearch host name.', dest='host')
    args = parser.parse_args()

    if args.fill:
        index.initialize_dsl(args.host)
        data_to_index(args.path)

    if args.save:
        index.save_model(args.model_name, args.host)

    if args.load:
        index.load_model(args.model_name, args.host)

    if args.clip_id is not None:
        index.initialize_dsl(args.host)
        similar_clips = index.get_similar_clips(args.clip_id)
        clips_list = clips_to_list(similar_clips)
        print(clips_list)
        print(json.dumps({args.clip_id: clips_list}, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
