from ftplib import FTP


class FTPClient:
    """
    FTP Client Native Wrapper
    """

    # Connection
    cnx = None

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self.cnx = FTP(host=self.host, user=self.username, passwd=self.password)

    def connect(self):
        """

        :return:
        """
        self.cnx.login()

    def send(self, filename, fd):
        """

        :param filename:
        :param fd:
        :return:
        """
        self.cnx.storbinary("STOR " + filename, fd)
        self.cnx.close()