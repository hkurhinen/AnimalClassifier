import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from animal_classifier_server.models.error import Error  # noqa: E501
from animal_classifier_server.models.event import Event  # noqa: E501
from animal_classifier_server import util
from animal_classifier_server.database.db import get_database

from bson import json_util
import json

def create_event():  # noqa: E501
    """Create a event.

    Creates new event # noqa: E501

    :param event: Payload
    :type event: dict | bytes

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        event = Event.from_dict(connexion.request.get_json())  # noqa: E501
        db = get_database()
        db["events"].insert_one(event.to_dict())
    return '201 Created successfully.'


def delete_event(event_id):  # noqa: E501
    """Deletes a event.

    Deletes event # noqa: E501

    :param event_id: event id
    :type event_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if (isinstance(event_id, int)):
        db = get_database()
        delete_event = db.events.delete_one({"id":event_id})
        if(delete_event.deleted_count == 1):
            return ('204 No content, deleted successfully.')
    return 'Invalid ID'



def find_event(event_id):  # noqa: E501
    """Find a event.

    Finds a event by id # noqa: E501

    :param event_id: event id
    :type event_id: int

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    if (isinstance(event_id, int)):
        db = get_database()
        return json.loads(json_util.dumps((db["events"].find({"id":event_id}))))          
    return ('{"code": 400,"message": "Invalid Id"}' ) # need improvement for id which is not in the collection


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
    db = get_database()
    return json.loads(json_util.dumps(list(db["events"].find({"created":{"$gte": created_after, "$lt": created_before}}))))



def update_event(event_id):  # noqa: E501
    """Updates a event.

    Updates event # noqa: E501

    :param event_id: event id
    :type event_id: int
    :param event: Payload
    :type event: dict | bytes

    :rtype: Union[Event, Tuple[Event, int], Tuple[Event, int, Dict[str, str]]
    """
    
    if (isinstance(event_id, int)):
        db = get_database()
        event_res = json.loads(json_util.dumps((db["events"].find({"id":event_id}))))
        if(event_res == []):
            print(event_res)
            return ('404 Collection not found')
        else:
            event = Event.from_dict(connexion.request.get_json())
            db["events"].replace_one({"id":event_id}, event.to_dict())
            return ('204 updated successfully' )
    return ('{"code": 404,"message": "Invalid Id"}' )