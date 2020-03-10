#LIBRERIAS NECESARIAS
import matplotlib.pyplot as plt
import math
from drawnow import *
import time 
import json

data = {"tweets": [], "sentiment_polarity": [], "sentiment_subjectivity": [], "index": []}
count = 0

def readDataFile(filename):
    text_file = open(filename, "r")
    data = json.loads(text_file.read())
    text_file.close()
    return data

def plotValues():
    global data
    global count
    count = count + 1
    plt.title('Análisis de Sentimientos')
    plt.grid(True)
    plt.ylabel('Valores')
    plt.plot(data['index'], data['sentiment_subjectivity'], 'y.-', label='Subjetividad')
    plt.plot(data['index'], data['sentiment_polarity'], 'g.-', label='Polaridad')
    plt.legend(loc='upper right')
    plt.savefig('output\\prueba_' + str(count) + '.png')

while True:
    try:
       last_array = data['index']
       data = readDataFile("output\\tweets.json")
       if last_array != data['index']:
          drawnow(plotValues)
          time.sleep(0.1)
    except Exception as e:
       print(e)