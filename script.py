#-*- coding: utf-8 -*-
import sys
import mysql.connector
from radar import radar_graph

# Recupere le pseudo que l'on veut analyser
if len(sys.argv) > 1:
	name_user = sys.argv[1]
else:
	print 'Usage: python script.py <name_user>'
	exit()

# Liste pour stocker les noms de nos indicateurs et leurs valeurs
labels = [u'Poster un nouveau message',u'Connexion',u'Citer un message',u'Répondre à un message']
values = []

# Connection a mysql
conn = mysql.connector.connect(host="localhost",user="root",password="123321", database="trace")
cursor = conn.cursor()

# Calcul des indicateurs via les données de la base mysql
for i in range(len(labels)):
	req = " SELECT COUNT(Titre) FROM transition WHERE Utilisateur='"+name_user+"' AND Titre='"+labels[i]+"' "
	cursor.execute(req)
	values.append(int(str(cursor.fetchall()[0]).replace('(','').replace(')','').replace(',','')))

# Deconnection de mysql
conn.close()

# Calcul d'un indicateur à partir d'autres indicateurs
labels.append(u'Message total')
values.append(values[2]+values[3])

# Ameliore les indicateurs par valeurs
for i in range(len(labels)):
	labels[i] += ' ('+str(values[i])+')'

# Creer radar chart
radar_graph(name_user, labels, values)
