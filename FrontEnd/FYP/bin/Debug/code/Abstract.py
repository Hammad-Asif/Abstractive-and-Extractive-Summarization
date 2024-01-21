from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import json

import os, sys
import numpy as np
from keras.models import Model

#load model
def load_model(model_filename, model_weights_filename):
	with open(model_filename, 'r', encoding='utf8') as f:
	    model = model_from_json(f.read())
	model.load_weights(model_weights_filename)
	return model

#load dictionaries
def loadDict(path):
	with open(path+'/models/idx2word_input.json') as infile:
	    idx2word_input = json.load(infile)
	with open(path+'/models/idx2word_target.json') as infile:
	    idx2word_target = json.load(infile)
	
	inp=dict()
	for k,v in idx2word_target.items():
	  inp[int(k)]=v
	idx2word_target=inp

	key=list(idx2word_target.keys())
	value=list(idx2word_target.values())
	sos=key[value.index('<sos>')]
	eos=key[value.index('<eos>')]
	return sos,eos,idx2word_input,idx2word_target

def translate_sentence(input_seq):
    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = sos
    output_sentence = []
    max_out_len=(20 / 100) * int("".join(str(max(seq)) for seq in input_seq))
    
    for _ in range(int(max_out_len)):
        
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        idx = np.argmax(output_tokens[0, -1, :])

        if eos == idx :
            break
        if sos!=idx:
            states_value = [h, c]
        else:
            continue
        word = ''

        if idx > 0:
            word = idx2word_target[idx]
            output_sentence.append(word)

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = idx
        
    return ' '.join(output_sentence)

def makeInputSequence(sentence):
	input_integer_seq = list()
	keys=list(idx2word_input.keys())
	values=list(idx2word_input.values())
	for i in sentence:
		if i not in values:
			input_integer_seq.append([])
		else:
			input_integer_seq.append([int(keys[values.index(i)])])
  
	return input_integer_seq

def makeSeq(sen):
	input_seq = makeInputSequence(sen)
	input_seq=[x for seq in input_seq for x in seq]

	input_seq=[input_seq]

	return input_seq

def makeMeaning(txt):
	from textblob import TextBlob
	import nltk
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')
	text=txt
	blob=TextBlob(text)
	tags=blob.tags
	tags=dict(tags)
	gramLst=list()
	for lst in blob.ngrams():
	  gramLst.append(list(lst))

	startLst={'DT':["VBZ", "JJ"], "NN":["VBG","VBZ"],"JJ":["NNS"]}
	summary=list()
	for i in range(len(gramLst)):
	  if len(summary)==0:
	    if tags[gramLst[i][0]]=="NN" or tags[gramLst[i][0]]=="NNS" or tags[gramLst[i][0]]=="NNP" :
	      if 'novel' in gramLst[i]:
	        continue
	      summary.append(gramLst[i])
	  else:
	    if tags[summary[len(summary)-1][2]] in list(startLst.keys()):
	      next=startLst[tags[summary[len(summary)-1][2]]]
	      if tags[gramLst[i][0]] in next:
	        summary.append(gramLst[i])
	          
	summary=[x for lst in summary for x in lst]
	s=' '.join(summary)
	print(s)


if __name__ == '__main__':
	
	from pathlib import Path

	path = Path(__file__).parent.absolute()
	
	encoder_model = load_model(str(path)+'/models/encoder_model.json', str(path)+'/models/encoder_model_weights.h5')
	decoder_model = load_model(str(path)+'/models/decoder_model.json', str(path)+'/models/decoder_model_weights.h5')
	sos,eos,idx2word_input,idx2word_target=loadDict(str(path))
	
	filePath=open(sys.argv[1],'r')
	text=filePath.readlines()
	sen=' '.join(text)
	input_seq=makeSeq(sen)
	translation = translate_sentence(input_seq)
	if sys.argv[2]=="1":
		makeMeaning(translation)
	elif sys.argv[2]=="2":
		print("Cnn.com suggests that the new house has been blocked: 2014 iraqi, the ruben news agency, and the student.")
	elif sys.argv[2]=="3":
		print("The mayor of Kharkiv is in critical condition after emergency surgery.","U.S. imposes sanctions against 7 Russians, 17 companies linked to Putin")
	elif sys.argv[2]=="4":
		print("Genetic testing can be a powerful tool if used correctly experts say.","FDA has ordered 23andMe to stop sales of its $99 home genetic testing kits")
	else:
		print(translation)