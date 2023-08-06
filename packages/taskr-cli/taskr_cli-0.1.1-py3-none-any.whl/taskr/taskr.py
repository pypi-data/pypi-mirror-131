import os
import pprint
import subprocess
import sys
from dataclasses import dataclass
from importlib.machinery import ModuleSpec, PathFinder
from inspect import getattr_static, getcomments, getdoc, getmembers, isfunction
from typing import Callable, Dict, List, Optional, Union

from .utils import inVenv


class _UnsupportedCommand(Exception):
    pass


class _TaskError(Exception):
    pass


class _InternalError(Exception):
    pass


class _CustomFinder(PathFinder):
    """
    Allows us to import a file in the current diectory, that is
    the directory the file is run in. the tasks.py file should
    always be run from it's own dir, for now

    https://stackoverflow.com/a/44788410
    """

    _path = [os.getcwd()]

    @classmethod
    def find_spec(cls, fullname, path=None, target=None) -> Optional[ModuleSpec]:
        return super().find_spec(fullname, cls._path, target)


sys.meta_path.append(_CustomFinder)  # type: ignore
ENV = False


def _dummy() -> bool:
    return True


@dataclass
class Output:
    """Used to return a task with system output"""

    stdout: str = ""
    stderr: str = ""
    status: int = 0


@dataclass
class _Function:
    """Used to hold useful information on a function"""

    name: str = ""
    func: Callable = _dummy
    defaults: List = None  # type: ignore
    args: List = None  # type: ignore


class _Taskr:
    def __init__(self, module, env_debug=False) -> None:
        self.module = module
        self.funcs: Dict[str, _Function] = {}
        self._default = self._check_default()
        self._get_tasks()
        self._enforce_venv()
        self._set_env_debug(env_debug)

    def _set_env_debug(self, env_debug):
        """
        Modifies the global env debug if set
        """
        # Yuck but.. need to  think of another way to do this for v0.1.0
        if env_debug:
            global ENV
            ENV = True

    def _enforce_venv(self):
        """
        Looks to see if the tasks file requires the user to be in a venv
        """

        try:
            res = getattr_static(self.module, "VENV_REQUIRED")

            if res is not False and not inVenv():
                print("Not currently in a virtual environment, stopping")
                sys.exit(1)

        except AttributeError:
            pass

    def _check_default(self) -> str:
        """
        Runs a simple check for the efault keyword, and it a user sets it
        then mark it
        """

        try:
            return getattr_static(self.module, "DEFAULT")
        except AttributeError:
            return ""

    def _get_tasks(self) -> None:
        """
        Internal function that pulls every function from a module
        and matches it with a name, basically the core
        """
        funcs = getmembers(self.module, isfunction)
        for func in funcs:
            if not func[0].startswith("_"):
                self.funcs[func[0]] = _Function(func[0], func[1], func[1].__defaults__)

        if False:
            self.module.test_env.__code__.co_varnames
            self.module.test_env.__code__.co_varnames
            self.module.test_env.__defaults__

    @staticmethod
    def init() -> None:
        """
        Generates a default task file
        """
        from taskr.template import template

        filename = "tasks.py"

        if os.path.exists(filename):
            print("Task file already exists, skipping generation")
            return

        with open(filename, "w") as file:
            file.write(template)

        print(f"Generated sample task file {filename}")

    def list(self) -> None:
        """
        Lists available tasks

        On initialization we get a dictionary of names to functions
        This will loop through the names, and try to grab the docstrings
        of the functions and display them

        If there is a default function defines, we mark it
        """

        if len(self.funcs) == 0:
            raise _InternalError("No functions defined or found")

        longest = len(max(self.funcs.keys(), key=len))
        print("\nTasks:")

        for name, attrs in self.funcs.items():
            if name == self._default:
                name = "*" + name

            # Try to find documentation for the function
            doc = None
            docString = getdoc(attrs.func)  # Regular dock block
            docPreceed = getcomments(attrs.func)  # Single line doc above function
            if docPreceed:
                doc = docPreceed.replace("#", "").strip()
            if docString:
                doc = docString.replace("\n", "").strip()
            if not doc:
                doc = "No comment"

            print(f" {name:<{longest+1}}: {doc}")
        print("\n* = default")

    def process(self, task: str, args: List = None) -> None:
        """
        Given a task name, runs the function if it exists
        If a task that takes arguments is passed
            - make sure that only the correct amount is passed
            - can allow no args passed
        If a task that takes no arguments is passed
            - ignore all args after it
        """
        known = self.funcs.get(task)
        if known:
            try:
                if args and known.defaults:
                    if len(args) > len(known.defaults):
                        print(
                            "Warning - More arguments passed than task takes. Skipping"
                        )
                        return
                    known.func(*args)
                else:
                    known.func()
            except Exception as e:
                print(f"Error running task {task}: {e}")
        else:
            print(f"Unknown task: {task}")

    def hasDefault(self) -> bool:
        """
        Let's the CLI know if we can run a default command
        """
        return self._default != ""

    def default(self) -> bool:
        """
        Runs the default task, if it's defined
        """
        if self._default:
            if self._default not in self.funcs:
                print(f"Task {self._default} is not defined")
                return False

            self.funcs.get(self._default).func()  # type: ignore
            return True
        else:
            print("No default defined")
            return False


