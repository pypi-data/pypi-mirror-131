"""Test math filter functions."""
# pylint: disable=too-many-public-methods,too-many-lines,missing-class-docstring
import unittest

from functools import partial
from inspect import isclass

from typing import NamedTuple
from typing import Any
from typing import List
from typing import Dict

from liquid.environment import Environment
from liquid.expression import NIL


from liquid.exceptions import Error
from liquid.exceptions import FilterError
from liquid.exceptions import FilterArgumentError
from liquid.exceptions import FilterValueError

from liquid.builtin.filters.array import join
from liquid.builtin.filters.array import first
from liquid.builtin.filters.array import last
from liquid.builtin.filters.array import concat
from liquid.builtin.filters.array import map_
from liquid.builtin.filters.array import reverse
from liquid.builtin.filters.array import sort
from liquid.builtin.filters.array import sort_natural
from liquid.builtin.filters.array import where
from liquid.builtin.filters.array import uniq
from liquid.builtin.filters.array import compact


class Case(NamedTuple):
    description: str
    val: Any
    args: List[Any]
    kwargs: Dict[Any, Any]
    expect: Any


class ArrayFilterTestCase(unittest.TestCase):
    """Test array filter functions."""

    def setUp(self) -> None:
        self.env = Environment()

    def _test(self, func, test_cases):
        if getattr(func, "with_environment", False):
            func = partial(func, environment=self.env)

        for case in test_cases:
            with self.subTest(msg=case.description):
                if isclass(case.expect) and issubclass(case.expect, Error):
                    with self.assertRaises(case.expect):
                        func(case.val, *case.args, **case.kwargs)
                else:
                    self.assertEqual(
                        func(case.val, *case.args, **case.kwargs), case.expect
                    )

    def test_join(self):
        """Test `join` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["a", "b"],
                args=[
                    "#",
                ],
                kwargs={},
                expect="a#b",
            ),
            Case(
                description="join a string",
                val="a, b",
                args=[
                    "#",
                ],
                kwargs={},
                expect="a, b",
            ),
            Case(
                description="lists of integers",
                val=[1, 2],
                args=[
                    "#",
                ],
                kwargs={},
                expect="1#2",
            ),
            Case(
                description="missing argument defaults to space",
                val=["a", "b"],
                args=[],
                kwargs={},
                expect="a b",
            ),
            Case(
                description="too many arguments",
                val=["a", "b"],
                args=[", ", ""],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="arguments not a string",
                val=["a", "b"],
                args=[5],
                kwargs={},
                expect="a5b",
            ),
            Case(
                description="value not an array",
                val=12,
                args=[", "],
                kwargs={},
                expect="12",
            ),
            Case(
                description="value array contains non string",
                val=["a", "b", 5],
                args=["#"],
                kwargs={},
                expect="a#b#5",
            ),
            Case(
                description="join an undefined variable with a string",
                val=self.env.undefined("test"),
                args=[", "],
                kwargs={},
                expect="",
            ),
            Case(
                description="join an array variable with undefined",
                val=["a", "b"],
                args=[self.env.undefined("test")],
                kwargs={},
                expect="ab",
            ),
        ]

        self._test(join, test_cases)

    def test_first(self):
        """Test `first` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["a", "b"],
                args=[],
                kwargs={},
                expect="a",
            ),
            Case(
                description="lists of things",
                val=["a", "b", 1, [], {}],
                args=[],
                kwargs={},
                expect="a",
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=None,
            ),
            Case(
                description="unexpected argument",
                val=["a", "b"],
                args=[", "],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=12,
                args=[],
                kwargs={},
                expect=None,
            ),
            Case(
                description="first of undefined",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=None,
            ),
        ]

        self._test(first, test_cases)

    def test_last(self):
        """Test `last` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["a", "b"],
                args=[],
                kwargs={},
                expect="b",
            ),
            Case(
                description="lists of things",
                val=["a", "b", 1, [], {}],
                args=[],
                kwargs={},
                expect={},
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=None,
            ),
            Case(
                description="unexpected argument",
                val=["a", "b"],
                args=[", "],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=12,
                args=[],
                kwargs={},
                expect=None,
            ),
            Case(
                description="last of undefined",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=None,
            ),
        ]

        self._test(last, test_cases)

    def test_concat(self):
        """Test `concat` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["a", "b"],
                args=[["c", "d"]],
                kwargs={},
                expect=["a", "b", "c", "d"],
            ),
            Case(
                description="missing argument",
                val=["a", "b"],
                args=[],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="too many arguments",
                val=["a", "b"],
                args=[["c", "d"], ""],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="arguments not a list",
                val=["a", "b"],
                args=[5],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="not an array",
                val="a, b",
                args=[["c", "d"]],
                kwargs={},
                expect=["a, b", "c", "d"],
            ),
            Case(
                description="array contains non string",
                val=["a", "b", 5],
                args=[["c", "d"]],
                kwargs={},
                expect=["a", "b", 5, "c", "d"],
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[["c", "d"]],
                kwargs={},
                expect=["c", "d"],
            ),
            Case(
                description="undefined argument",
                val=["a", "b"],
                args=[self.env.undefined("test")],
                kwargs={},
                expect=FilterArgumentError,
            ),
        ]

        self._test(concat, test_cases)

    def test_map(self):
        """Test `map` filter function."""

        test_cases = [
            Case(
                description="lists of objects",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "baz"}],
                args=["title"],
                kwargs={},
                expect=["foo", "bar", "baz"],
            ),
            Case(
                description="missing argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "baz"}],
                args=[],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="too many arguments",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "baz"}],
                args=["title", ""],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="missing property",
                val=[{"title": "foo"}, {"title": "bar"}, {"heading": "baz"}],
                args=["title"],
                kwargs={},
                expect=["foo", "bar", NIL],
            ),
            Case(
                description="value not an array",
                val=123,
                args=["title"],
                kwargs={},
                expect=FilterError,
            ),
            Case(
                description="array contains non object",
                val=[{"title": "foo"}, {"title": "bar"}, 5, []],
                args=["title"],
                kwargs={},
                expect=FilterError,
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=["title"],
                kwargs={},
                expect=[],
            ),
            Case(
                description="undefined argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "baz"}],
                args=[self.env.undefined("test")],
                kwargs={},
                expect=[NIL, NIL, NIL],
            ),
        ]

        self._test(map_, test_cases)

    def test_reverse(self):
        """Test `reverse` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["b", "a", "B", "A"],
                args=[],
                kwargs={},
                expect=["A", "B", "a", "b"],
            ),
            Case(
                description="lists of things",
                val=["a", "b", 1, [], {}],
                args=[],
                kwargs={},
                expect=[{}, [], 1, "b", "a"],
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="unexpected argument",
                val=["a", "b"],
                args=[", "],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=123,
                args=[],
                kwargs={},
                expect=FilterValueError,
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=[],
            ),
        ]

        self._test(reverse, test_cases)

    def test_sort(self):
        """Test `sort` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["b", "a", "C", "B", "A"],
                args=[],
                kwargs={},
                expect=["A", "B", "C", "a", "b"],
            ),
            Case(
                description="lists of objects with key",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "Baz"}],
                args=["title"],
                kwargs={},
                expect=[{"title": "Baz"}, {"title": "bar"}, {"title": "foo"}],
            ),
            Case(
                description="lists of objects with missing key",
                val=[{"title": "foo"}, {"title": "bar"}, {"heading": "Baz"}],
                args=["title"],
                kwargs={},
                expect=[{"title": "bar"}, {"title": "foo"}, {"heading": "Baz"}],
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="too many arguments",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "baz"}],
                args=["title", "heading"],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=123,
                args=[],
                kwargs={},
                expect=FilterValueError,
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="undefined argument",
                val=[{"z": "z", "title": "foo"}, {"title": "bar"}, {"title": "Baz"}],
                args=[self.env.undefined("test")],
                kwargs={},
                expect=FilterError,
            ),
            Case(
                description="sort by key targeting an array of strings",
                val=["Z", "b", "a", "C", "A", "B"],
                args=["title"],
                kwargs={},
                expect=["Z", "b", "a", "C", "A", "B"],
            ),
        ]

        self._test(sort, test_cases)

    def test_sort_natural(self):
        """Test `sort_natural` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["b", "a", "C", "B", "A"],
                args=[],
                kwargs={},
                expect=["a", "A", "b", "B", "C"],
            ),
            Case(
                description="lists of strings with a None",
                val=["b", "a", None, "C", "B", "A"],
                args=[],
                kwargs={},
                expect=["a", "A", "b", "B", "C", None],
            ),
            Case(
                description="lists of objects with key",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "Baz"}],
                args=["title"],
                kwargs={},
                expect=[{"title": "bar"}, {"title": "Baz"}, {"title": "foo"}],
            ),
            Case(
                description="lists of objects with missing key",
                val=[{"title": "foo"}, {"title": "bar"}, {"heading": "Baz"}],
                args=["title"],
                kwargs={},
                expect=[{"title": "bar"}, {"title": "foo"}, {"heading": "Baz"}],
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="too many arguments",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "Baz"}],
                args=["title", "heading"],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=1234,
                args=[],
                kwargs={},
                expect=FilterValueError,
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="undefined argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": "Baz"}],
                args=[self.env.undefined("test")],
                kwargs={},
                expect=[{"title": "bar"}, {"title": "Baz"}, {"title": "foo"}],
            ),
        ]

        self._test(sort_natural, test_cases)

    def test_where(self):
        """Test `where` filter function."""

        test_cases = [
            Case(
                description="lists of object",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=["title"],
                kwargs={},
                expect=[{"title": "foo"}, {"title": "bar"}],
            ),
            Case(
                description="lists of object with equality test",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=["title", "bar"],
                kwargs={},
                expect=[{"title": "bar"}],
            ),
            Case(
                description="value not an array",
                val=1234,
                args=["title"],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="missing argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=[],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="too many arguments",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=["title", "bar", "foo"],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=["title", "bar"],
                kwargs={},
                expect=[],
            ),
            Case(
                description="undefined first argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=[self.env.undefined("test"), "bar"],
                kwargs={},
                expect=[],
            ),
            Case(
                description="undefined second argument",
                val=[{"title": "foo"}, {"title": "bar"}, {"title": None}],
                args=["title", self.env.undefined("test")],
                kwargs={},
                expect=[{"title": "foo"}, {"title": "bar"}],
            ),
        ]

        self._test(where, test_cases)

    def test_uniq(self):
        """Test `uniq` filter function."""

        test_cases = [
            Case(
                description="lists of strings",
                val=["a", "b", "b", "a"],
                args=[],
                kwargs={},
                expect=["a", "b"],
            ),
            Case(
                description="lists of things",
                val=["a", "b", 1, 1],
                args=[],
                kwargs={},
                expect=["a", "b", 1],
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="unhashable items",
                val=["a", "b", [], {}, {}],
                args=[],
                kwargs={},
                expect=["a", "b", {}],
            ),
            Case(
                description="unexpected argument",
                val=["a", "b"],
                args=["foo", "bar"],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val="a, b",
                args=[],
                kwargs={},
                expect=["a, b"],
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=[],
            ),
        ]

        self._test(uniq, test_cases)

    def test_compact(self):
        """Test `compact` filter function."""

        test_cases = [
            Case(
                description="lists with nil",
                val=["b", "a", None, "A"],
                args=[],
                kwargs={},
                expect=["b", "a", "A"],
            ),
            Case(
                description="empty list",
                val=[],
                args=[],
                kwargs={},
                expect=[],
            ),
            Case(
                description="unexpected argument",
                val=["a", "b"],
                args=[", "],
                kwargs={},
                expect=FilterArgumentError,
            ),
            Case(
                description="value not an array",
                val=1,
                args=[],
                kwargs={},
                expect=[1],
            ),
            Case(
                description="undefined left value",
                val=self.env.undefined("test"),
                args=[],
                kwargs={},
                expect=[],
            ),
        ]

        self._test(compact, test_cases)
