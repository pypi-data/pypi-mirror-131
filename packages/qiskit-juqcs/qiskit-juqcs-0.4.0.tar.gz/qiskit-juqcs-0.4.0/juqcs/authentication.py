'''Manage Judoor credentials for the user and return an accessible JUNIQ server handle.'''

import os
from getpass import getpass
from configparser import ConfigParser
from base64 import b64encode

import pyunicore.client as unicore_client

from juqcs.exceptions import MissingTokenError, AuthenticationError


# JUNIQ server configuration
_BASE = 'https://zam2125.zam.kfa-juelich.de:9112'
_TARGET = 'JUNIQ'

# Token storage configuration
_config = ConfigParser()
_configpath = os.path.join(
                os.environ.get('APPDATA') or
                os.environ.get('XDG_CONFIG_HOME') or
                os.path.join(os.environ['HOME'], '.config'),
                'juniq')
_CONFIGFILE = os.path.join(_configpath, 'juniq.conf')


def _read_token():
    if os.path.isfile(_CONFIGFILE): # we are on local and theres a config file
        _config.read(_CONFIGFILE)
        TOKEN = _config['credentials'].get('TOKEN', fallback=None)
        OIDC = False
    else: # we are on HDFCloud
        TOKEN = os.getenv('UNITYJSCACCESSTOKEN')
        OIDC  = True

    if TOKEN:
        return TOKEN, OIDC
    else: # theres no token either way so raise
        raise MissingTokenError


def _delete_token():
    if os.path.exists(_CONFIGFILE):
        os.remove(_CONFIGFILE)
        print('Token file deleted')
    #else:
    #    print('No token file found')


def _prompt_user():
    user = input('Please type in your Judoor account username:')
    password = getpass('Please type in your Judoor account password:')
    TOKEN = b64encode(f'{user}:{password}'.encode()).decode('ascii')
    OIDC = False
    return TOKEN, OIDC


def _save_token(TOKEN, _CONFIGFILE):
    '''Store Judoor token in configparser-readable {_CONFIGFILE}.'''
    os.makedirs(_configpath, exist_ok=True)    
    _config['credentials'] = {'TOKEN': TOKEN}
    with open(_CONFIGFILE, 'w') as cfg:
        _config.write(cfg)


def _get_token():
    try:
        TOKEN, OIDC = _read_token()
    except MissingTokenError:
        TOKEN, OIDC = _prompt_user()
    return TOKEN, OIDC


def _connect_to(TOKEN, OIDC):
    '''
    Given the _BASE unicore gateway and a _TARGET system name 
    ('JUNIQ' or 'JUWELS') return a connection to the server
    e.g.: juwels = connect_to(_BASE, 'JUWELS')
    '''
    entrypoint = f'{_BASE}/{_TARGET}/rest/core'
    tr = unicore_client.Transport(TOKEN, oidc=OIDC)
    server = unicore_client.Client(tr, entrypoint)
    return server


def _check_access(server, TOKEN, OIDC):
    access = not server.access_info()['role']['selected']=='anonymous'
    if access:
        print('Credentials are valid! You may start using JUQCS now.')
    else:
        print('Credentials are not valid. Please try again...')
    return access


def _make_server():
    max_tries = 10
    trial = 0
    access = False
    while not access:
        TOKEN, OIDC = _get_token()
        server = _connect_to(TOKEN, OIDC)
        access = _check_access(server, TOKEN, OIDC)
        if not access:
            if OIDC == True:
                raise AuthenticationError(
                    'Your session has expired! '
                    'Please log in again to refresh it.')
            elif OIDC == False:    
                _delete_token()
                trial += 1
                print(f'{max_tries-trial} attempts remaining.')
                if trial >= max_tries:
                    raise AuthenticationError(
                        'Maximum number of authentication attempts exceeded! '
                        'Are you sure you are using valid Judoor credentials?')

    if not OIDC:
        _save_token(TOKEN, _CONFIGFILE)
    
    return server


_JUNIQ = _make_server()