"""ThreatConnect TI Email"""
from ..group import Group


class Tool(Group):
    """Unique API calls for Tool API Endpoints

    Args:
        name (str, kwargs): [Required for Create] The name for this Group.
        owner (str, kwargs): The name for this Group. Default to default Org when not provided
    """

    def __init__(self, ti: 'ThreatIntelligenc', **kwargs):
        """Initialize Class properties."""
        super().__init__(ti, sub_type='Tool', api_entity='tool', api_branch='tools', **kwargs)
