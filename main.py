from flask import Flask, render_template, request
from search import search
from util.util import getPartOfLyrics
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def search_box():
    if request.method == 'POST':
        query = request.form['searchTerm']
        search_result = search(query)
        
        songList = search_result['hits']['hits']
        for i in range(len(songList)):
            songList[i]['no'] = i + 1
            songList[i]['title'] = songList[i]['_source']['title']
            songList[i]['album'] = songList[i]['_source']['album']
            songList[i]['artist'] = songList[i]['_source']['artist']
            songList[i]['year'] = songList[i]['_source']['year']
            songList[i]['lyricist'] = songList[i]['_source']['lyricist']
            songList[i]['partOfLyrics'] = getPartOfLyrics(songList[i]['_source']['lyrics'])

        return render_template('index.html',query=query, songs=songList, songsCount=len(songList))
    if request.method == 'GET':
        return render_template('index.html',init='True')

if __name__ == "__main__":
    app.run(debug=True)