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
    from intersight.model.infra_hardware_info import InfraHardwareInfo
    from intersight.model.virtualization_compute_capacity import VirtualizationComputeCapacity
    from intersight.model.virtualization_guest_info import VirtualizationGuestInfo
    from intersight.model.virtualization_memory_capacity import VirtualizationMemoryCapacity
    globals()['InfraHardwareInfo'] = InfraHardwareInfo
    globals()['VirtualizationComputeCapacity'] = VirtualizationComputeCapacity
    globals()['VirtualizationGuestInfo'] = VirtualizationGuestInfo
    globals()['VirtualizationMemoryCapacity'] = VirtualizationMemoryCapacity


class VirtualizationBaseVirtualMachineAllOf(ModelNormal):
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
            'CLOUD.AWSVIRTUALMACHINE': "cloud.AwsVirtualMachine",
            'VIRTUALIZATION.IWEVIRTUALMACHINE': "virtualization.IweVirtualMachine",
            'VIRTUALIZATION.VMWAREVIRTUALMACHINE': "virtualization.VmwareVirtualMachine",
        },
        ('object_type',): {
            'CLOUD.AWSVIRTUALMACHINE': "cloud.AwsVirtualMachine",
            'VIRTUALIZATION.IWEVIRTUALMACHINE': "virtualization.IweVirtualMachine",
            'VIRTUALIZATION.VMWAREVIRTUALMACHINE': "virtualization.VmwareVirtualMachine",
        },
        ('hypervisor_type',): {
            'ESXI': "ESXi",
            'HYPERFLEXAP': "HyperFlexAp",
            'IWE': "IWE",
            'HYPER-V': "Hyper-V",
            'UNKNOWN': "Unknown",
        },
        ('power_state',): {
            'UNKNOWN': "Unknown",
            'POWERINGON': "PoweringOn",
            'POWEREDON': "PoweredOn",
            'POWERINGOFF': "PoweringOff",
            'POWEREDOFF': "PoweredOff",
            'STANDBY': "StandBy",
            'PAUSED': "Paused",
            'REBOOTING': "Rebooting",
            'EMPTY': "",
        },
        ('provider',): {
            'UNKNOWN': "Unknown",
            'VMWAREVSPHERE': "VMwarevSphere",
            'AMAZONWEBSERVICES': "AmazonWebServices",
            'MICROSOFTAZURE': "MicrosoftAzure",
            'GOOGLECLOUDPLATFORM': "GoogleCloudPlatform",
        },
        ('state',): {
            'NONE': "None",
            'CREATING': "Creating",
            'PENDING': "Pending",
            'STARTING': "Starting",
            'STARTED': "Started",
            'STOPPING': "Stopping",
            'STOPPED': "Stopped",
            'PAUSING': "Pausing",
            'PAUSED': "Paused",
            'SUSPENDING': "Suspending",
            'SUSPENDED': "Suspended",
            'DELETING': "Deleting",
            'TERMINATED': "Terminated",
            'REBOOTING': "Rebooting",
            'ERROR': "Error",
        },
    }

    validations = {
        ('uuid',): {
            'regex': {
                'pattern': r'^$|^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',  # noqa: E501
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
            'boot_time': (datetime,),  # noqa: E501
            'capacity': (InfraHardwareInfo,),  # noqa: E501
            'cpu_utilization': (float,),  # noqa: E501
            'guest_info': (VirtualizationGuestInfo,),  # noqa: E501
            'hypervisor_type': (str,),  # noqa: E501
            'identity': (str,),  # noqa: E501
            'ip_address': ([str], none_type,),  # noqa: E501
            'memory_capacity': (VirtualizationMemoryCapacity,),  # noqa: E501
            'memory_utilization': (float,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'power_state': (str,),  # noqa: E501
            'processor_capacity': (VirtualizationComputeCapacity,),  # noqa: E501
            'provider': (str,),  # noqa: E501
            'state': (str,),  # noqa: E501
            'uuid': (str,),  # noqa: E501
            'vm_creation_time': (datetime,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'boot_time': 'BootTime',  # noqa: E501
        'capacity': 'Capacity',  # noqa: E501
        'cpu_utilization': 'CpuUtilization',  # noqa: E501
        'guest_info': 'GuestInfo',  # noqa: E501
        'hypervisor_type': 'HypervisorType',  # noqa: E501
        'identity': 'Identity',  # noqa: E501
        'ip_address': 'IpAddress',  # noqa: E501
        'memory_capacity': 'MemoryCapacity',  # noqa: E501
        'memory_utilization': 'MemoryUtilization',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'power_state': 'PowerState',  # noqa: E501
        'processor_capacity': 'ProcessorCapacity',  # noqa: E501
        'provider': 'Provider',  # noqa: E501
        'state': 'State',  # noqa: E501
        'uuid': 'Uuid',  # noqa: E501
        'vm_creation_time': 'VmCreationTime',  # noqa: E501
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
    def __init__(self, class_id, object_type, *args, **kwargs):  # noqa: E501
        """VirtualizationBaseVirtualMachineAllOf - a model defined in OpenAPI

        Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data. The enum values provides the list of concrete types that can be instantiated from this abstract type.
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property. The enum values provides the list of concrete types that can be instantiated from this abstract type.

        Keyword Args:
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
            boot_time (datetime): Time when this VM booted up.. [optional]  # noqa: E501
            capacity (InfraHardwareInfo): [optional]  # noqa: E501
            cpu_utilization (float): Average CPU utilization percentage derived as a ratio of CPU used to CPU allocated. The value is calculated whenever inventory is performed.. [optional]  # noqa: E501
            guest_info (VirtualizationGuestInfo): [optional]  # noqa: E501
            hypervisor_type (str): Type of hypervisor where the virtual machine is hosted for example ESXi. * `ESXi` - The hypervisor running on the HyperFlex cluster is a Vmware ESXi hypervisor of any version. * `HyperFlexAp` - The hypervisor of the virtualization platform is Cisco HyperFlex Application Platform. * `IWE` - The hypervisor of the virtualization platform is Cisco Intersight Workload Engine. * `Hyper-V` - The hypervisor running on the HyperFlex cluster is Microsoft Hyper-V. * `Unknown` - The hypervisor running on the HyperFlex cluster is not known.. [optional] if omitted the server will use the default value of "ESXi"  # noqa: E501
            identity (str): The internally generated identity of this VM. This entity is not manipulated by users. It aids in uniquely identifying the virtual machine object. For VMware, this is MOR (managed object reference).. [optional]  # noqa: E501
            ip_address ([str], none_type): [optional]  # noqa: E501
            memory_capacity (VirtualizationMemoryCapacity): [optional]  # noqa: E501
            memory_utilization (float): Average memory utilization percentage derived as a ratio of memory used to available memory. The value is calculated whenever inventory is performed.. [optional]  # noqa: E501
            name (str): User-provided name to identify the virtual machine.. [optional]  # noqa: E501
            power_state (str): Power state of the virtual machine. * `Unknown` - The entity's power state is unknown. * `PoweringOn` - The entity is powering on. * `PoweredOn` - The entity is powered on. * `PoweringOff` - The entity is powering off. * `PoweredOff` - The entity is powered down. * `StandBy` - The entity is in standby mode. * `Paused` - The entity is in pause state. * `Rebooting` - The entity reboot is in progress. * `` - The entity's power state is not available.. [optional] if omitted the server will use the default value of "Unknown"  # noqa: E501
            processor_capacity (VirtualizationComputeCapacity): [optional]  # noqa: E501
            provider (str): Cloud platform, where the virtual machine is launched. * `Unknown` - Cloud provider is not known. * `VMwarevSphere` - Cloud provider named VMware vSphere. * `AmazonWebServices` - Cloud provider named Amazon Web Services. * `MicrosoftAzure` - Cloud provider named Microsoft Azure. * `GoogleCloudPlatform` - Cloud provider named Google Cloud Platform.. [optional] if omitted the server will use the default value of "Unknown"  # noqa: E501
            state (str): The current state of the virtual machine. For example, starting, stopped, etc. * `None` - A place holder for the default value. * `Creating` - Virtual machine creation is in progress. * `Pending` - The virtual machine is preparing to enter the started state. * `Starting` - The virtual machine is starting. * `Started` - The virtual machine is running and ready for use. * `Stopping` - The virtual machine is preparing to be stopped. * `Stopped` - The virtual machine is shut down and cannot be used. The virtual machine can be started again at any time. * `Pausing` - The virtual machine is preparing to be paused. * `Paused` - The virtual machine enters into paused state due to low free disk space. * `Suspending` - The virtual machine is preparing to be suspended. * `Suspended` - Virtual machine is in sleep mode.When a virtual machine is suspended, the current state of theoperating system, and applications is saved, and the virtual machine put into a suspended mode. * `Deleting` - The virtual machine is preparing to be terminated. * `Terminated` - The virtual machine has been permanently deleted and cannot be started. * `Rebooting` - The virtual machine reboot is in progress. * `Error` - The deployment of virtual machine is failed.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            uuid (str): The uuid of this virtual machine. The uuid is internally generated and not user specified.. [optional]  # noqa: E501
            vm_creation_time (datetime): Time when this virtualmachine is created.. [optional]  # noqa: E501
        """

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
