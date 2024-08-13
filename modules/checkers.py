from modules.log import log
from modules.dict import flags, nitro_types



def check_nitro(response):
    nitro_level = response.json()['premium_type']
    if nitro_level > 0:
        log.debug('Account has nitro, checking what level..')
        nitro_type = nitro_types.get(nitro_level, 'Cant get nitro level.')
        log.info(f'Nitro level is {nitro_type}')
        return nitro_type
    else:
        log.debug('Nitro not found.')
        return False


def check(name, thing):
    if thing is not None and thing != 'None':
        log.info(f'{name}: {thing}')


def getinfo(response):
    data = response.json()
    login = data.get('username', 'DiscerError')
    email = data.get('email', 'DiscerError')
    phone = data.get('phone', 'DiscerError')
    verified = data.get('verified', 'DiscerError')
    global_name = data.get('global_name', 'DiscerError')
    return login, email, phone, verified, global_name


def decode_flags(flag_value):
    user_flags = []
    for flag, name in flags.items():
        if flag_value & flag:
            user_flags.append(name)
    return user_flags


def check_badges(response):
    data = response.json()
    data_public = data['public_flags']
    # data_private = data['flags']
    if data_public > 0:
        badges = decode_flags(data_public)
        return " ".join(badges)
