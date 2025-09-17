from __future__ import annotations
from typing import Any, List, Optional, Annotated, Union
from typing_extensions import TypedDict


def _merge_dict(old: Optional[dict], new: Optional[dict]) -> Optional[dict]:
    if new is None:
        return old
    if not isinstance(new, dict):
        # Ignore invalid new types to avoid crashing merges
        return old
    if old is None or not isinstance(old, dict):
        return new
    out = dict(old)
    out.update(new)
    return out


def _merge_location(old: Optional[Union[dict, str]], new: Optional[Union[dict, str]]) -> Optional[dict]:
    if new is None:
        # keep old (normalize if string)
        if isinstance(old, str):
            return {"city": old}
        return old if isinstance(old, dict) else None
    # normalize new
    if isinstance(new, str):
        new = {"city": new}
    if not isinstance(new, dict):
        return None
    # normalize old
    if isinstance(old, str):
        old = {"city": old}
    if not isinstance(old, dict):
        return new
    out = dict(old)
    out.update(new)
    return out


def _merge_dates(old: Optional[dict], new: Optional[dict]) -> Optional[dict]:
    # Only accept dict-shaped dates; otherwise keep old
    if new is None:
        return old
    if not isinstance(new, dict):
        return old
    if old is None or not isinstance(old, dict):
        return new
    out = dict(old)
    out.update(new)
    return out


def _replace_if_new(old, new):
    return new if new is not None else old


def _replace_list(old: Optional[List[Any]], new: Optional[List[Any]]) -> Optional[List[Any]]:
    return list(new) if new is not None else old


class PlanState(TypedDict, total=False):
    # Inputs
    user_text: Annotated[Optional[str], _replace_if_new]
    origin: Annotated[Optional[dict], _merge_location]
    destinations: Annotated[List[dict], _replace_list]
    date_range: Annotated[Optional[dict], _merge_dates]
    nights: Annotated[Optional[int], _replace_if_new]
    interests: Annotated[List[str], _replace_list]
    pace: Annotated[Optional[str], _replace_if_new]
    with_kids: Annotated[bool, _replace_if_new]
    must_do: Annotated[List[str], _replace_list]
    avoid: Annotated[List[str], _replace_list]
    currency: Annotated[Optional[str], _replace_if_new]
    budget: Annotated[Optional[str], _replace_if_new]

    # Working
    poi_candidates: Annotated[List[dict], _replace_list]
    day_plans: Annotated[List[dict], _replace_list]
    hotel_options: Annotated[List[dict], _replace_list]
    flight_options: Annotated[List[dict], _replace_list]
    disambiguate_options: Annotated[List[dict], _replace_list]

    # Control
    need_info: Annotated[bool, _replace_if_new]
    questions: Annotated[List[str], _replace_list]
    error: Annotated[Optional[str], _replace_if_new]
    next: Annotated[Optional[str], _replace_if_new]
    intent: Annotated[Optional[str], _replace_if_new]
    short_term_memory: Annotated[Optional[str], _replace_if_new]
    response: Annotated[Optional[str], _replace_if_new]
    user_id: Annotated[Optional[str], _replace_if_new]


from app.schemas.common import Location


def _to_location(value: Union[dict, str, None]) -> Optional[Location]:
    if value is None:
        return None
    if isinstance(value, dict):
        return Location(**value)
    if isinstance(value, str):
        return Location(city=value)
    return None
