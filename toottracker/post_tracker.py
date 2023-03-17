from .api_accesser import ApiAccesser


class PostTracker:
    def __init__(self, instance_url):
        self._instance_url = instance_url

    def get_post_reach(self, post_id):
        # first we get id of the author
        boosters = [ApiAccesser.get_post(self._instance_url, post_id)[
            "account"]["id"]]

        boosters.extend([user["id"] for user in ApiAccesser.get_reblogged_by(
            self._instance_url, post_id)])

        reached_users = {}

        for booster_id in boosters:
            for follower in ApiAccesser.get_followers(self._instance_url, booster_id):
                reached_users[follower["id"]] = True

        return len(reached_users.keys())
