from unittest import mock
from unittest.mock import MagicMock

import pytest
from requests import HTTPError, ConnectionError
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from users import SubscriptionClient
from users.constants import SubscriptionConstants
from users.exceptions import SubscriptionClientException
from users.models import User


class TestSubscriptionClient:

    @mock.patch('users.clients.requests.get')
    def test_get_subscription(self, mock_request):
        service_data_response = {'subscription': SubscriptionConstants.ACTIVE}

        mock_response = MagicMock()
        mock_response.status_code = HTTP_200_OK
        mock_response.json.return_value = service_data_response

        mock_request.return_value = mock_response
        user = User(id=10)
        response = SubscriptionClient().get_subscription(user.id)
        assert response == service_data_response

    @mock.patch('users.clients.requests.get')
    @pytest.mark.parametrize("client_exception", [HTTPError, ConnectionError])
    def test_get_subscription_exceptions(self, mock_request, client_exception):
        mock_response = MagicMock()
        mock_response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        mock_response.raise_for_status.side_effect = client_exception
        mock_request.return_value = mock_response
        user = User(id=10)
        with pytest.raises(SubscriptionClientException):
            SubscriptionClient().get_subscription(user.id)
