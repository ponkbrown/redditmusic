from app import *

subprocess.call(['clear'])
listentothis = mediasubs('listentothis', 15)

for a in listentothis:
	print('\n'+'='*80+'\n',a.title)
	data = getMeta(a)
	if type(data) == dict:
		print('Artista: {0}\nTitulo: {1}\nAlbum: {2}\nFecha: {3}\nGenero: {4}'.format(data['artista'],
			data['titulo'], data['album'], data['fecha'], data['genero']))
		input()
		getmp3(a)
