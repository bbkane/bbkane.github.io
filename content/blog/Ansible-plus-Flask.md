+++
title = "Ansible Plus Flask"
date = 2017-08-24
updated = 2017-08-25
aliases = [ "2017/08/24/Ansible-plus-Flask.html" ]
+++

I was lurking on the *networktocode* Slack channel, when someone asked how to
get variables from an external system into an Ansible playbook. Intrigued, I
mocked up a quick Flask server to serve a REST API, and a playbook to consume
it. This proof of concept happily ignores a lot of issues you'd face in
production:

# The Server

In prod, this would hopefully be some high-powered IPAM with a REST API that
dealt properly with auth and could be a reliable source of truth.

- server.py

```python
from flask import Flask, jsonify
app = Flask(__name__)


# returns
# {

#     "result": {
#         "chassis": "chassis-007",
#         "ip": "0.0.0.0"
#     }

# }
@app.route('/get_ip')
def hello_world():
    # In reality, this info could come from a form, or a db or whatever
    # Don't forget to deal with auth!
    return jsonify(dict(result=dict(ip='0.0.0.0',
                                    chassis='chassis-007')))


def main():
    # Don't run these options in prod
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
```

Run it with `python server.py`

# The Hosts file

Since I'm not really doing anything, I'm using a minimal hosts file. In prod,
you could use a static hosts file, or a dynamic hosts system that also queries
your IPAM.

- hosts

```conf
[prod]
localhost ansible_connection=local
```

# The Playbook

This is the real meat of the work. I can decode the REST response from the HTTP
request by calling `from_json` filter on the content from the HTTP response,
then walking the JSON object. I'll admit, this isn't the prettiest way to do
something like this, but working ugly code is better than nonworking pretty
code...

- playbook.yaml

```yaml
---
- hosts: all
  gather_facts: false
  tasks:
    # https://serverfault.com/q/722852/383537
  - name: Get JSON from Source of Truth
    uri:
      # this shouldn't be hardcoded
      url: 'http://localhost:5000/get_ip'
      return_content: true
    register: json_response
  - name: Print the whole response to help with parsing
    debug:
      msg: "chassis is {% raw %}{{ json_response }}{% endraw %}"
  - name: Tell the world I got my chassis
    debug:
      # need to decode the response from the content part of the http response, then index into it
      msg: "chassis is {% raw %}{{ (json_response.content|from_json).result.chassis }}{% endraw %}"
```

Then run it with:

```
ansible-playbook -i hosts playbook.yaml
```

Ta-da! It prints `chassis-007`
