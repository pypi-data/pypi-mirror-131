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
    from intersight.model.firmware_base_distributable import FirmwareBaseDistributable
    from intersight.model.firmware_component_meta import FirmwareComponentMeta
    from intersight.model.firmware_distributable_meta_relationship import FirmwareDistributableMetaRelationship
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    from intersight.model.software_hyperflex_bundle_distributable_all_of import SoftwareHyperflexBundleDistributableAllOf
    from intersight.model.software_hyperflex_distributable_relationship import SoftwareHyperflexDistributableRelationship
    from intersight.model.softwarerepository_catalog_relationship import SoftwarerepositoryCatalogRelationship
    from intersight.model.softwarerepository_file_server import SoftwarerepositoryFileServer
    from intersight.model.softwarerepository_release_relationship import SoftwarerepositoryReleaseRelationship
    globals()['DisplayNames'] = DisplayNames
    globals()['FirmwareBaseDistributable'] = FirmwareBaseDistributable
    globals()['FirmwareComponentMeta'] = FirmwareComponentMeta
    globals()['FirmwareDistributableMetaRelationship'] = FirmwareDistributableMetaRelationship
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext
    globals()['SoftwareHyperflexBundleDistributableAllOf'] = SoftwareHyperflexBundleDistributableAllOf
    globals()['SoftwareHyperflexDistributableRelationship'] = SoftwareHyperflexDistributableRelationship
    globals()['SoftwarerepositoryCatalogRelationship'] = SoftwarerepositoryCatalogRelationship
    globals()['SoftwarerepositoryFileServer'] = SoftwarerepositoryFileServer
    globals()['SoftwarerepositoryReleaseRelationship'] = SoftwarerepositoryReleaseRelationship


