import ssl
import time
import json
from streamlit_lottie import st_lottie
import streamlit as st
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import hashlib
import random
import smtplib
#from streamlit_custom_notification_box import custom_notification_box

from streamlit_option_menu import option_menu

import datetime
import sqlite3
conn = sqlite3.connect('new.db')
c = conn.cursor()

import base64
import streamlit as st
import plotly.express as px

df = px.data.iris()

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("login-background (1).jpg")

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS final (username TEXT NOT NULL UNIQUE,password TEXT NOT NULL UNIQUE,mail TEXT NOT NULL UNIQUE);')
	conn.commit()
def add_userdata(username,password,mail):
	c.execute('INSERT INTO final (username,password,mail) VALUES (?,?,?)',(username,password,mail))
	conn.commit()

def add_feedback(username,feedback):
	now = datetime.datetime.now()
	c.execute('INSERT INTO fbf (username,fb,time) VALUES (?,?,?)',(username,feedback,str(now)))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM final WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM final')
	data = c.fetchall()
	st.write(data)
	st.write(type(data))
	return data

def isvalid(username):
	c.execute('SELECT * FROM final WHERE username =(?)', (username,))
	li=c.fetchall()
	return len(li)

def isvalidmail(mail):
	c.execute('SELECT * FROM final WHERE mail = (?)', (mail,))
	li=c.fetchall()
	return len(li)

def isvalidboth(username,mail):
	c.execute('SELECT * FROM final WHERE username = ? AND mail = ?', (username, mail))
	li=c.fetchall()
	return len(li)

def update(uname,password,mail):
	c.execute('UPDATE final SET password = ? WHERE username = ? AND mail = ?',(password,uname,mail))
	conn.commit()

def takemail(username):
	c.execute('SELECT * FROM final WHERE username = ?',(username,))
	li=c.fetchall()
	if(len(li)==0):
		return "no"
	return li[0][2]

with open("LASSO.txt",'rb')as f:
    model1 = pickle.load(f)

with open("RIDGE.txt", 'rb') as f:
    model2 = pickle.load(f)

with open("LINEAR.txt",'rb')as f:
    model3 = pickle.load(f)

with open("cclinear.txt",'rb')as f:
    cclinear = pickle.load(f)

with open("cclasso.txt",'rb')as f:
    cclasso = pickle.load(f)

with open("ccridge.txt",'rb')as f:
    ccridge = pickle.load(f)
	
with open("lclinear",'rb')as f:
    lclinear = pickle.load(f)

with open("lclasso",'rb')as f:
    lclasso = pickle.load(f)

with open("lcridge",'rb')as f:
    lcridge = pickle.load(f)


from email.message import EmailMessage
def otpmailing(con,mail):


	email_sender = "cfpredictor123@gmail.com"
	email_password = "qtlvbndfudxrvqrb"
	email_receiver = mail

	subject = "Authentication OTP for your login on CP predictor"
	body = str(con)

	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_receiver
	em['Subject'] = subject
	em.set_content(body)

	context = ssl.create_default_context()

	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(email_sender, email_password)
		smtp.sendmail(email_sender, email_receiver, em.as_string())


selected = option_menu(
    menu_title= None,
    options = ['Home','Predict','Contact'],
    icons = ['house','book','envelope'],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal"
)

def prediction(div,rank,rating):
	div = float(div)
	rank = float(rank)
	rating =float(rating)
	st.success("Lasso  Model  :"+str(model1.predict([[div,rank,rating]])))
	st.success("Ridge  Model  :"+str(model2.predict([[div,rank,rating]])))
	st.success("Linear Model  :"+str(model3.predict([[div,rank,rating]])))

def predictioncc(rank,rating):
	rank = float(rank)
	rating =float(rating)
	st.success("Lasso  Model  :"+str(cclasso.predict([[rank,rating]])))
	st.success("Ridge  Model  :"+str(ccridge.predict([[rank,rating]])))
	st.success("Linear Model  :"+str(cclinear.predict([[rank,rating]])))

def predictionlc(rank,rating):
	rank = float(rank)
	rating =float(rating)
	st.success("Lasso  Model  :"+str(lclasso.predict([[rank,rating]])))
	st.success("Ridge  Model  :"+str(lcridge.predict([[rank,rating]])))
	st.success("Linear Model  :"+str(lclinear.predict([[rank,rating]])))
	
import requests

def load_lottieurl(url : str):
	r = requests.get(url)
	if r.status_code !=200:
		return None
	return r.json()




