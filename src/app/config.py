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
    
    VOZ_CONTRACT_NUMBERS = [
                                        "1427973991"
                                        ,"1445769058"
                                        ,"1435769053"
                                        ,"1494263296"
                                        ,"1494062899"
                                        ,"1466769056"
                                        ,"1437769056"
                                        ,"1404869059"
                                        ,"1463869053"
                                        ,"1407769051"
                                        ,"1476769050"
                                        ,"1446769054"
                                        ,"1423369172"
                                        ,"1480369176"
                                        ,"1481369176"
                                        ,"1455269174"
                                        ,"1480369178"
                                        ,"1467269170"
                                        ,"1482369175"
                                        ,"1457269171"
                                        ,"1436269174"
                                        ,"1402369179"
                                        ,"1465269171"
                                        ,"1486769050"
                                        ,"1405269182"
                                        ,"1428269182"
                                        ,"1446269184"
                                        ,"1406269181"
                                        ,"1461369171"
                                        ,"1436269186"
                                        ,"1450369174"
                                        ,"1435269181"
                                        ,"1433369176"
                                        ,"1458269188"
                                        ,"1465269185"
                                        ,"1435269186"
                                        ,"1456269189"
                                        ,"1431469620"
                                        ,"1466969879"
                                        ,"1419770173"
                                        ,"1460770685"
                                        ,"1456670688"
                                        ,"1468071272"
                                        ,"1451071301"
                                        ,"1484773166"
                                        ,"1458769053"
                                        ,"1407769050"
                                        ,"1467269176"
                                        ,"1468769056"
                                        ,"1457769054"
                                        ,"1465769052"
                                        ,"1434869057"
                                        ,"1466769058"
                                        ,"1483269170"
                                        ,"1458269189"
                                        ,"1451369170"
                                        ,"1426269185"
                                        ,"1432369177"
                                        ,"1446269182"
                                        ,"1444269182"
                                        ,"1456570791"
                                        ,"1472670835"
                                        ,"1445769051"
                                        ,"1454869052"
                                        ,"1450369177"
                                        ,"1486269171"
                                        ,"1466269188"
                                        ,"1465869531"
                                        ,"1448069631"
                                        ,"1468369621"
                                        ,"1453269832"
                                        ,"1441969852"
                                        ,"1400070682"
                                        ,"1461770680"
                                        ,"1400871978"
                                        ,"1411871971"
                                        ,"1470671973"
                                        ,"1460671970"
                                        ,"1431671974"
                                        ,"1401871978"
                                        ,"1453073498"
                                        ,"1423869054"
                                        ,"1482869050"
                                        ,"1459769055"
                                        ,"1430868611"
                                                    ]

    # MySQL configurations
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "vulcano_db")
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
