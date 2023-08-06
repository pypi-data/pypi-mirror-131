import json
import logging
from typing import Union, List, TypeVar

from GuardiPy.CentraObject import Incident
from GuardiPy.helpers import CentraApiExportable, CentraEntity

AnyCentraEntity = TypeVar("AnyCentraEntity", CentraEntity, CentraApiExportable)


def test_execute(input_data: dict, return_type) -> Union[AnyCentraEntity, List[AnyCentraEntity]]:
    objects = []
    for obj in input_data.get('objects', []):
        logging.debug(f"casting this json to instance of {return_type}")
        objects.append(return_type(**obj))
    else:
        return objects


with open('test_data.json', 'r') as data_file:
    data = json.load(data_file)

result: List[Incident] = test_execute(input_data=data, return_type=Incident)
for incident in result:
    print(incident.labels)
