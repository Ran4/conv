Converts structures python/json object representations (i.e. json object -> python dict)

Like `python3 -m json.tool file.json` but reads from stdin by default.

#### Example:

```bash
$ curl some_endpoint
{"name": "foo", "active": false, "redirect_url": null}

$ curl some_endpoint | python3 -m conv json python
{"name": "foo", "active": False, "redirect_url": None}
```

### Installation

```bash
pip3 install -e git+https://github.com/Ran4/conv#egg=conv
```

conv requires python3.
