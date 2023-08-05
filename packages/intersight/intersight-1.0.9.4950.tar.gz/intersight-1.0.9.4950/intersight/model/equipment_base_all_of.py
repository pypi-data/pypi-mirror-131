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
    from intersight.model.equipment_fru_relationship import EquipmentFruRelationship
    globals()['EquipmentFruRelationship'] = EquipmentFruRelationship


class EquipmentBaseAllOf(ModelNormal):
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
            'ADAPTER.HOSTFCINTERFACE': "adapter.HostFcInterface",
            'ADAPTER.HOSTISCSIINTERFACE': "adapter.HostIscsiInterface",
            'ADAPTER.UNIT': "adapter.Unit",
            'ADAPTER.UNITEXPANDER': "adapter.UnitExpander",
            'BIOS.UNIT': "bios.Unit",
            'BOOT.CDDDEVICE': "boot.CddDevice",
            'BOOT.HDDDEVICE': "boot.HddDevice",
            'BOOT.ISCSIDEVICE': "boot.IscsiDevice",
            'BOOT.NVMEDEVICE': "boot.NvmeDevice",
            'BOOT.PCHSTORAGEDEVICE': "boot.PchStorageDevice",
            'BOOT.PXEDEVICE': "boot.PxeDevice",
            'BOOT.SANDEVICE': "boot.SanDevice",
            'BOOT.SDDEVICE': "boot.SdDevice",
            'BOOT.UEFISHELLDEVICE': "boot.UefiShellDevice",
            'BOOT.USBDEVICE': "boot.UsbDevice",
            'BOOT.VMEDIADEVICE': "boot.VmediaDevice",
            'COMPUTE.BLADE': "compute.Blade",
            'COMPUTE.BOARD': "compute.Board",
            'COMPUTE.RACKUNIT': "compute.RackUnit",
            'EQUIPMENT.CHASSIS': "equipment.Chassis",
            'EQUIPMENT.EXPANDERMODULE': "equipment.ExpanderModule",
            'EQUIPMENT.FAN': "equipment.Fan",
            'EQUIPMENT.FANCONTROL': "equipment.FanControl",
            'EQUIPMENT.FANMODULE': "equipment.FanModule",
            'EQUIPMENT.FEX': "equipment.Fex",
            'EQUIPMENT.FRU': "equipment.Fru",
            'EQUIPMENT.IOCARD': "equipment.IoCard",
            'EQUIPMENT.IOEXPANDER': "equipment.IoExpander",
            'EQUIPMENT.PSU': "equipment.Psu",
            'EQUIPMENT.PSUCONTROL': "equipment.PsuControl",
            'EQUIPMENT.RACKENCLOSURE': "equipment.RackEnclosure",
            'EQUIPMENT.RACKENCLOSURESLOT': "equipment.RackEnclosureSlot",
            'EQUIPMENT.SHAREDIOMODULE': "equipment.SharedIoModule",
            'EQUIPMENT.SWITCHCARD': "equipment.SwitchCard",
            'EQUIPMENT.SYSTEMIOCONTROLLER': "equipment.SystemIoController",
            'EQUIPMENT.TPM': "equipment.Tpm",
            'EQUIPMENT.TRANSCEIVER': "equipment.Transceiver",
            'GRAPHICS.CARD': "graphics.Card",
            'GRAPHICS.CONTROLLER': "graphics.Controller",
            'MEMORY.ARRAY': "memory.Array",
            'MEMORY.PERSISTENTMEMORYUNIT': "memory.PersistentMemoryUnit",
            'MEMORY.UNIT': "memory.Unit",
            'NETWORK.ELEMENT': "network.Element",
            'PCI.COPROCESSORCARD': "pci.CoprocessorCard",
            'PCI.DEVICE': "pci.Device",
            'PCI.LINK': "pci.Link",
            'PCI.SWITCH': "pci.Switch",
            'PROCESSOR.UNIT': "processor.Unit",
            'SECURITY.UNIT': "security.Unit",
            'STORAGE.CONTROLLER': "storage.Controller",
            'STORAGE.DISKSLOT': "storage.DiskSlot",
            'STORAGE.ENCLOSURE': "storage.Enclosure",
            'STORAGE.ENCLOSUREDISK': "storage.EnclosureDisk",
            'STORAGE.FLEXFLASHCONTROLLER': "storage.FlexFlashController",
            'STORAGE.FLEXFLASHCONTROLLERPROPS': "storage.FlexFlashControllerProps",
            'STORAGE.FLEXFLASHPHYSICALDRIVE': "storage.FlexFlashPhysicalDrive",
            'STORAGE.FLEXFLASHVIRTUALDRIVE': "storage.FlexFlashVirtualDrive",
            'STORAGE.FLEXUTILPHYSICALDRIVE': "storage.FlexUtilPhysicalDrive",
            'STORAGE.HITACHIARRAY': "storage.HitachiArray",
            'STORAGE.HITACHICONTROLLER': "storage.HitachiController",
            'STORAGE.HITACHIDISK': "storage.HitachiDisk",
            'STORAGE.NETAPPBASEDISK': "storage.NetAppBaseDisk",
            'STORAGE.NETAPPCLUSTER': "storage.NetAppCluster",
            'STORAGE.NETAPPNODE': "storage.NetAppNode",
            'STORAGE.PHYSICALDISK': "storage.PhysicalDisk",
            'STORAGE.PHYSICALDISKEXTENSION': "storage.PhysicalDiskExtension",
            'STORAGE.PUREARRAY': "storage.PureArray",
            'STORAGE.PURECONTROLLER': "storage.PureController",
            'STORAGE.PUREDISK': "storage.PureDisk",
            'STORAGE.SASEXPANDER': "storage.SasExpander",
            'STORAGE.VIRTUALDRIVE': "storage.VirtualDrive",
            'STORAGE.VIRTUALDRIVECONTAINER': "storage.VirtualDriveContainer",
        },
        ('object_type',): {
            'ADAPTER.HOSTFCINTERFACE': "adapter.HostFcInterface",
            'ADAPTER.HOSTISCSIINTERFACE': "adapter.HostIscsiInterface",
            'ADAPTER.UNIT': "adapter.Unit",
            'ADAPTER.UNITEXPANDER': "adapter.UnitExpander",
            'BIOS.UNIT': "bios.Unit",
            'BOOT.CDDDEVICE': "boot.CddDevice",
            'BOOT.HDDDEVICE': "boot.HddDevice",
            'BOOT.ISCSIDEVICE': "boot.IscsiDevice",
            'BOOT.NVMEDEVICE': "boot.NvmeDevice",
            'BOOT.PCHSTORAGEDEVICE': "boot.PchStorageDevice",
            'BOOT.PXEDEVICE': "boot.PxeDevice",
            'BOOT.SANDEVICE': "boot.SanDevice",
            'BOOT.SDDEVICE': "boot.SdDevice",
            'BOOT.UEFISHELLDEVICE': "boot.UefiShellDevice",
            'BOOT.USBDEVICE': "boot.UsbDevice",
            'BOOT.VMEDIADEVICE': "boot.VmediaDevice",
            'COMPUTE.BLADE': "compute.Blade",
            'COMPUTE.BOARD': "compute.Board",
            'COMPUTE.RACKUNIT': "compute.RackUnit",
            'EQUIPMENT.CHASSIS': "equipment.Chassis",
            'EQUIPMENT.EXPANDERMODULE': "equipment.ExpanderModule",
            'EQUIPMENT.FAN': "equipment.Fan",
            'EQUIPMENT.FANCONTROL': "equipment.FanControl",
            'EQUIPMENT.FANMODULE': "equipment.FanModule",
            'EQUIPMENT.FEX': "equipment.Fex",
            'EQUIPMENT.FRU': "equipment.Fru",
            'EQUIPMENT.IOCARD': "equipment.IoCard",
            'EQUIPMENT.IOEXPANDER': "equipment.IoExpander",
            'EQUIPMENT.PSU': "equipment.Psu",
            'EQUIPMENT.PSUCONTROL': "equipment.PsuControl",
            'EQUIPMENT.RACKENCLOSURE': "equipment.RackEnclosure",
            'EQUIPMENT.RACKENCLOSURESLOT': "equipment.RackEnclosureSlot",
            'EQUIPMENT.SHAREDIOMODULE': "equipment.SharedIoModule",
            'EQUIPMENT.SWITCHCARD': "equipment.SwitchCard",
            'EQUIPMENT.SYSTEMIOCONTROLLER': "equipment.SystemIoController",
            'EQUIPMENT.TPM': "equipment.Tpm",
            'EQUIPMENT.TRANSCEIVER': "equipment.Transceiver",
            'GRAPHICS.CARD': "graphics.Card",
            'GRAPHICS.CONTROLLER': "graphics.Controller",
            'MEMORY.ARRAY': "memory.Array",
            'MEMORY.PERSISTENTMEMORYUNIT': "memory.PersistentMemoryUnit",
            'MEMORY.UNIT': "memory.Unit",
            'NETWORK.ELEMENT': "network.Element",
            'PCI.COPROCESSORCARD': "pci.CoprocessorCard",
            'PCI.DEVICE': "pci.Device",
            'PCI.LINK': "pci.Link",
            'PCI.SWITCH': "pci.Switch",
            'PROCESSOR.UNIT': "processor.Unit",
            'SECURITY.UNIT': "security.Unit",
            'STORAGE.CONTROLLER': "storage.Controller",
            'STORAGE.DISKSLOT': "storage.DiskSlot",
            'STORAGE.ENCLOSURE': "storage.Enclosure",
            'STORAGE.ENCLOSUREDISK': "storage.EnclosureDisk",
            'STORAGE.FLEXFLASHCONTROLLER': "storage.FlexFlashController",
            'STORAGE.FLEXFLASHCONTROLLERPROPS': "storage.FlexFlashControllerProps",
            'STORAGE.FLEXFLASHPHYSICALDRIVE': "storage.FlexFlashPhysicalDrive",
            'STORAGE.FLEXFLASHVIRTUALDRIVE': "storage.FlexFlashVirtualDrive",
            'STORAGE.FLEXUTILPHYSICALDRIVE': "storage.FlexUtilPhysicalDrive",
            'STORAGE.HITACHIARRAY': "storage.HitachiArray",
            'STORAGE.HITACHICONTROLLER': "storage.HitachiController",
            'STORAGE.HITACHIDISK': "storage.HitachiDisk",
            'STORAGE.NETAPPBASEDISK': "storage.NetAppBaseDisk",
            'STORAGE.NETAPPCLUSTER': "storage.NetAppCluster",
            'STORAGE.NETAPPNODE': "storage.NetAppNode",
            'STORAGE.PHYSICALDISK': "storage.PhysicalDisk",
            'STORAGE.PHYSICALDISKEXTENSION': "storage.PhysicalDiskExtension",
            'STORAGE.PUREARRAY': "storage.PureArray",
            'STORAGE.PURECONTROLLER': "storage.PureController",
            'STORAGE.PUREDISK': "storage.PureDisk",
            'STORAGE.SASEXPANDER': "storage.SasExpander",
            'STORAGE.VIRTUALDRIVE': "storage.VirtualDrive",
            'STORAGE.VIRTUALDRIVECONTAINER': "storage.VirtualDriveContainer",
        },
    }

    validations = {
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
            'model': (str,),  # noqa: E501
            'presence': (str,),  # noqa: E501
            'revision': (str,),  # noqa: E501
            'serial': (str,),  # noqa: E501
            'vendor': (str,),  # noqa: E501
            'previous_fru': (EquipmentFruRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'model': 'Model',  # noqa: E501
        'presence': 'Presence',  # noqa: E501
        'revision': 'Revision',  # noqa: E501
        'serial': 'Serial',  # noqa: E501
        'vendor': 'Vendor',  # noqa: E501
        'previous_fru': 'PreviousFru',  # noqa: E501
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
        """EquipmentBaseAllOf - a model defined in OpenAPI

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
            model (str): This field identifies the model of the given component.. [optional]  # noqa: E501
            presence (str): This field identifies the presence (equipped) or absence of the given component.. [optional]  # noqa: E501
            revision (str): This field identifies the revision of the given component.. [optional]  # noqa: E501
            serial (str): This field identifies the serial of the given component.. [optional]  # noqa: E501
            vendor (str): This field identifies the vendor of the given component.. [optional]  # noqa: E501
            previous_fru (EquipmentFruRelationship): [optional]  # noqa: E501
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
