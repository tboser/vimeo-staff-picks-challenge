""" Docstring goes here. """#TODO

import os
import pandas as pd

from vimeo_challenge.index import index_clip


def data_to_df(base_dir='../data'):
    """ Load Vimeo's staff picks data as pandas dataframe. """
    # cat_metadata_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-categories.csv'))
    clip_info_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-clips.csv'))
    clip_cat_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-clip-categories.csv'))

    clip_info_df = clip_info_df.join(clip_cat_df.set_index('clip_id'),
                                     on='clip_id').drop(clip_info_df.columns[0], axis=1)
    return clip_info_df


def data_to_index(base_dir='../data'):
    """ Insert Vimeo's staff picks data into ES index. """
    df = data_to_df(base_dir)
    for _, row in df.iterrows():
        _ = index_clip(row)


def clips_to_dict(clips):
    """ Return dictionary from list of clips. """
    return {i+1:clip.to_dict() for i, clip in enumerate(clips)}
