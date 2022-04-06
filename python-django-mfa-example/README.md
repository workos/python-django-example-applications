# python-django-sso-example
An example Django application demonstrating how to use the [WorkOS MFA API](https://workos.com/docs/mfa/guide) using the [Python SDK](https://github.com/workos-inc/workos-python) to authenticate users.

## Prerequisites
- Python 3.6+


## Django Project Setup

1. Clone the main git repo for these Python example apps using your preferred secure method (HTTPS or SSH).
   ```bash
   # HTTPS
   $ git clone https://github.com/workos/python-django-example-applications.git
   ```

   or

   ```bash
   # SSH
   $ git clone git@github.com:workos/python-django-example-applications.git
   ```

2. Navigate to the Admin Portal example app within the cloned repo.
   ```bash
   $ cd python-django-example-applications/python-django-mfa-example
   ````


3. Create and source a Python virtual environment. You should then see `(env)` at the beginning of your command-line prompt.
   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   (env) $
   ```

4. Install the cloned app's dependencies. If the `pip` command doesn't work, try `pip3` instead.
   ```bash
   (env) $ pip install -r requirements.txt
   ```

5. Obtain and make note of the following values. In the next step, these will be set as environment variables.
   - Your [WorkOS API key](https://dashboard.workos.com/api-keys)
   - Your [SSO-specific, WorkOS Client ID](https://dashboard.workos.com/sso/configuration)
   - The redirect URI. For this example, we'll use http://localhost:8000/auth/callback

6. Ensure you're in the root directory for the example app, `python-django-sso-example/`. Create a `.env` file to securely store the environment variables. Open this file with the Nano text editor. (This file is listed in this repo's `.gitignore` file, so your sensitive information will not be checked into version control.)
   ```bash
   (env) $ touch .env
   (env) $ nano .env
   ```

7. Once the Nano text editor opens, you can directly edit the `.env` file by listing the environment variables:
   ```bash
   export WORKOS_API_KEY=<value found in step 6>
   export WORKOS_CLIENT_ID=<value found in step 6>
   ```

   To exit the Nano text editor, type `CTRL + x`. When prompted to "Save modified buffer", type `Y`, then press the `Enter` or `Return` key.

8. Source the environment variables so they are accessible to the operating system.
   ```bash
   (env) $ source .env
   ```

   You can ensure the environment variables were set correctly by running the following commands. The output should match the corresponding values.
   ```bash
   (env) $ echo $WORKOS_API_KEY
   (env) $ echo $WORKOS_CLIENT_ID
   ```

9. Run the Django migrations. Again, ensure you're in the `python-django-sso-example/` directory where the `manange.py` file is.
   ```bash
   (env) $ python3 manage.py migrate
   ```

   You should see output like:
   ```bash
   Operations to perform:
   Apply all migrations: admin, auth, contenttypes, sessions
   Running migrations:
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   . . .
   ```

10. In `python-django-sso-example/sso/views.py` change the `CONNECTION_ID` string value to the connection ID that you are targeting. This can be found in the WorkOS Dashboard under the Connection Settings. 

11. The final setup step is to start the server.
   ```bash
   (env) $ python3 manage.py runserver --insecure
   ```

   You'll know the server is running when you see no warnings or errors in the CLI, and output similar to the following is displayed:

   ```bash
   Watching for file changes with StatReloader
   Performing system checks...

   System check identified no issues (0 silenced).
   March 18, 2021 - 04:54:50
   Django version 3.1.7, using settings 'workos_django.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

   Navigate to `localhost:8000` in your web browser. You should see a "Login" link. If you click this link, you'll be redirected to an HTTP `404` page because we haven't set up SSO yet!

   You can stop the local Django server for now by entering `CTRL + c` on the command line.


## Using the MFA application

11. This application is meant to showcase the MFA API and how to interact with it using the WorkOS Python SDK. It is not meant to show a real-life example of how MFA should be implemented. 

   The app supports two types of MFA flows, SMS and Time-based One Time Password (TOTP). 

   SMS: The SMS flow requires you to send a code via text message. You can customize this message, but the message must include the string "{{code}}". This string of characters tells the WorkOS API to generate a random code that will be populated automatically. If "{{code}}" is not included in the message, the authentication cannot be completed. 

   TOTP: This type of authentication requires the use of a 3rd party authentication app (1Password, Authy, Google Authenticator, Microsoft Authenticator, Duo, etc). Scan the QR code from the Factor Details page to create the corresponding factor in the 3rd party app, then enter the time-based password when prompted in this MFA application.

   TOTP NOTE - Since all storage is being done via browser cookies, only 1 TOTP type connection can be added at a time to this app due to limitations on the size of the cookies that browsers can store. This is due to the size of the QR code. 

## Need help?

When you clone this repo, the `DEBUG` setting is `False` by default in `workos_django/settings.py`. You can set `DEBUG=True` if you need to troubleshoot something during the tutorial, but you must use `DEBUG=False` in order to successfully connect to the WorkOS API.

If you get stuck, make sure to reference the MFA docs at https://workos.com/docs/mfa/guide. 

If you're still having trouble and aren't able to resolve the issue by reading our API reference or tutorials, you can reach out to us at support@workos.com and we'll lend a hand.
