import os
import platform
import shlex
import subprocess
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


@task()
def start_server(ctx, separate_log_files=False):
    print("Starting development server")

    with open(pid_file) as f:
        pid = f.read().strip()

        if pid:
            try:
                os.kill(int(pid), 0)
            except OSError:
                pass
            else:
                print("Another instance of the development server is still running!")
                print("Process group ID:", pid)
                raise SystemExit(1)

    if separate_log_files:
        kwargs = {}
    else:
        kwargs = {"log_file": default_log_file}

    run_celery(**kwargs)
    run_django(**kwargs)
    run_redis(**kwargs)
    run_webpack(**kwargs)

    pid = str(os.getpid())

    with open(pid_file, 'w') as f:
        f.write(pid)

    print("\nStarted development server")
    print("Process group ID:", pid)


@task
def stop_server(ctx):
    print("Stopping development server")

    with open(pid_file, 'r+') as f:
        pid = f.read().strip()

        ctx.run(f"kill -TERM -- -{pid}")

        f.truncate(0)

    print("Stopped development server")


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
