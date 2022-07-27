# python-django-admin-portal-example
A basic Django app that uses the [WorkOS Python SDK](https://github.com/workos/workos-python) to access the Admin Portal.

## Prerequisites
- Python 3.6+


### Clone Directory

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
   $ cd python-django-example-applications/python-django-admin-portal-example
   ````

### Install Dependencies

3. Create and source a Python virtual environment. You should then see `(env)` at the beginning of your command-line prompt.
   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   (env) $
   ```

4. Move in to the app directory and install the cloned app's dependencies. There are two workos_django directories in this repo, however you'll want to be in the top level directory that includes the manage.py file for this step. 
   ```bash
   (env) $ cd workos_django
   (env) $ pip install -r requirements.txt
   ```

### Set Environment Variables

5. Obtain and make note of the following values. In the next step, these will be set as environment variables.
   - Your [WORKOS_API_KEY](https://dashboard.workos.com/api-keys)
   - Your `WORKOS_CLIENT_ID`, in the format `client_<random-alphanumeric-string>`, retrievable from WorkOS dashboard under Configuration.

6. Ensure you're in the root app directory for the example app, `workos_django/` where the `manage.py` file resides. Create a `.env` file to securely store the environment variables. Open this file with the Nano text editor. (This file is listed in this repo's `.gitignore` file, so your sensitive information will not be checked into version control.)
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

9. Run the Django migrations. Again, ensure you're in the `workos_django/` directory where the `manange.py` file is.
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

10. Update the Admin Portal Redirect Link in the Configuration page of your WorkOS Dashboard

   To configure the page where the user will be redirected after completing the organization creation/connection through Admin Portal, enter the url in the Admin Portal Redirect Link in the Configuration page of your WorkOS dashboard. This URL must be https. 


## Start the server

11. Start the server.
  
  To serve static files in development while still having `debug=True` in settings.py to able to send requests to WorkOS, be sure to include the `--insecure` flag when starting the server locally.
  ```bash
  (env) $ python3 manage.py runserver --insecure
  ```

  You'll know the server is running when you see no errors in the CLI, and output similar to the following is displayed:

  ```bash
  Watching for file changes with StatReloader
  Performing system checks...

  System check identified no issues (0 silenced).
  March 18, 2021 - 04:54:50
  Django version 3.1.7, using settings 'workos_django.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
  ```

12. Once the server is running, navigate to http://localhost:8000 to view the home page of the app. Here you'll enter the name of the Organization to be created, and all associated domains. The domains should be entered as space-separated values, e.g. `domain1.com domain2.com domain3.com`

Note that the organization must be a new organization that does not yet exists in your WorkOS dashboard. 

13. Click on the button to create your Organization and log in to the Admin Portal workflow! 

## Need help?

When you clone this repo, the `DEBUG` setting is `False` by default in `app.py`. You can set `DEBUG = True` if you need to troubleshoot something during the tutorial, but you must use `DEBUG = False` in order to successfully connect to the WorkOS API.

If you get stuck and aren't able to resolve the issue by reading our API reference or tutorials, please  reach out to us at support@workos.com and we'll help you out.