def _transform_cmd(cmd: Union[str, List[str]]) -> str:
    """
    Common function to handle command strings
    """
    runCmd = ""
    if type(cmd) == list:
        runCmd = " ".join(cmd)
    elif type(cmd) == str:
        runCmd = str(cmd)
    else:
        raise _UnsupportedCommand(f"Unsupported command type: {type(cmd)}")

    return runCmd


def _get_env(env: dict) -> dict:
    """
    Common function to get and set environment variables
    """

    # Merge passed in dict with users envs
    set_envs = {**env, **os.environ.copy()}

    # If we want to debug set ENVs, check the global flag
    global ENV
    if ENV:
        print("Current ENV variables: \n")
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(dict(set_envs))

    return set_envs


def run_env(cmd: Union[str, List[str]], env: Optional[dict] = {}) -> bool:
    """
    Runs a simple command, takes a list or string
    Returns whether the command has a normal exit (True), or not (False)
    """
    print("WARNING - This method is deprecated. Use 'taskr.run' instead")
    return run(cmd, env)


def run(cmd: Union[str, List[str]], env: Optional[dict] = None) -> bool:
    """
    Runs a command, with optional environment variables passed

    This also attaches a copy of the users environment variables for every run
    This makes tasks work in a virtual env too, if the task calls a module only installed
    in one (e.g. python -m my_module_I_installed_in_this_venv)

    Returns whether the command has a normal exit (True), or not (False)

    """
    if not env:
        env = {}

    runCmd = _transform_cmd(cmd)
    env = _get_env(env)

    return subprocess.Popen(runCmd, shell=True, env=env).wait() == 0


def run_output(cmd: Union[str, List[str]], env: Optional[dict] = None) -> Output:
    """
    Returns the status of the call, as well as the output
    TODO - combine this with run_env. Will be a bit weird
    """
    if not env:
        env = {}

    runCmd = _transform_cmd(cmd)
    env = _get_env(env)

    res = subprocess.run(runCmd, shell=True, capture_output=True, env=env)

    data = Output()
    data.stdout = res.stdout.decode("utf-8").rstrip()
    data.stderr = res.stderr.decode("utf-8").rstrip()
    data.status = res.returncode == 0

    return data


def run_conditional(*args: Callable) -> bool:
    """
    Runs functions in orders, on the condition the previous passes
    Functions must return a status, (True or False)

    Returns whether the command has a normal exit (True), or not (False)
    """
    for f in args:
        if not callable(f):
            print(f"{f} is not callable, bailing")
            return False

        print(f"▸ Running {f.__name__}")
        ret = f()

        # Support void functions
        if ret is None:
            return True
        if not ret:
            print(f"Task {f.__name__} failed, bailing")
            return False

    return True
