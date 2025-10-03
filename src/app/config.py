import os
from datetime import timedelta
import secrets


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200MB
    TARIFARIO = "VPNCC-M-MIN_DEF_"

    BLM_CONTRACT_NUMBERS = [
                                    "1439471962"
                                    ,"1487672087"
                                    ,"1472073010"
                                    ,"1423073116"
                                    ,"1425673383"
                                    ,"1440973739"
                                    ,"1455873749"
                                    ,"1463473883"
                                    ,"1454274018"
                                    ,"1472474022"
                                    ,"1485274019"
                                    ,"1489374024"
                                    ,"1418574035"
                                    ,"1429574036"
                                    ,"1483174123"
                                    ,"1411174128"
                                    ,"1475174124"
                                    ,"1459574281"
                                    ,"1481674297"
                                    ,"1462174620"
                                    ,"1428174408"
                                                ]

    # MySQL configurations
    MYSQL_HOST = "db"
    MYSQL_USER = "vulcano"
    MYSQL_PASSWORD = "vulcano"
    MYSQL_DB = "vulcano_db"
    MYSQL_CHARSET = "utf8mb4"

    # LDAP configurations
    LDAP_HOST = "n-dom-1.marinha.pt"
    LDAP_PORT = 636
    LDAP_BASE_DN = "OU=Marinha,dc=marinha,dc=pt"
    LDAP_USER_ATTRIBUTE = "sAMAccountName"
    LDAP_USERNAME_NET = "@marinha.pt"
    LDAP_SSL = True
    LDAP_TLS = False
    LDAP_START_TLS = True

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROCESSED_DIR = os.path.join(BASE_DIR, "processed")


class DevelopmentConfig(Config):
    SECRET_KEY = "dev-key"  # Only for development!


class ProductionConfig(Config):
    pass  # Requires env variable
