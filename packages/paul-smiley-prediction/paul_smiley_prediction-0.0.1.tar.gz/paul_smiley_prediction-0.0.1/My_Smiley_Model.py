import My_Smiley_Helper
import pickle
IMG_SIZE=28

# Uploading the model from pickle 
with open("CNN_Model.pkl", "rb") as pickle_file:
  CNN_model = pickle.load(pickle_file)

"""
This Function takes in a path of an image, and resizes
it to the specified IMG size

Then reshapes the image into a convolutional input value of
(1,28,28,1)

Then calls the model.predict function on this input

The output is dictionary with two keys: Happy / Sad
and there respective probabilities (confidence) for
the prediction

"""

def make_prediction(data, IMG_SIZE=IMG_SIZE):
    data = data.reshape(1, IMG_SIZE, IMG_SIZE, 1)
    prediction = CNN_model.predict(data)[0]
    return_dict = {"Sad": prediction[0], "Happy": prediction[1] }
    return return_dict
