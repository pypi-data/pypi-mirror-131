import logging
from dataclasses import dataclass
import requests

LOGGER = logging.getLogger(__name__)


@dataclass
class Logger:
    """
        Lib to send logs to Hoothoot.
    """
    url: str = "http://localhost:8000"
    user: str = ""
    password: str = ""
    application: str = ""

    def format_request(self, params: dict, type_logger: str) -> bool:
        """
            Function to format payload to send to application.
        """
        payload = {
            "protocol": params['protocol'],
            "application_name": self.application,
            "keyword_log": params['keyword'],
            "json_log": params['body'],
            "type": type_logger,
        }
        auth = (self.user, self.password)

        try:
            LOGGER.info("Send request to hoothoot!")
            response = requests.post(self.url, auth=auth, json=payload)
            if response.status_code == 200:
                return True
            return False
        except (Exception, requests.exceptions.ConnectionError) as error:
            LOGGER.error(error)
            return False

    def info(self, params: dict) -> bool:
        """
            Use to create log info.
        """
        LOGGER.info("Send log info!")
        return self.format_request(params, "INFO")

    def debug(self, params: dict) -> bool:
        """
            Use to create log debug.
        """
        LOGGER.info("Send log debug!")
        return self.format_request(params, "DEBUG")

    def error(self, params: dict) -> bool:
        """
            Use to create log error.
        """
        LOGGER.info("Send log error!")
        return self.format_request(params, "ERROR")
