import sys

contractions_dict = {
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I had",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it had",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "iit will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she had",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is",
"that'd": "that had",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there had",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they had",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we had",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you had",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}


def extractor(text):
    import tensorflow.keras.preprocessing as preprocess
    import nltk
    import pycountry
    nltk.download('punkt')
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    from nltk.probability import FreqDist
    import numpy as np

    origText = text
    for w in text.split():
        for key, value in contractions_dict.items():
            if w.lower() == key:
                text = text.replace(w, value, text.count(w))

        # removing digits
    text = ''.join(c for c in text if not c.isdigit())
    from string import punctuation

    text = ''.join(c for c in text if c not in punctuation.replace('-', '', 1))
    text = text.replace('\n', ' ', len(text))
    text = text.replace('--', '', len(text))

    for w in text.split():
        if w.isupper():
            if pycountry.countries.get(alpha_2=w) != None:
                text = text.replace(w, pycountry.countries.get(alpha_2=w).name, text.count(w))

    words = nltk.word_tokenize(text)

    # remove stopwords
    tokens = []
    for w in words:
        if w.lower() not in stopwords.words('english'):
            tokens.append(w.lower())

    freq = FreqDist(tokens)

    sentToken = nltk.sent_tokenize(origText, language='english')
    fr = list(freq.keys())
    k = 0
    summary = []
    import math
    length = (35 / 100) * len(sentToken)
    for k in range(0, math.floor(length + 1)):
        X = []
        for data in sentToken:
            vector = []
            for d in data.split():
                if d in fr:
                    vector.append(freq[d])
                else:
                    vector.append(0)
            X.append(vector)
        X = np.asarray(X)

        arr = preprocess.sequence.pad_sequences(X, padding='post')
        # arr=np.array([[1,0,0,0,2],[0,0,3,0,0],[0,0,0,0,0],[0,2,0,0,0]])
        u, s, vh = np.linalg.svd(arr)
        selected = vh[k]
        result = selected.argmax()
        res = int(result)
        res = res % len(sentToken)
        summary.append(sentToken[res])
        sentToken.pop(res)
        generatedSummary = ' '.join(summary)
    return generatedSummary




if __name__== "__main__":

    file=open(sys.argv[1],'r',encoding="utf-8")
    text=file.readlines()
    textused=' '.join(text)
    print(extractor(textused))

