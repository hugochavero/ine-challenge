"""
User's clients module
"""
import logging

import requests
from requests import HTTPError, ConnectionError

from users.constants import SubscriptionConstants
from users.exceptions import SubscriptionClientException

logger = logging.getLogger(__name__)


class SubscriptionClient:
    """
    Client to handle requests to Subscription service
    """
    def __init__(self):
        self.BASE_URL = "https://subscriptions.fake.service.test/api/v1/users/{user_id}"

    def get_subscription(self, user_id):
        """
        Main method to get user's subscription state
        :param user_id:
        :return:
        """
        endpoint = self.BASE_URL.format(user_id=user_id)
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except HTTPError as exc:
            logger.debug(exc)
            raise SubscriptionClientException from exc
        except ConnectionError as exc:
            logger.debug(exc)
            raise SubscriptionClientException from exc


class SubscriptionClientTest(SubscriptionClient):
    def get_subscription(self, user_id):
        return {"subscription": SubscriptionConstants.ACTIVE}
