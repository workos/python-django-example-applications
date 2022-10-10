# python-django-audit-logs-example

An example Django application demonstrating how to use the [WorkOS Python SDK](https://github.com/workos/workos-python) to send and retrieve Audit Log events. This example is not meant to show a real-world example of an Audit Logs implementation, but rather to show concrete examples of how events can be sent using the Python SDK.

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
   $ cd python-django-example-applications/python-django-audit-logs-example
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
   - Your [WorkOS Client ID](https://dashboard.workos.com/configuration)

6. Ensure you're in the root directory for the example app, `python-django-audit-logs-example/`. Create a `.env` file to securely store the environment variables. Open this file with the Nano text editor. (This file is listed in this repo's `.gitignore` file, so your sensitive information will not be checked into version control.)

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

10. The final setup step is to start the server.

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

Navigate to `localhost:8000` in your web browser. You should see a place to enter your organization ID. This can be found in the WorkOS Dashboard for the Organization you'd like to send logs to.

You can stop the local Django server for now by entering `CTRL + c` on the command line.

### Audit Logs Setup with WorkOS

11. Follow the [Audit Logs configuration steps](https://workos.com/docs/audit-logs/emit-an-audit-log-event/sign-in-to-your-workos-dashboard-account-and-configure-audit-log-event-schemas) to set up the following 5 events that are sent with this example:

Action title: "user.signed_in" | Target type: "team"
Action title: "user.logged_out" | Target type: "team"
Action title: "user.organization_set" | Target type: "team"
Action title: "user.organization_deleted" | Target type: "team"
Action title: "user.connection_deleted" | Target type: "team"

12. Next, take note of the Organization ID for the Org which you will be sending the Audit Log events for. This ID gets entered into the splash page of the example application.

13. Once you enter the Organization ID and submit it, you will be brought to the page where you'll be able to send the audit log events that were just configured. You'll also notice that the action of setting the Organization triggered an Audit Log already. Click the buttons to send the respective events.

14. To obtain a CSV of the Audit Log events that were sent for the last 30 days, click the "Export Events" button. This will bring you to a new page where you can download the events. Downloading the events is a 2 step process. First you need to create the report by clicking the "Generate CSV" button. Then click the "Access CSV" button to download a CSV of the Audit Log events for the selected Organization for the past 30 days.

## Need help?

If you get stuck and aren't able to resolve the issue by reading our API reference or tutorials, you can reach out to us at support@workos.com and we'll lend a hand.
