import time
from keras.models import load_model
import pickle
MAX_SEQUENCE_LENGTH = 60
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sentiment_code import decode_sentiment

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load model
model = load_model('W2Vmodel.h5')
# summarize model.
#model.summary()

def predict_text(text, include_neutral=True):
    start_at = time.time()
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    #return {"score": float(score)}  

    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    return float(score)

test = predict_text("@Nintendo I love your games!")
print(test)
