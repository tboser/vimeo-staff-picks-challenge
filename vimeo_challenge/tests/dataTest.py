""" Docstring goes here. """  # TODO

import os
import unittest
import pandas as pd

import vimeo_challenge.data as data


class DataTest(unittest.TestCase):
    """ Tests for methods in data.py """

    @classmethod
    def test_to_df(cls):
        """ Test data_to_df() """
        # TODO: generalize base_dir
        # TODO: make sure categories and clips correspond
        base_dir = './data'
        data_df = data.data_to_df(base_dir)

        info_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-clips.csv'))
        cat_df = pd.read_csv(os.path.join(base_dir, 'similar-staff-picks-challenge-clip-categories.csv'))

        assert(data_df['clip_id'].equals(info_df['clip_id']))
        assert(data_df['categories'].sort_values().equals(cat_df['categories'].sort_values()))

    @classmethod
    def test_to_index(cls):
        """ Test data_to_index() """
        # TODO: make this work. need to set up and tear down.

    @classmethod
    def test_to_dict(cls):
        """ Test data_to_dict() """


if __name__ == '__main__':
    unittest.main()
