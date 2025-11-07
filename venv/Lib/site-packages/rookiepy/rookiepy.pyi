from typing import Any, Dict, List, Optional
from sys import platform

CookieList = List[Dict[str, Any]]

def version() -> str:
    """
    Get rookie version

    :return: rookie version
    """
    ...

def firefox(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Firefox

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def zen(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Zen

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def firefox_based(
    key_path: str, db_path: str, domains: Optional[List[str]] = None
) -> CookieList:
    """
    Extract Cookies from Firefox-based browsers

    :param key_path: Path to the key file
    :param db_path: Path to the database file
    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def brave(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Brave browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def edge(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Microsoft Edge browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def chrome(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Google Chrome browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def chromium_based(db_path: str, domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Chromium-based browsers

    :param db_path: Path to the database file
    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def chromium(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Chromium browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def arc(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Arc browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def opera(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Opera browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def vivaldi(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Vivaldi browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def opera_gx(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from Opera GX browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def librewolf(domains: Optional[List[str]] = None) -> CookieList:
    """
    Extract Cookies from LibreWolf browser

    :param domains: Optional list of domains to extract only from them
    :return: A list of dictionaries of cookies
    """
    ...

def load(domains: Optional[List[str]] = None) -> CookieList:
    """
    Load Cookies from a browser

    :param domains: Optional list of domains to load cookies from
    :return: A list of dictionaries of cookies
    """
    ...

def any_browser(
    db_path: str, domains: Optional[List[str]] = ..., key_path: Optional[str] = ...
) -> List[Dict[str, str]]:
    """
    Extract Cookies from any browser.

    :param db_path: Path to browser database file.
    :param domains: Optional list of domains to extract cookies only from these domains.
    :param key_path: Optional path to key file used to decrypt `db_path`.
    :return: A list of dictionaries of cookies.
    """
    ...

# Windows
if platform == "win32":
    def internet_explorer(domains: Optional[List[str]] = None) -> CookieList:
        """
        Extract Cookies from Internet Explorer

        :param domains: Optional list of domains to extract only from them
        :return: A list of dictionaries of cookies
        """
        ...

    def octo_browser(domains: Optional[List[str]] = None) -> CookieList:
        """
        Extract Cookies from Octo browser

        :param domains: Optional list of domains to extract only from them
        :return: A list of dictionaries of cookies
        """
        ...

# MacOS
if platform == "darwin":
    def safari(domains: Optional[List[str]] = None) -> CookieList:
        """
        Extract Cookies from Safari browser

        :param domains: Optional list of domains to extract only from them
        :return: A list of dictionaries of cookies
        """
        ...
