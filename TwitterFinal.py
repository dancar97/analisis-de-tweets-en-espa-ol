import tweepy
from time import sleep
from datetime import datetime
from textblob import TextBlob 
import matplotlib.pyplot as plt 
from googletrans import Translator
from time import sleep
from urllib.parse  import urlencode
from urllib.request import urlopen, Request
import re
import json
import goslate
from classifier import *
import re
import datetime
import numpy as np
import pandas as pd

consumer_key = "w000000000000000000000000"
consumer_secret = "B0000000000000000000000000000000000000000000000000"
access_token = "000000000-0000000000000000000000000000000000000000"
access_token_secret = "x0000000000000000000000000000000000"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 


'''

def get_google_translate(text, translate_lang, source_lang=None):
    if source_lang == None:
        source_lang= 'auto'
    params = urlencode({'client':'t', 'tl':translate_lang, 'q':text.encode('utf-8'),
                       'sl':source_lang})
    http_headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)"}
    request_object = Request('http://translate.google.com/translate_a/t?'+params, 
                     None, http_headers)
    try:
        response = urlopen(request_object)
        string = re.sub(',,,|,,',',"0",', response.read())
        n = json.loads(string)
        translate_text = n[0][0][0]
        res_source_lang = n[2]
        return True, res_source_lang, translate_text
    except Exception as e:
        return False, '', e

'''


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


name = "sierraventur"

#😂
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

clf = SentimentClassifier()
results2 = api.get_user(id=name)

numberTweet = 0
if(results2.statuses_count < 200):
    numberTweet = results2.statuses_count
else:
    numberTweet = 200
results = api.user_timeline(id=name, count=numberTweet)


def ObtenerTweets(palabra, times, res=results):
    pos = 0
    neg = 0
    Npos = 0
    Nneg = 0
    neu = 0
    numero = 0
    popularidad_list = []
    numeros_list = []
    currFe = []
    results = res
    nCiclos = 0
    PromedioFechas = []
    for tweet in results:

        printProgressBar(numero, times)
        prediction = clf.predict(deEmojify(normalize(tweet.text)))
        currFe.append(tweet.created_at)
        if(nCiclos == 0):
            PromedioFechas.append(datetime.datetime.now()-tweet.created_at)
        else:
            PromedioFechas.append(currFe[nCiclos-1]-tweet.created_at)

        nCiclos = nCiclos + 1 

        twee1 = " ".join(filter(lambda x:x[0]!='@', deEmojify(normalize(tweet.text)).split()))
        twee = URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', str(twee1))
        twee = twee.replace('RT', '')
        if len(twee.split()) >1:
            popularidad_list.append(prediction)
            numeros_list.append(numero)
            numero = numero + 1
            if(prediction >= 0.8):
                pos = pos + 1
                
            elif(prediction < 0.1):
                neg = neg + 1
            else:
                neu = neu + 1

            if(prediction >= 0.5):
                Npos = Npos + 1
                
            elif(prediction < 0.5):
                Nneg = Nneg + 1
        
    print("-------------------------------------")
    print("tweets positivos "+ str(pos))
    print("tweets neutrales "+ str(neu))
    print("tweets negativos "+ str(neg))
    print("tweets Tendencia positiva "+ str(Npos/(Npos+Nneg)))
    print("tweets Tendencia negativa "+ str(Nneg/(Npos+Nneg)))
    print("la tendencia promedio parcial de esta cuenta es de "+str((pos)/(neu+pos+neg))+" a ser positivo")
    print("la tendencia promedio parcial de esta cuenta es de "+str((neg)/(neu+pos+neg))+" a ser negativo")
    print("la tendencia promedio parcial de esta cuenta es de "+str((neu)/(neu+pos+neg))+" a ser neutral")
    print("-----------")
    print("la tendencia promedio de esta cuenta sin tweets neutrales es de "+str((Npos)/(Npos+Nneg))+" a ser positivo")
    print("---------------------------------------------------------------------")
    s = sum(PromedioFechas,datetime.timedelta())/numero
    print("el usuario twittea con una frecuencia de "+ str(s))
    return (numeros_list,popularidad_list,numero)


def GraficarDatos(numeros_list,popularidad_list,numero, palabra):
    axes = plt.gca()
    axes.set_ylim([-1, 2]) 
    plt.scatter(numeros_list, popularidad_list)
    popularidadPromedio = (sum(popularidad_list))/(len(popularidad_list))
    popularidadPromedio = "{0:.0f}%".format(popularidadPromedio * 100)
    plt.text(0, 1.25, 
             "Sentimiento promedio:  " + str(popularidadPromedio) + "\n" , 
             fontsize=12, 
             bbox = dict(facecolor='none', 
                         edgecolor='black', 
                         boxstyle='square, pad = 1'))
    
    plt.title("Sentimientos sobre " + palabra + " en twitter")
    plt.xlabel("Numero de tweets")
    plt.ylabel("Sentimiento")
    print(str(name)+ " El promedio encontrado es de "+ str(popularidadPromedio)+ "")
    plt.show()
    
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()


results2 = api.get_user(id=name)
resultsFollowers = api.followers(id=name,count= results2.followers_count)
a= 0
countPersonas = 0
for user in resultsFollowers:
    a = a +1
    countPersonas = countPersonas + user.followers_count
print("miré " +str(a)+" perfiles")
print("Circulo inmediato "+ str(countPersonas)+ " Personas al alcance")

numeros_list,popularidad_list,numero = ObtenerTweets(name,numberTweet) 


print("------------------------------------------------") 
print("Nombre de la persona: "+str(results2.name))
print("Número de seguidores: "+str(results2.followers_count))
print("Personas a las que sigue "+str(results2.friends_count))
print("Número de favoritos "+str(results2.favourites_count))
print("Número de tweets "+str(results2.statuses_count))
print("------------------------------------------------") 
print("miré " +str(a)+" perfiles")
print("Circulo inmediato de primer grado: "+ str(results2.followers_count)+ " Personas al alcance")
print("Circulo inmediato de segundo grado: "+ str(countPersonas)+ " Personas al alcance")
print("------------########################---------")
print("Ultimos 5 tweets")
count= 0
for tweet in results:
    
    twee1 = " ".join(filter(lambda x:x[0]!='@', deEmojify(normalize(tweet.text)).split()))
    
    twee = URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', str(twee1))
    twee = twee.replace('RT', '')
    if len(twee.split()) >1:

        print("------------------------------------------------")
        print(twee)
        print(tweet.created_at)
        print("Sentimiento ="+ str(clf.predict(twee))+"%")
        print(datetime.datetime.now())
        print("Tweet hace "+ str(datetime.datetime.now()-tweet.created_at))
        print("------------------------------------------------")
        count = count + 1
        if count >4:
            break
GraficarDatos(numeros_list,popularidad_list,numero,name)

