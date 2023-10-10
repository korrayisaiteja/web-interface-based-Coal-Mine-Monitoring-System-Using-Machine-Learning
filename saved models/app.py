import pandas as pd
import numpy as np
import pickle
import streamlit as st

# loading in the model to predict on the data
pickle_in = open('rfc.pkl', 'rb')
heart = pickle.load(pickle_in)


def prediction(Temp	,conc_gas):

	prediction = heart.predict([[Temp,conc_gas]])
	print(prediction)
	return prediction
	

# this is the main function in which we define our webpage
def main():
	st.title("Coal Mine Monitoring System")
	Temp = st.slider("Temperature",15.0,150.0)
	conc_gas = st.slider("gas conscuntartion",15.0,450.0)
	result =""

	if st.button("Predict"):
		result = prediction(Temp,conc_gas)
		print(result)
		if result == 1:
			st.error("Danger evacute!")
		else:
			st.success("Safe")

	
	
if __name__=='__main__':
	main()
