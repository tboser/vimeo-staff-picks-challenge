""" Tests for index.py """

import unittest
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

import vimeo_challenge.index as index
from vimeo_challenge.exceptions import ClipNotFoundException
from vimeo_challenge.data import data_to_index


class IndexTest(unittest.TestCase):
    """ Tests for methods in index.py """
    es = Elasticsearch()

    @classmethod
    def setUpClass(cls):
        connections.create_connection(hosts=['localhost'])

    @classmethod
    def test_initialize(cls):
        """ Test initialize_dsl() """
        index.initialize_dsl()
        assert cls.es.indices.exists(index='clips') is True, 'clips index not created'

    @classmethod
    def test_index_clip(cls):
        """ Test index_clip() """
        clip = {'clip_id': '1', 'title': 'test title', 'caption': 'this is a caption',
                'thumbnail': 'www.thumbnailurl.com', 'categories': '1, 2, 10, 200'}
        _ = index.index_clip(clip)
        out = index.Clip.get(id=clip['clip_id'], ignore=404)

        assert out is not None, 'clip not stored in index'
        assert out.thumbnail == clip['thumbnail'], 'clip not stored properly'

    @classmethod
    def test_get_clip_by_id(cls):
        """ Test get_clip_by_id() """
        clip = {'clip_id': '1', 'title': 'test title', 'caption': 'this is a caption',
                'thumbnail': 'www.thumbnailurl.com', 'categories': '1, 2, 10, 200'}
        _ = index.index_clip(clip)
        out = index.get_clip_by_id(clip['clip_id'])

        assert out is not None, 'clip not stored in index'
        assert out.thumbnail == clip['thumbnail'], 'clip not stored properly'

    @classmethod
    def test_get_similar_clips(cls):
        """ Test get_similar_clips """
        data_to_index('./vimeo_challenge/tests/data')
        assert index.get_clip_by_id(250482473) is not None, 'data loading failed'

        connections.create_connection(hosts=['localhost'])
        similar_clips = index.get_similar_clips(250482473)
        assert len(similar_clips) == 10, 'does not return 10 similar clips'

        try:
            _ = index.get_similar_clips('this is not a clip_id')
            assert True is False, 'finds clip with false id'
        except ClipNotFoundException:
            assert True is True


if __name__ == '__main__':
    unittest.main()
