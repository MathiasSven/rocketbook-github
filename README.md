![Logo](https://i.imgur.com/qNeteXH.png)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
# Rocketbook Github
Small app that checks your Gmail for new Rocketbook emails and sends the attached pdf/jpeg to a specified Github repo and deletes the email.

## Setup
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
8. Lastly, upload the credintials.json to the application via the page that was open in step 4 (The index page of the Heroku application).
#  
That is it! After the application will start ruining the `Rocketbook --> Github` script every 3 minutes. You will be redirected to a dashboard where you can view the info logs and force the app to run the main script at your request (This will not stop the automatic execution)
