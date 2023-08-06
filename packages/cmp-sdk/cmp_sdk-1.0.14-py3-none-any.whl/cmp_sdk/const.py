import os

SERVER = os.environ.get('CMP_SERVER')
AUTH_NAME = os.environ.get('CMP_AUTH_NAME')
AUTH_PASSWORD = os.environ.get('CMP_AUTH_PASSWORD')
CRED_TTL = os.environ.get('CMP_CRED_TTL')
COMPANY_ID = os.environ.get('CMP_COMPANY_ID')
DRY_RUN = os.environ.get('CMP_DRY_RUN')


if not all([SERVER, AUTH_PASSWORD, AUTH_NAME, CRED_TTL, COMPANY_ID]):
    raise EnvironmentError(f'未设置完全CMP_SERVER/CMP_AUTH_NAME/CMP_AUTH_PASSWORD/CMP_CRED_TTL/CMP_COMPANY_ID环境变量')

COMPANY_ID = int(COMPANY_ID)
CRED_TTL = int(CRED_TTL)
