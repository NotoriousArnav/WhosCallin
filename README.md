# whoscallin

Whoscallin is a POC that aims to Reverse Engineer the Truecaller Web API to get the caller ID of a phone number.

## Installation

```bash
# Assuming you have uv installed
uv sync
```

## Usage
Currently the only way to use it is by using the Python REPL or making script with the `whoscallin` module.

```python
from whoscallin import WhosCallin

wc = WhosCallin('your token here')
# or
wc = WhosCallin.login('911234567890')  # phone number in E.164 format

result = wc.callerInfo('911234567890')  # phone number in E.164 format

# result is a `CallerInfo`` Pydantic model. Refer [Here](schemas/__init__.py) for the schema.
```

## Contributing
If you want to contribute, feel free to open an issue or a pull request. Any contributions are welcome!

## License
This Project is Unlicensed, because I know Truecaller will break this Project at some point. If I find myself in a position to maintain this project, I will license it under the GPL v3 License.
Until then, feel free to use it as you wish.