def main(data):
	print("HOME")
	create_usertable()
	if selected == "Home":
		st.subheader("CODING PLATFORMS RATING PREDICTOR")
		menu = ["Login", "SignUp","Logout"]
		choice = st.selectbox("Menu", menu)
		if(choice == 'Login'):
			username = st.text_input("User Name")
			password = st.text_input("Password",type='password')
			if st.button("Login"):
				# if password == '12345':
				#create_usertable()
				hashed_pswd = make_hashes(password)
				result = login_user(username,check_hashes(password,hashed_pswd))
				if result:
					st.success("Logged In as {}".format(username))
					st.balloons()
					with open('flag.txt', 'w') as f:
						d = '1'
						f.write(d)
					f.close()
					with open("uname.txt", 'w') as file:
						pass
					file.close()
					with open("uname.txt", "w") as file:
						file.write(username)
					file.close()
				else:
					st.warning("Incorrect Username/Password")
					with open('flag.txt', 'w') as f:
						d = '0'
						f.write(d)
					f.close()
					with open("uname.txt", 'w') as file:
						pass
					file.close()
			if(st.checkbox("Forget Password")):
				lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_73lUtMVj1h.json")
				st_lottie(
					lottie_hello,
					speed=1,
					reverse=False,
					loop=True,
					quality="low",  # medium ; high
					height=None,
					width=None,
					key=None,
				)
				mail = st.text_input("Please enter your registered mail:")
				if(st.checkbox("Confirm")):
					try:
						forgetmail = takemail(username)
						if(isvalidboth(username,forgetmail)):
							if (st.button("SEND MAIL")):
								y= random.randint(100000, 999999)
								try:
									otpmailing(y, forgetmail)
								except:
									st.warning("Invalid mail")

								with open('otp2.txt', 'w') as f:
									f.write(str(y))
							# st.write("Inside the form")
							otp = st.text_input("OTP")
						# Every form must have a submit button
							passval = st.text_input("New Password",type = 'password')
							submitted = st.button("Submit")
							if submitted:
								with open('otp2.txt', 'r') as f:
									y = f.read()
								otint = int(otp)
								print(otint)
								print(type(otint))
								x = int(y)
								print(x)
								print(type(x))
								if (otint == x):
									print('if')
									print('data')
									passval=str(passval)
									update(username, make_hashes(passval), mail)
									st.write(passval)
									st.success("You have successfully changed your password")
									print('yes')
									st.info("you can now login again with your new password")
									print('login')
								else:
									print('wrong')
									st.warning("Invalid OTP")
						else:
							st.warning("Please... Remember your username and mail id correctly")
					except:
						st.warning("No valid user ID")

				#--------------------


		elif choice == "SignUp":
			lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_QFWqUliTKj.json")
			st_lottie(
				lottie_hello,
				speed=1,
				reverse=False,
				loop=True,
				quality="low",  # medium ; high
				height=None,
				width=None,
				key=None,
			)
			st.subheader("Create New Account")
			new_user = st.text_input("Username")
			new_mail = st.text_input("Mail")
			new_password = st.text_input("Password",type='password')
			if(st.button("SEND MAIL")):
				y= random.randint(100000, 999999)
				try:
					otpmailing(y, new_mail)
				except:
					st.warning("Please enter a valid mail address")
				with open('otp.txt', 'w') as f:
					f.write(str(y))
				f.close()
			#st.write("Inside the form")
			otp = st.text_input("OTP")
			#st.write(otp)
			# Every form must have a submit button
			submitted = st.button("Verified")
			if submitted:
				if(isvalid(new_user)==0):
					if(isvalidmail(new_mail)==0):
						if(isvalidboth(new_user,new_mail)==0):
							with open('otp.txt', 'r') as f:
								y = f.read()
							otint = int(otp)
							print(otint)
							print(type(otint))
							x = int(y)
							print(x)
							print(type(x))

							if (otint == x):
								print('if')
								#create_usertable()
								add_userdata(new_user, make_hashes(new_password), new_mail)
								print('data')
								st.success("You have successfully created a valid Account")
								print('yes')
								st.info("Go to Login Menu to login")
								print('login')
							else:
								print('wrong')
								st.warning("Invalid OTP")
						else:
							st.warning("Please try with other username and mail....")
					else:
						st.warning("Mail already in link with another account")
				else:
					st.warning("Username not valid - Already taken by someone")

		elif choice == "Logout":
			lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_VBz0xZZjd6.json")
			st_lottie(
				lottie_hello,
				speed=1,
				reverse=False,
				loop=True,
				quality="low",  # medium ; high
				height=None,
				width=None,
				key=None,
			)
			st.subheader("Are you sure that you want to quit....")
			if(st.button("Confirm")):
				st.success("You have logged out successfully")
				with open('flag.txt', 'w') as f:
					d = '0'
					f.write(d)
				f.close()
				with open("uname.txt", 'w') as file:
					pass
				file.close()
	if selected == "Predict":
		if int(data)==1:
			with st.sidebar:
				add_radio = st.radio(
					"Choose a coding platform",
					("CodeForces", "CodeChef")
				)
				try:
					if add_radio == 'CodeForces':
						division = st.text_input("Division")
						rank = st.text_input("Rank")
						curr_rat = st.text_input("Current Rating")
						if (st.button("Predict")):
							# try:
							prediction(division, rank, curr_rat)
							st.balloons()
					elif add_radio == 'CodeChef':
						rank = st.text_input("Rank")
						curr_rat = st.text_input("Current Rating")
						if (st.button("Predict")):
						# try:
							predictioncc(rank, curr_rat)
							st.balloons()
					else:
						rank = st.text_input("Rank")
						curr_rat = st.text_input("Current Rating")
						if(st.button("Predict")):
							predictionlc(curr_rat, rank)
							st.balloons()
				except:
					st.warning("OOPS :) Something went wrong...!")
			lottie_hello = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_ZsO4t2Bow2.json")
			st_lottie(
				lottie_hello,
				speed=1,
				reverse=False,
				loop=True,
				quality="low",  # medium ; high
				height=None,
				width=None,
				key=None,
			)

				#except:
					#st.warning("Please... fill valid details")
		else :
			st.warning("You have to login First")

	elif selected == "Contact":
		if int(data) == 1:
			st.subheader("Welcome Techie ... !")
			text = st.text_area("Enter your feedback of our application : ")
			if(st.button("Submit FeedBack")):
				with open("uname.txt", 'r') as file:
					username = file.read()
				file.close()
				add_feedback(username,text)
				st.success("Your feedback has been submitted")
				st.snow()
		else :
			st.warning("You have to login First")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://kindertravelguide.com/wp-content/uploads/2015/12/login-background.jpg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}


[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

if __name__ == '__main__':

	with st.spinner("Please Wait..."):
		with open('flag.txt', 'r') as f:
			data = f.read()

	main(data)
