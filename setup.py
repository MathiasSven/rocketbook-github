import json
import platform
from getpass import getpass
from pathlib import Path
from subprocess import run

try:
    from virtualenv import cli_run
except ImportError:
    import sys

    print('ERROR: Please intall virtualenv with "pip install virtualenv"')
    sys.exit()

if not all(
    map(
        lambda i: int(i[0]) >= int(i[1]),
        zip(platform.python_version_tuple()[:-1], ("3", "8")),
    )
):
    print("WARNING: Softwear was only tested on Python 3.8 and above")

folder_path = Path(__file__).parent.absolute()
env_path = folder_path / "venv"

if not env_path.is_dir():
    cli_run([str(env_path)])

activator_path = [
    env_path / f"{folder}/activate_this.py" for folder in ["bin", "Scripts"]
]
python_path = [env_path / f"{folder}/python" for folder in ["bin", "Scripts"]]

try:
    exec(open(activator_path[0]).read(), {"__file__": activator_path[0]})
    python_path = python_path[0]
except FileNotFoundError:
    python_path = python_path[1]
    exec(open(activator_path[1]).read(), {"__file__": activator_path[1]})


run(["pip", "install", "-r", folder_path / "requirements.txt"])

__version__ = "1.0"
print("Original Repository: https://github.com/MathiasSven/rocketbook-github")
print(f"Version: {__version__}")
print("License: MIT")

with open(folder_path / "ecosystem.sample.json") as f:
    ecosystem = json.load(f)

ecosystem["script"] = str(folder_path / "manage.py")
ecosystem["interpreter"] = str(python_path)
ecosystem["env"]["GITHUB_TOKEN"] = getpass("Github Token: ")
ecosystem["env"]["GITHUB_REPO"] = input("The repo you want to push the files to: ")
ecosystem["env"]["GITHUB_BRANCH"] = input(
    "The branch the files should be pushed to, eg: heads/master or heads/main: "
)
ecosystem["env"]["GITHUB_DESTIONATION"] = input(
    "The folder/subfolder that the files should be pushed to: "
)
ecosystem["env"]["PASSWORD"] = getpass("Password to access the app: ")

port = input("Application Port (Blank for default 8031): ")
if port:
    ecosystem["env"]["PORT"] = port

with open(folder_path / "ecosystem.json", "w") as f:
    json.dump(ecosystem, f)

run(["pm2", "start", folder_path / "ecosystem.json"])
print("Done!")
