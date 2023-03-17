import requests

from .api_access_exception import ApiAccessException
from .api_access_iterable import ApiAccessIterable


class ApiAccesser:
    """ Class for abstraction of work with mastodon API """
    @classmethod
    def get_post(cls, instance_url: str, post_id: int) -> dict:
        """ Get dictionary with all information about post

        Parameters
        ----------
        instance_url : str
            url of mastodon instance

        post_id : int
            id of post

        Returns
        -------
        dict
            data about post

        """
        response = requests.get(f"{instance_url}/api/v1/statuses/{post_id}")

        json_response = response.json()

        if response.status_code == 401:
            raise ApiAccessException(
                response.status_code, f"Error while trying to access info about post {post_id}, instance is in authorized-fetch mode", json_response.get("error", None))
        elif response.status_code == 404:
            raise ApiAccessException(
                response.status_code, f"Error while trying to access info about post {post_id}, it does not exist or is private", json_response.get("error", None))
        elif response.status_code != 200:
            raise ApiAccessException(
                response.status_code, f"Error while trying to access info about post {post_id}", json_response.get("error", None))
        return json_response

    @classmethod
    def get_reblogged_by(cls, instance_url: str, post_id: int) -> list[dict]:
        """ Get list of users who boosted post

        Parameters
        ----------
        instance_url : str
            url of mastodon instance

        post_id : int
            id of post

        Returns
        -------
        list[dict]
            list of data about users as dictionaries

        """
        api_url = f"{instance_url}/api/v1/statuses/{post_id}/reblogged_by?limit=80"
        boosters_iterable = ApiAccessIterable(api_url)
        boosters = []
        try:
            for booster_portion in boosters_iterable:
                boosters.extend(booster_portion)
        except ApiAccessException as exc:
            if exc.status_code == 404:
                raise ApiAccessException(
                    exc.status_code, f"Error while accessing rebloggers of post {post_id}, it does not exist or is private", exc.api_error)
            else:
                raise ApiAccessException(
                    exc.status_code, f"Error while accessing rebloggers of post {post_id}", exc.api_error)
        return boosters

    @classmethod
    def get_followers(cls, instance_url: str, user_id: int) -> list[dict]:
        """ Get list of users followers

        Parameters
        ----------
        instance_url : str
            url of mastodon instance

        post_id : int
            id of user

        Returns
        -------
        list[dict]
            list of data about users as dictionaries
        """
        api_url = f"{instance_url}/api/v1/accounts/{user_id}/followers?limit=80"
        followers_iterable = ApiAccessIterable(api_url)
        followers = []
        try:
            for follower_portion in followers_iterable:
                followers.extend(follower_portion)
        except ApiAccessException as exc:
            if exc.status_code == 401:
                raise ApiAccessException(
                    exc.status_code, f"Error while trying to access followers of user {user_id}, unauthorized", exc.api_error)
            elif exc.status_code == 404:
                raise ApiAccessException(
                    exc.status_code, f"Error while trying to access followers of user {user_id}, account does not exist", exc.api_error)
            else:
                raise ApiAccessException(
                    exc.status_code, f"Error while trying to access followers of user {user_id}", exc.api_error)
        return followers
