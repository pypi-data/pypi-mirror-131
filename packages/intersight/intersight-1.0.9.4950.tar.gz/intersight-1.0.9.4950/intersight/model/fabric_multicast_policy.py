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
    from intersight.model.fabric_multicast_policy_all_of import FabricMulticastPolicyAllOf
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
    from intersight.model.policy_abstract_policy import PolicyAbstractPolicy
    globals()['DisplayNames'] = DisplayNames
    globals()['FabricMulticastPolicyAllOf'] = FabricMulticastPolicyAllOf
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext
    globals()['OrganizationOrganizationRelationship'] = OrganizationOrganizationRelationship
    globals()['PolicyAbstractPolicy'] = PolicyAbstractPolicy


class FabricMulticastPolicy(ModelComposed):
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
            'FABRIC.MULTICASTPOLICY': "fabric.MulticastPolicy",
        },
        ('object_type',): {
            'FABRIC.MULTICASTPOLICY': "fabric.MulticastPolicy",
        },
        ('querier_state',): {
            'DISABLED': "Disabled",
            'ENABLED': "Enabled",
        },
        ('snooping_state',): {
            'ENABLED': "Enabled",
            'DISABLED': "Disabled",
        },
    }

    validations = {
        ('querier_ip_address',): {
            'regex': {
                'pattern': r'^$|^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$',  # noqa: E501
            },
        },
        ('querier_ip_address_peer',): {
            'regex': {
                'pattern': r'^$|^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$',  # noqa: E501
            },
        },
        ('description',): {
            'max_length': 1024,
            'regex': {
                'pattern': r'^$|^[a-zA-Z0-9]+[\x00-\xFF]*$',  # noqa: E501
            },
        },
        ('name',): {
            'regex': {
                'pattern': r'^[a-zA-Z0-9_.:-]{1,64}$',  # noqa: E501
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
            'querier_ip_address': (str,),  # noqa: E501
            'querier_ip_address_peer': (str,),  # noqa: E501
            'querier_state': (str,),  # noqa: E501
            'snooping_state': (str,),  # noqa: E501
            'organization': (OrganizationOrganizationRelationship,),  # noqa: E501
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
            'description': (str,),  # noqa: E501
            'name': (str,),  # noqa: E501
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
        'querier_ip_address': 'QuerierIpAddress',  # noqa: E501
        'querier_ip_address_peer': 'QuerierIpAddressPeer',  # noqa: E501
        'querier_state': 'QuerierState',  # noqa: E501
        'snooping_state': 'SnoopingState',  # noqa: E501
        'organization': 'Organization',  # noqa: E501
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
        'description': 'Description',  # noqa: E501
        'name': 'Name',  # noqa: E501
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
        """FabricMulticastPolicy - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "fabric.MulticastPolicy", must be one of ["fabric.MulticastPolicy", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "fabric.MulticastPolicy", must be one of ["fabric.MulticastPolicy", ]  # noqa: E501
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
            querier_ip_address (str): Used to define the IGMP Querier IP address.. [optional]  # noqa: E501
            querier_ip_address_peer (str): Used to define the IGMP Querier IP address of the peer switch.. [optional]  # noqa: E501
            querier_state (str): Administrative state of the IGMP Querier for this VLAN. * `Disabled` - Admin configured Disabled State. * `Enabled` - Admin configured Enabled State.. [optional] if omitted the server will use the default value of "Disabled"  # noqa: E501
            snooping_state (str): Administrative state of the IGMP Snooping for this VLAN. * `Enabled` - Admin configured Enabled State. * `Disabled` - Admin configured Disabled State.. [optional] if omitted the server will use the default value of "Enabled"  # noqa: E501
            organization (OrganizationOrganizationRelationship): [optional]  # noqa: E501
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
            description (str): Description of the policy.. [optional]  # noqa: E501
            name (str): Name of the concrete policy.. [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "fabric.MulticastPolicy")
        object_type = kwargs.get('object_type', "fabric.MulticastPolicy")
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
              FabricMulticastPolicyAllOf,
              PolicyAbstractPolicy,
          ],
          'oneOf': [
          ],
        }
