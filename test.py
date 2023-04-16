import requests
import json


# r = requests.get('http://localhost:8080/search?text=Твердотельный&type=None')
r = requests.get('http://localhost:8080/add', json={
    'prod': {
        "name": " Видеокарта Palit Gamerock Omniblack GeForce RTX 4080 16Gb NED4080019T2-1030Q",
        "price": 103590,
        "link": "https://quke.ru/shop/UID_120157__palit_gamerock_omniblack_geforce_rtx_4080_16gb_ned4080019t21030q.html",
        "img_link": "https://quke.ru/resize/200x200/UserFiles/Landing/products/120157_1669731900_photos_0.jpeg",
        "type": "card"
    }
})

print(json.dumps(r.json(), indent=4, ensure_ascii=False))