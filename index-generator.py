from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json
import datetime

elasticsearchClient = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'sinhala-song'

def createIndex():
    settings = {
        "settings": {
            "index":{
                "number_of_shards": "1",
                "number_of_replicas": "1"
            },
            "analysis" :{
                "analyzer":{
                    "sinhala-analyzer":{
                        "type": "custom",
                        "tokenizer": "icu_tokenizer",
                        "filter":["edge_ngram_custom_filter"]
                    }
                },
                "filter" : {
                    "edge_ngram_custom_filter":{
                        "type": "edge_ngram",
                        "min_gram" : 2,
                        "max_gram" : 50,
                        "side" : "front"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                    "title": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer" : "sinhala-analyzer",
                        "search_analyzer": "standard"
                    },
                    "lyrics": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer" : "sinhala-analyzer",
                        "search_analyzer": "standard"
                    },
                    "artist": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer" : "sinhala-analyzer",
                        "search_analyzer": "standard"
                    },
                    "lyricist": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer" : "sinhala-analyzer",
                        "search_analyzer": "standard"
                    },
                    "album": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        },
                        "analyzer" : "sinhala-analyzer",
                        "search_analyzer": "standard"
                    },
                    "year": {
                        "type": "date",
                        "format": "yyyy",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "metaphors": {
                        "type": "nested",
                        "properties": {
                            "songPart": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                },
                                "analyzer" : "sinhala-analyzer",
                                "search_analyzer": "standard"
                            },
                            "interpretation": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                },
                                "analyzer" : "sinhala-analyzer",
                                "search_analyzer": "standard"
                            },
                            "type": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                },
                                "analyzer" : "sinhala-analyzer",
                                "search_analyzer": "standard"
                            },
                            "sourceDomain": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                },
                                "analyzer" : "sinhala-analyzer",
                                "search_analyzer": "standard"
                            },
                            "targetDomain": {
                                "type": "text",
                                "fields": {
                                    "keyword": {
                                        "type": "keyword",
                                        "ignore_above": 256
                                    }
                                },
                                "analyzer" : "sinhala-analyzer",
                                "search_analyzer": "standard"
                            }
                        }
                    }
            }
        }
    }
    result = elasticsearchClient.indices.create(index=INDEX , body =settings)
    print (result)


def readSongFile():
    currentPath = os.path.dirname(os.path.abspath(__file__))
    songFilePath = os.path.join(currentPath, 'data/song_list.json')
    songFile = open(songFilePath, 'r', encoding='utf8')

    songList = json.load(songFile)
    songFile.close()
    return songList


def getFormattedSongList():
    songList = readSongFile()

    for song in songList:

        title = song["title"]
        year = datetime.datetime(int(song["year"]), 1, 1).year
        artist = song["artist"]
        lyricist = song["lyricist"]
        album = song["album"]
        lyrics = song["lyrics"]
        metaphors = song["metaphors"]
        
        yield {
            "_index": INDEX,
            "_source": {
                "title": title,
                "artist": artist,
                "lyricist": lyricist,
                "album": album,
                "year": year,
                "lyrics": lyrics,
                "metaphors": metaphors
            },
        }



createIndex()
helpers.bulk(elasticsearchClient,getFormattedSongList(()))