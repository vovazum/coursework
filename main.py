import configparser
import json
from datetime import datetime


from api.vkapi import VkAPI
from api.ydapi import YandexDiskAPI
from utils.sn import get_vk_userid

# Чтение конфигурационного файла
config = configparser.ConfigParser()
config.read('config.ini')


# Функция для определения максимального разрешения фото
def get_max_resolution_photo(size_dict):
    return max(size_dict['width'], size_dict['height'])

# Функция для обработки фотографий из VK
def process_vk_photos(data, num_photos):
    for item in data['response']['items'][:num_photos]:
        sizes = item['sizes']
        max_size = max(sizes, key=get_max_resolution_photo)
        max_size_url = max_size['url']
        max_size_type = max_size['type']
        p_likes = item['likes']['count']
        
        if p_likes == 0:
            # Если количество лайков равно нулю, добавляем текущую дату в название фото
            photo_name = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
        else:
            photo_name = f'{p_likes}.jpg'

        # Записываем информацию о фото в файл JSON
        with open('photos.json', 'w') as f:
            json.dump([{"file_name": photo_name, "size": max_size_type}], f, indent=2, ensure_ascii=False)
        
         # Загружаем фото на Яндекс.Диск
        yd_api.upload_photo(photo_name, max_size_url, f"/VK_Backup/{photo_name}")

if __name__ == "__main__":

    # Получение токенов из конфигурационного файла
    tokenVK = config['tokens']['tokenVK']
    tokenYD = config['tokens']['tokenYD']
    
    target_profile = input("Введите ID или screen_name целевого профиля в ВКонтакте: ")
    num_photos = int(input("Введите количество фотографий для загрузки: "))

    vk_user_id = get_vk_userid(target_profile, tokenVK)
    
    # Инициализация API ВКонтакте и Яндекс.Диска
    vk_api = VkAPI(tokenVK)
    yd_api = YandexDiskAPI(tokenYD)

    # Получение данных о фотографиях из VK
    photos_data = vk_api.get_photos(vk_user_id)
    
    # Запись данных в файл
    with open("vk_photos.json", "w") as file:
        json.dump(photos_data, file, indent=2, ensure_ascii=False)
    
    # Создание папки на Яндекс.Диске для бэкапа
    yd_api.create_folder('VK_Backup')
    
    # Загрузка данных из файла и обработка фотографий
    with open("vk_photos.json", "r") as file:
        data_from_vk = json.load(file)
    
    process_vk_photos(data_from_vk, num_photos)
