import requests

class VkAPI:
    def __init__(self, token):
        self.token = token

    def get_photos(self, user_id):
        data_from_VK = requests.get("https://api.vk.com/method/photos.get?v=5.131", params={"access_token": self.token,
                                                                                             "owner_id": user_id,
                                                                                             "album_id": "profile",
                                                                                             "extended": 1,
                                                                                             "photo_sizes": 1,
                                                                                             "count": 8})
        return data_from_VK.json()