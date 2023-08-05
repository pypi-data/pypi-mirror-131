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
    from intersight.model.asset_device_registration_relationship import AssetDeviceRegistrationRelationship
    from intersight.model.infra_meta_data import InfraMetaData
    from intersight.model.virtualization_action_info import VirtualizationActionInfo
    from intersight.model.virtualization_base_cluster_relationship import VirtualizationBaseClusterRelationship
    from intersight.model.virtualization_base_host_relationship import VirtualizationBaseHostRelationship
    from intersight.model.virtualization_base_virtual_machine_relationship import VirtualizationBaseVirtualMachineRelationship
    from intersight.model.virtualization_base_vm_configuration import VirtualizationBaseVmConfiguration
    from intersight.model.virtualization_cloud_init_config import VirtualizationCloudInitConfig
    from intersight.model.virtualization_network_interface import VirtualizationNetworkInterface
    from intersight.model.virtualization_virtual_machine_disk import VirtualizationVirtualMachineDisk
    from intersight.model.workflow_workflow_info_relationship import WorkflowWorkflowInfoRelationship
    globals()['AssetDeviceRegistrationRelationship'] = AssetDeviceRegistrationRelationship
    globals()['InfraMetaData'] = InfraMetaData
    globals()['VirtualizationActionInfo'] = VirtualizationActionInfo
    globals()['VirtualizationBaseClusterRelationship'] = VirtualizationBaseClusterRelationship
    globals()['VirtualizationBaseHostRelationship'] = VirtualizationBaseHostRelationship
    globals()['VirtualizationBaseVirtualMachineRelationship'] = VirtualizationBaseVirtualMachineRelationship
    globals()['VirtualizationBaseVmConfiguration'] = VirtualizationBaseVmConfiguration
    globals()['VirtualizationCloudInitConfig'] = VirtualizationCloudInitConfig
    globals()['VirtualizationNetworkInterface'] = VirtualizationNetworkInterface
    globals()['VirtualizationVirtualMachineDisk'] = VirtualizationVirtualMachineDisk
    globals()['WorkflowWorkflowInfoRelationship'] = WorkflowWorkflowInfoRelationship


