#https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6

import tensorflow as tf 
from keras import layers, models, optimizers, regularizers, utils, Model
import pandas as pd 
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


test = pd.read_csv ('test.csv')
train = pd.read_csv ('train.csv')
EPOCHS = 100
Y = pd.get_dummies(train['Survived'])
def organize(df):
	del df['Name']
	del df['Ticket']
	del df['Cabin'] #, 'T
	df = pd.concat([df, pd.get_dummies(df['Embarked'])], axis = 1)
	del df['Embarked']
	df = pd.concat([df, pd.get_dummies(df['Pclass'])], axis = 1)
	del df['Pclass']
	df = pd.concat([df, pd.get_dummies(df['Sex'])], axis = 1)
	del df['Sex']
	del df['PassengerId']

	df['Age'] = df['Age'] / max(df['Age'])
	df['Fare'] = df['Fare'] / max(df['Fare'])
	df['SibSp'] = df['SibSp'] / max(df['SibSp'])
	df = df.fillna(0)
	return df

X = organize(train)
pred_x = organize(test)


print(X.head())

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.33, random_state= 42)


class simple_model(Model):
	def __init__(self, classes):
		super(simple_model, self).__init__()

		self.dense1 = layers.Dense(512, activation = 'relu', kernel_regularizer = 'l2')
		self.dense2 = layers.Dense(512, activation = 'relu', kernel_regularizer = 'l2')
		self.dense3 = layers.Dense(512, activation = 'relu', kernel_regularizer = regularizers.l1_l2(l1 = 0.01, l2 = 0.01))
		self.dense4 = layers.Dense(512, activation = 'relu')
		self.Output = layers.Dense(classes, activation = 'softmax')
		
	def call(self, inputs):
		x = self.dense1(inputs)
		x = self.dense2(x)
		x = self.dense3(x)
		x = self.dense4(x)
		x = self.dense2(x)
		x = self.dense3(x)
		x = self.dense4(x)
		x = self.dense2(x)
		x = self.dense3(x)
		x = self.dense4(x)
		Output = self.Output(x)
		return Output

model = simple_model(2)
model.compile(loss = 'categorical_crossentropy', optimizer = 'Adam', metrics = ['accuracy'])
model.fit(X_train, Y_train, epochs = EPOCHS, validation_data = (X_test, Y_test))


