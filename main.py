# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import json
import untruncate_json
import urllib.request


def invoke_anki_connect(action, **params):
    def request(r_action, **r_params):
        return {'action': r_action, 'params': r_params, 'version': 6}

    request_json = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', request_json)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def parse_search_result():
    data = json.loads(
        untruncate_json.complete(
            open('search2.json').read()
        )
    )
    plus = []
    products = data["data"]["products"]
    for product in products:
        plus.append(product["plu_number"])
    return plus


def get_anki_plus():
    notes = invoke_anki_connect('findNotes', query='"note:LIDL PLU"')
    note_infos = invoke_anki_connect('notesInfo', notes=notes)
    anki_plus = []
    for note in note_infos:
        anki_plus.append(note["fields"]["PLU"]["value"])
    return anki_plus


def main():
    current_PLUs = parse_search_result()
    my_PLUs = get_anki_plus()

    for plu in current_PLUs:
        if str(plu) not in my_PLUs:
            print("New PLU! {}".format(plu))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
