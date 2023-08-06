import logging

from GuardiPy import Centra
from GuardiPy.CentraObject import Agent, LabelMinimal
from secrets import host


def fetch_customer_label(gc: Centra, gc_customer_name: str):
    shared_instance = False
    customer_label = None
    query = LabelMinimal.list(
        assets='on,off',
        find_matches=True,
        dynamic_criteria_limit=500,
        key='Customers'
    )
    res = gc.execute(query)
    if res:
        shared_instance = True
        customer_label = next((i.id for i in res if i.value == gc_customer_name), None)
        # for i in res:
        #     if i.value == gc_customer_name:
        #         customer_label = i.id
    return shared_instance, customer_label


def fetch_agents(gc: Centra, cus_name: str = None) -> int:
    line_count = 0
    shared_instance, customer_label = fetch_customer_label(gc=gc, gc_customer_name=cus_name)
    print(customer_label)
    if (not shared_instance) or customer_label:
        query = Agent.list(sort_by_property='display_name')
        if customer_label:
            query.params['labels'] = customer_label
            pass
        result = gc.export_to_csv(query)
        line_count = len(result.splitlines()) - 1
    return line_count if line_count > 0 else 0


def main():
    print(host)
    gc = Centra(hostname=host['dev_host'], username=host['username'], password=host['password'])
    # agent_count = fetch_agents(gc=gc, cus_name=host['name'])
    agent_count = fetch_agents(gc=gc, cus_name=host['name'])
    print(f"{agent_count} agents found for {host['name']} on shared instance")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
