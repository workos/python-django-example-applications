# python-django-sso-example

An example Django application demonstrating how to use the [WorkOS Python SDK](https://github.com/workos/workos-python) to authenticate users via SSO.

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
   $ cd python-django-example-applications/python-django-sso-example
   ```

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
   export REDIRECT_URI='http://localhost:8000/auth/callback'
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
   (env) $ echo $REDIRECT_URI
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

10. In `python-django-sso-example/sso/views.py` change the `ORGANIZATION_ID` string value to the organization ID that you are targeting. This can be found in the WorkOS Dashboard under the Organization Settings.

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

## SSO Setup with WorkOS

Follow the [SSO authentication flow instructions](https://workos.com/docs/sso/guide/introduction) to set up an SSO connection.

When you get to the step where you provide the `REDIRECT_URI` value, use http://localhost:8000/auth/callback.

If you get stuck, please reach out to us at support@workos.com so we can help.

## Testing the Integration

12. Naviagte to the `python-django-sso-example` directory, which contains the `manage.py` file. Source the virtual environment we created earlier, if it isn't still activated from the steps above. Start the Django server locally.

```bash
$ cd ~/Desktop/python-django-sso-example/
$ source env/bin/activate
(env) $ python3 manage.py runserver
```

Once running, navigate to http://localhost:8000 to test out the SSO workflow.

Hooray!

## Need help?

When you clone this repo, the `DEBUG` setting is `False` by default in `workos_django/settings.py`. You can set `DEBUG=True` if you need to troubleshoot something during the tutorial, but you must use `DEBUG=False` in order to successfully connect to the WorkOS API.

If you get stuck and aren't able to resolve the issue by reading our API reference or tutorials, you can reach out to us at support@workos.com and we'll lend a hand.
