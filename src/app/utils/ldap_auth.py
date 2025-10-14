from ldap3 import Server, Connection, ALL, Tls
from MySQLdb.cursors import DictCursor
import ssl
from ..config import Config
from app.db import get_connection


def authenticate_user(username, password):
    """
    Autentica um usuário no servidor LDAP.

    Args:
        username (str): Nome de utilizador (sem o domínio).
        password (str): Senha do utilizador.

    Returns:
        dict: Um dicionário com as informações do utilizador se a autenticação for bem-sucedida, ou None caso contrário.
    """
    try:
        print(f"Tentando autenticar o usuário: {username}")

        # Verifica se o usuário existe na tabela de usuários do banco de dados
        conn = get_connection()
        cursor = conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
       # conn.close()

        if not user:
            print(f"Usuário {username} não encontrado no banco de dados.")
            return None

        # Configuração do servidor LDAP com LDAPS
        tls_configuration = (
            Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
            if Config.LDAP_START_TLS
            else None
        )
        server = Server(
            Config.LDAP_HOST,
            port=Config.LDAP_PORT,
            use_ssl=Config.LDAP_SSL,
            get_info=ALL,
            tls=tls_configuration,
        )
        print(f"Servidor LDAP configurado: {server}")

        # Gera o DN do usuário
        user_dn = f"{username}{Config.LDAP_USERNAME_NET}"
        print(f"DN do utilizador gerado: {user_dn}")

        # Conexão ao LDAP
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        print(f"Conexão LDAP estabelecida: {conn}")

        # Verifica se a autenticação foi bem-sucedida
        if conn.bind():
            print(f"Utilizador {username} autenticado com sucesso.")

            # Procura o usuário no LDAP para obter mais informações
            search_base = Config.LDAP_BASE_DN
            search_filter = f"(sAMAccountName={username})"
            conn.search(
                search_base,
                search_filter,
                attributes=["displayName", "mail", "givenName", "sn"],
            )  # Add other attributes you need

            # In ldap_auth.py, modify the return statement:
            if len(conn.entries) > 0:
                user_entry = conn.entries[0]
                display_name = (
                    str(user_entry.displayName)
                    if "displayName" in user_entry
                    else username
                )  # Fallback to username if displayName not available

                print(f"Utilizador {username} encontrado no LDAP.")
                return {
                    "username": username,
                    "display_name": display_name,
                    "is_admin": user["is_admin"],
                }
            else:
                print(f"Utilizador {username} não encontrado no LDAP.")
                return None
        else:
            print(f"Falha ao autenticar o utilizador {username}.")
            print(f"Resposta do LDAP: {conn.result}")
            return None
    except Exception as e:
        print(f"Erro durante a autenticação LDAP: {e}")
        return None