class SoftwareHyperflexBundleDistributable(ModelComposed):
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
            'SOFTWARE.HYPERFLEXBUNDLEDISTRIBUTABLE': "software.HyperflexBundleDistributable",
        },
        ('object_type',): {
            'SOFTWARE.HYPERFLEXBUNDLEDISTRIBUTABLE': "software.HyperflexBundleDistributable",
        },
        ('import_action',): {
            'NONE': "None",
            'GENERATEPRESIGNEDUPLOADURL': "GeneratePreSignedUploadUrl",
            'GENERATEPRESIGNEDDOWNLOADURL': "GeneratePreSignedDownloadUrl",
            'COMPLETEIMPORTPROCESS': "CompleteImportProcess",
            'MARKIMPORTFAILED': "MarkImportFailed",
            'PRECACHE': "PreCache",
            'CANCEL': "Cancel",
            'EXTRACT': "Extract",
            'EVICT': "Evict",
        },
        ('import_state',): {
            'READYFORIMPORT': "ReadyForImport",
            'IMPORTING': "Importing",
            'IMPORTED': "Imported",
            'PENDINGEXTRACTION': "PendingExtraction",
            'EXTRACTING': "Extracting",
            'EXTRACTED': "Extracted",
            'FAILED': "Failed",
            'METAONLY': "MetaOnly",
            'READYFORCACHE': "ReadyForCache",
            'CACHING': "Caching",
            'CACHED': "Cached",
            'CACHINGFAILED': "CachingFailed",
            'CORRUPTED': "Corrupted",
            'EVICTED': "Evicted",
            'INVALID': "Invalid",
        },
    }

    validations = {
        ('name',): {
            'max_length': 128,
        },
        ('supported_models',): {
            'min_items': 1,
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
            'catalog': (SoftwarerepositoryCatalogRelationship,),  # noqa: E501
            'images': ([SoftwareHyperflexDistributableRelationship], none_type,),  # noqa: E501
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
            'download_count': (int,),  # noqa: E501
            'import_action': (str,),  # noqa: E501
            'import_state': (str,),  # noqa: E501
            'imported_time': (datetime,),  # noqa: E501
            'last_access_time': (datetime,),  # noqa: E501
            'md5e_tag': (str,),  # noqa: E501
            'md5sum': (str,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'release_date': (datetime,),  # noqa: E501
            'sha512sum': (str,),  # noqa: E501
            'size': (int,),  # noqa: E501
            'software_advisory_url': (str,),  # noqa: E501
            'source': (SoftwarerepositoryFileServer,),  # noqa: E501
            'version': (str,),  # noqa: E501
            'bundle_type': (str,),  # noqa: E501
            'component_meta': ([FirmwareComponentMeta], none_type,),  # noqa: E501
            'guid': (str,),  # noqa: E501
            'image_type': (str,),  # noqa: E501
            'mdfid': (str,),  # noqa: E501
            'model': (str,),  # noqa: E501
            'platform_type': (str,),  # noqa: E501
            'recommended_build': (str,),  # noqa: E501
            'release_notes_url': (str,),  # noqa: E501
            'software_type_id': (str,),  # noqa: E501
            'supported_models': ([str], none_type,),  # noqa: E501
            'vendor': (str,),  # noqa: E501
            'distributable_metas': ([FirmwareDistributableMetaRelationship], none_type,),  # noqa: E501
            'release': (SoftwarerepositoryReleaseRelationship,),  # noqa: E501
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
        'catalog': 'Catalog',  # noqa: E501
        'images': 'Images',  # noqa: E501
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
        'download_count': 'DownloadCount',  # noqa: E501
        'import_action': 'ImportAction',  # noqa: E501
        'import_state': 'ImportState',  # noqa: E501
        'imported_time': 'ImportedTime',  # noqa: E501
        'last_access_time': 'LastAccessTime',  # noqa: E501
        'md5e_tag': 'Md5eTag',  # noqa: E501
        'md5sum': 'Md5sum',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'release_date': 'ReleaseDate',  # noqa: E501
        'sha512sum': 'Sha512sum',  # noqa: E501
        'size': 'Size',  # noqa: E501
        'software_advisory_url': 'SoftwareAdvisoryUrl',  # noqa: E501
        'source': 'Source',  # noqa: E501
        'version': 'Version',  # noqa: E501
        'bundle_type': 'BundleType',  # noqa: E501
        'component_meta': 'ComponentMeta',  # noqa: E501
        'guid': 'Guid',  # noqa: E501
        'image_type': 'ImageType',  # noqa: E501
        'mdfid': 'Mdfid',  # noqa: E501
        'model': 'Model',  # noqa: E501
        'platform_type': 'PlatformType',  # noqa: E501
        'recommended_build': 'RecommendedBuild',  # noqa: E501
        'release_notes_url': 'ReleaseNotesUrl',  # noqa: E501
        'software_type_id': 'SoftwareTypeId',  # noqa: E501
        'supported_models': 'SupportedModels',  # noqa: E501
        'vendor': 'Vendor',  # noqa: E501
        'distributable_metas': 'DistributableMetas',  # noqa: E501
        'release': 'Release',  # noqa: E501
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
        """SoftwareHyperflexBundleDistributable - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "software.HyperflexBundleDistributable", must be one of ["software.HyperflexBundleDistributable", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "software.HyperflexBundleDistributable", must be one of ["software.HyperflexBundleDistributable", ]  # noqa: E501
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
            catalog (SoftwarerepositoryCatalogRelationship): [optional]  # noqa: E501
            images ([SoftwareHyperflexDistributableRelationship], none_type): An array of relationships to softwareHyperflexDistributable resources.. [optional]  # noqa: E501
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
            description (str): User provided description about the file. Cisco provided description for image inventoried from a Cisco repository.. [optional]  # noqa: E501
            download_count (int): The number of times this file has been downloaded from the local repository. It is used by the repository monitoring process to determine the files that are to be evicted from the cache.. [optional]  # noqa: E501
            import_action (str): The action to be performed on the imported file. If 'PreCache' is set, the image will be cached in Appliance. Applicable in Intersight appliance deployment. If 'Evict' is set, the cached file will be removed. Applicable in Intersight appliance deployment. If 'GeneratePreSignedUploadUrl' is set, generates pre signed URL (s) for the file to be imported into the repository. Applicable for local machine source. The URL (s) will be populated under LocalMachine file server. If 'CompleteImportProcess' is set, the ImportState is marked as 'Imported'. Applicable for local machine source. If 'Cancel' is set, the ImportState is marked as 'Failed'. Applicable for local machine source. * `None` - No action should be taken on the imported file. * `GeneratePreSignedUploadUrl` - Generate pre signed URL of file for importing into the repository. * `GeneratePreSignedDownloadUrl` - Generate pre signed URL of file in the repository to download. * `CompleteImportProcess` - Mark that the import process of the file into the repository is complete. * `MarkImportFailed` - Mark to indicate that the import process of the file into the repository failed. * `PreCache` - Cache the file into the Intersight Appliance. * `Cancel` - The cancel import process for the file into the repository. * `Extract` - The action to extract the file in the external repository. * `Evict` - Evict the cached file from the Intersight Appliance.. [optional] if omitted the server will use the default value of "None"  # noqa: E501
            import_state (str): The state  of this file in the repository or Appliance. The importState is updated during the import operation and as part of the repository monitoring process. * `ReadyForImport` - The image is ready to be imported into the repository. * `Importing` - The image is being imported into the repository. * `Imported` - The image has been extracted and imported into the repository. * `PendingExtraction` - Indicates that the image has been imported but not extracted in the repository. * `Extracting` - Indicates that the image is being extracted into the repository. * `Extracted` - Indicates that the image has been extracted into the repository. * `Failed` - The image import from an external source to the repository has failed. * `MetaOnly` - The image is present in an external repository. * `ReadyForCache` - The image is ready to be cached into the Intersight Appliance. * `Caching` - Indicates that the image is being cached into the Intersight Appliance or endpoint cache. * `Cached` - Indicates that the image has been cached into the Intersight Appliance or endpoint cache. * `CachingFailed` - Indicates that the image caching into the Intersight Appliance failed or endpoint cache. * `Corrupted` - Indicates that the image in the local repository (or endpoint cache) has been corrupted after it was cached. * `Evicted` - Indicates that the image has been evicted from the Intersight Appliance (or endpoint cache) to reclaim storage space. * `Invalid` - Indicates that the corresponding distributable MO has been removed from the backend. This can be due to unpublishing of an image.. [optional] if omitted the server will use the default value of "ReadyForImport"  # noqa: E501
            imported_time (datetime): The time at which this image or file was imported/cached into the repositry. if the 'ImportState' is 'Imported', the time at which this image or file was imported. if the 'ImportState' is 'Cached', the time at which this image or file was cached.. [optional]  # noqa: E501
            last_access_time (datetime): The time at which this file was last downloaded from the local repository. It is used by the repository monitoring process to determine the files that are to be evicted from the cache.. [optional]  # noqa: E501
            md5e_tag (str): The MD5 ETag for a file that is stored in Intersight repository or in the appliance cache. Warning - MD5 is currently broken and this will be migrated to SHA shortly.. [optional]  # noqa: E501
            md5sum (str): The md5sum checksum of the file. This information is available for all Cisco distributed images and files imported to the local repository.. [optional]  # noqa: E501
            name (str): The name of the file. It is populated as part of the image import operation.. [optional]  # noqa: E501
            release_date (datetime): The date on which the file was released or distributed by its vendor.. [optional]  # noqa: E501
            sha512sum (str): The sha512sum of the file. This information is available for all Cisco distributed images and files imported to the local repository.. [optional]  # noqa: E501
            size (int): The size (in bytes) of the file. This information is available for all Cisco distributed images and files imported to the local repository.. [optional]  # noqa: E501
            software_advisory_url (str): The software advisory, if any, provided by the vendor for this file.. [optional]  # noqa: E501
            source (SoftwarerepositoryFileServer): [optional]  # noqa: E501
            version (str): Vendor provided version for the file.. [optional]  # noqa: E501
            bundle_type (str): The bundle type of the image, as published on cisco.com.. [optional]  # noqa: E501
            component_meta ([FirmwareComponentMeta], none_type): [optional]  # noqa: E501
            guid (str): The unique identifier for an image in a Cisco repository.. [optional]  # noqa: E501
            image_type (str): The type of image which the distributable falls into according to the component it can upgrade. For e.g.; Standalone server, Intersight managed server, UCS Managed Fabric Interconnect. The field is used in private appliance mode, where image does not have description populated from CCO.. [optional]  # noqa: E501
            mdfid (str): The mdfid of the image provided by cisco.com.. [optional]  # noqa: E501
            model (str): The endpoint model for which this firmware image is applicable.. [optional]  # noqa: E501
            platform_type (str): The platform type of the image.. [optional]  # noqa: E501
            recommended_build (str): The build which is recommended by Cisco.. [optional]  # noqa: E501
            release_notes_url (str): The url for the release notes of this image.. [optional]  # noqa: E501
            software_type_id (str): The software type id provided by cisco.com.. [optional]  # noqa: E501
            supported_models ([str], none_type): [optional]  # noqa: E501
            vendor (str): The vendor or publisher of this file.. [optional] if omitted the server will use the default value of "Cisco"  # noqa: E501
            distributable_metas ([FirmwareDistributableMetaRelationship], none_type): An array of relationships to firmwareDistributableMeta resources.. [optional]  # noqa: E501
            release (SoftwarerepositoryReleaseRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "software.HyperflexBundleDistributable")
        object_type = kwargs.get('object_type', "software.HyperflexBundleDistributable")
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
              FirmwareBaseDistributable,
              SoftwareHyperflexBundleDistributableAllOf,
          ],
          'oneOf': [
          ],
        }
