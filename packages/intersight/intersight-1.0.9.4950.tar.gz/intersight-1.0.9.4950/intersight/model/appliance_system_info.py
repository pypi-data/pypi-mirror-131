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
    from intersight.model.appliance_system_info_all_of import ApplianceSystemInfoAllOf
    from intersight.model.display_names import DisplayNames
    from intersight.model.mo_base_mo import MoBaseMo
    from intersight.model.mo_base_mo_relationship import MoBaseMoRelationship
    from intersight.model.mo_tag import MoTag
    from intersight.model.mo_version_context import MoVersionContext
    globals()['ApplianceSystemInfoAllOf'] = ApplianceSystemInfoAllOf
    globals()['DisplayNames'] = DisplayNames
    globals()['MoBaseMo'] = MoBaseMo
    globals()['MoBaseMoRelationship'] = MoBaseMoRelationship
    globals()['MoTag'] = MoTag
    globals()['MoVersionContext'] = MoVersionContext


class ApplianceSystemInfo(ModelComposed):
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
            'APPLIANCE.SYSTEMINFO': "appliance.SystemInfo",
        },
        ('object_type',): {
            'APPLIANCE.SYSTEMINFO': "appliance.SystemInfo",
        },
        ('cloud_conn_status',): {
            'EMPTY': "",
            'CONNECTED': "Connected",
            'NOTCONNECTED': "NotConnected",
            'CLAIMINPROGRESS': "ClaimInProgress",
            'UNCLAIMED': "Unclaimed",
            'CLAIMED': "Claimed",
        },
        ('operational_status',): {
            'UNKNOWN': "Unknown",
            'OPERATIONAL': "Operational",
            'IMPAIRED': "Impaired",
            'ATTENTIONNEEDED': "AttentionNeeded",
        },
        ('time_zone',): {
            'PACIFIC/NIUE': "Pacific/Niue",
            'PACIFIC/PAGO_PAGO': "Pacific/Pago_Pago",
            'PACIFIC/HONOLULU': "Pacific/Honolulu",
            'PACIFIC/RAROTONGA': "Pacific/Rarotonga",
            'PACIFIC/TAHITI': "Pacific/Tahiti",
            'PACIFIC/MARQUESAS': "Pacific/Marquesas",
            'AMERICA/ANCHORAGE': "America/Anchorage",
            'PACIFIC/GAMBIER': "Pacific/Gambier",
            'AMERICA/LOS_ANGELES': "America/Los_Angeles",
            'AMERICA/TIJUANA': "America/Tijuana",
            'AMERICA/VANCOUVER': "America/Vancouver",
            'AMERICA/WHITEHORSE': "America/Whitehorse",
            'PACIFIC/PITCAIRN': "Pacific/Pitcairn",
            'AMERICA/DAWSON_CREEK': "America/Dawson_Creek",
            'AMERICA/DENVER': "America/Denver",
            'AMERICA/EDMONTON': "America/Edmonton",
            'AMERICA/HERMOSILLO': "America/Hermosillo",
            'AMERICA/MAZATLAN': "America/Mazatlan",
            'AMERICA/PHOENIX': "America/Phoenix",
            'AMERICA/YELLOWKNIFE': "America/Yellowknife",
            'AMERICA/BELIZE': "America/Belize",
            'AMERICA/CHICAGO': "America/Chicago",
            'AMERICA/COSTA_RICA': "America/Costa_Rica",
            'AMERICA/EL_SALVADOR': "America/El_Salvador",
            'AMERICA/GUATEMALA': "America/Guatemala",
            'AMERICA/MANAGUA': "America/Managua",
            'AMERICA/MEXICO_CITY': "America/Mexico_City",
            'AMERICA/REGINA': "America/Regina",
            'AMERICA/TEGUCIGALPA': "America/Tegucigalpa",
            'AMERICA/WINNIPEG': "America/Winnipeg",
            'PACIFIC/GALAPAGOS': "Pacific/Galapagos",
            'AMERICA/BOGOTA': "America/Bogota",
            'AMERICA/CANCUN': "America/Cancun",
            'AMERICA/CAYMAN': "America/Cayman",
            'AMERICA/GUAYAQUIL': "America/Guayaquil",
            'AMERICA/HAVANA': "America/Havana",
            'AMERICA/IQALUIT': "America/Iqaluit",
            'AMERICA/JAMAICA': "America/Jamaica",
            'AMERICA/LIMA': "America/Lima",
            'AMERICA/NASSAU': "America/Nassau",
            'AMERICA/NEW_YORK': "America/New_York",
            'AMERICA/PANAMA': "America/Panama",
            'AMERICA/PORT-AU-PRINCE': "America/Port-au-Prince",
            'AMERICA/RIO_BRANCO': "America/Rio_Branco",
            'AMERICA/TORONTO': "America/Toronto",
            'PACIFIC/EASTER': "Pacific/Easter",
            'AMERICA/CARACAS': "America/Caracas",
            'AMERICA/ASUNCION': "America/Asuncion",
            'AMERICA/BARBADOS': "America/Barbados",
            'AMERICA/BOA_VISTA': "America/Boa_Vista",
            'AMERICA/CAMPO_GRANDE': "America/Campo_Grande",
            'AMERICA/CUIABA': "America/Cuiaba",
            'AMERICA/CURACAO': "America/Curacao",
            'AMERICA/GRAND_TURK': "America/Grand_Turk",
            'AMERICA/GUYANA': "America/Guyana",
            'AMERICA/HALIFAX': "America/Halifax",
            'AMERICA/LA_PAZ': "America/La_Paz",
            'AMERICA/MANAUS': "America/Manaus",
            'AMERICA/MARTINIQUE': "America/Martinique",
            'AMERICA/PORT_OF_SPAIN': "America/Port_of_Spain",
            'AMERICA/PORTO_VELHO': "America/Porto_Velho",
            'AMERICA/PUERTO_RICO': "America/Puerto_Rico",
            'AMERICA/SANTO_DOMINGO': "America/Santo_Domingo",
            'AMERICA/THULE': "America/Thule",
            'ATLANTIC/BERMUDA': "Atlantic/Bermuda",
            'AMERICA/ST_JOHNS': "America/St_Johns",
            'AMERICA/ARAGUAINA': "America/Araguaina",
            'AMERICA/ARGENTINA/BUENOS_AIRES': "America/Argentina/Buenos_Aires",
            'AMERICA/BAHIA': "America/Bahia",
            'AMERICA/BELEM': "America/Belem",
            'AMERICA/CAYENNE': "America/Cayenne",
            'AMERICA/FORTALEZA': "America/Fortaleza",
            'AMERICA/GODTHAB': "America/Godthab",
            'AMERICA/MACEIO': "America/Maceio",
            'AMERICA/MIQUELON': "America/Miquelon",
            'AMERICA/MONTEVIDEO': "America/Montevideo",
            'AMERICA/PARAMARIBO': "America/Paramaribo",
            'AMERICA/RECIFE': "America/Recife",
            'AMERICA/SANTIAGO': "America/Santiago",
            'AMERICA/SAO_PAULO': "America/Sao_Paulo",
            'ANTARCTICA/PALMER': "Antarctica/Palmer",
            'ANTARCTICA/ROTHERA': "Antarctica/Rothera",
            'ATLANTIC/STANLEY': "Atlantic/Stanley",
            'AMERICA/NORONHA': "America/Noronha",
            'ATLANTIC/SOUTH_GEORGIA': "Atlantic/South_Georgia",
            'AMERICA/SCORESBYSUND': "America/Scoresbysund",
            'ATLANTIC/AZORES': "Atlantic/Azores",
            'ATLANTIC/CAPE_VERDE': "Atlantic/Cape_Verde",
            'AFRICA/ABIDJAN': "Africa/Abidjan",
            'AFRICA/ACCRA': "Africa/Accra",
            'AFRICA/BISSAU': "Africa/Bissau",
            'AFRICA/CASABLANCA': "Africa/Casablanca",
            'AFRICA/EL_AAIUN': "Africa/El_Aaiun",
            'AFRICA/MONROVIA': "Africa/Monrovia",
            'AMERICA/DANMARKSHAVN': "America/Danmarkshavn",
            'ATLANTIC/CANARY': "Atlantic/Canary",
            'ATLANTIC/FAROE': "Atlantic/Faroe",
            'ATLANTIC/REYKJAVIK': "Atlantic/Reykjavik",
            'ETC/GMT': "Etc/GMT",
            'EUROPE/DUBLIN': "Europe/Dublin",
            'EUROPE/LISBON': "Europe/Lisbon",
            'EUROPE/LONDON': "Europe/London",
            'AFRICA/ALGIERS': "Africa/Algiers",
            'AFRICA/CEUTA': "Africa/Ceuta",
            'AFRICA/LAGOS': "Africa/Lagos",
            'AFRICA/NDJAMENA': "Africa/Ndjamena",
            'AFRICA/TUNIS': "Africa/Tunis",
            'AFRICA/WINDHOEK': "Africa/Windhoek",
            'EUROPE/AMSTERDAM': "Europe/Amsterdam",
            'EUROPE/ANDORRA': "Europe/Andorra",
            'EUROPE/BELGRADE': "Europe/Belgrade",
            'EUROPE/BERLIN': "Europe/Berlin",
            'EUROPE/BRUSSELS': "Europe/Brussels",
            'EUROPE/BUDAPEST': "Europe/Budapest",
            'EUROPE/COPENHAGEN': "Europe/Copenhagen",
            'EUROPE/GIBRALTAR': "Europe/Gibraltar",
            'EUROPE/LUXEMBOURG': "Europe/Luxembourg",
            'EUROPE/MADRID': "Europe/Madrid",
            'EUROPE/MALTA': "Europe/Malta",
            'EUROPE/MONACO': "Europe/Monaco",
            'EUROPE/OSLO': "Europe/Oslo",
            'EUROPE/PARIS': "Europe/Paris",
            'EUROPE/PRAGUE': "Europe/Prague",
            'EUROPE/ROME': "Europe/Rome",
            'EUROPE/STOCKHOLM': "Europe/Stockholm",
            'EUROPE/TIRANE': "Europe/Tirane",
            'EUROPE/VIENNA': "Europe/Vienna",
            'EUROPE/WARSAW': "Europe/Warsaw",
            'EUROPE/ZURICH': "Europe/Zurich",
            'AFRICA/CAIRO': "Africa/Cairo",
            'AFRICA/JOHANNESBURG': "Africa/Johannesburg",
            'AFRICA/MAPUTO': "Africa/Maputo",
            'AFRICA/TRIPOLI': "Africa/Tripoli",
            'ASIA/AMMAN': "Asia/Amman",
            'ASIA/BEIRUT': "Asia/Beirut",
            'ASIA/DAMASCUS': "Asia/Damascus",
            'ASIA/GAZA': "Asia/Gaza",
            'ASIA/JERUSALEM': "Asia/Jerusalem",
            'ASIA/NICOSIA': "Asia/Nicosia",
            'EUROPE/ATHENS': "Europe/Athens",
            'EUROPE/BUCHAREST': "Europe/Bucharest",
            'EUROPE/CHISINAU': "Europe/Chisinau",
            'EUROPE/HELSINKI': "Europe/Helsinki",
            'EUROPE/ISTANBUL': "Europe/Istanbul",
            'EUROPE/KALININGRAD': "Europe/Kaliningrad",
            'EUROPE/KIEV': "Europe/Kiev",
            'EUROPE/RIGA': "Europe/Riga",
            'EUROPE/SOFIA': "Europe/Sofia",
            'EUROPE/TALLINN': "Europe/Tallinn",
            'EUROPE/VILNIUS': "Europe/Vilnius",
            'AFRICA/KHARTOUM': "Africa/Khartoum",
            'AFRICA/NAIROBI': "Africa/Nairobi",
            'ANTARCTICA/SYOWA': "Antarctica/Syowa",
            'ASIA/BAGHDAD': "Asia/Baghdad",
            'ASIA/QATAR': "Asia/Qatar",
            'ASIA/RIYADH': "Asia/Riyadh",
            'EUROPE/MINSK': "Europe/Minsk",
            'EUROPE/MOSCOW': "Europe/Moscow",
            'ASIA/TEHRAN': "Asia/Tehran",
            'ASIA/BAKU': "Asia/Baku",
            'ASIA/DUBAI': "Asia/Dubai",
            'ASIA/TBILISI': "Asia/Tbilisi",
            'ASIA/YEREVAN': "Asia/Yerevan",
            'EUROPE/SAMARA': "Europe/Samara",
            'INDIAN/MAHE': "Indian/Mahe",
            'INDIAN/MAURITIUS': "Indian/Mauritius",
            'INDIAN/REUNION': "Indian/Reunion",
            'ASIA/KABUL': "Asia/Kabul",
            'ANTARCTICA/MAWSON': "Antarctica/Mawson",
            'ASIA/AQTAU': "Asia/Aqtau",
            'ASIA/AQTOBE': "Asia/Aqtobe",
            'ASIA/ASHGABAT': "Asia/Ashgabat",
            'ASIA/DUSHANBE': "Asia/Dushanbe",
            'ASIA/KARACHI': "Asia/Karachi",
            'ASIA/TASHKENT': "Asia/Tashkent",
            'ASIA/YEKATERINBURG': "Asia/Yekaterinburg",
            'INDIAN/KERGUELEN': "Indian/Kerguelen",
            'INDIAN/MALDIVES': "Indian/Maldives",
            'ASIA/CALCUTTA': "Asia/Calcutta",
            'ASIA/KOLKATA': "Asia/Kolkata",
            'ASIA/COLOMBO': "Asia/Colombo",
            'ASIA/KATMANDU': "Asia/Katmandu",
            'ANTARCTICA/VOSTOK': "Antarctica/Vostok",
            'ASIA/ALMATY': "Asia/Almaty",
            'ASIA/BISHKEK': "Asia/Bishkek",
            'ASIA/DHAKA': "Asia/Dhaka",
            'ASIA/OMSK': "Asia/Omsk",
            'ASIA/THIMPHU': "Asia/Thimphu",
            'INDIAN/CHAGOS': "Indian/Chagos",
            'ASIA/RANGOON': "Asia/Rangoon",
            'INDIAN/COCOS': "Indian/Cocos",
            'ANTARCTICA/DAVIS': "Antarctica/Davis",
            'ASIA/BANGKOK': "Asia/Bangkok",
            'ASIA/HOVD': "Asia/Hovd",
            'ASIA/JAKARTA': "Asia/Jakarta",
            'ASIA/KRASNOYARSK': "Asia/Krasnoyarsk",
            'ASIA/SAIGON': "Asia/Saigon",
            'INDIAN/CHRISTMAS': "Indian/Christmas",
            'ANTARCTICA/CASEY': "Antarctica/Casey",
            'ASIA/BRUNEI': "Asia/Brunei",
            'ASIA/CHOIBALSAN': "Asia/Choibalsan",
            'ASIA/HONG_KONG': "Asia/Hong_Kong",
            'ASIA/IRKUTSK': "Asia/Irkutsk",
            'ASIA/KUALA_LUMPUR': "Asia/Kuala_Lumpur",
            'ASIA/MACAU': "Asia/Macau",
            'ASIA/MAKASSAR': "Asia/Makassar",
            'ASIA/MANILA': "Asia/Manila",
            'ASIA/SHANGHAI': "Asia/Shanghai",
            'ASIA/SINGAPORE': "Asia/Singapore",
            'ASIA/TAIPEI': "Asia/Taipei",
            'ASIA/ULAANBAATAR': "Asia/Ulaanbaatar",
            'AUSTRALIA/PERTH': "Australia/Perth",
            'ASIA/PYONGYANG': "Asia/Pyongyang",
            'ASIA/DILI': "Asia/Dili",
            'ASIA/JAYAPURA': "Asia/Jayapura",
            'ASIA/SEOUL': "Asia/Seoul",
            'ASIA/TOKYO': "Asia/Tokyo",
            'ASIA/YAKUTSK': "Asia/Yakutsk",
            'PACIFIC/PALAU': "Pacific/Palau",
            'AUSTRALIA/ADELAIDE': "Australia/Adelaide",
            'AUSTRALIA/DARWIN': "Australia/Darwin",
            'ANTARCTICA/DUMONTDURVILLE': "Antarctica/DumontDUrville",
            'ASIA/MAGADAN': "Asia/Magadan",
            'ASIA/VLADIVOSTOK': "Asia/Vladivostok",
            'AUSTRALIA/BRISBANE': "Australia/Brisbane",
            'AUSTRALIA/HOBART': "Australia/Hobart",
            'AUSTRALIA/SYDNEY': "Australia/Sydney",
            'PACIFIC/CHUUK': "Pacific/Chuuk",
            'PACIFIC/GUAM': "Pacific/Guam",
            'PACIFIC/PORT_MORESBY': "Pacific/Port_Moresby",
            'PACIFIC/EFATE': "Pacific/Efate",
            'PACIFIC/GUADALCANAL': "Pacific/Guadalcanal",
            'PACIFIC/KOSRAE': "Pacific/Kosrae",
            'PACIFIC/NORFOLK': "Pacific/Norfolk",
            'PACIFIC/NOUMEA': "Pacific/Noumea",
            'PACIFIC/POHNPEI': "Pacific/Pohnpei",
            'ASIA/KAMCHATKA': "Asia/Kamchatka",
            'PACIFIC/AUCKLAND': "Pacific/Auckland",
            'PACIFIC/FIJI': "Pacific/Fiji",
            'PACIFIC/FUNAFUTI': "Pacific/Funafuti",
            'PACIFIC/KWAJALEIN': "Pacific/Kwajalein",
            'PACIFIC/MAJURO': "Pacific/Majuro",
            'PACIFIC/NAURU': "Pacific/Nauru",
            'PACIFIC/TARAWA': "Pacific/Tarawa",
            'PACIFIC/WAKE': "Pacific/Wake",
            'PACIFIC/WALLIS': "Pacific/Wallis",
            'PACIFIC/APIA': "Pacific/Apia",
            'PACIFIC/ENDERBURY': "Pacific/Enderbury",
            'PACIFIC/FAKAOFO': "Pacific/Fakaofo",
            'PACIFIC/TONGATAPU': "Pacific/Tongatapu",
            'PACIFIC/KIRITIMATI': "Pacific/Kiritimati",
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
            'cloud_conn_status': (str,),  # noqa: E501
            'deployment_size': (str,),  # noqa: E501
            'hostname': (str,),  # noqa: E501
            'init_done': (bool,),  # noqa: E501
            'operational_status': (str,),  # noqa: E501
            'serial_id': (str,),  # noqa: E501
            'time_zone': (str,),  # noqa: E501
            'version': (str,),  # noqa: E501
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
        'cloud_conn_status': 'CloudConnStatus',  # noqa: E501
        'deployment_size': 'DeploymentSize',  # noqa: E501
        'hostname': 'Hostname',  # noqa: E501
        'init_done': 'InitDone',  # noqa: E501
        'operational_status': 'OperationalStatus',  # noqa: E501
        'serial_id': 'SerialId',  # noqa: E501
        'time_zone': 'TimeZone',  # noqa: E501
        'version': 'Version',  # noqa: E501
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
        """ApplianceSystemInfo - a model defined in OpenAPI

        Args:

        Keyword Args:
            class_id (str): The fully-qualified name of the instantiated, concrete type. This property is used as a discriminator to identify the type of the payload when marshaling and unmarshaling data.. defaults to "appliance.SystemInfo", must be one of ["appliance.SystemInfo", ]  # noqa: E501
            object_type (str): The fully-qualified name of the instantiated, concrete type. The value should be the same as the 'ClassId' property.. defaults to "appliance.SystemInfo", must be one of ["appliance.SystemInfo", ]  # noqa: E501
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
            cloud_conn_status (str): Connection state of the Intersight Appliance to the Intersight. * `` - The target details have been persisted but Intersight has not yet attempted to connect to the target. * `Connected` - Intersight is able to establish a connection to the target and initiate management activities. * `NotConnected` - Intersight is unable to establish a connection to the target. * `ClaimInProgress` - Claim of the target is in progress. A connection to the target has not been fully established. * `Unclaimed` - The device was un-claimed from the users account by an Administrator of the device. Also indicates the failure to claim Targets of type HTTP Endpoint in Intersight. * `Claimed` - Target of type HTTP Endpoint is successfully claimed in Intersight. Currently no validation is performed to verify the Target connectivity from Intersight at the time of creation. However invoking API from Intersight Orchestrator fails if this Target is not reachable from Intersight or if Target API credentials are incorrect.. [optional] if omitted the server will use the default value of ""  # noqa: E501
            deployment_size (str): Current running deployment size for the Intersight Appliance cluster. Eg. small, medium, large etc.. [optional]  # noqa: E501
            hostname (str): Publicly accessible FQDN or IP address of the Intersight Appliance.. [optional]  # noqa: E501
            init_done (bool): Indicates that the setup initialization process has been completed.. [optional]  # noqa: E501
            operational_status (str): Operational status of the Intersight Appliance cluster. * `Unknown` - Operational status of the Intersight Appliance entity is Unknown. * `Operational` - Operational status of the Intersight Appliance entity is Operational. * `Impaired` - Operational status of the Intersight Appliance entity is Impaired. * `AttentionNeeded` - Operational status of the Intersight Appliance entity is AttentionNeeded.. [optional] if omitted the server will use the default value of "Unknown"  # noqa: E501
            serial_id (str): SerialId of the Intersight Appliance. SerialId is generated when the Intersight Appliance is setup. It is a unique UUID string, and serialId will not change for the life time of the Intersight Appliance.. [optional]  # noqa: E501
            time_zone (str): Timezone of the Intersight Appliance. * `Pacific/Niue` -  * `Pacific/Pago_Pago` -  * `Pacific/Honolulu` -  * `Pacific/Rarotonga` -  * `Pacific/Tahiti` -  * `Pacific/Marquesas` -  * `America/Anchorage` -  * `Pacific/Gambier` -  * `America/Los_Angeles` -  * `America/Tijuana` -  * `America/Vancouver` -  * `America/Whitehorse` -  * `Pacific/Pitcairn` -  * `America/Dawson_Creek` -  * `America/Denver` -  * `America/Edmonton` -  * `America/Hermosillo` -  * `America/Mazatlan` -  * `America/Phoenix` -  * `America/Yellowknife` -  * `America/Belize` -  * `America/Chicago` -  * `America/Costa_Rica` -  * `America/El_Salvador` -  * `America/Guatemala` -  * `America/Managua` -  * `America/Mexico_City` -  * `America/Regina` -  * `America/Tegucigalpa` -  * `America/Winnipeg` -  * `Pacific/Galapagos` -  * `America/Bogota` -  * `America/Cancun` -  * `America/Cayman` -  * `America/Guayaquil` -  * `America/Havana` -  * `America/Iqaluit` -  * `America/Jamaica` -  * `America/Lima` -  * `America/Nassau` -  * `America/New_York` -  * `America/Panama` -  * `America/Port-au-Prince` -  * `America/Rio_Branco` -  * `America/Toronto` -  * `Pacific/Easter` -  * `America/Caracas` -  * `America/Asuncion` -  * `America/Barbados` -  * `America/Boa_Vista` -  * `America/Campo_Grande` -  * `America/Cuiaba` -  * `America/Curacao` -  * `America/Grand_Turk` -  * `America/Guyana` -  * `America/Halifax` -  * `America/La_Paz` -  * `America/Manaus` -  * `America/Martinique` -  * `America/Port_of_Spain` -  * `America/Porto_Velho` -  * `America/Puerto_Rico` -  * `America/Santo_Domingo` -  * `America/Thule` -  * `Atlantic/Bermuda` -  * `America/St_Johns` -  * `America/Araguaina` -  * `America/Argentina/Buenos_Aires` -  * `America/Bahia` -  * `America/Belem` -  * `America/Cayenne` -  * `America/Fortaleza` -  * `America/Godthab` -  * `America/Maceio` -  * `America/Miquelon` -  * `America/Montevideo` -  * `America/Paramaribo` -  * `America/Recife` -  * `America/Santiago` -  * `America/Sao_Paulo` -  * `Antarctica/Palmer` -  * `Antarctica/Rothera` -  * `Atlantic/Stanley` -  * `America/Noronha` -  * `Atlantic/South_Georgia` -  * `America/Scoresbysund` -  * `Atlantic/Azores` -  * `Atlantic/Cape_Verde` -  * `Africa/Abidjan` -  * `Africa/Accra` -  * `Africa/Bissau` -  * `Africa/Casablanca` -  * `Africa/El_Aaiun` -  * `Africa/Monrovia` -  * `America/Danmarkshavn` -  * `Atlantic/Canary` -  * `Atlantic/Faroe` -  * `Atlantic/Reykjavik` -  * `Etc/GMT` -  * `Europe/Dublin` -  * `Europe/Lisbon` -  * `Europe/London` -  * `Africa/Algiers` -  * `Africa/Ceuta` -  * `Africa/Lagos` -  * `Africa/Ndjamena` -  * `Africa/Tunis` -  * `Africa/Windhoek` -  * `Europe/Amsterdam` -  * `Europe/Andorra` -  * `Europe/Belgrade` -  * `Europe/Berlin` -  * `Europe/Brussels` -  * `Europe/Budapest` -  * `Europe/Copenhagen` -  * `Europe/Gibraltar` -  * `Europe/Luxembourg` -  * `Europe/Madrid` -  * `Europe/Malta` -  * `Europe/Monaco` -  * `Europe/Oslo` -  * `Europe/Paris` -  * `Europe/Prague` -  * `Europe/Rome` -  * `Europe/Stockholm` -  * `Europe/Tirane` -  * `Europe/Vienna` -  * `Europe/Warsaw` -  * `Europe/Zurich` -  * `Africa/Cairo` -  * `Africa/Johannesburg` -  * `Africa/Maputo` -  * `Africa/Tripoli` -  * `Asia/Amman` -  * `Asia/Beirut` -  * `Asia/Damascus` -  * `Asia/Gaza` -  * `Asia/Jerusalem` -  * `Asia/Nicosia` -  * `Europe/Athens` -  * `Europe/Bucharest` -  * `Europe/Chisinau` -  * `Europe/Helsinki` -  * `Europe/Istanbul` -  * `Europe/Kaliningrad` -  * `Europe/Kiev` -  * `Europe/Riga` -  * `Europe/Sofia` -  * `Europe/Tallinn` -  * `Europe/Vilnius` -  * `Africa/Khartoum` -  * `Africa/Nairobi` -  * `Antarctica/Syowa` -  * `Asia/Baghdad` -  * `Asia/Qatar` -  * `Asia/Riyadh` -  * `Europe/Minsk` -  * `Europe/Moscow` -  * `Asia/Tehran` -  * `Asia/Baku` -  * `Asia/Dubai` -  * `Asia/Tbilisi` -  * `Asia/Yerevan` -  * `Europe/Samara` -  * `Indian/Mahe` -  * `Indian/Mauritius` -  * `Indian/Reunion` -  * `Asia/Kabul` -  * `Antarctica/Mawson` -  * `Asia/Aqtau` -  * `Asia/Aqtobe` -  * `Asia/Ashgabat` -  * `Asia/Dushanbe` -  * `Asia/Karachi` -  * `Asia/Tashkent` -  * `Asia/Yekaterinburg` -  * `Indian/Kerguelen` -  * `Indian/Maldives` -  * `Asia/Calcutta` -  * `Asia/Kolkata` -  * `Asia/Colombo` -  * `Asia/Katmandu` -  * `Antarctica/Vostok` -  * `Asia/Almaty` -  * `Asia/Bishkek` -  * `Asia/Dhaka` -  * `Asia/Omsk` -  * `Asia/Thimphu` -  * `Indian/Chagos` -  * `Asia/Rangoon` -  * `Indian/Cocos` -  * `Antarctica/Davis` -  * `Asia/Bangkok` -  * `Asia/Hovd` -  * `Asia/Jakarta` -  * `Asia/Krasnoyarsk` -  * `Asia/Saigon` -  * `Indian/Christmas` -  * `Antarctica/Casey` -  * `Asia/Brunei` -  * `Asia/Choibalsan` -  * `Asia/Hong_Kong` -  * `Asia/Irkutsk` -  * `Asia/Kuala_Lumpur` -  * `Asia/Macau` -  * `Asia/Makassar` -  * `Asia/Manila` -  * `Asia/Shanghai` -  * `Asia/Singapore` -  * `Asia/Taipei` -  * `Asia/Ulaanbaatar` -  * `Australia/Perth` -  * `Asia/Pyongyang` -  * `Asia/Dili` -  * `Asia/Jayapura` -  * `Asia/Seoul` -  * `Asia/Tokyo` -  * `Asia/Yakutsk` -  * `Pacific/Palau` -  * `Australia/Adelaide` -  * `Australia/Darwin` -  * `Antarctica/DumontDUrville` -  * `Asia/Magadan` -  * `Asia/Vladivostok` -  * `Australia/Brisbane` -  * `Australia/Hobart` -  * `Australia/Sydney` -  * `Pacific/Chuuk` -  * `Pacific/Guam` -  * `Pacific/Port_Moresby` -  * `Pacific/Efate` -  * `Pacific/Guadalcanal` -  * `Pacific/Kosrae` -  * `Pacific/Norfolk` -  * `Pacific/Noumea` -  * `Pacific/Pohnpei` -  * `Asia/Kamchatka` -  * `Pacific/Auckland` -  * `Pacific/Fiji` -  * `Pacific/Funafuti` -  * `Pacific/Kwajalein` -  * `Pacific/Majuro` -  * `Pacific/Nauru` -  * `Pacific/Tarawa` -  * `Pacific/Wake` -  * `Pacific/Wallis` -  * `Pacific/Apia` -  * `Pacific/Enderbury` -  * `Pacific/Fakaofo` -  * `Pacific/Tongatapu` -  * `Pacific/Kiritimati` -. [optional] if omitted the server will use the default value of "Pacific/Niue"  # noqa: E501
            version (str): Current software version of the Intersight Appliance.. [optional]  # noqa: E501
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
        """

        class_id = kwargs.get('class_id', "appliance.SystemInfo")
        object_type = kwargs.get('object_type', "appliance.SystemInfo")
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
              ApplianceSystemInfoAllOf,
              MoBaseMo,
          ],
          'oneOf': [
          ],
        }
