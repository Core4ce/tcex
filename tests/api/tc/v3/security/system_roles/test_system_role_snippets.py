"""Test the TcEx API Snippets."""
# first-party
from tcex.api.tc.v3.tql.tql_operator import TqlOperator
from tests.api.tc.v3.v3_helpers import TestV3, V3Helper


class TestSystemRolesSnippets(TestV3):
    """Test TcEx API Interface."""

    v3 = None

    def setup_method(self):
        """Configure setup before all tests."""
        print('')  # ensure any following print statements will be on new line
        self.v3_helper = V3Helper('system_roles')
        self.v3 = self.v3_helper.v3
        self.tcex = self.v3_helper.tcex

    def test_system_roles_get_all(self):
        """Test snippet"""
        # Begin Snippet
        for system_role in self.tcex.v3.system_roles():
            print(system_role.model.dict(exclude_none=True))
        # End Snippet

    def test_system_roles_tql_filter(self):
        """Test snippet"""
        # Begin Snippet
        system_roles = self.tcex.v3.system_roles()
        system_roles.filter.active(TqlOperator.EQ, True)
        system_roles.filter.assignable(TqlOperator.EQ, True)
        system_roles.filter.displayed(TqlOperator.EQ, True)
        for system_role in system_roles:
            print(system_role.model.dict(exclude_none=True))
        # End Snippet

    def test_system_role_get_by_id(self):
        """Test snippet"""
        # Begin Snippet
        system_role = self.tcex.v3.system_role(id=1)
        system_role.get()
        print(system_role.model.dict(exclude_none=True))
        # End Snippet
