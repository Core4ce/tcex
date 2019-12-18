# -*- coding: utf-8 -*-
"""ThreatConnect Case Management"""
import requests
from .artifact import Artifact, Artifacts
from .artifact_type import ArtifactType, ArtifactTypes
from .case import Case, Cases
from .task import Task, Tasks
from .note import Note, Notes
from .tag import Tag, Tags
from .workflow_event import WorkflowEvent, WorkflowEvents
from .workflow_template import WorkflowTemplate, WorkflowTemplates


class CaseManagement(object):
    """
    Interacts with TC V3 api endpoints.
    """

    def __init__(self, tcex):
        """
        Initialize CaseManagement Class.

        Args:
            tcex (obj): An instance of TcEx.
        """
        self.tcex = tcex

    def artifacts(self, **kwargs):
        """
        Returns a instance of Artifacts populated with the provided kwargs
        """
        return Artifacts(self.tcex, **kwargs)

    def artifact(self, **kwargs):
        """
        Returns a instance of a Artifact populated with the provided kwargs
        """
        return Artifact(self.tcex, **kwargs)

    def artifact_types(self, **kwargs):
        """
        Returns a instance of Artifact Types populated with the provided kwargs
        """
        return ArtifactTypes(self.tcex, **kwargs)

    def artifact_type(self, **kwargs):
        """
        Returns a instance of a Artifact Type populated with the provided kwargs
        """
        return ArtifactType(self.tcex, **kwargs)

    def cases(self, **kwargs):
        """
        Returns a instance of Cases populated with the provided kwargs
        """
        return Cases(self.tcex, **kwargs)

    def case(self, **kwargs):
        """
        Returns a instance of a Case populated with the provided kwargs
        """
        return Case(self.tcex, **kwargs)

    def note(self, **kwargs):
        """
        Returns a instance of a Note populated with the provided kwargs
        """
        return Note(self.tcex, **kwargs)

    def notes(self, **kwargs):
        """
        Returns a instance of Notes populated with the provided kwargs
        """
        return Notes(self.tcex, **kwargs)

    def task(self, **kwargs):
        """
        Returns a instance of a Task populated with the provided kwargs
        """
        return Task(self.tcex, **kwargs)

    def tasks(self, **kwargs):
        """
        Returns a instance of Tasks populated with the provided kwargs
        """
        return Tasks(self.tcex, **kwargs)

    def workflow_event(self, **kwargs):
        """
        Returns a instance of a Workflow Event populated with the provided kwargs
        """
        return WorkflowEvent(self.tcex, **kwargs)

    def workflow_events(self, **kwargs):
        """
        Returns a instance of Workflow Events populated with the provided kwargs
        """
        return WorkflowEvents(self.tcex, **kwargs)

    def workflow_template(self, **kwargs):
        """
        Returns a instance of a Workflow Template populated with the provided kwargs
        """
        return WorkflowTemplate(self.tcex, **kwargs)

    def workflow_templates(self, **kwargs):
        """
        Returns a instance of Workflow Templates populated with the provided kwargs
        """
        return WorkflowTemplates(self.tcex, **kwargs)

    def tag(self, **kwargs):
        """
        Returns a instance of a Tag populated with the provided kwargs
        """
        return Tag(self.tcex, **kwargs)

    def tags(self, **kwargs):
        """
        Returns a instance of Tags populated with the provided kwargs
        """
        return Tags(self.tcex, **kwargs)

    def obj_from_type(self, obj_type):
        """
        Returns a instance of the appropriate object for the given type.
        """
        obj_type = obj_type.lower()
        cm = None
        if obj_type == 'tag':
            cm = Tag(self.tcex, **{})
        elif obj_type == 'case':
            cm = Case(self.tcex, **{})
        elif obj_type == 'note':
            cm = Note(self.tcex, **{})
        elif obj_type == 'artifact':
            cm = Artifact(self.tcex, **{})
        elif obj_type == 'task':
            cm = Task(self.tcex, **{})
        elif obj_type in ['workflow_event', 'workflowevent', 'workflow event']:
            cm = WorkflowEvent(self.tcex, **{})
        elif obj_type in ['workflow_template', 'workflowtemplate', 'workflow template']:
            cm = WorkflowTemplate(self.tcex, **{})

        return cm

    def obj_from_entity(self, entity):
        """
        Returns a instance of the appropriate object populated with the kwargs of the provided dict.
        """
        obj_type = entity.pop('type').lower()
        if obj_type == 'tag':
            return Tag(self.tcex, **entity)
        elif obj_type == 'case':
            return Case(self.tcex, **entity)
        elif obj_type == 'note':
            return Note(self.tcex, **entity)
        elif obj_type == 'artifact':
            return Artifact(self.tcex, **entity)
        elif obj_type == 'task':
            return Task(self.tcex, **entity)
        elif obj_type in ['workflow_event', 'workflowevent', 'workflow event']:
            return WorkflowEvent(self.tcex, **entity)
        elif obj_type in ['workflow_template', 'workflowtemplate', 'workflow template']:
            return WorkflowTemplate(self.tcex, **entity)

        return None

    def create_entity(self, entity, owner):
        """
        Creates a CM objected provided a dict and owner.
        """
        entity_type = entity.get('type').lower()
        obj = self.obj_from_entity(entity)
        if obj is None:
            return None

        r = obj.submit()
        response = {}
        if isinstance(r, requests.models.Response):
            response['status_code'] = r.status_code
        else:
            response['status_code'] = 201
            response['unique_id'] = r.as_dict.get('id')

        response['main_type'] = 'Case_Management'
        response['sub_type'] = entity_type
        response['owner'] = owner

        return response
