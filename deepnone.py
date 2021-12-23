"""Utility that permits deeply accessing objects, defaulting to None on error.

    assert dn(1).get == 1
    assert dn("ASDF").lower().get == "asdf"
    assert dn(123).lower().get is None
    assert dn(123).lower().default("hi") == "hi"
    assert dn("ASDF").strip("F").get == "ASD"
    assert dn("").junk().get is None
    assert dn(3).real.get == 3
    assert dn({"asdf": ["a", "b", "c"]})["asdf"][1].get == "b"
    assert dn({"asdf": ["a", "b", "c"]})["asdf"][1].upper().get == "B"
    assert dn({"asdf": ["a", "b", "c"]})["fdas"][1].upper().get is None
    assert dn(3).fn(str).get == "3"
    assert dn({"a": "b"}).attr("get")("a").get == "b"
    assert dn(123).junk.fn(str).get is None
    assert dn(123).fn(str)
    assert not dn(123).fn(str).junk
    assert bool(dn(123).fn(str))
    assert not bool(dn(123).fn(str).junk.asdf)
    assert list(dn(1).junk) == []
    for x in dn({"x": [3]})["x"]:
        assert x == 3
    assert not any(dn("a").junk)
    assert any(dn([1]))
    assert dn("a") == "a"
    assert "a" == dn("a")
    assert dn("a").upper() == "A"
"""
from __future__ import annotations

from typing import Any, Callable, Generic, Iterable, TypeVar, Union

T = TypeVar("T")


class DeepNone(Generic[T]):
    """Implementation of `dn` utility.

    Note: this class should not be instantiated directly. Use `dn` instead.

    The `DeepNone` object is not useful until its result is "built". There are
    several ways of getting the built value:

    * `get`: returns the built value
    * `default`: returns the built value or the default value
    * bool(DeepNone_object): returns the truthiness of the built value
    """

    def __init__(self, value: T):
        self.first_value = value
        self.value = value
        self.exception = None

    def __bool__(self) -> bool:
        """Returns the truthiness of the built value. Convenient when you only
        care about the presence of a deep-property."""
        return bool(self.value)

    def __iter__(self) -> Iterable:
        """Materializes this as an iterable, defaulting to empty list."""
        return iter(self.value or [])

    def __eq__(self, other: object) -> bool:
        """Compares `other` against active value"""
        return self.value == other

    def __hash__(self) -> int:
        """Returns hash of active value."""
        return hash(self.value)

    @property
    def get(self):
        return self.value

    D = TypeVar("D")

    def default(self, default: D) -> D:
        """Returns the built value.

        Applies all actions to `value`, returning`None` on failure.
        """
        return self.get or default

    @property
    def or_first(self) -> T:
        return self.value or self.first_value

    def _action(fn) -> Callable[[*Any], DeepNone]:
        """Decorator to properly handle failures from transforms"""

        def helper(self, *args, **kwargs) -> DeepNone:
            if self.exception:
                return self
            try:
                self.value = fn(self, *args, **kwargs)
            except:
                self.exception = True
                self.value = None
            return self

        return helper

    @_action
    def fn(self, function: Callable[[Any], Any]):
        """Transforms this by passing current value to `function`.

        I.e., runs function(value) as new `DeepNone` result.
        """
        return function(self.value)

    @_action
    def attr(self, attr: str):
        """Safety-hatch for accessing field conflicting with API keywords.

        I.e., if you want to access the attribute `default` on `value`, the
        `default` API keyword does not permit `my_value.default` access.
        Instead, you can use this method `myvalue.attr('default')`.
        """
        return getattr(self.value, attr)

    @_action
    def __getitem__(self, item_key):
        """Transforms this by accessing `value[item_key]`."""
        return self.value[item_key]

    @_action
    def __getattr__(self, attribute_name):
        """Transforms this by returning `my_value.<attribute_name>`."""
        return getattr(self.value, attribute_name)

    @_action
    def __call__(self, *args: Any, **kwds: Any):
        """Transforms this by invoking `my_value` and passing args."""
        return self.value(*args, **kwds)


def dn(value: T) -> Union[DeepNone[T], T]:
    """Returns a new `DeepNone` object for `value`.

    If `value` is already a `DeepNone` object, returns it.

    assert dn(1).get == 1
    assert dn("ASDF").lower().get == "asdf"
    assert dn(123).lower().get is None
    assert dn(123).lower().default("hi") == "hi"
    assert dn("ASDF").strip("F").get == "ASD"
    assert dn("").junk().get is None
    assert dn(3).real.get == 3
    assert dn({"asdf": ["a", "b", "c"]})["asdf"][1].get == "b"
    assert dn({"asdf": ["a", "b", "c"]})["asdf"][1].upper().get == "B"
    assert dn({"asdf": ["a", "b", "c"]})["fdas"][1].upper().get is None
    assert dn(3).fn(str).get == "3"
    assert dn({"a": "b"}).attr("get")("a").get == "b"
    assert dn(123).junk.fn(str).get is None
    assert dn(123).fn(str)
    assert not dn(123).fn(str).junk
    assert bool(dn(123).fn(str))
    assert not bool(dn(123).fn(str).junk.asdf)
    """
    return DeepNone(value)
