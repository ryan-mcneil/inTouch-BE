[![Waffle.io - Columns and their card count](https://badge.waffle.io/ryan-mcneil/inTouch-BE.svg?columns=all)](https://waffle.io/ryan-mcneil/inTouch-BE)

Check out the frontend repo [here](https://github.com/Dhanciles/inTouch-FE)!

## Setup

Set up a python virtual environment where-ever you want it to live:
```

```

Next, set your DEBUG environment variable to True (for the virtual environment).
This lets you use a generic secret_key.
```
$ export DEBUG=True
```

If you want to make a true secret_key, use

Clone down the repo, activate the virtual environment, and install dependencies:
```
$ git clone git@github.com:ryan-mcneil/inTouch-BE.git
$ cd inTouch-BE
$ source <PATH_TO_VENV>/bin/activate
$ pip install -r requirements.txt
```


Next, set up a local database
```
$ psql
=# CREATE DATABASE in_touch_dev
```
