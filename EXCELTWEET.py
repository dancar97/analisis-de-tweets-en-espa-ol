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
import xlsxwriter
from pyxlsb import open_workbook as open_xlsb

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 

workbook = xlsxwriter.Workbook('Output_10000_5.xlsx')
worksheet = workbook.add_worksheet()

nwdf = pd.read_csv('Libro3.csv',sep=';')

temparray=[]
Nombre =[]
PersonasQueSigue =[]
PersonasCirculo1 =[]
PersonasCirculo2=[]
Favoritos = []
tweets =[]
tweetsPositivos=[]
tweetsNeutrales=[]
tweetsNegativos=[]
tendenciaPositiva=[]
tendenciaNegativa=[]
frecuenciaDeTweet=[]
RT =[]





cuentasT = nwdf["Cuenta"].tolist() 

def normalizador(cuenta):
    newAcc = cuenta.replace("'@", '')
    newAcc = newAcc.replace("https://twitter.com/", '')
    newAcc = newAcc.replace("@", '')
    newAcc = newAcc.replace("'", '')
    return newAcc


for i in range(0,len(nwdf)):
    temparray.append(normalizador(cuentasT[i]))



print(temparray)


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


#😂👌
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')




clf = SentimentClassifier()



def ObtenerTweets(palabra, times):
    res = api.user_timeline(id=palabra, count=times)
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
    countRT = 0
    RTInfoArray = []
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

            if(tweet.retweet_count>=1):
                countRT = countRT + 1
                if countRT <= 5:
                    RTInfoArray.append(RTinfo(tweet.id))


    s = sum(PromedioFechas,datetime.timedelta())/numero
    tweetsPos =str(pos)
    tweetsNeu =str(neu)
    tweetsNeg =str(neg)
    tendenciaP = str(Npos/(Npos+Nneg))
    tendenciaN = str(Nneg/(Npos+Nneg))
    frecuencia  = s
    return (numeros_list,popularidad_list,numero, tweetsPos,tweetsNeu,tweetsNeg,tendenciaP,tendenciaN,frecuencia,RTInfoArray)

    
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()



def RTinfo(idTweet):
    try:
        res2 = api.retweets(id=str(idTweet))
        retweeter = []
        for status in res2:
        #  print("Screen name "+str(status.user.screen_name))
        #  print("Screen Seguidores "+str(status.user.followers_count))
        #  print("Screen  Seguidos"+ str(status.user.friends_count))
            retweeter.append(status.user.screen_name)
            retweeter.append(status.user.followers_count)
            retweeter.append(status.user.friends_count)
            return retweeter
    except:
        retweeter.append("Cuenta protegida")
        retweeter.append("Cuenta protegida")
        retweeter.append("Cuenta protegida")
        return retweeter

    



