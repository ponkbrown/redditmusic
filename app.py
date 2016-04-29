# Un script para usar el api de reddit, basicamente se autentifica en reddit y baja una lista de canciones
# de algunos subreddit musicales para obtener recomendaciones y bajar los archivos para escuchar musica nueva
# cada dia.
# 
# Sat Apr 23 20:44:37 MST 2016
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TCON, TALB, error
import praw
import subprocess
import urllib.request
import youtube_dl
import os, shutil, re, subprocess, sys, datetime, zipfile

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
        patron = re.compile(r'(.+)\s-{1,2}\s(.+)\s*\[(.+)\].*\((\d+)\)')
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

    
def mediasubs(subreddit, num):
    r = praw.Reddit(user_agent=user_agent)
    # subreddit de musica
    activo = r.get_subreddit(subreddit)
    hot = activo.get_hot(limit=num+10) # cuantos post hay que bajar
    collection = []
    for post in hot:
        if type(post.media) == dict and post.media.get('type'):
            collection.append(post)
            if len(collection) == num:
                break
    return collection        

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def videoyconvierte(songX, dataX):
    filename = songX.subreddit.url.replace('/r/','')+dataX['artista'].strip()+' - '+dataX['titulo'].strip()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './temp/'+filename+'.%(ext)s',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songX.url])

def putTag(songX, dataX):
    filename = './temp/'+songX.subreddit.url.replace('/r/','')+dataX['artista'].strip()+' - '+dataX['titulo'].strip()+'.mp3'
    # bajamos el arte en ./temp
    thumbnailURL = songX.thumbnail
    thumbnailName = thumbnailURL.split('/')[-1]
    urllib.request.urlretrieve(songX.thumbnail,'./temp/'+thumbnailName) 

    #Agregar tags
    audio = MP3(filename, ID3=ID3)

    # Agrega un tag ID3 en caso de que no tenga
    try:
        audio.add_tags()
    except error:
        pass

    # Determina el mime nomas puede ser image/jpeg o mime/png
    if thumbnailName.endswith('png'):
        mime = 'image/png'
    elif thumbnailName.endswith('gif'):
        mime = 'image/gif'
    else:
        mime = 'image/jpeg'

    with open('./temp/'+thumbnailName, 'rb') as thumb:
        arte = thumb.read()

    audio.tags.add(
            APIC(
                encoding = 3, # 3 es para utf-8
                mime = mime,
                type = 3, # 3 es para la imagen de cover
                desc = u'Cover',
                data = arte
                )
            )
    audio.tags.add(
            TPE1(
                encoding = 3,
                text = [dataX['artista']]
                )
            )
    audio.tags.add(
            TIT2(
                encoding = 3,
                text = [dataX['titulo']]
                )
            )
    audio.tags.add(
            TCON(
                encoding = 3,
                text = [dataX['genero']]
                )
            )
    audio.tags.add(
            TALB(
                encoding = 3,
                text = [datetime.datetime.today().strftime('SoundTrack-%d%B')]
                )
            )
    audio.save()

def makeZip(dirOut, dirIn):
    today = datetime.datetime.today()
    filename = today.strftime('SoundTrack-%B%d%Y-%H%M.zip')
    os.chdir('temp/')
    zipName = os.path.join('../mp3', filename)

    zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('mp3'):
                zipf.write(os.path.join(root,file))
    zipf.close()