class VirtualizationVirtualMachineAllOf(ModelNormal):
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
            'VIRTUALIZATION.VIRTUALMACHINE': "virtualization.VirtualMachine",
        },
        ('object_type',): {
            'VIRTUALIZATION.VIRTUALMACHINE': "virtualization.VirtualMachine",
        },
        ('action',): {
            'NONE': "None",
            'POWERSTATE': "PowerState",
            'MIGRATE': "Migrate",
            'CREATE': "Create",
            'DELETE': "Delete",
        },
        ('guest_os',): {
            'LINUX': "linux",
            'WINDOWS': "windows",
        },
        ('hypervisor_type',): {
            'ESXI': "ESXi",
            'HYPERFLEXAP': "HyperFlexAp",
            'IWE': "IWE",
            'HYPER-V': "Hyper-V",
            'UNKNOWN': "Unknown",
        },
        ('power_state',): {
            'POWEROFF': "PowerOff",
            'POWERON': "PowerOn",
            'SUSPEND': "Suspend",
            'SHUTDOWNGUESTOS': "ShutDownGuestOS",
            'RESTARTGUESTOS': "RestartGuestOS",
            'RESET': "Reset",
            'RESTART': "Restart",
            'UNKNOWN': "Unknown",
        },
        ('provision_type',): {
            'OVA': "OVA",
            'TEMPLATE': "Template",
            'DISCOVERED': "Discovered",
        },
    }

    validations = {
        ('cpu',): {
            'inclusive_maximum': 40,
            'inclusive_minimum': 1,
        },
        ('memory',): {
            'inclusive_maximum': 4177920,
            'inclusive_minimum': 1,
        },
        ('name',): {
            'max_length': 128,
            'min_length': 1,
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
            'action_info': (VirtualizationActionInfo,),  # noqa: E501
            'affinity_selectors': ([InfraMetaData], none_type,),  # noqa: E501
            'anti_affinity_selectors': ([InfraMetaData], none_type,),  # noqa: E501
            'cloud_init_config': (VirtualizationCloudInitConfig,),  # noqa: E501
            'cluster_esxi': (str,),  # noqa: E501
            'cpu': (int,),  # noqa: E501
            'discovered': (bool,),  # noqa: E501
            'disk': ([VirtualizationVirtualMachineDisk], none_type,),  # noqa: E501
            'force_delete': (bool,),  # noqa: E501
            'guest_os': (str,),  # noqa: E501
            'host_esxi': (str,),  # noqa: E501
            'hypervisor_type': (str,),  # noqa: E501
            'interfaces': ([VirtualizationNetworkInterface], none_type,),  # noqa: E501
            'labels': ([InfraMetaData], none_type,),  # noqa: E501
            'memory': (int,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'power_state': (str,),  # noqa: E501
            'provision_type': (str,),  # noqa: E501
            'vm_config': (VirtualizationBaseVmConfiguration,),  # noqa: E501
            'cluster': (VirtualizationBaseClusterRelationship,),  # noqa: E501
            'host': (VirtualizationBaseHostRelationship,),  # noqa: E501
            'inventory': (VirtualizationBaseVirtualMachineRelationship,),  # noqa: E501
            'registered_device': (AssetDeviceRegistrationRelationship,),  # noqa: E501
            'workflow_info': (WorkflowWorkflowInfoRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'action': 'Action',  # noqa: E501
        'action_info': 'ActionInfo',  # noqa: E501
        'affinity_selectors': 'AffinitySelectors',  # noqa: E501
        'anti_affinity_selectors': 'AntiAffinitySelectors',  # noqa: E501
        'cloud_init_config': 'CloudInitConfig',  # noqa: E501
        'cluster_esxi': 'ClusterEsxi',  # noqa: E501
        'cpu': 'Cpu',  # noqa: E501
        'discovered': 'Discovered',  # noqa: E501
        'disk': 'Disk',  # noqa: E501
        'force_delete': 'ForceDelete',  # noqa: E501
        'guest_os': 'GuestOs',  # noqa: E501
        'host_esxi': 'HostEsxi',  # noqa: E501
        'hypervisor_type': 'HypervisorType',  # noqa: E501
        'interfaces': 'Interfaces',  # noqa: E501
        'labels': 'Labels',  # noqa: E501
        'memory': 'Memory',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'power_state': 'PowerState',  # noqa: E501
        'provision_type': 'ProvisionType',  # noqa: E501
        'vm_config': 'VmConfig',  # noqa: E501
        'cluster': 'Cluster',  # noqa: E501
        'host': 'Host',  # noqa: E501
        'inventory': 'Inventory',  # noqa: E501
        'registered_device': 'RegisteredDevice',  # noqa: E501
        'workflow_info': 'WorkflowInfo',  # noqa: E501
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
        """VirtualizationVirtualMachineAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "virtualization.VirtualMachine", must be one of ["virtualization.VirtualMachine", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "virtualization.VirtualMachine", must be one of ["virtualization.VirtualMachine", ]  # noqa: E501
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
            action (str): Action to be performed on a virtual machine (Create, PowerState, Migrate, Clone etc). * `None` - A place holder for the default value. * `PowerState` - Power action is performed on the virtual machine. * `Migrate` - The virtual machine will be migrated from existing node to a different node in cluster. The behavior depends on the underlying hypervisor. * `Create` - The virtual machine will be created on the specified hypervisor. This action is also useful if the virtual machine creation failed during first POST operation on VirtualMachine managed object. User can set this action to retry the virtual machine creation. * `Delete` - The virtual machine will be deleted from the specified hypervisor. User can either set this action or can do a DELETE operation on the VirtualMachine managed object.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            action_info (VirtualizationActionInfo): [optional]  # noqa: E501
            affinity_selectors ([InfraMetaData], none_type): [optional]  # noqa: E501
            anti_affinity_selectors ([InfraMetaData], none_type): [optional]  # noqa: E501
            cloud_init_config (VirtualizationCloudInitConfig): [optional]  # noqa: E501
            cluster_esxi (str): Cluster where virtual machine is deployed.. [optional]  # noqa: E501
            cpu (int): Number of vCPUs allocated to virtual machine.. [optional]  # noqa: E501
            discovered (bool): Flag to indicate whether the configuration is created from inventory object.. [optional]  # noqa: E501
            disk ([VirtualizationVirtualMachineDisk], none_type): [optional]  # noqa: E501
            force_delete (bool): Normally any virtual machine that is still powered on cannot be deleted. The expected sequence from a user is to first power off the virtual machine and then invoke the delete operation. However, in special circumstances, the owner of the virtual machine may know very well that the virtual machine is no longer needed and just wants to dispose it off. In such situations a delete operation of a virtual machine object is accepted only when this forceDelete attribute is set to true. Under normal circumstances (forceDelete is false), delete operation first confirms that the virtual machine is powered off and then proceeds to delete the virtual machine.. [optional]  # noqa: E501
            guest_os (str): Guest operating system running on virtual machine. * `linux` - A Linux operating system. * `windows` - A Windows operating system.. [optional] if omitted the server will use the default value of "linux"  # noqa: E501
            host_esxi (str): Host where virtual machine is deployed.. [optional]  # noqa: E501
            hypervisor_type (str): Identifies the broad product type of the hypervisor but without any version information. It is here to easily identify the type of the virtual machine. There are other entities (Host, Cluster, etc.) that can be indirectly used to determine the hypervisor but a direct attribute makes it easier to work with. * `ESXi` - The hypervisor running on the HyperFlex cluster is a Vmware ESXi hypervisor of any version. * `HyperFlexAp` - The hypervisor of the virtualization platform is Cisco HyperFlex Application Platform. * `IWE` - The hypervisor of the virtualization platform is Cisco Intersight Workload Engine. * `Hyper-V` - The hypervisor running on the HyperFlex cluster is Microsoft Hyper-V. * `Unknown` - The hypervisor running on the HyperFlex cluster is not known.. [optional] if omitted the server will use the default value of "ESXi"  # noqa: E501
            interfaces ([VirtualizationNetworkInterface], none_type): [optional]  # noqa: E501
            labels ([InfraMetaData], none_type): [optional]  # noqa: E501
            memory (int): Virtual machine memory in mebi bytes (one mebibyte, 1MiB, is 1048576 bytes, and 1KiB is 1024 bytes). Input must be a whole number and scientific notation is not acceptable. For example, enter 1730 and not 1.73e03.. [optional]  # noqa: E501
            name (str): Virtual machine name that is unique. Hypervisors enforce platform specific limits and character sets. The name length limit, both min and max, vary among hypervisors. Therefore, the basic limits are set here and proper enforcement is done elsewhere.. [optional]  # noqa: E501
            power_state (str): Expected power state of virtual machine (PowerOn, PowerOff, Restart). * `PowerOff` - The virtual machine will be powered off if it is already not in powered off state. If it is already powered off, no side-effects are expected. * `PowerOn` - The virtual machine will be powered on if it is already not in powered on state. If it is already powered on, no side-effects are expected. * `Suspend` - The virtual machine will be put into  a suspended state. * `ShutDownGuestOS` - The guest operating system is shut down gracefully. * `RestartGuestOS` - It can either act as a reset switch and abruptly reset the guest operating system, or it can send a restart signal to the guest operating system so that it shuts down gracefully and restarts. * `Reset` - Resets the virtual machine abruptly, with no consideration for work in progress. * `Restart` - The virtual machine will be restarted only if it is in powered on state. If it is powered off, it will not be started up. * `Unknown` - Power state of the entity is unknown.. [optional] if omitted the server will use the default value of "PowerOff"  # noqa: E501
            provision_type (str): Identifies the provision type to create a new virtual machine. * `OVA` - Deploy virtual machine using OVA/F file. * `Template` - Provision virtual machine using a template file. * `Discovered` - A virtual machine was 'discovered' and not created from Intersight. No provisioning information is available.. [optional] if omitted the server will use the default value of "OVA"  # noqa: E501
            vm_config (VirtualizationBaseVmConfiguration): [optional]  # noqa: E501
            cluster (VirtualizationBaseClusterRelationship): [optional]  # noqa: E501
            host (VirtualizationBaseHostRelationship): [optional]  # noqa: E501
            inventory (VirtualizationBaseVirtualMachineRelationship): [optional]  # noqa: E501
            registered_device (AssetDeviceRegistrationRelationship): [optional]  # noqa: E501
            workflow_info (WorkflowWorkflowInfoRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "virtualization.VirtualMachine")
        object_type = kwargs.get('object_type', "virtualization.VirtualMachine")
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
