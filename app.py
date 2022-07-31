
import queue
from unicodedata import name
import sounddevice as sd
import vosk
import json
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from doings import *


q = queue.Queue()

model = vosk.Model('small_model')

device = sd.default.device = 0, 4 # default device is  number (1,3)
samplerate = int(sd.query_devices(device[0], "input")['default_samplerate'])



def callback(indata, frames, time, status):
    
    q.put(bytes(indata))

def recognize(data, vectorizer , clf):
    #here we waiting for our call to our bot
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return
    #here we delete our keys from dict
    data.replace(list(trg)[0], '')
    #we uptake the result from list of values
    text_vector = vectorizer.transform([data]).toarray()[0]

    answer = clf.predict([text_vector])[0]
    
    func_name = answer.split()[0]
    speaker(answer.replace(func_name, ''))
    exec(func_name + '()')



'''here we uptake a voice from microphone and try to parse it
vector help us to find similiarities inside our words patterns'''
def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

#logistic regression help us to find out the similiarities btween keys and values
    clf = LogisticRegression()
    clf.fit(vectors,list(words.data_set.values()))

    del words.data_set#delete dict from operatives


    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',
                                channels=1, callback=callback):
            
            rec = vosk.KaldiRecognizer(model,samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):#if pause will be occured we put down the result
                    data = json.loads(rec.Result())['text']
                    recognize(data,vectorizer , clf)
    #as we dont need the partial results we commented this line         
                # else:
                #     print(rec.PartialResult())
               
if __name__ == '__main__':
    main()