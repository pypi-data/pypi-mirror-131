import logging

from GuardiPy import CentraApiPayload, Centra
from GuardiPy.CentraObject import User

from secrets import dev_host, test_user_data


def create_test_user(gc: Centra) -> dict:
    query: CentraApiPayload = User.add(**test_user_data)
    result = gc.execute(query)
    return result


def main():
    gc = Centra(hostname=dev_host['dev_host'], username=dev_host['username'], password=dev_host['password'])
    user_creation_result = create_test_user(gc=gc)
    logging.debug(user_creation_result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    main()
