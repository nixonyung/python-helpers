import os

from pydantic import TypeAdapter


# (ref.) [Python type hints: specify a class rather than an instance thereof](https://adamj.eu/tech/2021/05/16/python-type-hints-return-class-not-instance/)
def parse_env[T](env_class: type[T]) -> T:
    # (ref.) [how to use os.environ as a dictionary value](https://stackoverflow.com/questions/33239474/how-to-use-os-environ-as-a-dictionary-value)
    return TypeAdapter(env_class).validate_python(dict(os.environ))
