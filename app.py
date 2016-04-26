# Un script para usar el api de reddit, basicamente se autentifica en reddit y baja una lista de canciones
# de algunos subreddit musicales para obtener recomendaciones y bajar los archivos para escuchar musica nueva
# cada dia.
# 
# Sat Apr 23 20:44:37 MST 2016
import praw
import sys
import subprocess
import re

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
    
    
def getMeta(post):
    if not post.domain.startswith('self'):
        patron = re.compile(r'(.+)\s-{1,2}\s(.+)\s\[(.+)\].*\((\d+)\)')
        matcher = patron.search(post.title)
        if matcher:
            metadata = {
            'artista' : matcher.group(1),
            'titulo' : matcher.group(2),
            'album' : post.subreddit.title,
            'fecha' : matcher.group(4),
            'genero': matcher.group(3),
            'thumb' : post.thumbnail
           } 
            return metadata
        else:
            return "Sin Genero"
    return 'post de reddit'

def getmp3(url, data):
    try:
        subprocess.call(['youtube-dl', '-x', '--audio-format', 'mp3', url, '-o', './mp3/%(title)s.%(ext)s'])
    except 'FileNotFoundError':
        print('Error')
        return None
    
def mediasubs(subreddit, num):
    r = praw.Reddit(user_agent=user_agent)
    # subreddit de musica
    activo = r.get_subreddit(subreddit)
    hot = activo.get_hot(limit=num+10) # cuantos post hay que bajar
    collection = []
    for post in hot:
        if type(post.media) == dict and post.media.get('type'):
            collection.append(post)
    return collection        