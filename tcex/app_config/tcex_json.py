"""TcEx JSON App Config"""
# standard library
import json
import logging
import os
from collections import OrderedDict
from pathlib import Path

# third-party
import colorama as c

# first-party
from tcex.app_config import InstallJson
from tcex.backports import cached_property

from .models import TcexJsonModel
from .tcex_json_update import TcexJsonUpdate


class TcexJson:
    """Provide a model for the tcex.json config file."""

    def __init__(self, filename=None, path=None, logger=None):
        """Initialize class properties."""
        filename = filename or 'tcex.json'
        path = path or os.getcwd()
        self.log = logger or logging.getLogger('tcex_json')

        # properties
        self.fqfn = Path(os.path.join(path, filename))
        self.ij = InstallJson()

    @cached_property
    def contents(self) -> dict:
        """Return tcex.json file contents."""
        _contents = {}

        if self.fqfn.is_file():
            try:
                with self.fqfn.open() as fh:
                    _contents = json.load(fh, object_pairs_hook=OrderedDict)
            except OSError:  # pragma: no cover
                self.log.error(
                    f'feature=tcex-json, exception=failed-reading-file, filename={self.fqfn}'
                )
        else:  # pragma: no cover
            self.log.error(f'feature=tcex-json, exception=file-not-found, filename={self.fqfn}')

        return _contents

    @cached_property
    def data(self) -> TcexJsonModel:
        """Return the Install JSON model."""
        return TcexJsonModel(**self.contents)

    def print_warnings(self):
        """Print warning messages for tcex.json file."""

        # raise error if tcex.json is missing app_name field
        if self.data.package.app_name is None:  # pragma: no cover
            raise RuntimeError('The tcex.json file is missing the package.app_name field.')

        # log warning for old Apps
        if self.data.package.app_version is not None:
            print(
                f'{c.Fore.YELLOW}'
                'WARNING: The tcex.json file defines "app_version" which should only be '
                'defined in legacy Apps. Removing the value can cause the App to be treated '
                'as a new App by TcExchange. Please remove "app_version" when appropriate.'
                f'{c.Fore.RESET}'
            )

    @property
    def update(self) -> TcexJsonUpdate:
        """Return InstallJsonUpdate instance."""
        return TcexJsonUpdate(tj=self)

    def write(self) -> None:
        """Write current data file."""
        data = self.data.json(
            by_alias=True, exclude_defaults=True, exclude_none=True, indent=2, sort_keys=True
        )
        with self.fqfn.open(mode='w') as fh:
            fh.write(f'{data}\n')
