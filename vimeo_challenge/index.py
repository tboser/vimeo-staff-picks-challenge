""" Methods and classes for creating and interacting with the ES index. """

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch import Elasticsearch

from vimeo_challenge.exceptions import ClipNotFoundException


class Clip(Document):
    """
    All information relating to a clip from Vimeo's staff picks.
    """
    title = Text()
    caption = Text()
    thumbnail = Text()
    categories = Keyword(multi=True)

    class Index:
        """ Default index used for storing clips. """
        name = 'clips'

    def save(self, **kwargs):
        """ Save Clip to ES index. """
        return super(Clip, self).save(**kwargs)


def initialize_dsl(host='localhost'):
    """ Initialize Clip persistent layer, connect to index. """
    connections.create_connection(hosts=[{'host': host, 'port': 9200}])
    Clip.init()


def index_clip(clip):
    """ Index clip in form of dictionary or Pandas row. """
    categories = [0]  # 'regularize' categories so all clips have one in common
    try:
        categories.extend([int(i) for i in clip['categories'].replace(' ', '').split(',')])  # TODO this should be handled elsewhere
    except AttributeError:  # in case no categories are specified
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

    # Stop words taken from nltk's list of stop words.
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                  "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                  "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                  "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                  "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                  "until", "while", "of", "at", "by", "for", "with", "about", "into", "through", "now",  "should"
                  "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                  "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                  "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                  "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don"]

    dsl_search = Clip.search()
    similar_clips = dsl_search.query(MoreLikeThis(like={'_id': clip.meta.id},
                                                  fields=['title', 'caption', 'categories'],
                                                  min_term_freq=1, stop_words=stop_words,
                                                  min_doc_freq=5, minimum_should_match=0)).execute()
    return similar_clips


def save_model(name='clips_snapshot', host='localhost'):
    """ Create snapshot of clips index """  # TODO: Handle exceptions for save/load model!
    es = Elasticsearch(hosts=[{'host': host, 'port': 9200}])

    snapshot_body = {
        "type": "fs",
        "settings": {
            "location": "es-snapshots"
            }
        }
    es.snapshot.create_repository(repository='clips_repo', body=snapshot_body)
    es.snapshot.create(repository='clips_repo', snapshot=name, body={"indices": "clips"})


def load_model(name='clips_snapshot', host='localhost'):
    """ Restore snapshot of clips index """
    es = Elasticsearch(hosts=[{'host': host, 'port': 9200}])

    snapshot_body = {
        "type": "fs",
        "settings": {
            "location": "es-snapshots"
            }
        }
    es.snapshot.create_repository(repository='clips_repo', body=snapshot_body)

    es.indices.delete(index='clips', ignore=[400, 404])
    restore_body = {
        "indices": "clips"
    }
    es.snapshot.restore(repository='clips_repo', snapshot=name, body=restore_body)
