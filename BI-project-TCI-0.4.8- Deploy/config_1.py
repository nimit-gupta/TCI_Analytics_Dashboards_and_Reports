CONN_INFO = {
    'host': '124.7.209.92',
    'port': 1521,
    'user': 'xpscore',
    'psw': 'abc',
    'service': 'ORCL',
}

CONN_STR = '{user}/{psw}@{host}:{port}/{service}'.format(**CONN_INFO)