from collections import namedtuple
from enum import Enum
import traceback
import logging
import attr

from .. import repositories, services, entities

logger = logging.getLogger(name=__name__)


class OrganizationsPlans(str, Enum):
    PREMIUM = "premium"
    FREEMIUM = "freemium"


class MemberOrgRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


@attr.s()
class Organization(entities.BaseEntity):
    """
    Organization entity
    """

    members = attr.ib(type=list)
    groups = attr.ib(type=list)
    accounts = attr.ib(type=list)
    created_at = attr.ib()
    updated_at = attr.ib()
    id = attr.ib(repr=False)
    name = attr.ib(repr=False)
    logo_url = attr.ib(repr=False)
    plan = attr.ib(repr=False)
    owner = attr.ib(repr=False)
    created_by = attr.ib(repr=False)

    # api
    _client_api = attr.ib(type=services.ApiClient, repr=False)

    # repositories
    _repositories = attr.ib(repr=False)

    @property
    def createdAt(self):
        return self.created_at

    @property
    def updatedAt(self):
        return self.updated_at

    @property
    def createdBy(self):
        return self.created_by

    @_repositories.default
    def set_repositories(self):
        reps = namedtuple('repositories',
                          field_names=['organizations', 'projects', 'integrations'])

        r = reps(projects=repositories.Projects(client_api=self._client_api, org=self),
                 organizations=repositories.Organizations(client_api=self._client_api),
                 integrations=repositories.Integrations(client_api=self._client_api, org=self)
                 )
        return r

    @property
    def platform_url(self):
        return self._client_api._get_resource_url("iam/{}/members".format(self.id))

    @property
    def projects(self):
        assert isinstance(self._repositories.projects, repositories.Projects)
        return self._repositories.projects

    @property
    def organizations(self):
        assert isinstance(self._repositories.organizations, repositories.Organizations)
        return self._repositories.organizations

    @property
    def integrations(self):
        assert isinstance(self._repositories.integrations, repositories.Integrations)
        return self._repositories.integrations

    @staticmethod
    def _protected_from_json(_json, client_api):
        """
        Same as from_json but with try-except to catch if error
        :param _json: platform json
        :param client_api: ApiClient entity

        :return: update status: bool, Organization entity
        """
        try:
            organization = Organization.from_json(_json=_json,
                                                  client_api=client_api)
            status = True
        except Exception:
            organization = traceback.format_exc()
            status = False
        return status, organization

    @classmethod
    def from_json(cls, _json, client_api, is_fetched=True):
        """
        Build a Project entity object from a json

        :param is_fetched: is Entity fetched from Platform
        :param _json: _json response from host
        :param client_api: ApiClient entity

        :return: Project object
        """
        inst = cls(members=_json.get('members', None),
                   groups=_json.get('groups', None),
                   accounts=_json.get('accounts', None),
                   created_at=_json.get('createdAt', None),
                   updated_at=_json.get('updatedAt', None),
                   id=_json.get('id', None),
                   name=_json.get('name', None),
                   logo_url=_json.get('logoUrl', None),
                   plan=_json.get('plan', None),
                   owner=_json.get('owner', None),
                   created_by=_json.get('createdBy', None),
                   client_api=client_api)
        inst.is_fetched = is_fetched
        return inst

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        """
        output_dict = attr.asdict(self,
                                  filter=attr.filters.exclude(attr.fields(Organization)._client_api,
                                                              attr.fields(Organization)._repositories,
                                                              attr.fields(Organization).created_at,
                                                              attr.fields(Organization).updated_at,
                                                              attr.fields(Organization).created_by,
                                                              ))
        output_dict['members'] = self.members
        output_dict['groups'] = self.groups
        output_dict['accounts'] = self.accounts
        output_dict['createdAt'] = self.created_at
        output_dict['updatedAt'] = self.updated_at
        output_dict['id'] = self.id
        output_dict['name'] = self.name
        output_dict['logo_url'] = self.logo_url
        output_dict['plan'] = self.plan
        output_dict['owner'] = self.owner
        output_dict['createdBy'] = self.created_by

        return output_dict

    def list_project(self, user_id: str = None):
        """
        list all organization projects

        """
        return self.organizations.list_project(organization=self, user_id=user_id)

    def list_groups(self):
        """
        list all organization groups

        """
        return self.organizations.list_groups(organization=self)

    def list_integrations(self, only_available=False):
        """
        list all organization integrations

        """
        logger.warning('Deprecation Warning - list_integrations will not use from 1.40.0'
                       'Next time use a org.integrations.list() or project.integrations.list()')
        return self.organizations.list_integrations(organization=self, only_available=only_available)

    def get_integrations(self, integrations_id: str):
        """
        get organization integrations

        """
        logger.warning('Deprecation Warning - get_integrations will not use from 1.40.0'
                       'Next time use a org.integrations.get() or project.integrations.get()')

        return self.organizations.get_integrations(organization=self, integrations_id=integrations_id)

    def list_members(self, role: MemberOrgRole = None):
        """
        list all organization members

        """
        return self.organizations.list_members(organization=self, role=role)

    def update(self, plan: str):
        """
        Update the Organization

        :return: Organization object
        """
        return self.organizations.update(organization=self, plan=plan)

    def add_member(self, email, role: MemberOrgRole = MemberOrgRole):
        """
        Add member to the Organization

        :return: True
        """
        return self.organizations.add_member(organization=self, email=email, role=role)

    def delete_member(self, user_id: str, sure: bool = False, really: bool = False):
        """
        delete member from the Organization

        :return: True
        """
        return self.organizations.delete_member(organization=self, user_id=user_id, sure=sure, really=really)

    def update_member(self, email: str, role: MemberOrgRole = MemberOrgRole.MEMBER):
        """
        Update the member role

        :return: True
        """
        return self.organizations.update_member(organization=self, email=email, role=role)

    def open_in_web(self):
        """
        Open the organizations in web platform

        """
        self._client_api._open_in_web(url=self.platform_url)

    def add_integrations(self, integrations_type, name, options):
        """
        Add integrations to the Organization
        Options for each type should be a dict with the following:
        s3 - {key: "", secret: ""}
        gcs - {key: "", secret: "", content: ""},
        azureblob - {key: "", secret: "", clientId: "", tenantId: ""}

        :param integrations_type: "s3" , "gcs", "azureblob"
        :param name: integrations name
        :param options: dict options for each type

        :return: True
        """
        logger.warning('Deprecation Warning - add_integrations will not use from 1.40.0'
                       'Next time use a org.integrations.create() or project.integrations.create()')
        return self.organizations.add_integrations(organization=self,
                                                   integrations_type=integrations_type,
                                                   name=name,
                                                   options=options)

    def delete_integrations(self, integrations_id: str,
                            sure: bool = False,
                            really: bool = False) -> bool:
        """
        Delete integrations from the Organization
        :param integrations_id:
        :param sure: are you sure you want to delete?
        :param really: really really?
        :return: True
        """
        logger.warning('Deprecation Warning - delete_integrations will not use from 1.40.0'
                       'Next time use a org.integrations.delete() or project.integrations.delete()')
        return self.organizations.delete_integrations(organization=self,
                                                      integrations_id=integrations_id,
                                                      sure=sure,
                                                      really=really)

    def update_integrations(self, new_name: str, ):
        """
        Update the integrations with new name
        :param new_name:
        """
        logger.warning('Deprecation Warning - update_integrations will not use from 1.40.0'
                       'Next time use a org.integrations.update() or project.integrations.update()')
        return self.organizations.update_integrations(organization=self, new_name=new_name)
