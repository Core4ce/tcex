"""ThreatConnect REST API Authentication"""
import base64  # authorization
import hashlib  # authorization
import hmac  # authorization
import logging
import sys
import time

from requests import (auth, exceptions, get)


class TcExAuth(auth.AuthBase):
    """ThreatConnect Authorization"""
    def __init__(self, logger=None):
        """Initialize Class Properties"""
        self.log = self._logger
        if logger is not None:
            self.log = logger

    @staticmethod
    def _logger():
        """Initialize basic stream logger"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # create a stream handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        # add handler
        logger.addHandler(ch)

        # return configured logger
        return logger

    def __call__(self, r):
        """Place holder"""
        pass


class TcExHmacAuth(TcExAuth):
    """ThreatConnect HMAC Authorization"""
    def __init__(self, access_id, secret_key, logger=None):
        """Initialize Class Properties"""
        super(TcExHmacAuth, self).__init__(logger)
        self._access_id = access_id
        self._secret_key = secret_key
        self.log = self._logger
        if logger is not None:
            self.log = logger

    def __call__(self, r):
        """Return requests"""
        timestamp = int(time.time())
        signature = '{}:{}:{}'.format(r.path_url, r.method, timestamp)
        hmac_signature = hmac.new(
            self._secret_key.encode(), signature.encode(), digestmod=hashlib.sha256).digest()
        authorization = 'TC {}:{}'.format(
            self._access_id, base64.b64encode(hmac_signature).decode())

        r.headers['Authorization'] = authorization
        r.headers['Timestamp'] = timestamp
        return r


class TcExTokenAuth(TcExAuth):
    """ThreatConnect Auth"""
    def __init__(self, session, token, token_expiration, token_url, logger=None):
        """Initialize Class Properties"""
        super(TcExTokenAuth, self).__init__(logger)
        self._token = token
        self._token_expiration = int(token_expiration)
        self._token_url = token_url
        self._session = session  # use same value as session for verify
        self.log = self._logger
        if logger is not None:
            self.log = logger

    def _renew_token(self):
        """Renew and expired ThreatConnect Token"""
        self.log.info('Token Expiration: {}'.format(self._token_expiration))
        self.log.info('Renewing ThreatConnect Token')
        try:
            payload = {'expiredToken': self._token}
            url = '{}/appAuth'.format(self._token_url)
            r = get(url, params=payload, verify=self._session.verify)
            data = r.json()
            self._token = data.get('apiToken')
            self._token_expiration = int(data['apiTokenExpires'])
            self.log.debug('Updated Token Expiration: {}'.format(self._token_expiration))
        except exceptions.SSLError:
            self.log.error(u'SSL Error during token renewal.')
        except Exception:
            # TODO: Limit this exception
            self.log.error(u'Failure during token renewal.')

    def __call__(self, r):
        """ """
        window_padding = 60  # pad renewal by 60 seconds
        current_time = int(time.time()) + window_padding
        if self._token_expiration < current_time:
            self._renew_token()
        r.headers['Authorization'] = 'TC-Token {}'.format(self._token)
        return r
