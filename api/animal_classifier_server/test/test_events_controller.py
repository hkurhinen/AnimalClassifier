# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from animal_classifier_server.models.error import Error  # noqa: E501
from animal_classifier_server.models.event import Event  # noqa: E501
from animal_classifier_server.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_create_event(self):
        """Test case for create_event

        Create a event.
        """
        event = {"image":"image","classifications":[{"result":"result","confidence":6.027456183070403},{"result":"result","confidence":6.027456183070403}],"created":"2000-01-23T04:56:07.000+00:00","latitude":1.4658129805029452,"modified":"2000-01-23T04:56:07.000+00:00","id":0,"longitude":5.962133916683182}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/events',
            method='POST',
            headers=headers,
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_event(self):
        """Test case for delete_event

        Deletes a event.
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/events/{event_id}'.format(event_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_event(self):
        """Test case for find_event

        Find a event.
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/events/{event_id}'.format(event_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_events(self):
        """Test case for list_events

        List events.
        """
        query_string = [('createdAfter', '2013-10-20T19:20:30+01:00'),
                        ('createdBefore', '2013-10-20T19:20:30+01:00')]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/events',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_event(self):
        """Test case for update_event

        Updates a event.
        """
        event = {"image":"image","classifications":[{"result":"result","confidence":6.027456183070403},{"result":"result","confidence":6.027456183070403}],"created":"2000-01-23T04:56:07.000+00:00","latitude":1.4658129805029452,"modified":"2000-01-23T04:56:07.000+00:00","id":0,"longitude":5.962133916683182}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/events/{event_id}'.format(event_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
