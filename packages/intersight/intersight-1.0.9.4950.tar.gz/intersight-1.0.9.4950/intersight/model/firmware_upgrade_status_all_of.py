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
    from intersight.model.firmware_upgrade_base_relationship import FirmwareUpgradeBaseRelationship
    from intersight.model.workflow_workflow_info_relationship import WorkflowWorkflowInfoRelationship
    globals()['FirmwareUpgradeBaseRelationship'] = FirmwareUpgradeBaseRelationship
    globals()['WorkflowWorkflowInfoRelationship'] = WorkflowWorkflowInfoRelationship


class FirmwareUpgradeStatusAllOf(ModelNormal):
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
            'FIRMWARE.UPGRADESTATUS': "firmware.UpgradeStatus",
        },
        ('object_type',): {
            'FIRMWARE.UPGRADESTATUS': "firmware.UpgradeStatus",
        },
        ('ep_power_status',): {
            'NONE': "none",
            'POWERED_ON': "powered on",
            'POWERED_OFF': "powered off",
        },
        ('overallstatus',): {
            'NONE': "none",
            'STARTED': "started",
            'PREPARE_INITIATING': "prepare initiating",
            'PREPARE_INITIATED': "prepare initiated",
            'PREPARED': "prepared",
            'DOWNLOAD_INITIATING': "download initiating",
            'DOWNLOAD_INITIATED': "download initiated",
            'DOWNLOADING': "downloading",
            'DOWNLOADED': "downloaded",
            'UPGRADE_INITIATING_ON_FABRIC_A': "upgrade initiating on fabric A",
            'UPGRADE_INITIATED_ON_FABRIC_A': "upgrade initiated on fabric A",
            'UPGRADING_FABRIC_A': "upgrading fabric A",
            'REBOOTING_FABRIC_A': "rebooting fabric A",
            'UPGRADED_FABRIC_A': "upgraded fabric A",
            'UPGRADE_INITIATING_ON_FABRIC_B': "upgrade initiating on fabric B",
            'UPGRADE_INITIATED_ON_FABRIC_B': "upgrade initiated on fabric B",
            'UPGRADING_FABRIC_B': "upgrading fabric B",
            'REBOOTING_FABRIC_B': "rebooting fabric B",
            'UPGRADED_FABRIC_B': "upgraded fabric B",
            'UPGRADE_INITIATING': "upgrade initiating",
            'UPGRADE_INITIATED': "upgrade initiated",
            'UPGRADING': "upgrading",
            'OOB_IMAGES_STAGING': "oob images staging",
            'OOB_IMAGES_STAGED': "oob images staged",
            'REBOOTING': "rebooting",
            'UPGRADED': "upgraded",
            'SUCCESS': "success",
            'FAILED': "failed",
            'TERMINATED': "terminated",
            'PENDING': "pending",
            'READYFORCACHE': "ReadyForCache",
            'CACHING': "Caching",
            'CACHED': "Cached",
            'CACHINGFAILED': "CachingFailed",
        },
        ('pending_type',): {
            'NONE': "none",
            'PENDING_FOR_NEXT_REBOOT': "pending for next reboot",
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
            'download_message': (str,),  # noqa: E501
            'download_percentage': (int,),  # noqa: E501
            'download_stage': (str,),  # noqa: E501
            'ep_power_status': (str,),  # noqa: E501
            'overall_error': (str,),  # noqa: E501
            'overall_percentage': (int,),  # noqa: E501
            'overallstatus': (str,),  # noqa: E501
            'pending_type': (str,),  # noqa: E501
            'sd_card_download_error': (str,),  # noqa: E501
            'upgrade': (FirmwareUpgradeBaseRelationship,),  # noqa: E501
            'workflow': (WorkflowWorkflowInfoRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'download_message': 'DownloadMessage',  # noqa: E501
        'download_percentage': 'DownloadPercentage',  # noqa: E501
        'download_stage': 'DownloadStage',  # noqa: E501
        'ep_power_status': 'EpPowerStatus',  # noqa: E501
        'overall_error': 'OverallError',  # noqa: E501
        'overall_percentage': 'OverallPercentage',  # noqa: E501
        'overallstatus': 'Overallstatus',  # noqa: E501
        'pending_type': 'PendingType',  # noqa: E501
        'sd_card_download_error': 'SdCardDownloadError',  # noqa: E501
        'upgrade': 'Upgrade',  # noqa: E501
        'workflow': 'Workflow',  # noqa: E501
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
        """FirmwareUpgradeStatusAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "firmware.UpgradeStatus", must be one of ["firmware.UpgradeStatus", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "firmware.UpgradeStatus", must be one of ["firmware.UpgradeStatus", ]  # noqa: E501
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
            download_message (str): The message from the endpoint during the download.. [optional]  # noqa: E501
            download_percentage (int): The percentage of the image downloaded in the endpoint.. [optional]  # noqa: E501
            download_stage (str): The image download stages. Example:downloading, flashing.. [optional]  # noqa: E501
            ep_power_status (str): The server power status after the upgrade request is submitted in the endpoint. * `none` - Server power status is none. * `powered on` - Server power status is powered on. * `powered off` - Server power status is powered off.. [optional] if omitted the server will use the default value of "none"  # noqa: E501
            overall_error (str): The reason for the operation failure.. [optional]  # noqa: E501
            overall_percentage (int): The overall percentage of the operation.. [optional]  # noqa: E501
            overallstatus (str): The overall status of the operation. * `none` - Upgrade stage is no upgrade stage. * `started` - Upgrade stage is started. * `prepare initiating` - Upgrade configuration is being prepared. * `prepare initiated` - Upgrade configuration is initiated. * `prepared` - Upgrade configuration is prepared. * `download initiating` - Upgrade stage is download initiating. * `download initiated` - Upgrade stage is download initiated. * `downloading` - Upgrade stage is downloading. * `downloaded` - Upgrade stage is downloaded. * `upgrade initiating on fabric A` - Upgrade stage is in upgrade initiating when upgrade is being started in endopint. * `upgrade initiated on fabric A` - Upgrade stage is in upgrade initiated when the upgrade has started in endpoint. * `upgrading fabric A` - Upgrade stage is in upgrading when the upgrade requires reboot to complete. * `rebooting fabric A` - Upgrade is in rebooting when the endpoint is being rebooted. * `upgraded fabric A` - Upgrade stage is in upgraded when the corresponding endpoint has completed. * `upgrade initiating on fabric B` - Upgrade stage is in upgrade initiating when upgrade is being started in endopint. * `upgrade initiated on fabric B` - Upgrade stage is in upgrade initiated when upgrade has started in endpoint. * `upgrading fabric B` - Upgrade stage is in upgrading when the upgrade requires reboot to complete. * `rebooting fabric B` - Upgrade is in rebooting when the endpoint is being rebooted. * `upgraded fabric B` - Upgrade stage is in upgraded when the corresponding endpoint has completed. * `upgrade initiating` - Upgrade stage is upgrade initiating. * `upgrade initiated` - Upgrade stage is upgrade initiated. * `upgrading` - Upgrade stage is upgrading. * `oob images staging` - Out-of-band component images staging. * `oob images staged` - Out-of-band component images staged. * `rebooting` - Upgrade is rebooting the endpoint. * `upgraded` - Upgrade stage is upgraded. * `success` - Upgrade stage is success. * `failed` - Upgrade stage is upgrade failed. * `terminated` - Upgrade stage is terminated. * `pending` - Upgrade stage is pending. * `ReadyForCache` - The image is ready to be cached into the Intersight Appliance. * `Caching` - The image will be cached into Intersight Appliance or an endpoint cache. * `Cached` - The image has been cached into the Intersight Appliance or endpoint cache. * `CachingFailed` - The image caching into the Intersight Appliance failed or endpoint cache.. [optional] if omitted the server will use the default value of "none"  # noqa: E501
            pending_type (str): Pending reason for the upgrade waiting. * `none` - Upgrade pending reason is none. * `pending for next reboot` - Upgrade pending reason is pending for next reboot.. [optional] if omitted the server will use the default value of "none"  # noqa: E501
            sd_card_download_error (str): The error message from the endpoint during the SD card download.. [optional]  # noqa: E501
            upgrade (FirmwareUpgradeBaseRelationship): [optional]  # noqa: E501
            workflow (WorkflowWorkflowInfoRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "firmware.UpgradeStatus")
        object_type = kwargs.get('object_type', "firmware.UpgradeStatus")
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
