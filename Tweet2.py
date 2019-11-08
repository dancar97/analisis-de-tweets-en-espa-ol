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

 


consumer_key = "jgRayRaeRfkRzqEfOME3Yu3n6"
consumer_secret = "BESI3SVvJBFC4r7rSWdsii3RVrNXaaXudUDY7Q6TfUOgP05SXd"
access_token = "331074060-xHMWu3bzDJDRDJYAi9rLu3ACvELBo5MNxPml32cL"
access_token_secret = "TAifANQGAT9V1DWUkl805ncs95WZnU75nGha7w8Zx1zxb"




# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 



clf = SentimentClassifier()



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



print(get_google_translate("Hola ESto es severa prueba jajajaja xd","en"))



# re positivo name = "ftcelebraciones"
name = "sierraventur"
neg = 0
pos = 0

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


clf = SentimentClassifier()

def ObtenerTweets(palabra, times):
    pos = 0
    neg = 0
    neu = 0
    numero = 0
    popularidad_list = []
    numeros_list = []
    results = api.user_timeline(id=palabra, count=times)
    for tweet in results:
        printProgressBar(numero, times)
        prediction = clf.predict(deEmojify(tweet.text))
        popularidad_list.append(prediction)
        numeros_list.append(numero)
        numero = numero + 1
        if(prediction == 1):
            print("------------------------------------------------")
            print("-Muy Positivo-")
            print(tweet.text)
            print(tweet.created_at)
            print(tweet.user.screen_name)
            print("------------------------------------------------")
        if(prediction == 0):
            print("------------------------------------------------")
            print("-Muy Negativo-")
            print(tweet.text)
            print(tweet.created_at)
            print(tweet.user.screen_name)
            print("------------------------------------------------") 
        if(prediction >= 0.8):
            pos = pos + 1
            
        elif(prediction < 0.1):
            neg = neg + 1
        else:
            neu = neu + 1

    print("tweets positivos "+ str(pos))
    print("tweets negativos "+ str(neg))
    print("tweets Neutrales "+ str(neu))
    return (numeros_list,popularidad_list,numero)


def GraficarDatos(numeros_list,popularidad_list,numero, palabra):
    axes = plt.gca()
    axes.set_ylim([-1, 2])
    
    plt.scatter(numeros_list, popularidad_list)
    popularidadPromedio = (sum(popularidad_list))/(len(popularidad_list))
    popularidadPromedio = "{0:.0f}%".format(popularidadPromedio * 100)
    time  = datetime.now().strftime("hora : %H:%M\n dia: %m-%d-%y")
    plt.text(0, 1.25, 
             "Sentimiento promedio:  " + str(popularidadPromedio) + "\n" + time, 
             fontsize=12, 
             bbox = dict(facecolor='none', 
                         edgecolor='black', 
                         boxstyle='square, pad = 1'))
    
    plt.title("Sentimientos sobre " + palabra + " en twitter")
    plt.xlabel("Numero de tweets")
    plt.ylabel("Sentimiento")
    print(str(name)+ " Tiene un promedio positivo de "+ str(popularidadPromedio)+ "")
    plt.show()
    
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()

'''
tweetCount = 20
results = api.user_timeline(id=name, count=tweetCount)
for tweet in results:
    print("------------------------------------------------")
    print (tweet.text)
    print (tweet.created_at)
    print(tweet.user.screen_name)
    print("------------------------------------------------")     



results2 = api.get_user(id=name)
#print(results2)
print("------------------------------------------------") 
print("Nombre de la persona: "+str(results2.name))
print("Número de seguidores: "+str(results2.followers_count))
print("Personas a las que sigue "+str(results2.friends_count))
print("Número de favoritos "+str(results2.favourites_count))
print("Número de tweets "+str(results2.statuses_count))
print("------------------------------------------------") 


'''


resultsFollowers = api.followers(id=name,count= results2.followers_count)

a= 0
countPersonas = 0

for user in resultsFollowers:
    a = a +1
    countPersonas = countPersonas + user.followers_count

print("miré " +str(a)+" perfiles")
print("Circulo inmediato "+ str(countPersonas)+ " Personas al alcance")

numberTweet = 0
if(results2.statuses_count < 200):
    numberTweet = results2.statuses_count
else:
    numberTweet = 200

numeros_list,popularidad_list,numero = ObtenerTweets(name,numberTweet) 
results2 = api.get_user(id=name)
#print(results2)
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
GraficarDatos(numeros_list,popularidad_list,numero,name)





