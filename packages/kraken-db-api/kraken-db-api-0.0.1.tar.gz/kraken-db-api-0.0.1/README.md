Python library to access kraken-db via api

How to use:

import kraken_db_api as db

db.set_db_url('url of the db server')

Post
db.post(observation)

Get
observations = db.get(record_type, record_id, key, value)

Search
search_params = {
    'record_type': 'person',
    'record_id': 'id',
    'order_by': 'created_date',
    'order_direction': 'desc',
    'limit': 20,
    'offset': 20
}
observations = db.search(search_params)
