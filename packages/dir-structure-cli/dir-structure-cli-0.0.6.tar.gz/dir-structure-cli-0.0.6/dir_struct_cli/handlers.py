import os
import shutil
import subprocess
from posixpath import abspath, join
from pathlib import Path

import click


class BaseHandler(object):
    def __init__(self, app_name, path) -> None:
        super().__init__()
        self.path = path
        self.app_name = app_name
        self.dir_path = join(self.path, self.app_name)
        self.base_dir = Path(__file__).resolve().parent

    def check_pipenv(self):
        return bool(shutil.which("pipenv"))

    def check_pipenv_or_install(self):
        if self.check_pipenv():
            return True

        if click.confirm("Install pipenv?: "):
            click.secho("Installing Pipenv...", fg="green")

            pip_path = shutil.which("pip")

            try:
                subprocess.run([pip_path, "install", "--user", "pipenv"])
            except subprocess.SubprocessError as err:
                click.secho("Pipenv installation failed...", fg="red")
                return False
        else:
            click.secho(
                """Please follow the official installation guide
                website: https://pipenv.pypa.io/en/latest/""",
                fg="yellow",
            )
            return False

        return True

    def git_init(self):
        click.echo("Initializing git repository...")
        git = shutil.which("git")

        if git is None:
            click.echo("Failed to find git executable...Skipping!")
            return False

        os.environ["GIT_WORK_TREE"] = self.dir_path
        os.environ["GIT_DIR"] = os.path.join(self.dir_path, ".git")

        try:
            subprocess.run([git, "init"], check=True)
        except subprocess.SubprocessError:
            click.secho("A problem occurred whith git...", fg="red")
            return False

        return True

    def check_path_and_create_dir(self):
        path_to_dir = self.dir_path

        try:
            os.mkdir(path_to_dir)
        except FileExistsError:
            click.secho(
                f"'{path_to_dir}' exists. Please delete the directory or change the APP_NAME",
                fg="red",
            )
            return False

        return True

    def get_pipenv(self):
        return shutil.which("pipenv")

    def clean(self):
        pipenv_path = (
            subprocess.Popen([self.get_pipenv(), "--venv"], stdout=subprocess.PIPE)
            .communicate()[0]
            .decode("utf-8")
            .strip()
        )
        shutil.rmtree(self.dir_path)
        shutil.rmtree(pipenv_path)


class DjangoHandler(BaseHandler):
    DJANGO_REPO_URL = (
        "https://github.com/handyXx/django-skeleton/archive/refs/heads/main.zip"
    )

    def __init__(self, app_name, path) -> None:
        super().__init__(app_name, path)
        self.DJANGO_REQUIREMENTS_FILE_PATH = abspath(
            join(self.base_dir, "requirements/dj_requirements.txt")
        )

    def handle(self):
        try:
            if self.check_path_and_create_dir():
                os.chdir(self.dir_path)
                if not self.git_init():
                    click.secho(
                        """Please make sure that you have the right
                    configration of git and than run the program again.""",
                        fg="bright_cyan",
                    )
                    return False

                if self.check_pipenv_or_install():
                    pipenv = self.get_pipenv()
                    self.clone_django(pipenv)
        except Exception as e:
            self.clean()

    def clone_django(self, venv_path):
        try:
            subprocess.run(
                [venv_path, "install", "-r", self.DJANGO_REQUIREMENTS_FILE_PATH]
            )
            django_admin_path = join(
                subprocess.Popen([venv_path, "--venv"], stdout=subprocess.PIPE)
                .communicate()[0]
                .decode("utf-8")
                .strip(),
                "bin/django-admin",
            )
            subprocess.run(
                [
                    django_admin_path,
                    "startproject",
                    f"--template={self.DJANGO_REPO_URL}",
                    self.app_name,
                    ".",
                ]
            )
        except subprocess.SubprocessError:
            click.secho("There is something went wrong...")
            return False
