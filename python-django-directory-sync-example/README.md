# python-django-directory-sync-example
A basic Django app that uses the [WorkOS Python SDK](https://github.com/workos-inc/workos-python) to support Directory Sync.

## Prerequisites
- Python 3.6+

## Directory Sync Setup with WorkOS
First, follow the [Create a New Directory Connection](https://workos.com/docs/directory-sync/guide/create-new-directory-connection) step in the WorkOS Directory Sync guide.

If you get stuck, please reach out to us at support@workos.com so we can help.

## Django Project Setup

### Clone Directory

1. In your CLI, navigate to the directory into which you want to clone this git repo.
   ```bash
   $ cd ~/Desktop/
   ```

2. Clone the main git repo for these Python example apps using your preferred secure method (HTTPS or SSH).
   ```bash
   # HTTPS
   $ git clone https://github.com/workos-inc/python-django-example-applications.git
   ```

   or

   ```bash
   # SSH
   $ git clone git@github.com:workos-inc/python-django-example-applications.git
   ```

3. Navigate to the Directory Sync example app within the cloned repo.
   ```bash
   $ cd python-django-example-applications/python-django-directory-sync-example
   ````

### Install Dependencies

4. Create and source a Python virtual environment. You should then see `(env)` at the beginning of your command-line prompt.
   ```bash
   $ python3 -m venv env
   $ source env/bin/activate
   (env) $
   ```

5. Install the cloned app's dependencies. If the `pip` command doesn't work, try `pip3` instead.
   ```bash
   (env) $ pip install -r requirements.txt
   ```

### Set Environment Variables

6. Obtain and make note of the following values. In the next step, these will be set as environment variables.
   - Your [WorkOS API key](https://dashboard.workos.com/api-keys)
   - Your `WEBHOOKS_SECRET`, retrievable from the URL in the WEBHOOKS area of the WorkOS dashboard. This is only required if you are utilizing the webhooks route of this application to receive and validate webhook events. 

7. Ensure you're in the root directory for the example app, `python-django-directory-sync-example/`. Create a `.env` file to securely store the environment variables. Open this file with the Nano text editor. (This file is listed in this repo's `.gitignore` file, so your sensitive information will not be checked into version control.)
   ```bash
   (env) $ touch .env
   (env) $ nano .env
   ```

8. Once the Nano text editor opens, you can directly edit the `.env` file by listing the environment variables:
    ```bash
    export WORKOS_API_KEY=<value found in step 6>
    export WEBHOOKS_SECRET=<value found in step 6>
    ```

   To exit the Nano text editor, type `CTRL + x`. When prompted to "Save modified buffer", type `Y`, then press the `Enter` or `Return` key.

9. Source the environment variables so they are accessible to the operating system.
   ```bash
   (env) $ source .env
   ```

   You can ensure the environment variables were set correctly by running the following commands. The output should match the corresponding values.
   ```bash
   (env) $ echo $WORKOS_API_KEY
   (env) $ echo $WEBHOOKS_SECRET
   ```

### Run Django Migrations and Start Server

10. Run the Django migrations. Again, ensure you're in the `python-django-directory-sync-example/` directory where the `manange.py` file is.
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

11. Start the server.
  ```bash
  (env) $ python3 manage.py runserver
  ```
  To serve static files in development while still having debug=True in settings.py to able to send requests to WorkOS, be sure to include the --insecure flag when starting the server locally.
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

12. Once the server is running, navigate to http://localhost:8000 to view the home page of the app where you can then select the view for users or groups.

    - The `/users` URL corresponds to the WorkOS API's [List Directory Users endpoint](https://workos.com/docs/reference/directory-sync/user/list)
    - The `/groups` URL corresponds to the WorkOS API's [List Directory Groups endpoint](https://workos.com/docs/reference/directory-sync/group/list)
    - You can extend this Django example app by adding views to `directory_sync/views.py` for the other available [Directory Sync API endpoints](https://workos.com/docs/reference/directory-sync).


13. WorkOS sends Webhooks as a way of managing updates to Directory Sync connections. The Webhooks section of the WorkOS Dashboard allows you to send test webhooks to your application. The Test Webhooks section of this application allows you to visualize the validated webhooks directly in this application in real-time. [Please review the tutorial here](https://workos.com/blog/test-workos-webhooks-locally-ngrok) for details on how this can be done locally. 

## Need help?

When you clone this repo, the `DEBUG` setting is `False` by default in `workos_django/settings.py`. You can set `DEBUG=True` if you need to troubleshoot something during the tutorial, but you must use `DEBUG=False` in order to successfully connect to the WorkOS API. You may also leave the `DEBUG` setting as `False` and connect with WorkOS if you include the `--insecure` flag as referenced in step 11. 

If you get stuck and aren't able to resolve the issue by reading our API reference or tutorials, please  reach out to us at support@workos.com and we'll help you out.
