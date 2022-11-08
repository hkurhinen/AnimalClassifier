# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from animal_classifier_server.models.error import Error  # noqa: E501
from animal_classifier_server.test import BaseTestCase


class TestSystemController(BaseTestCase):
    """SystemController integration test stubs"""

    def test_ping(self):
        """Test case for ping

        System ping endpoint
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/system/ping',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
