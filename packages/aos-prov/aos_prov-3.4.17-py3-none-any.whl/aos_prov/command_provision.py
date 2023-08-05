#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#
import time

from colorama import Fore, Style

from aos_prov.communication.cloud.cloud_api import CloudAPI
from aos_prov.communication.unit.v0.unit_communacation import UnitCommunication
from aos_prov.communication.unit.v1.unit_communacation_v1 import UnitCommunicationV1
from aos_prov.utils.config import Config
from aos_prov.utils.errors import GrpcUnimplemented, BoardError
from aos_prov.utils.utils import generate_random_password

COMMAND_TO_DECRYPT = 'diskencryption'


def run_provision(unit_address: str, cloud_api: CloudAPI, reconnect_times=1):
    config = Config()
    uc = UnitCommunicationV1(unit_address)
    model_name = ''
    for retry in range(reconnect_times):
        try:
            print('Starting provisioning using protocol v1')
            config.system_id, model_name = uc.get_system_info()
            break
        except GrpcUnimplemented:
            print('v1 is not supported. Using protocol v0')
            uc = UnitCommunication(unit_address)
            config.system_id, model_name = uc.get_system_info()
            break
        except BoardError as be:
            if retry + 1 < reconnect_times:
                time.sleep(5)
            else:
                raise be

    if config.system_id is None:
        raise BoardError('Cannot read system_id')

    config.set_model(model_name)
    cloud_api.check_unit_is_not_provisioned(config.system_id)

    config.supported_cert_types = uc.get_cert_types()

    password = generate_random_password()

    for cert_type in config.supported_cert_types:
        uc.clear(cert_type)

    for cert_type in config.supported_cert_types:
        uc.set_cert_owner(cert_type, password)

    if COMMAND_TO_DECRYPT in config.supported_cert_types:
        config.supported_cert_types.remove(COMMAND_TO_DECRYPT)
        uc.encrypt_disk(password)
        uc.wait_for_connection()

    for cert_type in config.supported_cert_types:
        config.unit_certificates.append(uc.create_keys(cert_type, password))

    register_payload = {
        'hardware_id': config.system_id,
        'system_uid':  config.system_id,
        'board_model_name': config.model_name,
        'board_model_version': config.model_version,
        'provisioning_software': "aos-provisioning:{version}".format(version=3.1),
        'additional_csrs': []
    }

    for c in config.unit_certificates:
        if c.cert_type == 'online':
            register_payload['online_public_csr'] = c.csr
        elif c.cert_type == 'offline':
            register_payload['offline_public_csr'] = c.csr
        else:
            register_payload['additional_csrs'].append({'cert_type': c.cert_type, 'csr': c.csr})

    response = cloud_api.register_device(register_payload)
    system_uid = response.get('system_uid')
    additional_certs = response.get('additional_certs', [])
    for c in config.unit_certificates:
        if c.cert_type == 'online':
            c.certificate = response.get('online_certificate')
        elif c.cert_type == 'offline':
            c.certificate = response.get('offline_certificate')
        else:
            for ac in additional_certs:
                if ac['cert_type'] == c.cert_type:
                    c.certificate = ac['cert']
                    break

    for c in config.unit_certificates:
        uc.apply_certificate(c)

    claims = response.get('claim')
    if claims:
        uc.set_users([claims])

    uc.finish_provisioning()

    print(f'{Fore.GREEN}Finished successfully!{Style.RESET_ALL}')
    link = cloud_api.get_unit_link_by_system_uid(system_uid)
    if link:
        print(f'You may find your unit on the cloud here: {Fore.GREEN}{link}{Style.RESET_ALL}')
