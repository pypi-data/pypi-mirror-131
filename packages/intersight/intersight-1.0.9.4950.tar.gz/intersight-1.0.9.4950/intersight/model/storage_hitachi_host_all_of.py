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
    from intersight.model.storage_hitachi_array_relationship import StorageHitachiArrayRelationship
    globals()['AssetDeviceRegistrationRelationship'] = AssetDeviceRegistrationRelationship
    globals()['StorageHitachiArrayRelationship'] = StorageHitachiArrayRelationship


class StorageHitachiHostAllOf(ModelNormal):
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
            'STORAGE.HITACHIHOST': "storage.HitachiHost",
        },
        ('object_type',): {
            'STORAGE.HITACHIHOST': "storage.HitachiHost",
        },
        ('authentication_mode',): {
            'N/A': "N/A",
            'CHAP': "CHAP",
            'NONE': "NONE",
            'BOTH': "BOTH",
        },
        ('type',): {
            'FC': "FC",
            'ISCSI': "iSCSI",
            'FCOE': "FCoE",
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
            'authentication_mode': (str,),  # noqa: E501
            'host_group_id': (str,),  # noqa: E501
            'host_group_number': (int,),  # noqa: E501
            'host_mode_options': ([int], none_type,),  # noqa: E501
            'is_chap_mutual': (bool,),  # noqa: E501
            'iscsi_name': (str,),  # noqa: E501
            'port_id': (str,),  # noqa: E501
            'port_lun_security': (bool,),  # noqa: E501
            'type': (str,),  # noqa: E501
            'wwn': (str,),  # noqa: E501
            'array': (StorageHitachiArrayRelationship,),  # noqa: E501
            'registered_device': (AssetDeviceRegistrationRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'authentication_mode': 'AuthenticationMode',  # noqa: E501
        'host_group_id': 'HostGroupId',  # noqa: E501
        'host_group_number': 'HostGroupNumber',  # noqa: E501
        'host_mode_options': 'HostModeOptions',  # noqa: E501
        'is_chap_mutual': 'IsChapMutual',  # noqa: E501
        'iscsi_name': 'IscsiName',  # noqa: E501
        'port_id': 'PortId',  # noqa: E501
        'port_lun_security': 'PortLunSecurity',  # noqa: E501
        'type': 'Type',  # noqa: E501
        'wwn': 'Wwn',  # noqa: E501
        'array': 'Array',  # noqa: E501
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
        """StorageHitachiHostAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "storage.HitachiHost", must be one of ["storage.HitachiHost", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "storage.HitachiHost", must be one of ["storage.HitachiHost", ]  # noqa: E501
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
            authentication_mode (str): Authentication mode for the iSCSI target. * `N/A` - Authentication Mode is not available. * `CHAP` - CHAP-authentication mode. * `NONE` - Authentication mode is not set. * `BOTH` - Comply with Host Setting.. [optional] if omitted the server will use the default value of "N/A"  # noqa: E501
            host_group_id (str): ID of the host group.. [optional]  # noqa: E501
            host_group_number (int): Host group number for this host.. [optional]  # noqa: E501
            host_mode_options ([int], none_type): [optional]  # noqa: E501
            is_chap_mutual (bool): Mutual CHAP setting that is Enabled or Disabled.. [optional]  # noqa: E501
            iscsi_name (str): IQN (iSCSI qualified name). Can be up to 255 characters long.. [optional]  # noqa: E501
            port_id (str): Port ID of the host group.. [optional]  # noqa: E501
            port_lun_security (bool): LUN security setting for the port.. [optional]  # noqa: E501
            type (str): Host Group type, it can be FC or iSCSI. * `FC` - Port supports fibre channel protocol. * `iSCSI` - Port supports iSCSI protocol. * `FCoE` - Port supports fibre channel over ethernet protocol.. [optional] if omitted the server will use the default value of "FC"  # noqa: E501
            wwn (str): World wide port name, 64 bit address represented in hexa decimal notation.. [optional]  # noqa: E501
            array (StorageHitachiArrayRelationship): [optional]  # noqa: E501
            registered_device (AssetDeviceRegistrationRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "storage.HitachiHost")
        object_type = kwargs.get('object_type', "storage.HitachiHost")
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
