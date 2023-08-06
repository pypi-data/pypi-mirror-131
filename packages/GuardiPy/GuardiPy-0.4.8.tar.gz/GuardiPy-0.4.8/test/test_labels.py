import logging
from datetime import timedelta
from typing import Optional

from GuardiPy import CentraApiPayload, Centra
from GuardiPy.CentraObject import Incident, LabelMinimal

from secrets import host


def fetch_customer_label(gc: Centra, gc_customer_name: str) -> (bool, Optional[str]):
    query: CentraApiPayload = LabelMinimal.list(
        assets='on,off',
        find_matches=True,
        dynamic_criteria_limit=500,
        key='Customers'
    )
    res = gc.execute(query)
    label_id = None
    shared_instance = False
    if res:
        shared_instance = True
        for label in res:
            if label.value == gc_customer_name:
                label_id = label.id
    return shared_instance, label_id


def fetch_incidents(gc: Centra, hours: int = 24, customer_label: str = None) -> int:
    hours = abs(hours)
    query = Incident.list(
        from_time=timedelta(hours=-hours),
        incident_type='Reveal',
        tags_include='Reputation',
        severity=["Medium", "High"],
        prefixed_filter='bad_reputation'
    )
    if customer_label:
        query.params['any_side'] = customer_label
    result = gc.export_to_csv(query)
    line_count = len(result.splitlines()) - 1
    return line_count if line_count > 0 else 0


def main():
    gc = Centra(hostname=host['dev_host'], username=host['username'], password=host['password'])
    shared_gc_instance, customer_label = fetch_customer_label(gc=gc, gc_customer_name="IdealCloud")
    print(shared_gc_instance, customer_label)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
