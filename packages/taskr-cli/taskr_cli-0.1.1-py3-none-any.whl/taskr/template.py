template = '''from taskr import taskr

# Taskr config settings

## The default task to run, when typing just 'taskr'
DEFAULT = "all"

## If you want people to only use taskr in a VENV, set this to True. If not, set to
## false or delete it
VENV_REQUIRES = True

def build() -> bool:
    """
    Builds a wheel
    """
    return taskr.run(["python -m build --wheel -n;", "echo 'Artifact:'; ls dist/"])


# Remove build artifacts, cache, etc.
def clean() -> bool:
    ret = taskr.cleanBuilds()
    ret = taskr.cleanCompiles()
    return ret


# Run tests
def test() -> bool:
    return taskr.run("python -m pytest tests/ -vv")


# Run black
def fmt() -> bool:
    return taskr.run("python -m black .")


# Sort imports
def sort() -> bool:
    return taskr.run("python -m isort --atomic .")


# Checks types
def mypy() -> bool:
    return taskr.run("python -m mypy")


# Check flake8
def flake() -> bool:
    return taskr.run("python -m flake8")


# Runs all static analysis tools
def all() -> bool:
    return taskr.run_conditional(fmt, mypy, sort, flake)


# Runs a server based on a passed in variable
def run_server(env: str = "dev") -> bool:
    ENVS = {"ENV": env}
    return taskr.run("python server.py", ENVS)


# Bump setup.py version
def bump(version: str = None) -> bool:
    return taskr.bumpVersion(version)
'''
