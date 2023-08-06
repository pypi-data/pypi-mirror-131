from typing import TypedDict

StackParameterKey = str
RegionName = str


class ApiParameter(TypedDict, total=False):
    ParameterKey: StackParameterKey
    ParameterValue: str

    # "ResolvedValue" is never set by CFP but Boto3 expects it in the typed
    # dictionary schema.
    ResolvedValue: str

    UsePreviousValue: bool
