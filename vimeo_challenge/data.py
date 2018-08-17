""" Methods to handle clips data outside of the Elasticsearch index. """

import os
import pandas as pd

from vimeo_challenge.index import index_clip


def data_to_df(base_dir='../data'):
    """ Load Vimeo's staff picks data as pandas dataframe. """
    # cat_metadata_df could be used to use category name instead of ID number.
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


def clips_to_list(clips):
    """ Return ordered list of clips from results of clips search """
    clips_list = [clip.to_dict() for clip in clips]
    for clip_dict, clip in zip(clips_list, clips):
        clip_dict['clip_id'] = clip.meta.id
    return clips_list
