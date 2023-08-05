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
    from intersight.model.asset_target_relationship import AssetTargetRelationship
    from intersight.model.cloud_base_sku import CloudBaseSku
    from intersight.model.cloud_custom_attributes import CloudCustomAttributes
    from intersight.model.cloud_sku_volume_type_all_of import CloudSkuVolumeTypeAllOf
    from intersight.model.display_names import DisplayNames
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    globals()['AssetTargetRelationship'] = AssetTargetRelationship
    globals()['CloudBaseSku'] = CloudBaseSku
    globals()['CloudCustomAttributes'] = CloudCustomAttributes
    globals()['CloudSkuVolumeTypeAllOf'] = CloudSkuVolumeTypeAllOf
    globals()['DisplayNames'] = DisplayNames
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext


class CloudSkuVolumeType(ModelComposed):
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
            'CLOUD.SKUVOLUMETYPE': "cloud.SkuVolumeType",
        },
        ('object_type',): {
            'CLOUD.SKUVOLUMETYPE': "cloud.SkuVolumeType",
        },
        ('platform_type',): {
            'EMPTY': "",
            'APIC': "APIC",
            'DCNM': "DCNM",
            'UCSFI': "UCSFI",
            'UCSFIISM': "UCSFIISM",
            'IMC': "IMC",
            'IMCM4': "IMCM4",
            'IMCM5': "IMCM5",
            'IMCRACK': "IMCRack",
            'UCSIOM': "UCSIOM",
            'HX': "HX",
            'HYPERFLEXAP': "HyperFlexAP",
            'IWE': "IWE",
            'UCSD': "UCSD",
            'INTERSIGHTAPPLIANCE': "IntersightAppliance",
            'INTERSIGHTASSIST': "IntersightAssist",
            'PURESTORAGEFLASHARRAY': "PureStorageFlashArray",
            'NEXUSDEVICE': "NexusDevice",
            'UCSC890': "UCSC890",
            'NETAPPONTAP': "NetAppOntap",
            'NETAPPACTIVEIQUNIFIEDMANAGER': "NetAppActiveIqUnifiedManager",
            'EMCSCALEIO': "EmcScaleIo",
            'EMCVMAX': "EmcVmax",
            'EMCVPLEX': "EmcVplex",
            'EMCXTREMIO': "EmcXtremIo",
            'VMWAREVCENTER': "VmwareVcenter",
            'MICROSOFTHYPERV': "MicrosoftHyperV",
            'APPDYNAMICS': "AppDynamics",
            'DYNATRACE': "Dynatrace",
            'NEWRELIC': "NewRelic",
            'SERVICENOW': "ServiceNow",
            'READHATOPENSTACK': "ReadHatOpenStack",
            'CLOUDFOUNDRY': "CloudFoundry",
            'MICROSOFTAZUREAPPLICATIONINSIGHTS': "MicrosoftAzureApplicationInsights",
            'OPENSTACK': "OpenStack",
            'MICROSOFTSQLSERVER': "MicrosoftSqlServer",
            'KUBERNETES': "Kubernetes",
            'AMAZONWEBSERVICE': "AmazonWebService",
            'AMAZONWEBSERVICEBILLING': "AmazonWebServiceBilling",
            'MICROSOFTAZURESERVICEPRINCIPAL': "MicrosoftAzureServicePrincipal",
            'MICROSOFTAZUREENTERPRISEAGREEMENT': "MicrosoftAzureEnterpriseAgreement",
            'DELLCOMPELLENT': "DellCompellent",
            'HPE3PAR': "HPE3Par",
            'REDHATENTERPRISEVIRTUALIZATION': "RedHatEnterpriseVirtualization",
            'NUTANIXACROPOLIS': "NutanixAcropolis",
            'HPEONEVIEW': "HPEOneView",
            'SERVICEENGINE': "ServiceEngine",
            'HITACHIVIRTUALSTORAGEPLATFORM': "HitachiVirtualStoragePlatform",
            'IMCBLADE': "IMCBlade",
            'TERRAFORMCLOUD': "TerraformCloud",
            'TERRAFORMAGENT': "TerraformAgent",
            'CUSTOMTARGET': "CustomTarget",
            'ANSIBLEENDPOINT': "AnsibleEndpoint",
            'HTTPENDPOINT': "HTTPEndpoint",
            'SSHENDPOINT': "SSHEndpoint",
            'CISCOCATALYST': "CiscoCatalyst",
            'POWERSHELLENDPOINT': "PowerShellEndpoint",
        },
        ('service_category',): {
            'COMPUTE': "Compute",
            'STORAGE': "Storage",
            'DATABASE': "Database",
            'NETWORK': "Network",
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
            'iops_unit': (str,),  # noqa: E501
            'is_bootable': (bool,),  # noqa: E501
            'is_default': (bool,),  # noqa: E501
            'is_provisioned_iops': (bool,),  # noqa: E501
            'max_iops': (float,),  # noqa: E501
            'max_read_iops': (float,),  # noqa: E501
            'max_read_throughput': (float,),  # noqa: E501
            'max_throughput': (float,),  # noqa: E501
            'max_volume_size': (float,),  # noqa: E501
            'max_write_iops': (float,),  # noqa: E501
            'max_write_throughput': (float,),  # noqa: E501
            'min_volume_size': (float,),  # noqa: E501
            'throughput_unit': (str,),  # noqa: E501
            'type': (str,),  # noqa: E501
            'volume_size_unit': (str,),  # noqa: E501
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
            'custom_attributes': ([CloudCustomAttributes], none_type,),  # noqa: E501
            'description': (str,),  # noqa: E501
            'is_active': (bool,),  # noqa: E501
            'is_auto_discovered': (bool,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'platform_type': (str,),  # noqa: E501
            'service_category': (str,),  # noqa: E501
            'service_family': (str,),  # noqa: E501
            'service_name': (str,),  # noqa: E501
            'target': (AssetTargetRelationship,),  # noqa: E501
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
        'iops_unit': 'IopsUnit',  # noqa: E501
        'is_bootable': 'IsBootable',  # noqa: E501
        'is_default': 'IsDefault',  # noqa: E501
        'is_provisioned_iops': 'IsProvisionedIops',  # noqa: E501
        'max_iops': 'MaxIops',  # noqa: E501
        'max_read_iops': 'MaxReadIops',  # noqa: E501
        'max_read_throughput': 'MaxReadThroughput',  # noqa: E501
        'max_throughput': 'MaxThroughput',  # noqa: E501
        'max_volume_size': 'MaxVolumeSize',  # noqa: E501
        'max_write_iops': 'MaxWriteIops',  # noqa: E501
        'max_write_throughput': 'MaxWriteThroughput',  # noqa: E501
        'min_volume_size': 'MinVolumeSize',  # noqa: E501
        'throughput_unit': 'ThroughputUnit',  # noqa: E501
        'type': 'Type',  # noqa: E501
        'volume_size_unit': 'VolumeSizeUnit',  # noqa: E501
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
        'custom_attributes': 'CustomAttributes',  # noqa: E501
        'description': 'Description',  # noqa: E501
        'is_active': 'IsActive',  # noqa: E501
        'is_auto_discovered': 'IsAutoDiscovered',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'platform_type': 'PlatformType',  # noqa: E501
        'service_category': 'ServiceCategory',  # noqa: E501
        'service_family': 'ServiceFamily',  # noqa: E501
        'service_name': 'ServiceName',  # noqa: E501
        'target': 'Target',  # noqa: E501
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
        """CloudSkuVolumeType - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "cloud.SkuVolumeType", must be one of ["cloud.SkuVolumeType", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "cloud.SkuVolumeType", must be one of ["cloud.SkuVolumeType", ]  # noqa: E501
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
            iops_unit (str): The units to measure IOPS.. [optional]  # noqa: E501
            is_bootable (bool): Indicates if this volume can be used as a boot volume.. [optional]  # noqa: E501
            is_default (bool): Flag to indicate if this is a default volume. Default volumes will be used when an instance type is launched unless another volume type is specified.. [optional]  # noqa: E501
            is_provisioned_iops (bool): Indicates if this volume type supports provisioned IOPS.. [optional]  # noqa: E501
            max_iops (float): The max I/O operations per second that this volume type supports. Read or write numbers does not go beyond this value.. [optional]  # noqa: E501
            max_read_iops (float): The maximum read IOPS that this volume type supports.. [optional]  # noqa: E501
            max_read_throughput (float): The maximum read throughput limit for this volume type.. [optional]  # noqa: E501
            max_throughput (float): The maximum throughput limit for this volume type.. [optional]  # noqa: E501
            max_volume_size (float): The maximum storage size that this volume type supports.. [optional]  # noqa: E501
            max_write_iops (float): The maximum write IOPS that this volume type supports.. [optional]  # noqa: E501
            max_write_throughput (float): The maximum write throughput limit for this volume type.. [optional]  # noqa: E501
            min_volume_size (float): The minimum storage size that this volume type supports.. [optional]  # noqa: E501
            throughput_unit (str): The units for measuring throughput.. [optional]  # noqa: E501
            type (str): The volume type like gp2 or st1.. [optional]  # noqa: E501
            volume_size_unit (str): The units for measuring volume size.. [optional]  # noqa: E501
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
            custom_attributes ([CloudCustomAttributes], none_type): [optional]  # noqa: E501
            description (str): Any additional description for the instance type.. [optional]  # noqa: E501
            is_active (bool): Flag to indicate if this SKU is active or not.. [optional] if omitted the server will use the default value of True  # noqa: E501
            is_auto_discovered (bool): Flag to indicate if SKU is discovered during inventory collection.. [optional]  # noqa: E501
            name (str): The display name for instance type.. [optional]  # noqa: E501
            platform_type (str): The platformType for this SKU. * `` - The device reported an empty or unrecognized platform type. * `APIC` - An Application Policy Infrastructure Controller cluster. * `DCNM` - A Data Center Network Manager instance. Data Center Network Manager (DCNM) is the network management platform for all NX-OS-enabled deployments, spanning new fabric architectures, IP Fabric for Media, and storage networking deployments for the Cisco Nexus-powered data center. * `UCSFI` - A UCS Fabric Interconnect in HA or standalone mode, which is being managed by UCS Manager (UCSM). * `UCSFIISM` - A UCS Fabric Interconnect in HA or standalone mode, managed directly by Intersight. * `IMC` - A standalone UCS Server Integrated Management Controller. * `IMCM4` - A standalone UCS M4 Server. * `IMCM5` - A standalone UCS M5 server. * `IMCRack` - A standalone UCS M6 and above server. * `UCSIOM` - An UCS Chassis IO module. * `HX` - A HyperFlex storage controller. * `HyperFlexAP` - A HyperFlex Application Platform. * `IWE` - An Intersight Workload Engine. * `UCSD` - A UCS Director virtual appliance. Cisco UCS Director automates, orchestrates, and manages Cisco and third-party hardware. * `IntersightAppliance` - A Cisco Intersight Connected Virtual Appliance. * `IntersightAssist` - A Cisco Intersight Assist. * `PureStorageFlashArray` - A Pure Storage FlashArray device. * `NexusDevice` - A generic platform type to support Nexus Network Device. This can also be extended to support all network devices later on. * `UCSC890` - A standalone Cisco UCSC890 server. * `NetAppOntap` - A NetApp ONTAP storage system. * `NetAppActiveIqUnifiedManager` - A NetApp Active IQ Unified Manager. * `EmcScaleIo` - An EMC ScaleIO storage system. * `EmcVmax` - An EMC VMAX storage system. * `EmcVplex` - An EMC VPLEX storage system. * `EmcXtremIo` - An EMC XtremIO storage system. * `VmwareVcenter` - A VMware vCenter device that manages Virtual Machines. * `MicrosoftHyperV` - A Microsoft Hyper-V system that manages Virtual Machines. * `AppDynamics` - An AppDynamics controller that monitors applications. * `Dynatrace` - A software-intelligence monitoring platform that simplifies enterprise cloud complexity and accelerates digital transformation. * `NewRelic` - A software-intelligence monitoring platform that simplifies enterprise cloud complexity and accelerates digital transformation. * `ServiceNow` - A cloud-based workflow automation platform that enables enterprise organizations to improve operational efficiencies by streamlining and automating routine work tasks. * `ReadHatOpenStack` - An OpenStack target manages Virtual Machines, Physical Machines, Datacenters and Virtual Datacenters using different OpenStack services as administrative endpoints. * `CloudFoundry` - An open source cloud platform on which developers can build, deploy, run and scale applications. * `MicrosoftAzureApplicationInsights` - A feature of Azure Monitor, is an extensible Application Performance Management service for developers and DevOps professionals to monitor their live applications. * `OpenStack` - An OpenStack target manages Virtual Machines, Physical Machines, Datacenters and Virtual Datacenters using different OpenStack services as administrative endpoints. * `MicrosoftSqlServer` - A Microsoft SQL database server. * `Kubernetes` - A Kubernetes cluster that runs containerized applications. * `AmazonWebService` - A Amazon web service target that discovers and monitors different services like EC2. It discovers entities like VMs, Volumes, regions etc. and monitors attributes like Mem, CPU, cost. * `AmazonWebServiceBilling` - A Amazon web service billing target to retrieve billing information stored in S3 bucket. * `MicrosoftAzureServicePrincipal` - A Microsoft Azure Service Principal target that discovers all the associated Azure subscriptions. * `MicrosoftAzureEnterpriseAgreement` - A Microsoft Azure Enterprise Agreement target that discovers cost, billing and RIs. * `DellCompellent` - A Dell Compellent storage system. * `HPE3Par` - A HPE 3PAR storage system. * `RedHatEnterpriseVirtualization` - A Red Hat Enterprise Virtualization Hypervisor system that manages Virtual Machines. * `NutanixAcropolis` - A Nutanix Acropolis system that combines servers and storage into a distributed infrastructure platform. * `HPEOneView` - A HPE Oneview management system that manages compute, storage, and networking. * `ServiceEngine` - Cisco Application Services Engine. Cisco Application Services Engine is a platform to deploy and manage applications. * `HitachiVirtualStoragePlatform` - A Hitachi Virtual Storage Platform also referred to as Hitachi VSP. It includes various storage systems designed for data centers. * `IMCBlade` - An Intersight managed UCS Blade Server. * `TerraformCloud` - A Terraform Cloud account. * `TerraformAgent` - A Terraform Cloud Agent that Intersight will deploy in datacenter. The agent will execute Terraform plan for Terraform Cloud workspace configured to use the agent. * `CustomTarget` - An external endpoint added as Target that can be accessed through its HTTP API interface in Intersight Orchestrator automation workflow.Standard HTTP authentication scheme supported: Basic. * `AnsibleEndpoint` - An external endpoint added as Target that can be accessed through Ansible in Intersight Cloud Orchestrator automation workflow. * `HTTPEndpoint` - An external endpoint added as Target that can be accessed through its HTTP API interface in Intersight Orchestrator automation workflow.Standard HTTP authentication scheme supported: Basic, Bearer Token. * `SSHEndpoint` - An external endpoint added as Target that can be accessed through SSH in Intersight Cloud Orchestrator automation workflow. * `CiscoCatalyst` - A Cisco Catalyst networking switch device. * `PowerShellEndpoint` - A Windows machine on which PowerShell scripts can be executed remotely.. [optional] if omitted the server will use the default value of ""  # noqa: E501
            service_category (str): Indicates if this sku belongs to Compute, Storage, Database or Network category. * `Compute` - Compute service offered by cloud provider. * `Storage` - Storage service offered by cloud provider. * `Database` - Database service offered by cloud provider. * `Network` - Network service offered by cloud provider.. [optional] if omitted the server will use the default value of "Compute"  # noqa: E501
            service_family (str): Property to identify the family of service that the sku belongs to.. [optional]  # noqa: E501
            service_name (str): Any display name for the ServiceCategory if available.. [optional]  # noqa: E501
            target (AssetTargetRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "cloud.SkuVolumeType")
        object_type = kwargs.get('object_type', "cloud.SkuVolumeType")
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
              CloudBaseSku,
              CloudSkuVolumeTypeAllOf,
          ],
          'oneOf': [
          ],
        }
