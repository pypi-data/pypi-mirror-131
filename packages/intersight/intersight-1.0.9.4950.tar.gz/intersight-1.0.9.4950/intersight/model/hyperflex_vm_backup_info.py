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
    from intersight.model.display_names import DisplayNames
    from intersight.model.hyperflex_backup_cluster_relationship import HyperflexBackupClusterRelationship
    from intersight.model.hyperflex_cluster_relationship import HyperflexClusterRelationship
    from intersight.model.hyperflex_entity_reference import HyperflexEntityReference
    from intersight.model.hyperflex_error_stack import HyperflexErrorStack
    from intersight.model.hyperflex_map_cluster_id_to_protection_info import HyperflexMapClusterIdToProtectionInfo
    from intersight.model.hyperflex_replication_cluster_reference_to_schedule import HyperflexReplicationClusterReferenceToSchedule
    from intersight.model.hyperflex_virtual_machine import HyperflexVirtualMachine
    from intersight.model.hyperflex_vm_backup_info_all_of import HyperflexVmBackupInfoAllOf
    from intersight.model.mo_base_mo import MoBaseMo
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    globals()['DisplayNames'] = DisplayNames
    globals()['HyperflexBackupClusterRelationship'] = HyperflexBackupClusterRelationship
    globals()['HyperflexClusterRelationship'] = HyperflexClusterRelationship
    globals()['HyperflexEntityReference'] = HyperflexEntityReference
    globals()['HyperflexErrorStack'] = HyperflexErrorStack
    globals()['HyperflexMapClusterIdToProtectionInfo'] = HyperflexMapClusterIdToProtectionInfo
    globals()['HyperflexReplicationClusterReferenceToSchedule'] = HyperflexReplicationClusterReferenceToSchedule
    globals()['HyperflexVirtualMachine'] = HyperflexVirtualMachine
    globals()['HyperflexVmBackupInfoAllOf'] = HyperflexVmBackupInfoAllOf
    globals()['MoBaseMo'] = MoBaseMo
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext


