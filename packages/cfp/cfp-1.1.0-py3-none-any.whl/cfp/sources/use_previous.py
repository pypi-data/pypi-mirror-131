from dataclasses import dataclass

from cfp.sources.source import Source


@dataclass
class UsePreviousValue(Source):
    """
    Indicates that the previous value should be reused.

    For example:

    .. code-block:: python

       from cfp import StackParameters
       from cfp.sources import UsePreviousValue

       sp = StackParameters()
       sp.add("InstanceType", UsePreviousValue())
    """
