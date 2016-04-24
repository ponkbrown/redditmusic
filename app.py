# Un script para usar el api de reddit, basicamente se autentifica en reddit y baja una lista de canciones
# de algunos subreddit musicales para obtener recomendaciones y bajar los archivos para escuchar musica nueva
# cada dia.
# 
# Sat Apr 23 20:44:37 MST 2016
import youtube_dl
import praw
import sys
import os

# Buscando el id y el secret para usar el api de reddit de el archivo auth.txt

with open('auth.txt', 'r') as f:
    for line in f.readlines():
        if line.split(' : ')[0].strip() == 'id':
            id = line.split(' : ')[1].strip()

        if line.split(' : ')[0].strip() == 'secret':
            secret = line.split(' : ')[1].strip()

        if line.split(' : ')[0].strip() == 'platform':
            platform = line.split(' : ')[1].strip()
            
        if line.split(' : ')[0].strip() == 'version':
            version = line.split(' : ')[1].strip()

        if line.split(' : ')[0].strip() == 'user':
            user = line.split(' : ')[1].strip()

user_agent = platform + ':' + id + ':' + version + '(u {0})'.format(user)

r = praw.Reddit(user_agent=user_agent)

# subreddit de musica
listentothis = r.get_subreddit('listentothis')
hot = listentothis.get_hot(limit=5) # cuantos post hay que bajar

# Configuracion de youtube-dl

options = {
	'format' : 'bestaudio/best',
	'extractaudio' : True,
	'audioformat' : 'mp3',
	'noplaylist' : True
}

collection = []
for post in hot:
    if type(post.media) == dict and post.media.get('type') == 'youtube.com':
        print(str(post.title) + ':' + str(post.url))
        #bajando y convirtiendo a mp3
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([post.url])
            os.system('mv *.mp3 mp3')

        collection.append(post)

