from fastapi import FastAPI, Request
from fastapi.datastructures import Address
from fastapi.concurrency import run_in_threadpool
import uvicorn
from time import sleep
import json
from typing import Union
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
import parser
from fuzzywuzzy import fuzz

app = FastAPI()
db = []

shop_files = ['quke.ru.json']
# types = ['card', 'processor', 'motherboard', 'RAM', 'power', 'memory', ]

baskets = {}


def get_db():
    for file in shop_files:
        shop_data: dict = json.load(open(file, 'r', encoding='utf8'))
        db.extend(shop_data)


get_db()


@app.get("/update")
async def update_page() -> dict:
    print('start updating...')
    rst = await run_in_threadpool(parser.main)
    print('finished updating!')
    return {
        'result': 'update all db',
        'ok'    : True,
        'answer': 'success'
    }


@app.get("/search")
async def update_page(text: str, type: Union[str, None], requests: Request) -> Union[dict, list]:
    db_t = db.copy()
    if type != 'None':
        db_t = list(filter(lambda x: x.get('type', '') == type, db_t))

    data = sorted(db_t, key=lambda x: fuzz.partial_ratio(text, x['name']), reverse=True)[:20]

    return {
        'result': data,
        'ok'    : True,
        'answer': 'success'
    }


@app.get("/basket")
async def basket_page(requests: Request) -> Union[dict, list]:
    print(requests.client.host)
    return {
        'result': baskets.get(requests.client.host, []),
        'ok'    : True,
        'answer': 'success'
    }


@app.post("/add")
async def basket_page(requests: Request) -> Union[dict, list]:
    r_json: dict = await requests.json()
    print(requests.client.host)
    if r_json.get('prod'):
        if requests.client.host in baskets:
            baskets[requests.client.host].append(r_json['prod'])
        else:
            baskets[requests.client.host] = [r_json['prod']]

        return {
            'result': baskets[requests.client.host],
            'ok'    : True,
            'answer': 'success'
        }
    else:
        return {
            'result': 'error',
            'ok'    : False,
            'answer': 'no prod in json requests'
        }


@app.get("/all")
def all_db_page():
    return db


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)