import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from animal_classifier_server.models.error import Error  # noqa: E501
from animal_classifier_server.models.event import Event  # noqa: E501
from animal_classifier_server import util


def create_event(event):  # noqa: E501
    """Create a event.

    Creates new event # noqa: E501

    :param event: Payload
    :type event: dict | bytes

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        event = Event.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_event(event_id):  # noqa: E501
    """Deletes a event.

    Deletes event # noqa: E501

    :param event_id: event id
    :type event_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def find_event(event_id):  # noqa: E501
    """Find a event.

    Finds a event by id # noqa: E501

    :param event_id: event id
    :type event_id: int

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_events(created_after=None, created_before=None):  # noqa: E501
    """List events.

    Lists events # noqa: E501

    :param created_after: Created after filter
    :type created_after: str
    :param created_before: Created before filter
    :type created_before: str

    :rtype: Union[List[Event], Tuple[List[Event], int], Tuple[List[Event], int, Dict[str, str]]
    """
    created_after = util.deserialize_datetime(created_after)
    created_before = util.deserialize_datetime(created_before)
    return 'do some magic!'


def update_event(event_id, event):  # noqa: E501
    """Updates a event.

    Updates event # noqa: E501

    :param event_id: event id
    :type event_id: int
    :param event: Payload
    :type event: dict | bytes

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        event = Event.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
