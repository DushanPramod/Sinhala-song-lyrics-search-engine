def getPartOfLyrics(lyrics):
    index = lyrics[200:].index(' ')
    return lyrics[:200 + index] + ' ...'
