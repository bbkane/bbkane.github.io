+++
title = "REST Server and Client in Python"
date = 2017-09-22
updated = 2017-09-22
aliases = [ "2017/09/22/REST-Server-and-Client-in-Python.html" ]
+++

I recently demonstrated a very quick REST backend server and client in Python
for an intern, and I thought I'd paste the code here.


## The Server

The Server's job is to grab/calculate information from some source (database,
another server, whatever), and package it up in a pretty JSON format and expose
it to clients via a URL.

This example server code is practically useless. It doesn't grab information
from anywhere, but has it hardcoded in the code itself. It does expose
information via API, which is the part we care about right now:

```python
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/get_ips')
def get_ips():
    return jsonify(dict(results=[dict(ip='1.2.3.4'), dict(ip='9.2.3.4')]))


def main():
    # This is a quick and dirty way to run the app.
    # Refer to the Flask tutorial to see the *right* way to do it
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
```

## The Client

The client is similarly useless in what it does with data (it just prints it),
but it does demonstrate how to use the `requests` library to grab the data from
the API.

```python
import pdb
import pprint
import requests


def main():
    response = requests.get('http://127.0.0.1:5000/get_ips')
    # pdb.set_trace()
    response_json = response.json()
    pprint.pprint(response_json)


if __name__ == "__main__":
    main()
```

The `pdb.set_trace()` line, when uncommented, will pause the app so you
can inpsect what you get.

So, if you uncomment that line, you get the following:

```
10:11 $ python client.py  # -- Run the app first
--Return--
> /Users/bkane/Code/Python/REST_tutorial/client.py(7)main()->None
-> pdb.set_trace()  # -- Your code is now paused and an pdb interpreter is
opened so you can play with it
(Pdb) response  # -- print it
<Response [200]>
(Pdb) dir(response)  # -- See what's in the reponse object. Some of these are
callable and some aren't
['__attrs__', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_content', '_content_consumed', 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
(Pdb) response.json()  # -- the json part looks interesting, and calling like a
method gets us what we want
{'results': [{'ip': '1.2.3.4'}, {'ip': '9.2.3.4'}]}
```
