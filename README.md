![Logo](https://i.imgur.com/qNeteXH.png)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
# Rocketbook Github
Small app that checks your Gmail for new Rocketbook emails and sends the attached pdf/jpeg to a specified Github repo and deletes the email.

## Free Setup (Heroku)
1. Create a [Personal access token](https://github.com/settings/tokens) and give it `repo` access, making note of the generated token.

2. [Signup](https://signup.heroku.com/) to Heroku if you don't already have an account and deploy the app using the button bellow:

   [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

3. At deployment chose a name for your application and set the appropriate configurations. *Note*: The PASSWORD variable is only required to access the webpage where you can upload Google API Credentials and look at info logs on the app.

4. Open the app. After login (with the password you provided) you will be taken to the index page, make note of the `redirect uri` provided and click on the Google API link.

5. Once in the Google Cloud Platform click on `Select a project` as shown in image bellow and create a new project.

   ![enter image description here](https://i.imgur.com/uc7djnLl.png)
6. After creating the project and selecting it, look for the *Gmail API* as shown in the image bellow. Select it and then Enabled it.

   ![enter image description here](https://i.imgur.com/9xEtcYfl.png)
7. Once enabled you will be taken to this page:

   ![enter image description here](https://i.imgur.com/6pkfX9Xl.png)
   
   As show click on `Create Credentials`. For this section just follow these configurations:
	- Select an API --- **Gmail API**
	- What data will you be accessing? --- **User data**
		- Next
	- App name --- *Something*
	- User support email **and** Developer contact information --- *Your Email*
	  - Save and Continue
	- *Skip Scopes*
	  - Save and Continue
	- Application type --- **Web application**
	- Authorized redirect URIs --- **ADD URI**
	
   On the ADD URI section just paste the `redirect uri` provided in step 4. Finally once that is done click on *Create* and download the credentials generated.
8. Upload the credintials.json to the application via the page that was open in step 4 (The index page of the Heroku application).

9. Lastly, given you are running a free tier of Heroku, you will need a seperate service to ping your app at least once every 30 mins otherwise it will idle and stop running tasks. I recommend [Kaffeine](http://kaffeine.herokuapp.com/) with sleep turned on but if you find another one it should also work, though keep in mind you want one that can also stop pinging on set times because without setting a credit card Heroku only gives you about 22 days of continuous dyno operation per month as of late 2021.
#  
That is it! After that the application will start ruining the `Rocketbook --> Github` script every 3 minutes. You will be redirected to a dashboard where you can view the info logs and force the app to run the main script at your request (This will not stop the automatic execution)
## Server Setup
1. Create a [Personal access token](https://github.com/settings/tokens) and give it `repo` access, making note of the generated token.

2. Make sure both [pm2](https://pm2.keymetrics.io/docs/usage/quick-start/) and [virutalenv](https://pypi.org/project/virtualenv/) are installed.

3. `git clone` this repository where you want to have the application located.

4. Run `setup.py` and provide it with the appropriate variables.

5. Open the port on your firewall, `utf allow PORT` if you are using Ubuntu.

6. Access your app at `http://SERVERIP:PORT`, follow steps 4-8 from the setup above and that is it! No need to worry about Dyno idling.
## Generic Setup Info
To deploy the app use `python manage.py` and these are the required **ENVs**:
- GITHUB_TOKEN `An access token as described on step 1 on Free Setup`
- GITHUB_REPO `The repo you want to push the files to`
- GITHUB_BRANCH `The branch the files should be pushed to, eg: heads/master or heads/main`
- GITHUB_DESTIONATION `The folder/subfolder that the files should be pushed to`
- PASSWORD `Password to access the app`
- PORT `Port in which the app should run`
