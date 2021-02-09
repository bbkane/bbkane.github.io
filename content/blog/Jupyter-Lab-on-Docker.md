+++
title = "Jupyter Lab on Docker"
date = 2018-10-24
updated = 2018-10-24
aliases = [ "2018/10/24/Jupyter-Lab-on-Docker.html" ]
+++

Assuming you have Docker installed, setting up a basic Jupyter Lab environment
is pretty easy! I'm going to be installing the [jupyter
scipy-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/). The
following command mounts a directory with the correct permissions for the
Docker user to access it.

```bash
mkdir -p "$HOME/Code/Jupyter"
docker run \
    --rm \
    --user "$UID" \
    --group-add users \
    -p 8888:8888 \
    -v "$HOME/Code/Jupyter:/home/jovyan/work" \
    jupyter/scipy-notebook \
    start.sh jupyter lab \
```

This prints out a URL for you to access. Click the link to get into the
notebook. One thing to note- this link includes a generated token that's
regenerated each time. Because I like to run this on a server, then click a
bookmark on my browser, I want the link to be stable. Fortunately, this docker
image [includes a method to set a
password](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#notebook-options).
First, use the method above to get the lab working, and, once you have access
to Python (from Jupyter Notebook, for example), run the following code to set
up a password:

```python
In [1]: from IPython.lib import passwd

In [2]: passwd('new_password')
Out[2]: 'sha1:2c83e1f15852:a3e9402655248a12a25ae973487b84f431a28f19'
```

Take that password hash and plug it into the Docker command like so:

```bash
mkdir -p "$HOME/Code/Jupyter"
password_hash='sha1:2c83e1f15852:a3e9402655248a12a25ae973487b84f431a28f19'
docker run \
    --rm \
    --user "$UID" \
    --group-add users \
    -p 8888:8888 \
    -v "$HOME/Code/Jupyter:/home/jovyan/work" \
    jupyter/scipy-notebook \
    start.sh jupyter lab \
    --NotebookApp.password="$password_hash" \
```

Then you can head to `http://<hostname>:8888` and enter the password you set up
into the password prompt to get to your lab. And, it's a stable link, so it's
ready for bookmarking.
