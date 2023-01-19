from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import advanced_queries
client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'sinhala-song'

synonym_artist = ['ගායකයා','ගයනවා','ගායනා','ගායනා','ගැයු','ගයන','ගයපු']
synonym_lyricist = ['ගත්කරු','රචකයා','ලියන්නා','ලියන','රචිත','ලියපු','ලියව්‌ව','රචනා','රචක','ලියන්','ලියූ']
synonym_album = ['ඇල්බමය', 'ඇල්බම්']
synonym_list = [ synonym_artist, synonym_lyricist, synonym_album ]



def search(search_query):
    processed_query = ""
    tokens = search_query.split()
    processed_tokens = search_query.split()
    search_fields = []
    year = 0
    field_list = ["artist", "lyricist","album","year", "metaphors" ]
    all_fields = ["title","artist", "lyricist", "album", "lyrics", "metaphors"]
    final_fields = []
    year_array = []

    for word in tokens:
        print (word)

        if word.isdigit():
            temp_word = word
            if(len(str(word)) == 1):
                temp_word+="000"
            elif((len(str(word)) == 2)):
                temp_word+="00"
            elif((len(str(word)) == 3)):
                temp_word+="0"
            elif((len(str(word)) > 4)):
                temp_word = word[0:4]
            print(temp_word)
            year = int(temp_word)
            year_array.append(year)
            search_query = year
            processed_tokens.remove(word)
            print ('Identified year ',year)
    


        for i in range(0, 3):
            if word in synonym_list[i]:
                print('Adding field', field_list[i], 'for ', word, 'search field list')
                search_fields.append(field_list[i])
                if(i%2==0):
                    search_fields.append(field_list[i+1])
                else:
                    search_fields.append(field_list[i -1])
                processed_tokens.remove(word)

    if (len(processed_tokens)==0):
        processed_query = search_query
    else:
        processed_query = " ".join(processed_tokens)

    final_fields = search_fields

    if (year==0):
        print('Faceted Query')
        if(len(search_fields)==0):
            query_es = advanced_queries.multi_match_agg_cross(processed_query, all_fields)
        elif (len(search_fields) == 2):
            query_es = advanced_queries.multi_match_agg_phrase(processed_query, all_fields)
        else:
            query_es = advanced_queries.multi_match_agg_cross(processed_query, final_fields)

    else:
        print('Range Query')
        if (len(search_fields) == 0):
            query_es = advanced_queries.multi_match_agg_sort_cross(processed_query, year, ["year"])
        elif (len(search_fields) == 2):
            query_es = advanced_queries.multi_match_agg_sort_phrase(processed_query, year, all_fields)
        else:
            query_es = advanced_queries.multi_match_agg_sort_cross(processed_query, year, final_fields)

    print("QUERY BODY")
    print(query_es)
    search_result = client.search(index=INDEX, body=query_es)
    return search_result





