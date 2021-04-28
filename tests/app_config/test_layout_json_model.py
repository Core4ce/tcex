"""Test LayoutJson"""
# pylint: disable=R1710
# standard library
import json
import os
import shutil
from pathlib import Path

# third-party
from deepdiff import DeepDiff

# first-party
from tcex.app_config.install_json import InstallJson
from tcex.app_config.layout_json import LayoutJson
from tcex.app_config.models.layout_json_model import OutputsModel, ParametersModel


class TestLayoutJson:
    """App Config LayoutJson testing."""

    # @staticmethod
    # def test_dev_testing():
    #     """."""
    #     fqfn = Path('tests/app_config/layout_json_samples/tcpb/tcpb-example1-layout.json')
    #     try:
    #         lj = LayoutJson(filename=fqfn.name, path=fqfn.parent)
    #     except Exception as ex:
    #         assert False, f'Failed parsing file {fqfn.name} ({ex})'

    #     # ij = InstallJson(
    #     #     filename='tcpb_-_blackberry_optics-install.json',
    #     #     path='tests/app_config/install_json_samples/tcpb',
    #     # )
    #     print('\nfilename', filename)
    #     # lj.create(inputs=ij.data.params, outputs=ij.data.playbook.output_variables)
    #     print('lj.data.inputs', lj.data.inputs)
    #     # print('lj.data.outputs', lj.data.outputs)

    @staticmethod
    def ij(app_name: str = 'app_1', app_type: str = 'tcpb'):
        """Return install.json instance."""
        ij_fqfn = os.path.join('tests', 'app_config', 'apps', app_type, app_name, 'install.json')
        fqfn = Path(ij_fqfn)
        try:
            return InstallJson(filename=fqfn.name, path=fqfn.parent)
        except Exception as ex:
            assert False, f'Failed parsing file {fqfn.name} ({ex})'

    @staticmethod
    def lj(app_name: str = 'app_1', app_type: str = 'tcpb'):
        """Return layout.json instance."""
        lj_fqfn = os.path.join('tests', 'app_config', 'apps', app_type, app_name, 'layout.json')
        fqfn = Path(lj_fqfn)
        try:
            return LayoutJson(filename=fqfn.name, path=fqfn.parent)
        except Exception as ex:
            assert False, f'Failed parsing file {fqfn.name} ({ex})'

    @staticmethod
    def lj_bad(app_name: str = 'app_bad_layout_json', app_type: str = 'tcpb'):
        """Return layout.json instance with "bad" file."""
        base_fqpn = os.path.join('tests', 'app_config', 'apps', app_type, app_name)
        shutil.copy2(
            os.path.join(base_fqpn, 'layout-template.json'),
            os.path.join(base_fqpn, 'layout.json'),
        )
        fqfn = Path(os.path.join(base_fqpn, 'layout.json'))
        try:
            return LayoutJson(filename=fqfn.name, path=fqfn.parent)
        except Exception as ex:
            assert False, f'Failed parsing file {fqfn.name} ({ex})'

    @staticmethod
    def model_validate(path: str) -> None:
        """Validate input model in and out."""
        lj_path = Path(path)
        for fqfn in sorted(lj_path.glob('**/*layout.json')):
            fqfn = Path(fqfn)
            with fqfn.open() as fh:
                json_dict = json.load(fh)

            try:
                lj = LayoutJson(filename=fqfn.name, path=fqfn.parent)
                # lj.update.multiple()
            except Exception as ex:
                assert False, f'Failed parsing file {fqfn.name} ({ex})'

            ddiff = DeepDiff(
                json_dict,
                # template requires json dump to serialize certain fields
                json.loads(lj.data.json(by_alias=True, exclude_defaults=True, exclude_none=True)),
                ignore_order=True,
            )
            assert ddiff == {}, f'Failed validation of file {fqfn.name}'

    def test_create(self):
        """Test method"""
        ij = self.ij(app_type='tcpb')
        lj = self.lj(app_name='app_create_layout', app_type='tcpb')
        lj.create(inputs=ij.data.params, outputs=ij.data.playbook.output_variables)
        assert lj.fqfn.is_file()

        # remove temp file
        lj.fqfn.unlink()

    def test_has_layout(self):
        """Test method"""
        assert self.lj().has_layout

    def test_model_get_param(self):
        """Test method"""
        assert isinstance(self.lj().data.get_param('tc_action'), ParametersModel)

    def test_model_get_output(self):
        """Test method"""
        assert isinstance(self.lj().data.get_output('action_1.binary.output1'), OutputsModel)

    def test_model_output_(self):
        """Test method"""
        assert isinstance(self.lj().data.outputs_, dict)

    def test_model_param_names(self):
        """Test method"""
        assert isinstance(self.lj().data.param_names, list)

    def test_update(self):
        """Test method"""
        ij = self.lj_bad()
        try:
            ij.update.multiple()
            assert True
        except Exception as ex:
            assert False, f'Failed to update install.json file ({ex}).'
        finally:
            # cleanup temp file
            ij.fqfn.unlink()

    def test_tcpb_support(self):
        """Validate layout.json files."""
        self.model_validate('tests/app_config/app/tcpb')

    def test_tcvc_support(self):
        """Validate layout.json files."""
        self.model_validate('tests/app_config/app/tcvc')
