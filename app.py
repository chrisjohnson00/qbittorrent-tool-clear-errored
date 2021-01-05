import os
from qbittorrent import Client
import pygogo as gogo

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main(host, port):
    qb = Client('http://{}:{}/'.format(host, port))
    qb.login()
    torrents = qb.torrents()
    to_delete = []

    for torrent in torrents:
        if torrent['state'] == "missingFiles":
            logger.debug("Torrent:", extra={'json': torrent})
            to_delete.append(torrent['hash'])

    logger.info("Deleting {} torrents with missing files".format(len(to_delete)))
    qb.delete(to_delete)


def get_config(key):
    """
    Get an environment variable
    :param key: The name of the env variable
    :return: The value of the env variable, or None if it doesn't exist
    """
    if os.environ.get(key):
        return os.environ.get(key)
    return None


if __name__ == "__main__":
    if not get_config("QBITTORRENT_HOST") or not get_config("QBITTORRENT_PORT"):
        exit("Must set QBITTORRENT_HOST & QBITTORRENT_PORT environment variables")
    main(get_config("QBITTORRENT_HOST"), get_config("QBITTORRENT_PORT"))
