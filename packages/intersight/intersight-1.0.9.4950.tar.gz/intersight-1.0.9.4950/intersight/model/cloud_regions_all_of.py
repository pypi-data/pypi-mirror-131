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
    globals()['AssetTargetRelationship'] = AssetTargetRelationship


class CloudRegionsAllOf(ModelNormal):
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
            'CLOUD.REGIONS': "cloud.Regions",
        },
        ('object_type',): {
            'CLOUD.REGIONS': "cloud.Regions",
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
            'alternate_names': ([str], none_type,),  # noqa: E501
            'default_zone': (str,),  # noqa: E501
            'group': (str,),  # noqa: E501
            'is_active': (bool,),  # noqa: E501
            'is_billing_only': (bool,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'platform_type': (str,),  # noqa: E501
            'region_end_point': (str,),  # noqa: E501
            'region_id': (str,),  # noqa: E501
            'zones': ([str], none_type,),  # noqa: E501
            'target': (AssetTargetRelationship,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'class_id': 'ClassId',  # noqa: E501
        'object_type': 'ObjectType',  # noqa: E501
        'alternate_names': 'AlternateNames',  # noqa: E501
        'default_zone': 'DefaultZone',  # noqa: E501
        'group': 'Group',  # noqa: E501
        'is_active': 'IsActive',  # noqa: E501
        'is_billing_only': 'IsBillingOnly',  # noqa: E501
        'name': 'Name',  # noqa: E501
        'platform_type': 'PlatformType',  # noqa: E501
        'region_end_point': 'RegionEndPoint',  # noqa: E501
        'region_id': 'RegionId',  # noqa: E501
        'zones': 'Zones',  # noqa: E501
        'target': 'Target',  # noqa: E501
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
        """CloudRegionsAllOf - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "cloud.Regions", must be one of ["cloud.Regions", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "cloud.Regions", must be one of ["cloud.Regions", ]  # noqa: E501
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
            alternate_names ([str], none_type): [optional]  # noqa: E501
            default_zone (str): The default zone for this region.. [optional]  # noqa: E501
            group (str): Property to identify regions in same category which shares credentials. For e.g. AWS Govcloud Vs AWS Global Vs AWS China.. [optional]  # noqa: E501
            is_active (bool): Flag to indicate of this region is active or not.. [optional] if omitted the server will use the default value of True  # noqa: E501
            is_billing_only (bool): Property to pick regions for orchestration.. [optional]  # noqa: E501
            name (str): The display name of the region.. [optional]  # noqa: E501
            platform_type (str): The platform type for this region. For e.g. AmazonWebService. * `` - The device reported an empty or unrecognized platform type. * `APIC` - An Application Policy Infrastructure Controller cluster. * `DCNM` - A Data Center Network Manager instance. Data Center Network Manager (DCNM) is the network management platform for all NX-OS-enabled deployments, spanning new fabric architectures, IP Fabric for Media, and storage networking deployments for the Cisco Nexus-powered data center. * `UCSFI` - A UCS Fabric Interconnect in HA or standalone mode, which is being managed by UCS Manager (UCSM). * `UCSFIISM` - A UCS Fabric Interconnect in HA or standalone mode, managed directly by Intersight. * `IMC` - A standalone UCS Server Integrated Management Controller. * `IMCM4` - A standalone UCS M4 Server. * `IMCM5` - A standalone UCS M5 server. * `IMCRack` - A standalone UCS M6 and above server. * `UCSIOM` - An UCS Chassis IO module. * `HX` - A HyperFlex storage controller. * `HyperFlexAP` - A HyperFlex Application Platform. * `IWE` - An Intersight Workload Engine. * `UCSD` - A UCS Director virtual appliance. Cisco UCS Director automates, orchestrates, and manages Cisco and third-party hardware. * `IntersightAppliance` - A Cisco Intersight Connected Virtual Appliance. * `IntersightAssist` - A Cisco Intersight Assist. * `PureStorageFlashArray` - A Pure Storage FlashArray device. * `NexusDevice` - A generic platform type to support Nexus Network Device. This can also be extended to support all network devices later on. * `UCSC890` - A standalone Cisco UCSC890 server. * `NetAppOntap` - A NetApp ONTAP storage system. * `NetAppActiveIqUnifiedManager` - A NetApp Active IQ Unified Manager. * `EmcScaleIo` - An EMC ScaleIO storage system. * `EmcVmax` - An EMC VMAX storage system. * `EmcVplex` - An EMC VPLEX storage system. * `EmcXtremIo` - An EMC XtremIO storage system. * `VmwareVcenter` - A VMware vCenter device that manages Virtual Machines. * `MicrosoftHyperV` - A Microsoft Hyper-V system that manages Virtual Machines. * `AppDynamics` - An AppDynamics controller that monitors applications. * `Dynatrace` - A software-intelligence monitoring platform that simplifies enterprise cloud complexity and accelerates digital transformation. * `NewRelic` - A software-intelligence monitoring platform that simplifies enterprise cloud complexity and accelerates digital transformation. * `ServiceNow` - A cloud-based workflow automation platform that enables enterprise organizations to improve operational efficiencies by streamlining and automating routine work tasks. * `ReadHatOpenStack` - An OpenStack target manages Virtual Machines, Physical Machines, Datacenters and Virtual Datacenters using different OpenStack services as administrative endpoints. * `CloudFoundry` - An open source cloud platform on which developers can build, deploy, run and scale applications. * `MicrosoftAzureApplicationInsights` - A feature of Azure Monitor, is an extensible Application Performance Management service for developers and DevOps professionals to monitor their live applications. * `OpenStack` - An OpenStack target manages Virtual Machines, Physical Machines, Datacenters and Virtual Datacenters using different OpenStack services as administrative endpoints. * `MicrosoftSqlServer` - A Microsoft SQL database server. * `Kubernetes` - A Kubernetes cluster that runs containerized applications. * `AmazonWebService` - A Amazon web service target that discovers and monitors different services like EC2. It discovers entities like VMs, Volumes, regions etc. and monitors attributes like Mem, CPU, cost. * `AmazonWebServiceBilling` - A Amazon web service billing target to retrieve billing information stored in S3 bucket. * `MicrosoftAzureServicePrincipal` - A Microsoft Azure Service Principal target that discovers all the associated Azure subscriptions. * `MicrosoftAzureEnterpriseAgreement` - A Microsoft Azure Enterprise Agreement target that discovers cost, billing and RIs. * `DellCompellent` - A Dell Compellent storage system. * `HPE3Par` - A HPE 3PAR storage system. * `RedHatEnterpriseVirtualization` - A Red Hat Enterprise Virtualization Hypervisor system that manages Virtual Machines. * `NutanixAcropolis` - A Nutanix Acropolis system that combines servers and storage into a distributed infrastructure platform. * `HPEOneView` - A HPE Oneview management system that manages compute, storage, and networking. * `ServiceEngine` - Cisco Application Services Engine. Cisco Application Services Engine is a platform to deploy and manage applications. * `HitachiVirtualStoragePlatform` - A Hitachi Virtual Storage Platform also referred to as Hitachi VSP. It includes various storage systems designed for data centers. * `IMCBlade` - An Intersight managed UCS Blade Server. * `TerraformCloud` - A Terraform Cloud account. * `TerraformAgent` - A Terraform Cloud Agent that Intersight will deploy in datacenter. The agent will execute Terraform plan for Terraform Cloud workspace configured to use the agent. * `CustomTarget` - An external endpoint added as Target that can be accessed through its HTTP API interface in Intersight Orchestrator automation workflow.Standard HTTP authentication scheme supported: Basic. * `AnsibleEndpoint` - An external endpoint added as Target that can be accessed through Ansible in Intersight Cloud Orchestrator automation workflow. * `HTTPEndpoint` - An external endpoint added as Target that can be accessed through its HTTP API interface in Intersight Orchestrator automation workflow.Standard HTTP authentication scheme supported: Basic, Bearer Token. * `SSHEndpoint` - An external endpoint added as Target that can be accessed through SSH in Intersight Cloud Orchestrator automation workflow. * `CiscoCatalyst` - A Cisco Catalyst networking switch device. * `PowerShellEndpoint` - A Windows machine on which PowerShell scripts can be executed remotely.. [optional] if omitted the server will use the default value of ""  # noqa: E501
            region_end_point (str): HTTP endpoint of the region. For example https://ec2.us-east-2.amazonaws.com.. [optional]  # noqa: E501
            region_id (str): The region Id which is assigned by the cloud provider. For e.g. us-east-1.. [optional]  # noqa: E501
            zones ([str], none_type): [optional]  # noqa: E501
            target (AssetTargetRelationship): [optional]  # noqa: E501
        """

        class_id = kwargs.get('class_id', "cloud.Regions")
        object_type = kwargs.get('object_type', "cloud.Regions")
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
