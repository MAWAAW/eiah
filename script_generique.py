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

conn = mysql.connector.connect(host="localhost",user="root",password="123321", database="trace")
cursor = conn.cursor()

# Liste pour stocker les noms de nos indicateurs et leurs valeurs
labels = [u'Poster un nouveau message',u'Connexion',u'Citer un message',u'Répondre à un message']
values = []

# TYPE
class CMCtool:     
    def __init__(self):
		self.type = ''
		cursor.execute(" SELECT Attribut FROM transition ")
		self.name = cursor.fetchall()

# MESSAGE
class Content:
    def __init__(self):
		self.text = ''
		self.contentId = ''

class Attributes:
    def __init__(self):
		cursor.execute(" SELECT Titre FROM transition ")
		self.title = cursor.fetchall()
		self.attachedFile = ''

class Message:
	def __init__(self):
		self.content = Content()
		cursor.execute(" SELECT Date FROM transition ")
		self.date = cursor.fetchall()
		cursor.execute(" SELECT Utilisateur FROM transition ")
		self.sender = cursor.fetchall()
		self.receiver = ''
		self.attributes = Attributes()

# ACTION
class Action:   
    def __init__(self):
		self.type = ''
		self.date = time.time()

# MAIN
class traceCMC:
    def __init__(self):
		self.cmctool = CMCtool()
		self.message = Message()
		cursor.execute(" SELECT Utilisateur FROM transition ")
		self.user = cursor.fetchall()
		self.action = Action()
		conn.close()


# Calcul des indicateurs via les données de la base mysql
for i in range(len(labels)):
	req = " SELECT COUNT(Titre) FROM transition WHERE Utilisateur='"+name_user+"' AND Titre='"+labels[i]+"' "
	cursor.execute(req)
	values.append(int(str(cursor.fetchall()[0]).replace('(','').replace(')','').replace(',','')))

# Calcul d'un indicateur à partir d'autres indicateurs
labels.append(u'Message total')
values.append(values[2]+values[3])

# Ameliore les indicateurs par valeurs
for i in range(len(labels)):
	labels[i] += ' ('+str(values[i])+')'

# Creer radar chart
radar_graph(name_user, labels, values)


model = traceCMC()

