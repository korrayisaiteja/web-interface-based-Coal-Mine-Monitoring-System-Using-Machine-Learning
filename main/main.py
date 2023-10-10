import streamlit as st
import pandas as pd
import pickle
import base64
import sqlite3
import hashlib

# loading in the model to predict on the data
pickle_in = open('gt.pkl', 'rb')
heart = pickle.load(pickle_in)
# Security
#passlib,hashlib,bcrypt,scrypt

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():

	st.title("Coal Mining System")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		def add_bg_from_local(image_file):
			with open(image_file, "rb") as image_file:
				encoded_string = base64.b64encode(image_file.read())
				st.markdown(
					f"""
		    <style>.stApp {{
		background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
	    background-size: cover
        }}
    </style>
    """,
        unsafe_allow_html=True)
		add_bg_from_local('images/home.jpg')

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))
				def prediction(Temp	,conc_gas):
					prediction = heart.predict([[Temp,conc_gas]])
					print(prediction)
					return prediction
				st.title("Coal Mine Monitoring System")
				Temp = st.slider("Temperature",15.0,150.0)
				conc_gas = st.slider("gas conscuntartion",15.0,450.0)
				result =""
				if st.button("Predict"):
					result = prediction(Temp,conc_gas)
					if result == 1:
						st.error("Danger evacute!")
					else:
						st.success("Safe")
                	

				
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()