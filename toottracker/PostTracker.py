import requests
import re


class PostTracker:
    def __init__(self, instance_url):
        self._instance_url = instance_url

    def get_post_reach(self, post_id):
        response = requests.get(
            f"{self._instance_url}/api/v1/statuses/{post_id}")
        if response.status_code != 200:
            raise Exception(
                f"Error encountered while accessing post {post_id} status code {response.status_code}")

        # first we get id of the author
        boosters = [response.json()["account"]["id"]]

        # now we must iterate over accounts that boosted this post and add them to boosters list

        api_url = f"{self._instance_url}/api/v1/statuses/{post_id}/reblogged_by"
        while True:
            response = requests.get(api_url, {"limit": 80})
            if response.status_code != 200:
                raise Exception(
                    f"Error encountered while trying to find boosting users, status code {response.status_code}")
            for boost in response.json():
                boosters.append(boost["id"])
            next = re.search(r'<(.*)>; rel="next"', response.headers.get("Link")
                             ) if response.headers.get("Link") else None
            if next:
                api_url = next.group(1)
            else:
                break

        reached_users = {}

        # now we iterate through boosters and join their lists of followers.
        # mastodon instance assigns internal API even for remote users, so we can use
        # the original API url
        for booster in boosters:
            # initially assign the limit here because next link in Link header provides us
            # with the same limit
            api_url = f"{self._instance_url}/api/v1/accounts/{booster}/followers?limit=80"
            while True:
                response = requests.get(api_url)
                if response.status_code != 200:
                    raise Exception(
                        f"Error encountered while trying to get followers of account with id {booster}")

                for follower in response.json():
                    reached_users[follower["id"]] = True

                next = re.search(r'<(.*)>; rel="next"', response.headers.get("Link")
                                 ) if response.headers.get("Link") else None
                if next:
                    api_url = next.group(1)
                else:
                    break

        return len(reached_users.keys())
