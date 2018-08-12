""" Docstring goes here. """#TODO

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, analyzer
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis
# from elasticsearch import Elasticsearch

from vimeo_challenge.exceptions import ClipNotFoundException


class Clip(Document):
    """
    All information relating to a clip from Vimeo's staff picks.
    """
    title = Text(analyzer='snowball')
    caption = Text(analyzer='snowball')
    thumbnail = Text()
    categories = Keyword(multi=True)

    class Index:
        """ Default index used for storing clips. """
        name = 'clips'

    def save(self, **kwargs):
        """ Save Clip to ES index. """
        return super(Clip, self).save(**kwargs)


def initialize_dsl():
    """ Initialize Clip persistent layer, connect to index. """
    connections.create_connection(hosts=['localhost'])
    #
    # es = Elasticsearch()
    # if not es.indices.exists(index='clips'):
    #     es.index(index='clips', body={})
    #
    Clip.init()


def index_clip(clip):
    """ Index clip in form of dictionary or Pandas row. """
    categories = [0]
    try:
        categories.extend([int(i) for i in clip['categories'].replace(' ', '').split(',')])  # TODO this should be handled elsewhere
    except AttributeError:
        pass

    clip_es = Clip(title=str(clip['title']), caption=str(clip['caption']),
                   thumbnail=str(clip['thumbnail']), categories=categories)
    clip_es.meta.id = clip['clip_id']

    clip_es.save()
    return clip_es


def get_clip_by_id(clip_id):
    """ Search for clip in ES index by clip_id. Return None if not found. """
    return Clip.get(id=clip_id, ignore=404)


def get_similar_clips(clip_id):
    """ Return 10 clips deemed to be most similar. """
    clip = get_clip_by_id(clip_id)
    if clip is None:
        raise ClipNotFoundException(["clip_id searched for not in index."])

    dsl_search = Clip.search()
    similar_clips = dsl_search.query(MoreLikeThis(like=clip.caption,
                                                  fields=['title', 'caption'])).execute()
    return similar_clips
