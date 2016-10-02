# -*- coding: utf-8 -*-
from zope.viewlet.viewlet import ViewletBase

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName

class WorkflowViewlet(ViewletBase):

    def update(self):
        
        # Workflow
        workflow = getToolByName(self.context, 'portal_workflow')

        self.workflowStatus = workflow.getInfoFor(self.context, 'review_state', None)

        workflows = workflow.getWorkflowsFor(self.context)

        self.workflowStates = [
            workflow.getInfoFor(self.context, wf.state_var, None)
            for wf in workflows
        ]

        self.workflowNames = [wf.getId() for wf in workflows]

        # Permissions

        self.roles = self.context.validRoles()
        self.permissionInfo = []

        sm = getSecurityManager()

        for p in self.context.permission_settings():
            name = p['name']
            acquired = p['acquire'] == 'CHECKED'
            granted = bool(sm.checkPermission(name, self.context))

            roles = [r['selected'] == 'SELECTED'
                        for r in self.context.rolesOfPermission(name)]
            
            self.permissionInfo.append({
                'name': name,
                'granted': granted,
                'acquired': acquired,
                'roles': roles,
            })
