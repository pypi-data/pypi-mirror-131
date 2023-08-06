import logging
from datetime import timedelta
from typing import Optional

from GuardiPy import CentraApiPayload, Centra
from GuardiPy.CentraObject import Incident, LabelMinimal

from secrets import host, dev_host


def fetch_pv_incidents_csv(gc: Centra, cus_name: str, hours=-24) -> int:
    shared_instance = False
    customer_label = None
    query = LabelMinimal.list(assets='on,off', find_matches=True, dynamic_criteria_limit=500, key='Customers')
    res = gc.execute(query)
    if res:
        shared_instance = True
        customer_label = next((i for i in res if i.value == cus_name), None)

    if (not shared_instance) or customer_label:
        query = Incident.list(
            from_time=timedelta(hours=hours),
            incident_type='Reveal',
            tags_include='Policy Violation',
            severity=['Low', 'Medium', 'High'],
            prefixed_filter='policy_violations'
        )
        if customer_label:
            query.params['any_side'] = customer_label
        result = gc.export_to_csv(query)
    else:
        result = ""

    line_count = len(result.splitlines()) - 1
    return line_count if line_count > 0 else 0


def main():
    # gc = Centra(hostname=dev_host['dev_host'], username=dev_host['username'], password=dev_host['password'])
    # customer_label = fetch_customer_label(gc=gc, gc_customer_name=dev_host['name'])
    # pv_incidents = fetch_incidents(gc=gc, hours=48, customer_label=customer_label)
    # logging.info("Number of PV incidents fetched for dev instance: %d", pv_incidents)
    gc = Centra(hostname=host['dev_host'], username=host['username'], password=host['password'])

    # pv_incidents = fetch_incidents(gc=gc, hours=24)
    pv_incidents = fetch_pv_incidents_csv(gc=gc, cus_name=host['name'])
    logging.info("Number of PV incidents fetched for %s in shared instance: %d", host['name'], pv_incidents)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
