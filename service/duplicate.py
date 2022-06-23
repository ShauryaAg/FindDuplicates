import asyncio
import collections
from os import lstat
from typing import List, Any, Mapping, Tuple, Union

from fuzzywuzzy import fuzz

from utils import validate_model


def find_duplicates(profiles: List, fields: List[str]) -> Tuple[int, Mapping[str, List[str]]]:
    """
    Find duplicates in a list of profiles

    Arguments:
        profiles: List of profiles
        fields: List of fields to compare

    Returns:
        Score and mapping of attributes that are "matching", "non_matching" or "ignored"
    """

    profile_one = profiles[0]
    profile_two = profiles[1]

    # Validate if the contain the mentioned fields
    validate_model(profile_one, fields)
    validate_model(profile_two, fields)

    # Process special fields `first_name`, `last_name` and `email_field`
    name_result = _process_name_fields(
        profile_one, profile_two, fields)

    # Process all the other fields
    result = asyncio.run(_find_duplicates_pairwise(
        profile_one, profile_two, fields))

    score = 0
    attributes = collections.defaultdict(list, name_result)
    for item in result:
        score += item.get('score')
        attributes[item.get('type')].append(item.get('field'))

    return score, dict(attributes)


async def _find_duplicates_pairwise(profile_one: Any, profile_two: Any, fields: List[str]) -> List[Mapping[str, Union[str, int]]]:
    """
    Pairwise process two profiles
    """
    coro = []
    fields = set(fields) - set(['first_name', 'last_name', 'email_field'])

    for field in fields:
        coro.append(_compare_fields(
            profile_one, profile_two, field))

    values = await asyncio.gather(*coro)
    return values


def _process_name_fields(profile_one: Any, profile_two: Any, fields: List[str]) -> Mapping[str, Union[int, list]]:
    """
    Compare two profiles by name fields
    """
    fields = {'first_name', 'last_name',
              'email_field'}.intersection(fields)
    if not fields:
        return 0, []

    score = 0
    name_one = ' '.join([getattr(profile_one, field, '')
                        for field in fields])
    name_two = ' '.join([getattr(profile_two, field, '')
                        for field in fields])

    if name_one == name_two:
        if fuzz.partial_ratio(name_one, name_two) > 80:
            score = 1

    if score:
        type = "matching"
    else:
        type = "non_matching"
    return {"score": score, type: list(fields)}


async def _compare_fields(profile_one: Any, profile_two: Any, field: str) -> Mapping[str, Union[str, int]]:
    """
    Compare two profiles by a field
    """
    field_one = getattr(profile_one, field, None)
    field_two = getattr(profile_two, field, None)
    if field_one and field_two:
        if (field_one == field_two):
            score = 1
            type = "matching"
        else:
            score = -1
            type = "non_matching"
    else:
        score = 0
        type = "ignored"

    return {"score": score, "type": type, "field": field}
