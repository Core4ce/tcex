"""Install JSON Model"""
# standard library
import os
import uuid
from enum import Enum
from functools import lru_cache
from typing import List, Optional, Union

# third-party
from pydantic import BaseModel
from pydantic.types import constr

# first-party
from tcex.pleb import NoneModel

__all__ = ['InstallJsonModel']


def snake_to_camel(snake_string: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class DeprecationModel(BaseModel):
    """Model for install_json.deprecation"""

    indicator_type: Optional[str]
    interval_says: Optional[int]
    confidence_amount: Optional[int]
    delete_at_minimum: bool = False
    percentage: bool = False

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class FirstRunParamsModel(BaseModel):
    """Model for install_json.deprecation"""

    param: str
    value: Union[int, str]

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class FeedsModel(BaseModel):
    """Model for install_json.feeds"""

    attributes_file: Optional[str]
    deprecation: Optional[List[DeprecationModel]]
    document_storage_limit_mb: int
    enable_bulk_json: bool = False
    firstRunParams: Optional[List[FirstRunParamsModel]]
    indicator_limit: int
    job_file: str
    source_category: str
    source_description: str
    source_name: str

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class ExposePlaybookKeyAsEnum(str, Enum):
    """Enum for install_json.params[].exposePlaybookAs"""

    Binary = 'Binary'
    BinaryArray = 'BinaryArray'
    KeyValue = 'KeyValue'
    KeyValueArray = 'KeyValueArray'
    String = 'String'
    StringArray = 'StringArray'
    TCEntity = 'TCEntity'
    TCEntityArray = 'TCEntityArray'


class TypeEnum(str, Enum):
    """Enum for install_json.params[].type"""

    Boolean = 'Boolean'
    Choice = 'Choice'
    KeyValueList = 'KeyValueList'
    MultiChoice = 'MultiChoice'
    String = 'String'
    StringMixed = 'StringMixed'


class ParamsModel(BaseModel):
    """Model for install_json.params"""

    allow_multiple: bool = False
    default: Optional[Union[bool, str]]
    encrypt: bool = False
    expose_playbook_key_as: Optional[ExposePlaybookKeyAsEnum]
    feed_deployer: bool = False
    hidden: bool = False
    intel_type: Optional[List[str]]
    label: str
    name: str
    note: Optional[str]
    playbook_data_type: Optional[List[str]]
    required: bool = False
    sequence: Optional[int]
    service_config: bool = False
    setup: bool = False
    type: TypeEnum
    valid_values: Optional[List[str]]

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class OutputVariablesModel(BaseModel):
    """Model for install_json.playbook.outputVariables"""

    intel_type: Optional[List]
    name: str
    note: Optional[str]
    type: str

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class RetryModel(BaseModel):
    """Model for install_json.playbook.retry"""

    allowed: bool = False
    default_delay_minutes: Optional[int] = 1
    default_max_retries: Optional[int] = 1

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class PlaybookModel(BaseModel):
    """Model for install_json.playbook"""

    output_prefix: Optional[str]
    output_variables: Optional[List[OutputVariablesModel]]
    retry: Optional[RetryModel]
    type: str

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


class ServiceModel(BaseModel):
    """Model for install_json.service"""

    discovery_types: List

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True


def get_commit_hash() -> Optional[str]:
    """Return the current commit hash if available.

    This is not a required task so best effort is fine. In other words this is not guaranteed
    to work 100% of the time.
    """
    commit_hash = None
    branch = None
    branch_file = '.git/HEAD'  # ref: refs/heads/develop

    # get current branch
    if os.path.isfile(branch_file):
        with open(branch_file) as f:
            try:
                branch = f.read().strip().split('/')[2]
            except IndexError:
                pass

        # get commit hash
        if branch:
            hash_file = f'.git/refs/heads/{branch}'
            if os.path.isfile(hash_file):
                with open(hash_file) as f:
                    commit_hash = f.read().strip()
    return commit_hash


class InstallJsonModel(BaseModel):
    """Install JSON Model"""

    allow_on_demand: bool
    allow_run_as_user: Optional[bool]
    api_user_token_param: Optional[bool]
    app_id: str = uuid.uuid5(uuid.NAMESPACE_X500, os.path.basename(os.getcwd()).lower())
    commit_hash: Optional[str] = get_commit_hash()
    display_name: constr(min_length=3, max_length=100)
    display_path: Optional[constr(min_length=3, max_length=100)]
    docker_image: Optional[str]
    features: List
    feeds: Optional[List[FeedsModel]]
    labels: Optional[List]
    language_version: Optional[str]
    list_delimiter: str
    min_server_version: Optional[str]
    note: Optional[str]
    params: Optional[List[ParamsModel]]
    playbook: Optional[PlaybookModel]
    program_icon: Optional[str]
    program_language: str
    program_main: str
    program_name: Optional[str]
    program_version: str
    publish_out_files: Optional[List]
    repeating_minutes: Optional[List]
    runtime_context: Optional[List]
    runtime_level: Union[List, str]
    service: Optional[ServiceModel]

    class Config:
        """DataModel Config"""

        alias_generator = snake_to_camel
        validate_assignment = True

    @property
    def app_output_var_type(self) -> str:
        """Return the appropriate output var type for the current App."""
        if self.runtime_level.lower() in ['triggerservice', 'webhooktriggerservice']:
            return 'Trigger'
        return 'App'

    @property
    def app_prefix(self) -> str:
        """Return the appropriate output var type for the current App."""
        if self.runtime_level.lower() == 'organization':
            return 'TC_-_'
        if self.runtime_level.lower() == 'playbook':
            return 'TCPB_-_'
        if self.runtime_level.lower() == 'apiservice':
            return 'TCVA_-_'
        if self.runtime_level.lower() == 'triggerservice':
            return 'TCVC_-_'
        if self.runtime_level.lower() == 'webhooktriggerservice':
            return 'TCVW-_'
        return ''

    def filter_params(
        self,
        name: Optional[str] = None,
        hidden: Optional[bool] = None,
        required: Optional[bool] = None,
        service_config: Optional[bool] = None,
        _type: Optional[str] = None,
        input_permutations: Optional[List] = None,
    ) -> dict[str, ParamsModel]:
        """Return params as name/data dict.

        Args:
            name: The name of the input to return.
            hidden: If set the inputs will be filtered based on hidden field.
            required: If set the inputs will be filtered based on required field.
            service_config: If set the inputs will be filtered based on serviceConfig field.
            _type: The type of input to return.
            input_permutations: A list of valid input names for provided permutation.

        Returns:
            dict: All valid inputs for current filter.
        """
        params = {}
        for p in self.params:

            if name is not None:
                if p.name != name:
                    continue

            if hidden is not None:
                if p.hidden is not hidden:
                    continue

            if required is not None:
                if p.required is not required:
                    continue

            if service_config is not None:
                if p.service_config is not service_config:
                    continue

            if _type is not None:
                if p.type != _type:
                    continue

            if input_permutations is not None:
                if p.name not in input_permutations:
                    continue

            params.setdefault(p.name, p)
        return params

    def get_param(self, name: str) -> ParamsModel:
        """Return param for the matching name or {}."""
        return self.params_dict.get(name) or NoneModel()

    @property
    @lru_cache
    def optional_params(self) -> dict[str, ParamsModel]:
        """Return params as name/data model."""
        return {p.name: p for p in self.params if p.required is False}

    @property
    @lru_cache
    def param_names(self) -> List[str]:
        """Return the "name" field from all params."""
        return [p.name for p in self.params]

    @property
    @lru_cache
    def params_dict(self) -> dict[str, ParamsModel]:
        """Return params as name/data dict."""
        return {p.name: p for p in self.params}

    def params_to_args(
        self,
        name: Optional[str] = None,
        hidden: Optional[bool] = None,
        required: Optional[bool] = None,
        service_config: Optional[bool] = None,
        _type: Optional[str] = None,
        input_permutations: Optional[List] = None,
    ) -> dict[str, any]:
        """Return params as cli args.

        Args:
            name: The name of the input to return. Defaults to None.
            required: If set the inputs will be filtered based on required field.
            service_config: If set the inputs will be filtered based on serviceConfig field.
            _type: The type of input to return. Defaults to None.
            input_permutations: A list of valid input names for provided permutation.

        Returns:
            dict: All args for current filter
        """
        args = {}
        for n, p in self.filter_params(
            name, hidden, required, service_config, _type, input_permutations
        ).items():
            if p.type.lower() == 'boolean':
                args[n] = self._to_bool(p.get('default', False))
            elif p.type.lower() == 'choice':
                # use the value from input_permutations if available or provide valid values
                valid_values = f"[{'|'.join(self.expand_valid_values(p.valid_values))}]"
                if input_permutations is not None:
                    valid_values = input_permutations.get(n, valid_values)
                args[n] = valid_values
            elif p.type.lower() == 'multichoice':
                args[n] = p.valid_values
            elif p.type.lower() == 'keyvaluelist':
                args[n] = '<KeyValueArray>'
            elif n in ['api_access_id', 'api_secret_key']:
                # leave these parameters set to the value defined in defaults
                pass
            else:
                types = '|'.join(p.playbook_data_type)
                if types:
                    args[n] = p.default or f'<{types}>'
                else:
                    args[n] = p.default or ''
        return args

    @property
    @lru_cache
    def playbook_outputs(self) -> dict[str, ParamsModel]:
        """Return outputs as name/data model."""
        return {o.name: o for o in self.playbook.output_variables}

    @property
    @lru_cache
    def required_params(self) -> dict[str, ParamsModel]:
        """Return params as name/data dict."""
        return {p.name: p for p in self.params if p.required is True}

    @property
    @lru_cache
    def service_config_params(self) -> dict[str, ParamsModel]:
        """Return params as name/data dict."""
        return {p.name: p for p in self.params if p.service_config is True}

    @property
    @lru_cache
    def service_playbook_params(self) -> dict[str, ParamsModel]:
        """Return params as name/data dict."""
        return {p.name: p for p in self.params if p.service_config is False}
