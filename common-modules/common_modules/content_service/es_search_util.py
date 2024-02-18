import hashlib

def str_to_id(text):
    m = hashlib.md5()
    m.update(text.encode())
    id = str(int(m.hexdigest(), 16))[0:13]
    return id


# Always pass the list
def get_idsearch_query(id: list):
    search_param = {
        "query": {
            "ids": {
                "values": id
            }
        }
    }
    return search_param



