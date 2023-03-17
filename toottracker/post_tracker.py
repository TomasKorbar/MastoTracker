from .api_accesser import ApiAccesser


class PostTracker:
    """ Class providing statistics about posts """

    def __init__(self, instance_url: str):
        """

        Parameters
        ----------
        instance_url : str
            url of mastodon instance

        Returns
        -------

        """
        self._instance_url = instance_url

    def get_post_reach(self, post_id: int) -> int:
        """ Get how many users received this post on their feed

        Parameters
        ----------
        post_id : int
            id of post

        Returns
        -------
        int
            count of users that received this post on their feeds

        """
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