class HyperflexVmBackupInfo(ModelComposed):
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
            'HYPERFLEX.VMBACKUPINFO': "hyperflex.VmBackupInfo",
        },
        ('object_type',): {
            'HYPERFLEX.VMBACKUPINFO': "hyperflex.VmBackupInfo",
        },
        ('backup_status',): {
            'INITIALIZINGPROTECTION': "InitializingProtection",
            'PROTECTED': "Protected",
            'EXCEEDSINTERVAL': "ExceedsInterval",
        },
        ('protection_status',): {
            'PREPARE_FAILOVER_STARTED': "PREPARE_FAILOVER_STARTED",
            'PREPARE_FAILOVER_FAILED': "PREPARE_FAILOVER_FAILED",
            'PREPARE_FAILOVER_COMPLETED': "PREPARE_FAILOVER_COMPLETED",
            'FAILOVER_STARTED': "FAILOVER_STARTED",
            'FAILOVER_FAILED': "FAILOVER_FAILED",
            'FAILOVER_COMPLETED': "FAILOVER_COMPLETED",
            'PREPARE_REVERSEPROTECT_STARTED': "PREPARE_REVERSEPROTECT_STARTED",
            'PREPARE_REVERSEPROTECT_FAILED': "PREPARE_REVERSEPROTECT_FAILED",
            'PREPARE_REVERSEPROTECT_COMPLETED': "PREPARE_REVERSEPROTECT_COMPLETED",
            'REVERSEPROTECT_STARTED': "REVERSEPROTECT_STARTED",
            'REVERSEPROTECT_FAILED': "REVERSEPROTECT_FAILED",
            'ACTIVE': "ACTIVE",
            'CREATION_IN_PROGRESS': "CREATION_IN_PROGRESS",
            'CREATION_FAILED': "CREATION_FAILED",
            'LOCAL_RESTORE_STARTED': "LOCAL_RESTORE_STARTED",
            'LOCAL_RESTORE_FAILED': "LOCAL_RESTORE_FAILED",
        },
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

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
            'backup_status': (str,),  # noqa: E501
            'cluster_entity_reference': (HyperflexEntityReference,),  # noqa: E501
            'cluster_id_protection_info_map': ([HyperflexMapClusterIdToProtectionInfo], none_type,),  # noqa: E501
            'error': (HyperflexErrorStack,),  # noqa: E501
            'local_snapshot_retention_count': (int,),  # noqa: E501
            'power_on': (bool,),  # noqa: E501
            'protection_status': (str,),  # noqa: E501
            'schedule': ([HyperflexReplicationClusterReferenceToSchedule], none_type,),  # noqa: E501
            'snapshot_retention_count': (int,),  # noqa: E501
            'src_cluster_name': (str,),  # noqa: E501
            'tgt_cluster_name': (str,),  # noqa: E501
            'vm_entity_reference': (HyperflexEntityReference,),  # noqa: E501
            'vm_info': (HyperflexVirtualMachine,),  # noqa: E501
            'src_backup_cluster': (HyperflexBackupClusterRelationship,),  # noqa: E501
            'src_cluster': (HyperflexClusterRelationship,),  # noqa: E501
            'tgt_cluster': (HyperflexClusterRelationship,),  # noqa: E501
            'account_moid': (str,),  # noqa: E501
            'create_time': (datetime,),  # noqa: E501
            'domain_group_moid': (str,),  # noqa: E501
            'mod_time': (datetime,),  # noqa: E501
            'moid': (str,),  # noqa: E501
            'owners': ([str], none_type,),  # noqa: E501
            'shared_scope': (str,),  # noqa: E501
            'tags': ([MoTag], none_type,),  # noqa: E501
            'version_context': (MoVersionContext,),  # noqa: E501
            'ancestors': ([MoBaseMoRelationship], none_type,),  # noqa: E501
            'parent': (MoBaseMoRelationship,),  # noqa: E501
            'permission_resources': ([MoBaseMoRelationship], none_type,),  # noqa: E501
            'display_names': (DisplayNames,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        val = {
        }
        if not val:
            return None
        return {'class_id': val}

    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'backup_status': 'BackupStatus',  # noqa: E501
        'cluster_entity_reference': 'ClusterEntityReference',  # noqa: E501
        'cluster_id_protection_info_map': 'ClusterIdProtectionInfoMap',  # noqa: E501
        'error': 'Error',  # noqa: E501
        'local_snapshot_retention_count': 'LocalSnapshotRetentionCount',  # noqa: E501
        'power_on': 'PowerOn',  # noqa: E501
        'protection_status': 'ProtectionStatus',  # noqa: E501
        'schedule': 'Schedule',  # noqa: E501
        'snapshot_retention_count': 'SnapshotRetentionCount',  # noqa: E501
        'src_cluster_name': 'SrcClusterName',  # noqa: E501
        'tgt_cluster_name': 'TgtClusterName',  # noqa: E501
        'vm_entity_reference': 'VmEntityReference',  # noqa: E501
        'vm_info': 'VmInfo',  # noqa: E501
        'src_backup_cluster': 'SrcBackupCluster',  # noqa: E501
        'src_cluster': 'SrcCluster',  # noqa: E501
        'tgt_cluster': 'TgtCluster',  # noqa: E501
        'account_moid': 'AccountMoid',  # noqa: E501
        'create_time': 'CreateTime',  # noqa: E501
        'domain_group_moid': 'DomainGroupMoid',  # noqa: E501
        'mod_time': 'ModTime',  # noqa: E501
        'moid': 'Moid',  # noqa: E501
        'owners': 'Owners',  # noqa: E501
        'shared_scope': 'SharedScope',  # noqa: E501
        'tags': 'Tags',  # noqa: E501
        'version_context': 'VersionContext',  # noqa: E501
        'ancestors': 'Ancestors',  # noqa: E501
        'parent': 'Parent',  # noqa: E501
        'permission_resources': 'PermissionResources',  # noqa: E501
        'display_names': 'DisplayNames',  # noqa: E501
    }

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
        '_composed_instances',
        '_var_name_to_model_instances',
        '_additional_properties_model_instances',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """HyperflexVmBackupInfo - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "hyperflex.VmBackupInfo", must be one of ["hyperflex.VmBackupInfo", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "hyperflex.VmBackupInfo", must be one of ["hyperflex.VmBackupInfo", ]  # noqa: E501
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
            backup_status (str): Description of the backup status of this VmBackupInfo. * `InitializingProtection` - Protection has started, but not completed. * `Protected` - Protection has completed successfully. * `ExceedsInterval` - Protection has not completed successfully in over two times the backup interval.. [optional] if omitted the server will use the default value of "InitializingProtection"  # noqa: E501
            cluster_entity_reference (HyperflexEntityReference): [optional]  # noqa: E501
            cluster_id_protection_info_map ([HyperflexMapClusterIdToProtectionInfo], none_type): [optional]  # noqa: E501
            error (HyperflexErrorStack): [optional]  # noqa: E501
            local_snapshot_retention_count (int): Retention count from backup policy for local snapshots.. [optional]  # noqa: E501
            power_on (bool): The power state of the Virtual Machine.. [optional]  # noqa: E501
            protection_status (str): Description of the protection status of this VmBackupInfo. * `PREPARE_FAILOVER_STARTED` - The protection status is prepare failover started. * `PREPARE_FAILOVER_FAILED` - The protection status is prepare failover failed. * `PREPARE_FAILOVER_COMPLETED` - The protection status is prepaire failover completed. * `FAILOVER_STARTED` - The protection status is failover started. * `FAILOVER_FAILED` - The protection status is failover failed. * `FAILOVER_COMPLETED` - The protection status is failover completed. * `PREPARE_REVERSEPROTECT_STARTED` - The protection status is prepare reverse protect started. * `PREPARE_REVERSEPROTECT_FAILED` - The protection status is prepare reverse protect failed. * `PREPARE_REVERSEPROTECT_COMPLETED` - The protection status is prepair reverse protect completed. * `REVERSEPROTECT_STARTED` - The protection status is reverse protect started. * `REVERSEPROTECT_FAILED` - The protection status is reverse protect failed. * `ACTIVE` - The protection status is active. * `CREATION_IN_PROGRESS` - The protection status is failover in progress. * `CREATION_FAILED` - The protection status is creation failed. * `LOCAL_RESTORE_STARTED` - The protection status is local restore started. * `LOCAL_RESTORE_FAILED` - The protection status is local restore failed.. [optional] if omitted the server will use the default value of "PREPARE_FAILOVER_STARTED"  # noqa: E501
            schedule ([HyperflexReplicationClusterReferenceToSchedule], none_type): [optional]  # noqa: E501
            snapshot_retention_count (int): Retention count from backup policy for remote snapshots.. [optional]  # noqa: E501
            src_cluster_name (str): Name for the source cluster this Virtual Machine is residing on.. [optional]  # noqa: E501
            tgt_cluster_name (str): Name for the target cluster this Virtual Machine is residing on.. [optional]  # noqa: E501
            vm_entity_reference (HyperflexEntityReference): [optional]  # noqa: E501
            vm_info (HyperflexVirtualMachine): [optional]  # noqa: E501
            src_backup_cluster (HyperflexBackupClusterRelationship): [optional]  # noqa: E501
            src_cluster (HyperflexClusterRelationship): [optional]  # noqa: E501
            tgt_cluster (HyperflexClusterRelationship): [optional]  # noqa: E501
            account_moid (str): The Account ID for this managed object.. [optional]  # noqa: E501
            create_time (datetime): The time when this managed object was created.. [optional]  # noqa: E501
            domain_group_moid (str): The DomainGroup ID for this managed object.. [optional]  # noqa: E501
            mod_time (datetime): The time when this managed object was last modified.. [optional]  # noqa: E501
            moid (str): The unique identifier of this Managed Object instance.. [optional]  # noqa: E501
            owners ([str], none_type): [optional]  # noqa: E501
            shared_scope (str): Intersight provides pre-built workflows, tasks and policies to end users through global catalogs. Objects that are made available through global catalogs are said to have a 'shared' ownership. Shared objects are either made globally available to all end users or restricted to end users based on their license entitlement. Users can use this property to differentiate the scope (global or a specific license tier) to which a shared MO belongs.. [optional]  # noqa: E501
            tags ([MoTag], none_type): [optional]  # noqa: E501
            version_context (MoVersionContext): [optional]  # noqa: E501
            ancestors ([MoBaseMoRelationship], none_type): An array of relationships to moBaseMo resources.. [optional]  # noqa: E501
            parent (MoBaseMoRelationship): [optional]  # noqa: E501
            permission_resources ([MoBaseMoRelationship], none_type): An array of relationships to moBaseMo resources.. [optional]  # noqa: E501
            display_names (DisplayNames): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "hyperflex.VmBackupInfo")
        object_type = kwargs.get('object_type', "hyperflex.VmBackupInfo")
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        required_args = {
            'class_id': class_id,
            'object_type': object_type,
        }
        model_args = {}
        model_args.update(required_args)
        model_args.update(kwargs)
        composed_info = validate_get_composed_info(
            constant_args, model_args, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        unused_args = composed_info[3]

        for var_name, var_value in required_args.items():
            setattr(self, var_name, var_value)
        for var_name, var_value in kwargs.items():
            if var_name in unused_args and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        not self._additional_properties_model_instances:
                # discard variable.
                continue
            setattr(self, var_name, var_value)

    @cached_property
    def _composed_schemas():
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error beause the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        lazy_import()
        return {
          'anyOf': [
          ],
          'allOf': [
              HyperflexVmBackupInfoAllOf,
              MoBaseMo,
          ],
          'oneOf': [
          ],
        }
