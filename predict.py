import time
from cleantweet import preprocess_apply
from sentiment_code import decode_sentiment
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

tokenizer = Tokenizer(filters="", lower=False, oov_token="<oov>")
interpreter = tf.lite.Interpreter('sentiment_model.tflite')

def predict_text(text, include_neutral=True, model=None):
    start_at = time.time()
    # Clean text
    text = preprocess_apply(text)
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=20)
    # Predict
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    input_shape = input_details[0]['shape']
    input_tensor = np.array(np.expand_dims(x_test, 0), dtype=np.float32)

    input_index = interpreter.get_input_details()[0]["index"]
    interpreter.set_tensor(input_index, input_tensor)

    interpreter.invoke()

    output_details = interpreter.get_output_details()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Decode sentiment
    # label = decode_sentiment(score, include_neutral=include_neutral)

    # return {"label": label, "score": float(score),
    #    "elapsed_time": time.time()-start_at}

    return output_data

if __name__ == "__main__":
    print(predict_text("i love you"))