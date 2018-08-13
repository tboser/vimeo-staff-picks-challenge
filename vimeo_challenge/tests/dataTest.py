""" Docstring goes here. """  # TODO

import os
import unittest
import pandas as pd
from elasticsearch_dsl.connections import connections

import vimeo_challenge.data as data
from vimeo_challenge.index import get_clip_by_id

class DataTest(unittest.TestCase):
    """ Tests for methods in data.py """

    @classmethod
    def setUpClass(cls):
        connections.create_connection(hosts=['localhost'])

    @classmethod
    def test_to_df(cls):
        """ Test data_to_df() """
        # TODO: generalize base_dir
        # TODO: make sure categories and clips correspond
        base_dir = './vimeo_challenge/tests/data'
        data_df = data.data_to_df(base_dir)

        info_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-clips.csv'))

        assert data_df['clip_id'].equals(info_df['clip_id'])

    @classmethod
    def test_to_index(cls):
        """ Test data_to_index() """
        base_dir = './vimeo_challenge/tests/data'
        data.data_to_index(base_dir)

        clip = get_clip_by_id(250482473)
        assert clip is not None, 'clips not stored in index'

    @classmethod
    def test_to_dict(cls):
        """ Test data_to_dict() """
        clip = get_clip_by_id(250482473)
        assert clip is not None, 'clips not stored in index'

        clip_dict = data.clips_to_dict([clip])
        assert type(clip_dict) == dict, 'clip_to_dict failed'


if __name__ == '__main__':
    unittest.main()
