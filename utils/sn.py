import requests

# функция для обработки screen_name и ID пользователя
def get_vk_userid(target_profile, tokenVK):
    if not target_profile.isdigit():
        params = {
            'screen_name': target_profile,
            'access_token': tokenVK,
            'v': '5.199',
            }
        response = requests.get(
        'https://api.vk.com/method/utils.resolveScreenName',
        params=params,
        )
        response.raise_for_status()
        return response.json()['response']['object_id']