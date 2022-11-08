import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from animal_classifier_server.models.error import Error  # noqa: E501
from animal_classifier_server import util


def ping():  # noqa: E501
    """System ping endpoint

     # noqa: E501


    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'
