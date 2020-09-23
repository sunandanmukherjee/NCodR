#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf

import argparse
import os, sys


parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
parser.add_argument("-i", "--input", required=True, dest="input_file", type=str,
					help="Input file name [required].")
parser.add_argument("-m", "--model", required=True, dest="model_path", type=str,
					help="Model prefix or path [required].")
parser.add_argument("-n", "--no-of-epochs", required=False, dest="number_of_epochs", default=2, type=int,
                    help="Number of epochs [default = 2].")
args = parser.parse_args()
input_file = args.input_file
model_path = args.model_path
number_of_epochs = args.number_of_epochs



#checking the input file
if input_file != "":
	if(os.path.isfile(input_file) == False): #checking input_file
		print ("input location/file: "+input_file+" provided by the user doesn't exist", file=sys.stderr)
		sys.exit(1)


dataset_full = pd.read_csv(input_file, sep='\t')
train_data, test_data = train_test_split(dataset_full, test_size=0.1, shuffle=True)
print("Number of training samples: ",len(train_data))
print("Number of testing sample: ",len(test_data))

num_class = {'L':1, 'M':2, 'R':3, 'SNO':3, 'T':4, 'SN':5, 'P':6}

x_train_data = train_data.drop(["Sequence_Descriptor", "Y"], axis=1)
y_train_data = train_data["Y"]
x_test_data = test_data.drop(["Sequence_Descriptor", "Y"], axis=1)
y_test_data = test_data["Y"]
y_train_data = (pd.Series(y_train_data)).map(num_class)
y_test_data = (pd.Series(y_test_data)).map(num_class)
NUM_COLUMNS = len(x_train_data.columns)
dataset_train = tf.data.Dataset.from_tensor_slices((x_train_data.values,y_train_data.values))
for feat, targ in dataset_train.take(5):
	print ('Features: {}, Target: {}'.format(feat, targ))

train_dataset = dataset_train.shuffle(len(train_data)).batch(1)
dataset_test = tf.data.Dataset.from_tensor_slices((x_test_data.values,y_test_data.values))
test_dataset = dataset_test.shuffle(len(train_data)).batch(1)

'''
#This part needs to tested to find the correct values
tf.keras.optimizers.Adam(
	learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False,
	name='Adam', **kwargs
)
'''

def get_compiled_model():
	model = tf.keras.Sequential([
		tf.keras.layers.Dense(128, activation='relu'),
		tf.keras.layers.Dense(128, activation='relu'),
		tf.keras.layers.Dense(1)
		])
	model.compile(optimizer='adam',
			   loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
			   metrics=['accuracy'])
	return model

model = get_compiled_model()
checkpoint_path = model_path+"{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

cp_callback = tf.keras.callbacks.ModelCheckpoint(
	filepath=checkpoint_path,
	verbose=1, 
	save_weights_only=True,
	period=1)


model.fit(train_dataset, 
		  epochs=number_of_epochs,
		  callbacks=[cp_callback])

#model.save_weights('training_1/trial1')

test_loss, test_accuracy = model.evaluate(test_dataset)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))
predictions = model.predict(test_dataset)





