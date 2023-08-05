"""
    Cisco Intersight

    Cisco Intersight is a management platform delivered as a service with embedded analytics for your Cisco and 3rd party IT infrastructure. This platform offers an intelligent level of management that enables IT organizations to analyze, simplify, and automate their environments in more advanced ways than the prior generations of tools. Cisco Intersight provides an integrated and intuitive management experience for resources in the traditional data center as well as at the edge. With flexible deployment options to address complex security needs, getting started with Intersight is quick and easy. Cisco Intersight has deep integration with Cisco UCS and HyperFlex systems allowing for remote deployment, configuration, and ongoing maintenance. The model-based deployment works for a single system in a remote location or hundreds of systems in a data center and enables rapid, standardized configuration and deployment. It also streamlines maintaining those systems whether you are working with small or very large configurations. The Intersight OpenAPI document defines the complete set of properties that are returned in the HTTP response. From that perspective, a client can expect that no additional properties are returned, unless these properties are explicitly defined in the OpenAPI document. However, when a client uses an older version of the Intersight OpenAPI document, the server may send additional properties because the software is more recent than the client. In that case, the client may receive properties that it does not know about. Some generated SDKs perform a strict validation of the HTTP response body against the OpenAPI document.  # noqa: E501

    The version of the OpenAPI document: 1.0.9-4903
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
    from intersight.model.asset_device_registration_relationship import AssetDeviceRegistrationRelationship
    from intersight.model.display_names import DisplayNames
    from intersight.model.hyperflex_alarm_summary import HyperflexAlarmSummary
    from intersight.model.hyperflex_base_cluster import HyperflexBaseCluster
    from intersight.model.hyperflex_base_cluster_relationship import HyperflexBaseClusterRelationship
    from intersight.model.hyperflex_cluster_relationship import HyperflexClusterRelationship
    from intersight.model.hyperflex_hxap_cluster_all_of import HyperflexHxapClusterAllOf
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    from intersight.model.policy_abstract_profile_relationship import PolicyAbstractProfileRelationship
    from intersight.model.virtualization_compute_capacity import VirtualizationComputeCapacity
    from intersight.model.virtualization_cpu_allocation import VirtualizationCpuAllocation
    from intersight.model.virtualization_memory_allocation import VirtualizationMemoryAllocation
    from intersight.model.virtualization_memory_capacity import VirtualizationMemoryCapacity
    globals()['AssetDeviceRegistrationRelationship'] = AssetDeviceRegistrationRelationship
    globals()['DisplayNames'] = DisplayNames
    globals()['HyperflexAlarmSummary'] = HyperflexAlarmSummary
    globals()['HyperflexBaseCluster'] = HyperflexBaseCluster
    globals()['HyperflexBaseClusterRelationship'] = HyperflexBaseClusterRelationship
    globals()['HyperflexClusterRelationship'] = HyperflexClusterRelationship
    globals()['HyperflexHxapClusterAllOf'] = HyperflexHxapClusterAllOf
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext
    globals()['PolicyAbstractProfileRelationship'] = PolicyAbstractProfileRelationship
    globals()['VirtualizationComputeCapacity'] = VirtualizationComputeCapacity
    globals()['VirtualizationCpuAllocation'] = VirtualizationCpuAllocation
    globals()['VirtualizationMemoryAllocation'] = VirtualizationMemoryAllocation
    globals()['VirtualizationMemoryCapacity'] = VirtualizationMemoryCapacity


class HyperflexHxapCluster(ModelComposed):
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
            'HYPERFLEX.HXAPCLUSTER': "hyperflex.HxapCluster",
        },
        ('object_type',): {
            'HYPERFLEX.HXAPCLUSTER': "hyperflex.HxapCluster",
        },
        ('hypervisor_type',): {
            'ESXI': "ESXi",
            'HYPERFLEXAP': "HyperFlexAp",
            'IWE': "IWE",
            'HYPER-V': "Hyper-V",
            'UNKNOWN': "Unknown",
        },
        ('status',): {
            'UNKNOWN': "Unknown",
            'DEGRADED': "Degraded",
            'CRITICAL': "Critical",
            'OK': "Ok",
        },
        ('cluster_purpose',): {
            'STORAGE': "Storage",
            'COMPUTE': "Compute",
            'UNKNOWN': "Unknown",
        },
        ('deployment_type',): {
            'NA': "NA",
            'DATACENTER': "Datacenter",
            'STRETCHED_CLUSTER': "Stretched Cluster",
            'EDGE': "Edge",
        },
        ('drive_type',): {
            'NA': "NA",
            'ALL-FLASH': "All-Flash",
            'HYBRID': "Hybrid",
        },
    }

    validations = {
        ('name',): {
            'regex': {
                'pattern': r'^[a-zA-Z0-9]+[\sa-zA-Z0-9_-]{1,32}$',  # noqa: E501
            },
        },
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
            'configured_cpu_over_sub_factor': (float,),  # noqa: E501
            'cpu_allocation': (VirtualizationCpuAllocation,),  # noqa: E501
            'current_cpu_over_sub_factor': (float,),  # noqa: E501
            'datacenter_name': (str,),  # noqa: E501
            'failure_reason': (str,),  # noqa: E501
            'hypervisor_build': (str,),  # noqa: E501
            'management_ip_address': (str,),  # noqa: E501
            'memory_allocation': (VirtualizationMemoryAllocation,),  # noqa: E501
            'hx_cluster': (HyperflexClusterRelationship,),  # noqa: E501
            'registered_device': (AssetDeviceRegistrationRelationship,),  # noqa: E501
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
            'hypervisor_type': (str,),  # noqa: E501
            'identity': (str,),  # noqa: E501
            'memory_capacity': (VirtualizationMemoryCapacity,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'processor_capacity': (VirtualizationComputeCapacity,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'total_cores': (int,),  # noqa: E501
            'alarm_summary': (HyperflexAlarmSummary,),  # noqa: E501
            'capacity_runway': (int,),  # noqa: E501
            'cluster_name': (str,),  # noqa: E501
            'cluster_purpose': (str,),  # noqa: E501
            'compute_node_count': (int,),  # noqa: E501
            'converged_node_count': (int,),  # noqa: E501
            'deployment_type': (str,),  # noqa: E501
            'drive_type': (str,),  # noqa: E501
            'hx_version': (str,),  # noqa: E501
            'hypervisor_version': (str,),  # noqa: E501
            'storage_capacity': (int,),  # noqa: E501
            'storage_node_count': (int,),  # noqa: E501
            'storage_utilization': (float,),  # noqa: E501
            'utilization_percentage': (float,),  # noqa: E501
            'utilization_trend_percentage': (float,),  # noqa: E501
            'associated_profile': (PolicyAbstractProfileRelationship,),  # noqa: E501
            'child_clusters': ([HyperflexBaseClusterRelationship], none_type,),  # noqa: E501
            'parent_cluster': (HyperflexBaseClusterRelationship,),  # noqa: E501
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
        'configured_cpu_over_sub_factor': 'ConfiguredCpuOverSubFactor',  # noqa: E501
        'cpu_allocation': 'CpuAllocation',  # noqa: E501
        'current_cpu_over_sub_factor': 'CurrentCpuOverSubFactor',  # noqa: E501
        'datacenter_name': 'DatacenterName',  # noqa: E501
        'failure_reason': 'FailureReason',  # noqa: E501
        'hypervisor_build': 'HypervisorBuild',  # noqa: E501
        'management_ip_address': 'ManagementIpAddress',  # noqa: E501
        'memory_allocation': 'MemoryAllocation',  # noqa: E501
        'hx_cluster': 'HxCluster',  # noqa: E501
        'registered_device': 'RegisteredDevice',  # noqa: E501
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
        'hypervisor_type': 'HypervisorType',  # noqa: E501
        'identity': 'Identity',  # noqa: E501
        'memory_capacity': 'MemoryCapacity',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'processor_capacity': 'ProcessorCapacity',  # noqa: E501
        'status': 'Status',  # noqa: E501
        'total_cores': 'TotalCores',  # noqa: E501
        'alarm_summary': 'AlarmSummary',  # noqa: E501
        'capacity_runway': 'CapacityRunway',  # noqa: E501
        'cluster_name': 'ClusterName',  # noqa: E501
        'cluster_purpose': 'ClusterPurpose',  # noqa: E501
        'compute_node_count': 'ComputeNodeCount',  # noqa: E501
        'converged_node_count': 'ConvergedNodeCount',  # noqa: E501
        'deployment_type': 'DeploymentType',  # noqa: E501
        'drive_type': 'DriveType',  # noqa: E501
        'hx_version': 'HxVersion',  # noqa: E501
        'hypervisor_version': 'HypervisorVersion',  # noqa: E501
        'storage_capacity': 'StorageCapacity',  # noqa: E501
        'storage_node_count': 'StorageNodeCount',  # noqa: E501
        'storage_utilization': 'StorageUtilization',  # noqa: E501
        'utilization_percentage': 'UtilizationPercentage',  # noqa: E501
        'utilization_trend_percentage': 'UtilizationTrendPercentage',  # noqa: E501
        'associated_profile': 'AssociatedProfile',  # noqa: E501
        'child_clusters': 'ChildClusters',  # noqa: E501
        'parent_cluster': 'ParentCluster',  # noqa: E501
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
        """HyperflexHxapCluster - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "hyperflex.HxapCluster", must be one of ["hyperflex.HxapCluster", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "hyperflex.HxapCluster", must be one of ["hyperflex.HxapCluster", ]  # noqa: E501
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
            configured_cpu_over_sub_factor (float): CPU oversubscription factor configured on the cluster.. [optional]  # noqa: E501
            cpu_allocation (VirtualizationCpuAllocation): [optional]  # noqa: E501
            current_cpu_over_sub_factor (float): Current oversubscription factor of the cluster.. [optional]  # noqa: E501
            datacenter_name (str): Datacenter to which the cluster belongs.. [optional]  # noqa: E501
            failure_reason (str): Reason for the failure when cluster is in failed state.. [optional]  # noqa: E501
            hypervisor_build (str): Hypervisor version of HyperFlex compute cluster along with build number.. [optional]  # noqa: E501
            management_ip_address (str): Management IP Address of the cluster.. [optional]  # noqa: E501
            memory_allocation (VirtualizationMemoryAllocation): [optional]  # noqa: E501
            hx_cluster (HyperflexClusterRelationship): [optional]  # noqa: E501
            registered_device (AssetDeviceRegistrationRelationship): [optional]  # noqa: E501
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
            hypervisor_type (str): Identifies the broad type of the underlying hypervisor. * `ESXi` - The hypervisor running on the HyperFlex cluster is a Vmware ESXi hypervisor of any version. * `HyperFlexAp` - The hypervisor of the virtualization platform is Cisco HyperFlex Application Platform. * `IWE` - The hypervisor of the virtualization platform is Cisco Intersight Workload Engine. * `Hyper-V` - The hypervisor running on the HyperFlex cluster is Microsoft Hyper-V. * `Unknown` - The hypervisor running on the HyperFlex cluster is not known.. [optional] if omitted the server will use the default value of "ESXi"  # noqa: E501
            identity (str): The internally generated identity of this cluster. This entity is not manipulated by users. It aids in uniquely identifying the cluster object. In case of VMware, this is a MOR (managed object reference).. [optional]  # noqa: E501
            memory_capacity (VirtualizationMemoryCapacity): [optional]  # noqa: E501
            name (str): The user-provided name for this cluster to facilitate identification.. [optional]  # noqa: E501
            processor_capacity (VirtualizationComputeCapacity): [optional]  # noqa: E501
            status (str): Cluster health status as reported by the hypervisor platform. * `Unknown` - Entity status is unknown. * `Degraded` - State is degraded, and might impact normal operation of the entity. * `Critical` - Entity is in a critical state, impacting operations. * `Ok` - Entity status is in a stable state, operating normally.. [optional] if omitted the server will use the default value of "Unknown"  # noqa: E501
            total_cores (int): Total number of CPU cores in this cluster. It is a cumulative number across all hosts in the cluster.. [optional]  # noqa: E501
            alarm_summary (HyperflexAlarmSummary): [optional]  # noqa: E501
            capacity_runway (int): The number of days remaining before the cluster's storage utilization reaches the recommended capacity limit of 76%. Default value is math.MaxInt32 to indicate that the capacity runway is \"Unknown\" for a cluster that is not connected or with not sufficient data.. [optional] if omitted the server will use the default value of 2147483647  # noqa: E501
            cluster_name (str): The name of this HyperFlex cluster.. [optional]  # noqa: E501
            cluster_purpose (str): This can be a Storage or Compute cluster. A storage cluster contains storage nodes that are used to persist data. A compute cluster contains compute nodes that are used for executing business logic. * `Storage` - Cluster of storage nodes used to persist data. * `Compute` - Cluster of compute nodes used to execute business logic. * `Unknown` - This cluster type is Unknown. Expect Compute or Storage as valid values.. [optional] if omitted the server will use the default value of "Storage"  # noqa: E501
            compute_node_count (int): The number of compute nodes that belong to this cluster.. [optional]  # noqa: E501
            converged_node_count (int): The number of converged nodes that belong to this cluster.. [optional]  # noqa: E501
            deployment_type (str): The deployment type of the HyperFlex cluster. The cluster can have one of the following configurations: 1. Datacenter: The HyperFlex cluster consists of UCS Fabric Interconnect-attached nodes on a single site. 2. Stretched Cluster: The HyperFlex cluster consists of UCS Fabric Interconnect-attached nodes distributed across multiple sites. 3. Edge: The HyperFlex cluster consists of 2-4 standalone nodes. If the cluster is running a HyperFlex Data Platform version less than 4.0 or if the deployment type cannot be determined, the deployment type is set as 'NA' (not available). * `NA` - The deployment type of the HyperFlex cluster is not available. * `Datacenter` - The deployment type of a HyperFlex cluster consisting of UCS Fabric Interconnect-attached nodes on the same site. * `Stretched Cluster` - The deployment type of a HyperFlex cluster consisting of UCS Fabric Interconnect-attached nodes across different sites. * `Edge` - The deployment type of a HyperFlex cluster consisting of 2 or more standalone nodes.. [optional] if omitted the server will use the default value of "NA"  # noqa: E501
            drive_type (str): The type of the drives used for storage in this cluster. * `NA` - The drive type of the HyperFlex cluster is not available. * `All-Flash` - Indicates that this HyperFlex cluster contains flash drives only. * `Hybrid` - Indicates that this HyperFlex cluster contains both flash and hard disk drives.. [optional] if omitted the server will use the default value of "NA"  # noqa: E501
            hx_version (str): The HyperFlex Data or Application Platform version of this cluster.. [optional]  # noqa: E501
            hypervisor_version (str): The version of hypervisor running on this cluster.. [optional]  # noqa: E501
            storage_capacity (int): The storage capacity in this cluster.. [optional]  # noqa: E501
            storage_node_count (int): The number of storage nodes that belong to this cluster.. [optional]  # noqa: E501
            storage_utilization (float): The storage utilization is computed based on total capacity and current capacity utilization.. [optional]  # noqa: E501
            utilization_percentage (float): The storage utilization percentage is computed based on total capacity and current capacity utilization.. [optional]  # noqa: E501
            utilization_trend_percentage (float): The storage utilization trend percentage represents the trend in percentage computed using the first and last point from historical data.. [optional]  # noqa: E501
            associated_profile (PolicyAbstractProfileRelationship): [optional]  # noqa: E501
            child_clusters ([HyperflexBaseClusterRelationship], none_type): An array of relationships to hyperflexBaseCluster resources.. [optional]  # noqa: E501
            parent_cluster (HyperflexBaseClusterRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "hyperflex.HxapCluster")
        object_type = kwargs.get('object_type', "hyperflex.HxapCluster")
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
              HyperflexBaseCluster,
              HyperflexHxapClusterAllOf,
          ],
          'oneOf': [
          ],
        }
