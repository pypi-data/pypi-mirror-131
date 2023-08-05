"""
    Cisco Intersight

    Cisco Intersight is a management platform delivered as a service with embedded analytics for your Cisco and 3rd party IT infrastructure. This platform offers an intelligent level of management that enables IT organizations to analyze, simplify, and automate their environments in more advanced ways than the prior generations of tools. Cisco Intersight provides an integrated and intuitive management experience for resources in the traditional data center as well as at the edge. With flexible deployment options to address complex security needs, getting started with Intersight is quick and easy. Cisco Intersight has deep integration with Cisco UCS and HyperFlex systems allowing for remote deployment, configuration, and ongoing maintenance. The model-based deployment works for a single system in a remote location or hundreds of systems in a data center and enables rapid, standardized configuration and deployment. It also streamlines maintaining those systems whether you are working with small or very large configurations. The Intersight OpenAPI document defines the complete set of properties that are returned in the HTTP response. From that perspective, a client can expect that no additional properties are returned, unless these properties are explicitly defined in the OpenAPI document. However, when a client uses an older version of the Intersight OpenAPI document, the server may send additional properties because the software is more recent than the client. In that case, the client may receive properties that it does not know about. Some generated SDKs perform a strict validation of the HTTP response body against the OpenAPI document.  # noqa: E501

    The version of the OpenAPI document: 1.0.9-4950
    Contact: intersight@cisco.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from intersight.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)

def lazy_import():
    from intersight.model.iam_account_relationship import IamAccountRelationship
    from intersight.model.iam_permission_relationship import IamPermissionRelationship
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
    from intersight.model.workflow_message import WorkflowMessage
    from intersight.model.workflow_pending_dynamic_workflow_info_relationship import WorkflowPendingDynamicWorkflowInfoRelationship
    from intersight.model.workflow_task_info_relationship import WorkflowTaskInfoRelationship
    from intersight.model.workflow_workflow_ctx import WorkflowWorkflowCtx
    from intersight.model.workflow_workflow_definition_relationship import WorkflowWorkflowDefinitionRelationship
    from intersight.model.workflow_workflow_info_properties import WorkflowWorkflowInfoProperties
    globals()['IamAccountRelationship'] = IamAccountRelationship
    globals()['IamPermissionRelationship'] = IamPermissionRelationship
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['OrganizationOrganizationRelationship'] = OrganizationOrganizationRelationship
    globals()['WorkflowMessage'] = WorkflowMessage
    globals()['WorkflowPendingDynamicWorkflowInfoRelationship'] = WorkflowPendingDynamicWorkflowInfoRelationship
    globals()['WorkflowTaskInfoRelationship'] = WorkflowTaskInfoRelationship
    globals()['WorkflowWorkflowCtx'] = WorkflowWorkflowCtx
    globals()['WorkflowWorkflowDefinitionRelationship'] = WorkflowWorkflowDefinitionRelationship
    globals()['WorkflowWorkflowInfoProperties'] = WorkflowWorkflowInfoProperties


class WorkflowWorkflowInfoAllOf(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('class_id',): {
            'WORKFLOW.WORKFLOWINFO': "workflow.WorkflowInfo",
        },
        ('object_type',): {
            'WORKFLOW.WORKFLOWINFO': "workflow.WorkflowInfo",
        },
        ('action',): {
            'NONE': "None",
            'CREATE': "Create",
            'START': "Start",
            'PAUSE': "Pause",
            'RESUME': "Resume",
            'RETRY': "Retry",
            'RETRYFAILED': "RetryFailed",
            'CANCEL': "Cancel",
        },
        ('last_action',): {
            'NONE': "None",
            'CREATE': "Create",
            'START': "Start",
            'PAUSE': "Pause",
            'RESUME': "Resume",
            'RETRY': "Retry",
            'RETRYFAILED': "RetryFailed",
            'CANCEL': "Cancel",
        },
        ('pause_reason',): {
            'NONE': "None",
            'TASKWITHWARNING': "TaskWithWarning",
            'SYSTEMMAINTENANCE': "SystemMaintenance",
        },
        ('wait_reason',): {
            'NONE': "None",
            'GATHERTASKS': "GatherTasks",
            'DUPLICATE': "Duplicate",
            'RATELIMIT': "RateLimit",
            'WAITTASK': "WaitTask",
            'PENDINGRETRYFAILED': "PendingRetryFailed",
            'WAITINGTOSTART': "WaitingToStart",
        },
        ('workflow_meta_type',): {
            'SYSTEMDEFINED': "SystemDefined",
            'USERDEFINED': "UserDefined",
            'DYNAMIC': "Dynamic",
        },
    }

    validations = {
        ('email',): {
            'regex': {
                'pattern': r'^$|^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$',  # noqa: E501
            },
        },
        ('name',): {
            'regex': {
                'pattern': r'^[^:]{1,92}$',  # noqa: E501
            },
        },
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'class_id': (str,),  # noqa: E501
            'object_type': (str,),  # noqa: E501
            'action': (str,),  # noqa: E501
            'cleanup_time': (datetime,),  # noqa: E501
            'email': (str,),  # noqa: E501
            'end_time': (datetime,),  # noqa: E501
            'failed_workflow_cleanup_duration': (int,),  # noqa: E501
            'input': (bool, date, datetime, dict, float, int, list, str, none_type,),  # noqa: E501
            'inst_id': (str,),  # noqa: E501
            'internal': (bool,),  # noqa: E501
            'last_action': (str,),  # noqa: E501
            'message': ([WorkflowMessage], none_type,),  # noqa: E501
            'meta_version': (int,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'output': (bool, date, datetime, dict, float, int, list, str, none_type,),  # noqa: E501
            'pause_reason': (str,),  # noqa: E501
            'progress': (float,),  # noqa: E501
            'properties': (WorkflowWorkflowInfoProperties,),  # noqa: E501
            'retry_from_task_name': (str,),  # noqa: E501
            'src': (str,),  # noqa: E501
            'start_time': (datetime,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'success_workflow_cleanup_duration': (int,),  # noqa: E501
            'trace_id': (str,),  # noqa: E501
            'type': (str,),  # noqa: E501
            'user_action_required': (bool,),  # noqa: E501
            'user_id': (str,),  # noqa: E501
            'wait_reason': (str,),  # noqa: E501
            'workflow_ctx': (WorkflowWorkflowCtx,),  # noqa: E501
            'workflow_meta_type': (str,),  # noqa: E501
            'workflow_task_count': (int,),  # noqa: E501
            'workflow_worker_task_count': (int,),  # noqa: E501
            'account': (IamAccountRelationship,),  # noqa: E501
            'associated_object': (MoBaseMoRelationship,),  # noqa: E501
            'organization': (OrganizationOrganizationRelationship,),  # noqa: E501
            'parent_task_info': (WorkflowTaskInfoRelationship,),  # noqa: E501
            'pending_dynamic_workflow_info': (WorkflowPendingDynamicWorkflowInfoRelationship,),  # noqa: E501
            'permission': (IamPermissionRelationship,),  # noqa: E501
            'task_infos': ([WorkflowTaskInfoRelationship], none_type,),  # noqa: E501
            'workflow_definition': (WorkflowWorkflowDefinitionRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'action': 'Action',  # noqa: E501
        'cleanup_time': 'CleanupTime',  # noqa: E501
        'email': 'Email',  # noqa: E501
        'end_time': 'EndTime',  # noqa: E501
        'failed_workflow_cleanup_duration': 'FailedWorkflowCleanupDuration',  # noqa: E501
        'input': 'Input',  # noqa: E501
        'inst_id': 'InstId',  # noqa: E501
        'internal': 'Internal',  # noqa: E501
        'last_action': 'LastAction',  # noqa: E501
        'message': 'Message',  # noqa: E501
        'meta_version': 'MetaVersion',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'output': 'Output',  # noqa: E501
        'pause_reason': 'PauseReason',  # noqa: E501
        'progress': 'Progress',  # noqa: E501
        'properties': 'Properties',  # noqa: E501
        'retry_from_task_name': 'RetryFromTaskName',  # noqa: E501
        'src': 'Src',  # noqa: E501
        'start_time': 'StartTime',  # noqa: E501
        'status': 'Status',  # noqa: E501
        'success_workflow_cleanup_duration': 'SuccessWorkflowCleanupDuration',  # noqa: E501
        'trace_id': 'TraceId',  # noqa: E501
        'type': 'Type',  # noqa: E501
        'user_action_required': 'UserActionRequired',  # noqa: E501
        'user_id': 'UserId',  # noqa: E501
        'wait_reason': 'WaitReason',  # noqa: E501
        'workflow_ctx': 'WorkflowCtx',  # noqa: E501
        'workflow_meta_type': 'WorkflowMetaType',  # noqa: E501
        'workflow_task_count': 'WorkflowTaskCount',  # noqa: E501
        'workflow_worker_task_count': 'WorkflowWorkerTaskCount',  # noqa: E501
        'account': 'Account',  # noqa: E501
        'associated_object': 'AssociatedObject',  # noqa: E501
        'organization': 'Organization',  # noqa: E501
        'parent_task_info': 'ParentTaskInfo',  # noqa: E501
        'pending_dynamic_workflow_info': 'PendingDynamicWorkflowInfo',  # noqa: E501
        'permission': 'Permission',  # noqa: E501
        'task_infos': 'TaskInfos',  # noqa: E501
        'workflow_definition': 'WorkflowDefinition',  # noqa: E501
    }

    _composed_schemas = {}

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """WorkflowWorkflowInfoAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "workflow.WorkflowInfo", must be one of ["workflow.WorkflowInfo", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "workflow.WorkflowInfo", must be one of ["workflow.WorkflowInfo", ]  # noqa: E501
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            action (str): The action of the workflow such as start, cancel, retry, pause. * `None` - No action is set, this is the default value for action field. * `Create` - Create a new instance of the workflow but it does not start the execution of the workflow. Use the Start action to start execution of the workflow. * `Start` - Start a new execution of the workflow. * `Pause` - Pause the workflow, this can only be issued on workflows that are in running state. * `Resume` - Resume the workflow which was previously paused through pause action on the workflow. * `Retry` - Retry the workflow that has previously reached a final state and has the retryable property set to true. A running or waiting workflow cannot be retried. If the property retryFromTaskName is also passed along with this action, the workflow will be started from that specific task, otherwise the workflow will be restarted from the first task.  The task name in retryFromTaskName must be one of the tasks that completed or failed in the previous run. It is not possible to retry a workflow from a task which wasn't run in the previous iteration. * `RetryFailed` - Retry the workflow that has failed. A running or waiting workflow or a workflow that completed successfully cannot be retried. Only the tasks that failed in the previous run will be retried and the rest of workflow will be run. This action does not restart the workflow and also does not support retrying from a specific task. * `Cancel` - Cancel the workflow that is in running or waiting state.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            cleanup_time (datetime): The time when the workflow info will be removed from database.. [optional]  # noqa: E501
            email (str): The email address of the user who started this workflow.. [optional]  # noqa: E501
            end_time (datetime): The time when the workflow reached a final state.. [optional]  # noqa: E501
            failed_workflow_cleanup_duration (int): The duration in hours after which the workflow info for failed, terminated or timed out workflow will be removed from database.. [optional] if omitted the server will use the default value of 2160  # noqa: E501
            input (bool, date, datetime, dict, float, int, list, str, none_type): All the given inputs for the workflow.. [optional]  # noqa: E501
            inst_id (str): A workflow instance Id which is the unique identified for the workflow execution.. [optional]  # noqa: E501
            internal (bool): Denotes if this workflow is internal and should be hidden from user view of running workflows.. [optional]  # noqa: E501
            last_action (str): The last action that was issued on the workflow is saved in this field. * `None` - No action is set, this is the default value for action field. * `Create` - Create a new instance of the workflow but it does not start the execution of the workflow. Use the Start action to start execution of the workflow. * `Start` - Start a new execution of the workflow. * `Pause` - Pause the workflow, this can only be issued on workflows that are in running state. * `Resume` - Resume the workflow which was previously paused through pause action on the workflow. * `Retry` - Retry the workflow that has previously reached a final state and has the retryable property set to true. A running or waiting workflow cannot be retried. If the property retryFromTaskName is also passed along with this action, the workflow will be started from that specific task, otherwise the workflow will be restarted from the first task.  The task name in retryFromTaskName must be one of the tasks that completed or failed in the previous run. It is not possible to retry a workflow from a task which wasn't run in the previous iteration. * `RetryFailed` - Retry the workflow that has failed. A running or waiting workflow or a workflow that completed successfully cannot be retried. Only the tasks that failed in the previous run will be retried and the rest of workflow will be run. This action does not restart the workflow and also does not support retrying from a specific task. * `Cancel` - Cancel the workflow that is in running or waiting state.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            message ([WorkflowMessage], none_type): [optional]  # noqa: E501
            meta_version (int): Version of the workflow metadata for which this workflow execution was started.. [optional]  # noqa: E501
            name (str): A name of the workflow execution instance.. [optional]  # noqa: E501
            output (bool, date, datetime, dict, float, int, list, str, none_type): All the generated outputs for the workflow.. [optional]  # noqa: E501
            pause_reason (str): Denotes the reason workflow is in paused status. * `None` - Pause reason is none, which indicates there is no reason for the pause state. * `TaskWithWarning` - Pause reason indicates the workflow is in this state due to a task that has a status as completed with warnings. * `SystemMaintenance` - Pause reason indicates the workflow is in this state based on actions of system admin for maintenance.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            progress (float): This field indicates percentage of workflow task execution.. [optional]  # noqa: E501
            properties (WorkflowWorkflowInfoProperties): [optional]  # noqa: E501
            retry_from_task_name (str): This field is applicable when Retry action is issued for a workflow which is in 'final' state. When this field is not specified, the workflow will be retried from the start i.e., the first task. When this field is specified then the workflow will be retried from the specified task. This field should specify the task name which is the unique name of the task within the workflow. The task name must be one of the tasks that completed or failed in the previous run. It is not possible to retry a workflow from a task which wasn't run in the previous iteration.. [optional]  # noqa: E501
            src (str): The source microservice name which is the owner for this workflow.. [optional]  # noqa: E501
            start_time (datetime): The time when the workflow was started for execution.. [optional]  # noqa: E501
            status (str): A status of the workflow (RUNNING, WAITING, COMPLETED, TIME_OUT, FAILED).. [optional]  # noqa: E501
            success_workflow_cleanup_duration (int): The duration in hours after which the workflow info for successful workflow will be removed from database.. [optional] if omitted the server will use the default value of 2160  # noqa: E501
            trace_id (str): The trace id to keep track of workflow execution.. [optional]  # noqa: E501
            type (str): A type of the workflow (serverconfig, ansible_monitoring).. [optional]  # noqa: E501
            user_action_required (bool): Property will be set when an user action is required on the workflow. This can be because the workflow is waiting for a wait task to be updated, workflow is paused or workflow launched by a configuration object has failed and needs to be retried in order to complete successfully.. [optional] if omitted the server will use the default value of False  # noqa: E501
            user_id (str): The user identifier which indicates the user that started this workflow.. [optional]  # noqa: E501
            wait_reason (str): Denotes the reason workflow is in waiting status. * `None` - Wait reason is none, which indicates there is no reason for the waiting state. * `GatherTasks` - Wait reason is gathering tasks, which indicates the workflow is in this state in order to gather tasks. * `Duplicate` - Wait reason is duplicate, which indicates the workflow is a duplicate of current running workflow. * `RateLimit` - Wait reason is rate limit, which indicates the workflow is rate limited by account/instance level throttling threshold. * `WaitTask` - Wait reason when there are one or more wait tasks in the workflow which are yet to receive a task status update. * `PendingRetryFailed` - Wait reason when the workflow is pending a RetryFailed action. * `WaitingToStart` - Workflow is waiting to start on workflow engine.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            workflow_ctx (WorkflowWorkflowCtx): [optional]  # noqa: E501
            workflow_meta_type (str): The type of workflow meta. Derived from the workflow meta that is used to launch this workflow instance. * `SystemDefined` - System defined workflow definition. * `UserDefined` - User defined workflow definition. * `Dynamic` - Dynamically defined workflow definition.. [optional] if omitted the server will use the default value of "SystemDefined"  # noqa: E501
            workflow_task_count (int): Total number of workflow tasks in this workflow.. [optional]  # noqa: E501
            workflow_worker_task_count (int): Total number of worker tasks in this workflow. This count doesn't include the control tasks in the workflow.. [optional]  # noqa: E501
            account (IamAccountRelationship): [optional]  # noqa: E501
            associated_object (MoBaseMoRelationship): [optional]  # noqa: E501
            organization (OrganizationOrganizationRelationship): [optional]  # noqa: E501
            parent_task_info (WorkflowTaskInfoRelationship): [optional]  # noqa: E501
            pending_dynamic_workflow_info (WorkflowPendingDynamicWorkflowInfoRelationship): [optional]  # noqa: E501
            permission (IamPermissionRelationship): [optional]  # noqa: E501
            task_infos ([WorkflowTaskInfoRelationship], none_type): An array of relationships to workflowTaskInfo resources.. [optional]  # noqa: E501
            workflow_definition (WorkflowWorkflowDefinitionRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "workflow.WorkflowInfo")
        object_type = kwargs.get('object_type', "workflow.WorkflowInfo")
        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.class_id = class_id
        self.object_type = object_type
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
