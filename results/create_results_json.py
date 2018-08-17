#! /usr/bin/env python

""" Script for building results.json """

import json

import vimeo_challenge.index as index
from vimeo_challenge.data import clips_to_list


def main():
    index.initialize_dsl()
    index.load_model('clips_snapshot', 'localhost')

    clip_ids = [14434107, 249393804, 71964690, 78106175, 228236677, 11374425, 93951774, 35616659, 112360862, 116368488]
    results = {}
    for clip_id in clip_ids:
        results[clip_id] = clips_to_list(index.get_similar_clips(clip_id))

    with open('results/results.json', 'w') as outfile:
        json.dump(results, outfile)


if __name__ == '__main__':
    main()
