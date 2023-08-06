from dataclasses import dataclass, asdict
from uuid import uuid5, UUID, NAMESPACE_DNS

from cbaxter1988_utils.pymongo_utils import (
    add_item,
    get_client,
    get_collection,
    get_database,
    get_item,
    safe_update_item,
    safe_delete_item
)


@dataclass
class PersonModel:
    _id: UUID
    first_name: str
    last_name: str
    version: int = 1


def test_occ_update():
    person_model = PersonModel(
        _id=uuid5(NAMESPACE_DNS, f'Elijah'),
        first_name='Elijah',
        last_name='Baxter'
    )

    client = get_client(db_host='192.168.1.5', db_port=27017)
    database = get_database(client=client, db_name='test_db')
    collection = get_collection(database=database, collection='test_collection')
    item_id = UUID('be3a2142-c794-5817-9023-4764c36d0cdd')
    elijah_id = UUID('9607cc96-c17e-5af4-91cb-52aaeb182177')

    try:
        add_item(collection=collection, item=asdict(person_model))
    except Exception as err:
        print(err)

    item = get_item(collection=collection, item_id=item_id)
    data = item.next()

    expected_version = data.get("version")
    resp = safe_update_item(
        collection=collection,
        item_id=item_id,
        expected_version=expected_version,
        new_values={"last_name": "Baxter", "age": 6}
    )

    resp = safe_delete_item(collection=collection, item_id=elijah_id, expected_version=1)
