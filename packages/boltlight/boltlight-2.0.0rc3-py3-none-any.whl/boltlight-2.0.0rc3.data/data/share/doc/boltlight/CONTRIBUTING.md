# Contributing

Here's a brief list of areas where contributions are particularly welcome:
- adding support for new LN implementations
- maintaining or extending the existing LN implementation support
- security improvements
- testing and bugfixing

To get started, please consider the following:
- first discuss the change via issue, email or any other method
  with the project owners
- follow our [coding guidelines](/doc/coding_guidelines.md) when developing


## Testing

Boltlight has unit and functional tests.
Both test suites are implemented using the
[`unittest`](https://docs.python.org/3/library/unittest.html) framework.

To run all available tests, use:

```bash
$ ./unix_helper test
```

This will use [`tox`](https://tox.readthedocs.io/en/latest/) and, if available,
[`pyenv`](https://github.com/pyenv/pyenv) (in order to test the code with
multiple Python versions).
If `tox` is not installed you will be prompted with a message asking if you
wish to install it.

Running specific tests (see `-f` below) requires
[`tox-factor`](https://github.com/rpkilby/tox-factor). If it's not installed,
you will be prompted to do so.

### Unit

To run only the unit tests, use:

```bash
$ ./unix_helper test -f unit
```

### Functional

To run only the functional tests, use:

```bash
$ ./unix_helper test -f functional
```


## Linting

To check the code for common errors run:

```bash
$ ./unix_helper lint
```

This will check the code with
[`pycodestyle`](https://github.com/PyCQA/pycodestyle) and
[`pylint`](https://github.com/PyCQA/pylint).

Results of linting procedure are output in the `reports` directory.


## Formatting

To format the code we use [`yapf`](https://github.com/google/yapf).

Run `git config core.hooksPath .githooks` in order to change the project git
hooks location. Doing so `yapf` will be automatically called at pre-commit
time on staged files, eventually adding unstaged formatting changes.

Otherwise, if you don't wish to activate the git hook, you can manually call
`./unix_helper format` from the project root directory. This will check if
`yapf` is installed, installs it if missing and runs the same script that the
git hook calls.


## Developing in Docker

Sometimes it can be useful to run boltlight in a docker container, e.g. when
running the underlying LN node in docker as well.

To ease development using a docker container, the image can be built with
boltlight installed in editable mode. Assuming the running user has access to
the docker daemon, this results in the ability to mount the developer's working
source code inside the container, having it updated at all times without the
need to re-build the image after every change.

To enable development mode for the docker image, pass `DEVELOPMENT=1` as build
argument. The `unix_helper` script will automatically do so if the environment
variable `DEVELOPMENT` is set to `1` and tag the resulting image will be tagged
with the `-dev` suffix added to its version.

The `unix_helper` script will also set the `USER_ID` variable to the current
users's uid if development mode is on, in order to avoid issues with file and
directory permissions while trying to access files created outside the
container from inside of it or vice versa.

To build the image export the `DEVELOPMENT` variable and call `unix_helper`:

```bash
$ export DEVELOPMENT=1
$ ./unix_helper docker_build
[...]
Successfully tagged hashbeam/boltlight:<version>-dev
```

To run the working directory version of boltlight in a docker container, invoke
docker specifying mounts for boltlight's data directory and the paths
containing the changes to be reflected in the running container.
The entrypoint can additionally change the user's uid or gid dynamically if the
`MYUID` or `MYGID` environment variables are set inside the container. This is
optional and can be useful to run the container as a user other than the one
who was used to build the image.
As a full example:

```bash
$ docker run --name boltlight-dev \
  -v $(pwd)/.data-dev:/srv/app/.boltlight \
  -v $(pwd)/boltlight:/srv/app/boltlight \
  -v $(pwd)/tests:/srv/app/tests \
  -e MYUID=1002 -e MYGID=1002 \
  hashbeam/boltlight:<version>-dev
```

After changing the code (inside the mounted paths) a simple restart will apply
them on the running instance:

```bash
$ docker restart boltlight-dev
```

Do not mount the full root project directory, as that will stop boltlight from
working inside the container. If needed, mount instead additional individual
paths, like `tox.ini` as a possible example.

Testing in docker can be achieved overriding the entrypoint and calling
`unix_helper` inside the container with either the `lint` or `test`
parameter. Given this is typically a one-shot operations, the use of the `--rm`
flag is recommended. Here is an example invocation to run the tests:

```bash
$ docker run --rm -it --name boltlight-dev \
  -v $(pwd)/boltlight:/srv/app/boltlight \
  -v $(pwd)/tests:/srv/app/tests \
  -v $(pwd)/reports:/srv/app/reports \
  --entrypoint bash \
  hashbeam/boltlight:<version>-dev -i -c './unix_helper test'
```


## Merge Request Process

1. Rebase on develop for new features or master for fixes

1. Test and lint the code to make sure there are no regressions

1. Update the README.md with details about the introduced changes

1. Create the merge request


## Code of Conduct

This project adheres to No Code of Conduct. We are all adults.
We accept anyone's contributions. Nothing else matters.

For more information please visit the
[No Code of Conduct](https://github.com/domgetter/NCoC) homepage.
