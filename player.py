from app import *

subprocess.call(['clear'])
listentothis = mediasubs('listentousagain', 10)

#for a in listentothis:
#	print('\n'+'='*80+'\n',a.title)
#	data = getMeta(a)
#	if type(data) == dict:
#		print('Artista: {0}\nTitulo: {1}\nAlbum: {2}\nFecha: {3}\nGenero: {4}'.format(data['artista'],
#			data['titulo'], data['album'], data['fecha'], data['genero']))
#		input()
#		getmp3(a)


songX = listentothis[0]
dataX = getMeta(songX)

for song in listentothis:
    data = getMeta(song)
    if type(data) != dict:
        print('+'*10+data+'+'*10)
        continue
    for tag in data.keys():
        print(tag, data[tag])
    videoyconvierte(song,data)
    putTag(song,data)
    print('='*20+'LISTO'+'='*20)

print('Fin, revisa el folder temp/ y si esta todo bien, escribe la funcion makeZip() AHORA!!')

