# flake8: noqa
# pylint: disable=useless-import-alias,missing-module-docstring

__version__ = "1.0.1"

try:
    from markupsafe import escape
    from markupsafe import Markup
except ImportError:
    from liquid.exceptions import escape  # type: ignore
    from liquid.exceptions import Markup  # type: ignore

from .mode import Mode as Mode
from .token import Token
from .expression import Expression

from .loaders import FileSystemLoader
from .loaders import DictLoader
from .loaders import ChoiceLoader

from .context import Context
from .context import Undefined
from .context import DebugUndefined
from .context import StrictUndefined
from .context import is_undefined as is_undefined

from .environment import Environment as Environment
from .environment import Template as Template
