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


 


consumer_key = "jgRayRaeRfkRzqEfOME3Yu3n6"
consumer_secret = "BESI3SVvJBFC4r7rSWdsii3RVrNXaaXudUDY7Q6TfUOgP05SXd"
access_token = "331074060-xHMWu3bzDJDRDJYAi9rLu3ACvELBo5MNxPml32cL"
access_token_secret = "TAifANQGAT9V1DWUkl805ncs95WZnU75nGha7w8Zx1zxb"




# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 



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



name = "IaraAmico3"
neg = 0
pos = 0

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


def ObtenerTweets(palabra, times, lenguaje="es"):
    popularidad_list = []
    numeros_list = []
    numero = 1
    tweetCount = times
    errores = 0
    results = api.user_timeline(id=palabra, count=times)
    for tweet in results:            
            #translator = Translator()
            #translatorVar = translator.translate(deEmojify(tweet.text), dest='en')
            #analisis = TextBlob(translatorVar.text)
            gs = goslate.Goslate()
            analisis = gs.translate(deEmojify(tweet.text), 'es')
            sleep(0.05)
            analisis = analisis.sentiment
            
            popularidad = analisis.polarity
            if(popularidad > 0.5 or popularidad < -0.5):
                print("------------------------------------------------")
                print(tweet.text)
                print(popularidad)
                print("------------------------------------------------")
            if popularidad <= 0:
                neg = 1
            else:
                pos +=1

            popularidad_list.append(popularidad)
            numeros_list.append(numero)
            numero = numero + 1
            if(errores >15):
                break
                print("la embarré "+str(errores)+ " veces")
            
    print("la embarré "+str(errores)+ " veces")
    print("tweets negativos"+ str(neg))
    print("tweets positivos"+ str(pos))
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
    print(str(name)+ " actúa de forma positiva el "+ str(popularidadPromedio)+ " de las veces")
    plt.show()
    


'''
tweetCount = 20
results = api.user_timeline(id=name, count=tweetCount)
for tweet in results:
    print("------------------------------------------------")
    print (tweet.text)
    print (tweet.created_at)
    print(tweet.user.screen_name)
    print("------------------------------------------------")     
'''


results2 = api.get_user(id=name)
#print(results2)
print("------------------------------------------------") 
print("Nombre de la persona: "+str(results2.name))
print("Número de seguidores: "+str(results2.followers_count))
print("Personas a las que sigue "+str(results2.friends_count))
print("Número de favoritos "+str(results2.favourites_count))
print("Número de tweets "+str(results2.statuses_count))
print("------------------------------------------------") 





resultsFollowers = api.followers(id=name,count= results2.followers_count)

a= 0
countPersonas = 0

for user in resultsFollowers:
    a = a +1
    countPersonas = countPersonas + user.followers_count

print("miré " +str(a)+" perfiles")
print("Circulo inmediato "+ str(countPersonas)+ " Personas al alcance")

numberTweet = 0
if(results2.statuses_count < 20):
    numberTweet = results2.statuses_count
else:
    numberTweet = 20



numeros_list,popularidad_list,numero = ObtenerTweets(name,numberTweet,"es") 
GraficarDatos(numeros_list,popularidad_list,numero,name)



