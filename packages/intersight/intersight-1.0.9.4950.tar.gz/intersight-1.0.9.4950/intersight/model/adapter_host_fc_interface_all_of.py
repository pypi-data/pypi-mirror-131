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
    from intersight.model.adapter_unit_relationship import AdapterUnitRelationship
    from intersight.model.asset_device_registration_relationship import AssetDeviceRegistrationRelationship
    from intersight.model.inventory_device_info_relationship import InventoryDeviceInfoRelationship
    globals()['AdapterUnitRelationship'] = AdapterUnitRelationship
    globals()['AssetDeviceRegistrationRelationship'] = AssetDeviceRegistrationRelationship
    globals()['InventoryDeviceInfoRelationship'] = InventoryDeviceInfoRelationship


class AdapterHostFcInterfaceAllOf(ModelNormal):
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
        },
        ('object_type',): {
            'ADAPTER.HOSTFCINTERFACE': "adapter.HostFcInterface",
        },
        ('oper_reason',): {
            'None': None,
            'UNKNOWN': "Unknown",
            'OK': "OK",
            'OFFLINE': "Offline",
            'MISSING': "Missing",
            'TEMPERATUREWARNING': "TemperatureWarning",
            'TEMPERATURECRITICAL': "TemperatureCritical",
            'INPUTVOLTAGEWARNING': "InputVoltageWarning",
            'INPUTVOLTAGECRITICAL': "InputVoltageCritical",
            'OUTPUTVOLTAGEWARNING': "OutputVoltageWarning",
            'OUTPUTVOLTAGECRITICAL': "OutputVoltageCritical",
            'OUTPUTCURRENTWARNING': "OutputCurrentWarning",
            'OUTPUTCURRENTCRITICAL': "OutputCurrentCritical",
            'SPEEDWARNING': "SpeedWarning",
            'SPEEDCRITICAL': "SpeedCritical",
            'FANMISSINGWARNING': "FanMissingWarning",
            'FANSMISSINGCRITICAL': "FansMissingCritical",
            'IOCARDPOSTWARNING': "IocardPostWarning",
            'ASICPOSTWARNING': "AsicPostWarning",
            'FRUSTATECRITICAL': "FruStateCritical",
            'FRUSTATEWARNING': "FruStateWarning",
            'ALTERNATEIMAGEWARNING': "AlternateImageWarning",
            'SELECTEDIMAGEWARNING': "SelectedImageWarning",
            'LOWMEMORYCRITICAL': "LowMemoryCritical",
            'LOWMEMORYWARNING': "LowMemoryWarning",
            'POWERCRITICAL': "PowerCritical",
            'POWERWARNING': "PowerWarning",
            'THERMALSAFEMODECRITICAL': "ThermalSafeModeCritical",
            'PSUREDUNDANCYLOSTCRITICAL': "PsuRedundancyLostCritical",
            'INPUTPOWERWARNING': "InputPowerWarning",
            'INPUTPOWERCRITICAL': "InputPowerCritical",
            'OUTPUTPOWERWARNING': "OutputPowerWarning",
            'OUTPUTPOWERCRITICAL': "OutputPowerCritical",
            'FANGENERALCRITICAL': "FanGeneralCritical",
            'POWERSUPPLYGENERALCRITICAL': "PowerSupplyGeneralCritical",
            'POWERSUPPLYINPUTWARNING': "PowerSupplyInputWarning",
            'POWERSUPPLYOUTPUTCRITICAL': "PowerSupplyOutputCritical",
            'POWERSUPPLYINPUTLOSTWARNING': "PowerSupplyInputLostWarning",
            'POWERSUPPLYUNRESPONSIVECRITICAL': "PowerSupplyUnresponsiveCritical",
            'FANUNRESPONSIVECRITICAL': "FanUnresponsiveCritical",
            'MEMORYUNCORRECTABLEERROR': "MemoryUncorrectableError",
            'MEMORYTEMPERATUREWARNING': "MemoryTemperatureWarning",
            'MEMORYTEMPERATURECRITICAL': "MemoryTemperatureCritical",
            'MEMORYBANKERROR': "MemoryBankError",
            'MEMORYRANKERROR': "MemoryRankError",
            'MEMORYPOPERROR': "MemoryPopError",
            'MEMORYRASERROR': "MemoryRasError",
            'MEMORYMISMATCHERROR': "MemoryMismatchError",
            'MEMORYSPDERROR': "MemorySpdError",
            'MEMORYBISTERROR': "MemoryBistError",
            'MEMORYTYPEERROR': "MemoryTypeError",
            'MOTHERBOARDPOWERCRITICAL': "MotherBoardPowerCritical",
            'MOTHERBOARDTEMPERATUREWARNING': "MotherBoardTemperatureWarning",
            'MOTHERBOARDTEMPERATURECRITICAL': "MotherBoardTemperatureCritical",
            'MOTHERBOARDVOLTAGEWARNING': "MotherBoardVoltageWarning",
            'MOTHERBOARDVOLTAGECRITICAL': "MotherBoardVoltageCritical",
            'PROCESSORCATERR': "ProcessorCatErr",
            'PROCESSORTHERMTRIP': "ProcessorThermTrip",
            'COMPONENTNOTOPERATIONAL': "ComponentNotOperational",
            'COMPONENTNOTREACHABLE': "ComponentNotReachable",
            'PROCESSORTEMPERATUREWARNING': "ProcessorTemperatureWarning",
            'PROCESSORTEMPERATURECRITICAL': "ProcessorTemperatureCritical",
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
            'admin_state': (str,),  # noqa: E501
            'ep_dn': (str,),  # noqa: E501
            'host_fc_interface_id': (int,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'oper_reason': ([str], none_type,),  # noqa: E501
            'oper_state': (str,),  # noqa: E501
            'operability': (str,),  # noqa: E501
            'original_wwnn': (str,),  # noqa: E501
            'original_wwpn': (str,),  # noqa: E501
            'peer_dn': (str,),  # noqa: E501
            'wwnn': (str,),  # noqa: E501
            'wwpn': (str,),  # noqa: E501
            'adapter_unit': (AdapterUnitRelationship,),  # noqa: E501
            'inventory_device_info': (InventoryDeviceInfoRelationship,),  # noqa: E501
            'registered_device': (AssetDeviceRegistrationRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'admin_state': 'AdminState',  # noqa: E501
        'ep_dn': 'EpDn',  # noqa: E501
        'host_fc_interface_id': 'HostFcInterfaceId',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'oper_reason': 'OperReason',  # noqa: E501
        'oper_state': 'OperState',  # noqa: E501
        'operability': 'Operability',  # noqa: E501
        'original_wwnn': 'OriginalWwnn',  # noqa: E501
        'original_wwpn': 'OriginalWwpn',  # noqa: E501
        'peer_dn': 'PeerDn',  # noqa: E501
        'wwnn': 'Wwnn',  # noqa: E501
        'wwpn': 'Wwpn',  # noqa: E501
        'adapter_unit': 'AdapterUnit',  # noqa: E501
        'inventory_device_info': 'InventoryDeviceInfo',  # noqa: E501
        'registered_device': 'RegisteredDevice',  # noqa: E501
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
        """AdapterHostFcInterfaceAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "adapter.HostFcInterface", must be one of ["adapter.HostFcInterface", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "adapter.HostFcInterface", must be one of ["adapter.HostFcInterface", ]  # noqa: E501
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
            admin_state (str): Admin Configured State of Host Fibre Channel Interface.. [optional]  # noqa: E501
            ep_dn (str): The Endpoint Config Dn of the Host Fibre Channel Interface.. [optional]  # noqa: E501
            host_fc_interface_id (int): Identifier of Host Fibre Channel Interface.. [optional]  # noqa: E501
            name (str): Name of Host Fibre Channel Interface.. [optional]  # noqa: E501
            oper_reason ([str], none_type): [optional]  # noqa: E501
            oper_state (str): Operational State of Host Fibre Channel Interface.. [optional]  # noqa: E501
            operability (str): Operability status of Host Fibre Channel Interface.. [optional]  # noqa: E501
            original_wwnn (str): The uniquely distinguishable factory default  World Wide Node Name of the Host.. [optional]  # noqa: E501
            original_wwpn (str): The uniquely distinguishable factory default World Wide Port Name of the Host Fibre Channel Interface.. [optional]  # noqa: E501
            peer_dn (str): PeerPort Dn of Host Fibre Channel Interface.. [optional]  # noqa: E501
            wwnn (str): The uniquely distinguishable user configured World Wide Node Name of the Host.. [optional]  # noqa: E501
            wwpn (str): The uniquely distinguishable user configured World Wide Port Name of the Host Fibre Channel Interface.. [optional]  # noqa: E501
            adapter_unit (AdapterUnitRelationship): [optional]  # noqa: E501
            inventory_device_info (InventoryDeviceInfoRelationship): [optional]  # noqa: E501
            registered_device (AssetDeviceRegistrationRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "adapter.HostFcInterface")
        object_type = kwargs.get('object_type', "adapter.HostFcInterface")
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