for i in range(0,len(nwdf)):
    try:
        results3 = api.get_user(id=temparray[i])

        numberTweet = 0
        if(results3.statuses_count < 200):
            numberTweet = results3.statuses_count
        else:
            numberTweet = 200
        
        if (numberTweet > 1):
            try:
                numeros_list,popularidad_list,numero,a,b,c,d,e,f,g = ObtenerTweets(temparray[i],numberTweet) 
                tweetsPositivos.append(a)
                tweetsNeutrales.append(b)
                tweetsNegativos.append(c)
                tendenciaPositiva.append(d)
                tendenciaNegativa.append(e)
                frecuenciaDeTweet.append(f)
                RT.append(g)
            except:
                tweetsPositivos.append("Error clasificando tweets")
                tweetsNeutrales.append("Error clasificando tweets")
                tweetsNegativos.append("Error clasificando tweets")
                tendenciaPositiva.append("Error clasificando tweets")
                tendenciaNegativa.append("Error clasificando tweets")
                frecuenciaDeTweet.append("Error clasificando tweets")
                RT.append("Error clasificando tweets")

        else:
            tweetsPositivos.append("Cuenta Protegida o vacia")
            tweetsNeutrales.append("Cuenta Protegida o vacia")
            tweetsNegativos.append("Cuenta Protegida o vacia")
            tendenciaPositiva.append("Cuenta Protegida o vacia")
            tendenciaNegativa.append("Cuenta Protegida o vacia")
            frecuenciaDeTweet.append("Cuenta Protegida o vacia")
            RT.append("Error clasificando tweets")

        try:
            resultsFollowers = api.followers(id=temparray[i],count= results3.followers_count)
            a= 0
            countPersonas = 0
            for user in resultsFollowers:
                a = a +1
                countPersonas = countPersonas + user.followers_count
            PersonasCirculo2.append(str(countPersonas))
        except:
            PersonasCirculo2.append("no se pudo llegar al segundo circulo de amigos")

            
        try:
            Nombre.append(str(results3.name))
            PersonasQueSigue.append(str(results3.friends_count))
            PersonasCirculo1.append(str(results3.followers_count))
            Favoritos.append(str(results3.favourites_count))
            tweets.append(str(results3.statuses_count))
        except:
            Nombre.append("No se pudo conseguir info basica")
            PersonasQueSigue.append("No se pudo conseguir info basica")
            PersonasCirculo1.append("No se pudo conseguir info basica")
            Favoritos.append("No se pudo conseguir info basica")
            tweets.append("No se pudo conseguir info basica")

    except:
        a = "Cuenta no encontrada"
        tweetsPositivos.append(a)
        tweetsNeutrales.append(a)
        tweetsNegativos.append(a)
        tendenciaPositiva.append(a)
        tendenciaNegativa.append(a)
        frecuenciaDeTweet.append(a)
        Nombre.append(a)
        PersonasQueSigue.append(a)
        PersonasCirculo1.append(a)
        PersonasCirculo2.append(a)
        Favoritos.append(a)
        tweets.append(a)
        RT.append(a)
    print("voy "+ str(i+1) +" de "+ str(len(nwdf))+ "la cuenta es "+ str(temparray[i]))


for i in range(0,len(nwdf)+1):
    try:   
        if (i == 0):
            worksheet.write('A'+str(i+1), str("Cuenta"))
            worksheet.write('B'+str(i+1), str("Persona"))  
            worksheet.write('C'+str(i+1), str("Sigue A"))
            worksheet.write('D'+str(i+1), str("Circulo 1 de seguidores"))
            worksheet.write('E'+str(i+1), str("Circulo 2 de seguidores"))
            worksheet.write('F'+str(i+1), str("Favoritos"))
            worksheet.write('G'+str(i+1), str("Tweets"))
            worksheet.write('H'+str(i+1), str("Tweets positivos"))
            worksheet.write('I'+str(i+1), str("Tweets neutrales"))
            worksheet.write('J'+str(i+1), str("Tweets negativos"))
            worksheet.write('K'+str(i+1), str("Tendencia positiva"))
            worksheet.write('L'+str(i+1), str("Tendencia negativa"))
            worksheet.write('M'+str(i+1), str("Frecuencia de twittero"))
            worksheet.write('N'+str(i+1), str("InfoDeREtweets"))
        else:
            worksheet.write('A'+str(i+1), str(temparray[i-1]))
            worksheet.write('B'+str(i+1), str(Nombre[i-1]))  
            worksheet.write('C'+str(i+1), str(PersonasQueSigue[i-1]))
            worksheet.write('D'+str(i+1), str(PersonasCirculo1[i-1]))
            worksheet.write('E'+str(i+1), str(PersonasCirculo2[i-1]))
            worksheet.write('F'+str(i+1), str(Favoritos[i-1]))
            worksheet.write('G'+str(i+1), str(tweets[i-1]))
            worksheet.write('H'+str(i+1), str(tweetsPositivos[i-1]))
            worksheet.write('I'+str(i+1), str(tweetsNeutrales[i-1]))
            worksheet.write('J'+str(i+1), str(tweetsNegativos[i-1]))
            worksheet.write('K'+str(i+1), str(tendenciaPositiva[i-1]))
            worksheet.write('L'+str(i+1), str(tendenciaNegativa[i-1]))
            worksheet.write('M'+str(i+1), str(frecuenciaDeTweet[i-1]))
            worksheet.write('N'+str(i+1), str(RT[i-1]))
    except:
        print("An exception occurred")
        worksheet.write('A'+str(i+1), 'null')
workbook.close()
