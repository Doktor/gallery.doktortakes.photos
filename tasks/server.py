import os
import platform
import shlex
import signal
import subprocess
import traceback
from invoke import task

wsl = "microsoft" in platform.uname()[3].lower()

log_dir = "logs"
default_log_file = "dev_server.log"
pid_file = os.path.join(log_dir, "dev_server.pid")


def run_command(c: str, filename: str) -> subprocess.Popen:
    return subprocess.Popen(
        shlex.split(c),
        stdout=open(os.path.join(log_dir, filename), 'ab'),
        stderr=subprocess.STDOUT)


def run_celery(log_file="celery.log"):
    print("Starting Celery worker")
    run_command("celery -A core worker --loglevel=info", log_file)


def run_django(log_file="django.log"):
    print("Starting Django development server")
    run_command("python manage.py runserver 0.0.0.0:8000", log_file)
    print("Listening on 0.0.0.0:8000")


def run_redis(log_file="redis.log"):
    print("Starting Redis server")
    run_command("redis-server", log_file)


def run_webpack(log_file="webpack.log"):
    print("Starting Webpack build listener")
    run_command("./node_modules/.bin/webpack --config webpack.dev.js", log_file)


def stop_development_server(pid):
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        print("Warning: the development server is not running.")
    except OSError as e:
        print("An unknown error occurred when attempting to stop the development server.")
        traceback.print_exc()
        raise SystemExit(1)
    else:
        print("Successfully stopped development server.")
    finally:
        with open(pid_file, 'w') as f:
            f.truncate(0)


@task()
def start_server(ctx, separate_log_files=False):
    print("Starting development server.")

    # Check if the server is already running
    with open(pid_file) as f:
        pid = f.read().strip()

        if pid:
            if input("Another instance of the development server is still "
                     "running. Attempt to stop it? (Y/N) ").lower() == "y":
                stop_development_server(int(pid))
                print("Continuing with development server startup.")
            else:
                print("Development server not started.")
                print("Existing process group ID:", pid)
                raise SystemExit(1)

    kwargs = {}

    if not separate_log_files:
        kwargs["log_file"] = default_log_file

    run_celery(**kwargs)
    run_django(**kwargs)
    run_redis(**kwargs)
    run_webpack(**kwargs)

    pid = str(os.getpid())

    with open(pid_file, 'w') as f:
        f.write(pid)

    print("\nStarted development server.")
    print("Process group ID:", pid)


@task
def stop_server(ctx):
    print("Stopping development server.")

    with open(pid_file) as f:
        pid = f.read().strip()

        if pid:
            stop_development_server(int(pid))
        else:
            print("Invalid process group ID:", pid)
            raise SystemExit(1)


@task(pre=[stop_server], post=[start_server])
def restart_server(ctx):
    pass


@task
def logs(ctx):
    log_file = os.path.join(log_dir, default_log_file)

    if wsl:
        ctx.run(f"tail ---disable-inotify -f {log_file}")
    else:
        ctx.run(f"tail -f {log_file}")
