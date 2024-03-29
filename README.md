# Sinhala-song-lyrics-search-engine

## Introduction 
This is a Sinhala song lyrics search engine. it provides song user information, lyrics as well as song metaphors in the song released date from 1990 to 2015. Elasticsearch was used to develop this search engine. Elasticsearch is a RESTful powerful indexing and search tool, which is a part of the Elastic Stack. Music data, which can be several GBs in size, is perfect for Elasticsearch since it is horizontally scalable. Elasticsearch also features a flexible data schema, high availability, and quick query execution. Elasticsearch qualifies as a quick and dependable search engine since the objective is to create a song search engine. The search engine backend was developed using flask and frontend is single html page. 

## Song Corpus
The song corpus collected by manually. Because in this case we have to extract metaphors contains in the song, there is no way to extract metaphor statement automatically. The corpus contains 110 Sinhala song released 1990 to 2020. Each song contains following attributes. Each attribute is in Sinhala.
- Title – title of the song
- Year – released year of the song
- Album – the album name of the song included
- Artist – the singer of the song (can be multiple)
- Lyricist – author of the song
- Lyrics – full lyrics of the song
- Metaphors – metaphors in the song (can be multiple). Each metaphor has following attributes. 
    - Song part
    - Interpretation
    - Type
    - Source Domain
    - Target Domain 

## High Level architecture
![Alt text](/img/High%20Level%20architecture.JPG "High Level architecture diagram")

## Search Engine Application
<!-- <img src="/img/ui.JPG" width="50%"> -->
![Alt text](/img/ui.JPG "Search Application UI")

### Setting up
- Download the Elasticsearch https://www.elastic.co/downloads/elasticsearch
- First need to install icu_tokenizer in Elasticsearch 
    - Go to the bin folder and open the cmd 
    - Execute the following command
    - `elasticsearch-plugin install analysis-icu`
- Open the ‘elasticsearch.bat’ file in the bin folder
- Clone the GitHub repository
- Run the index-generator.py file. It will create the index and save the song corpus into elasticsearch.
- Run the main.py file (execute ‘flask run’ command)
- Open the browser and go to http://127.0.0.1:5000/ and you will see the search box.

### Main functionalities
- Full text search – if a given search string not specified any of the synonyms keyword similar to artist, lyricists or album it will search through in all the fields.
- Search by year
- Search through Synonyms
    - For artist - ගායකයා, ගයනවා, ගායනා, ගායනා, ගැයු, ගයන, ගයපු
    - For lyricist - ගත්කරු, රචකයා, ලියන්නා, ලියන, රචිත, ලියපු, ලියව්‌ව, රචනා, රචක, ලියන්, ලියූ
    - For album - ඇල්බමය ඇල්බම්
    
    If the given search string contains any of the above word. It will specifically search through that relevant field.
    
    Ex: - search string ‘ඉරාජ් වීරරත්න ගැයු ගීත’
    
    This query specifically searches in artist filed.