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
    from intersight.model.telemetry_druid_base_request import TelemetryDruidBaseRequest
    from intersight.model.telemetry_druid_data_source import TelemetryDruidDataSource
    from intersight.model.telemetry_druid_filter import TelemetryDruidFilter
    from intersight.model.telemetry_druid_query_context import TelemetryDruidQueryContext
    from intersight.model.telemetry_druid_scan_request_all_of import TelemetryDruidScanRequestAllOf
    globals()['TelemetryDruidBaseRequest'] = TelemetryDruidBaseRequest
    globals()['TelemetryDruidDataSource'] = TelemetryDruidDataSource
    globals()['TelemetryDruidFilter'] = TelemetryDruidFilter
    globals()['TelemetryDruidQueryContext'] = TelemetryDruidQueryContext
    globals()['TelemetryDruidScanRequestAllOf'] = TelemetryDruidScanRequestAllOf


class TelemetryDruidScanRequest(ModelComposed):
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
        ('query_type',): {
            'TIMESERIES': "timeseries",
            'TOPN': "topN",
            'GROUPBY': "groupBy",
            'SCAN': "scan",
            'TIMEBOUNDARY': "timeBoundary",
            'SEGMENTMETADATA': "segmentMetadata",
            'DATASOURCEMETADATA': "dataSourceMetadata",
            'SEARCH': "search",
        },
        ('result_format',): {
            'LIST': "list",
        },
        ('order',): {
            'NONE': "none",
            'ASCENDING': "ascending",
            'DESCENDING': "descending",
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
            'query_type': (str,),  # noqa: E501
            'data_source': (TelemetryDruidDataSource,),  # noqa: E501
            'intervals': ([str],),  # noqa: E501
            'result_format': (str,),  # noqa: E501
            'filter': (TelemetryDruidFilter,),  # noqa: E501
            'columns': ([str],),  # noqa: E501
            'batch_size': (int,),  # noqa: E501
            'limit': (int,),  # noqa: E501
            'order': (str,),  # noqa: E501
            'legacy': (bool,),  # noqa: E501
            'context': (TelemetryDruidQueryContext,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'query_type': 'queryType',  # noqa: E501
        'data_source': 'dataSource',  # noqa: E501
        'intervals': 'intervals',  # noqa: E501
        'result_format': 'resultFormat',  # noqa: E501
        'filter': 'filter',  # noqa: E501
        'columns': 'columns',  # noqa: E501
        'batch_size': 'batchSize',  # noqa: E501
        'limit': 'limit',  # noqa: E501
        'order': 'order',  # noqa: E501
        'legacy': 'legacy',  # noqa: E501
        'context': 'context',  # noqa: E501
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
    def __init__(self, query_type, data_source, intervals, *args, **kwargs):  # noqa: E501
        """TelemetryDruidScanRequest - a model defined in OpenAPI

        Args:
            query_type (str): null
            data_source (TelemetryDruidDataSource):
            intervals ([str]): A JSON Object representing ISO-8601 Intervals. This defines the time ranges to run the query over.

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
            result_format (str): How the results are represented, list, compactedList or valueVector. Currently only list is supported.. [optional] if omitted the server will use the default value of "list"  # noqa: E501
            filter (TelemetryDruidFilter): [optional]  # noqa: E501
            columns ([str]): A String array of dimensions and metrics to scan. If left empty, all dimensions and metrics are returned.. [optional]  # noqa: E501
            batch_size (int): The maximum number of rows buffered before being returned to the client.. [optional] if omitted the server will use the default value of 20480  # noqa: E501
            limit (int): How many rows to return. If not specified, all rows will be returned.. [optional]  # noqa: E501
            order (str): The ordering of returned rows based on timestamp. \"ascending\", \"descending\", and \"none\" (default) are supported. Currently, \"ascending\" and \"descending\" are only supported for queries where the __time column is included in the columns field and the requirements outlined in the time ordering section are met.. [optional] if omitted the server will use the default value of "none"  # noqa: E501
            legacy (bool): Return results consistent with the legacy \"scan-query\" contrib extension. Defaults to the value set by druid.query.scan.legacy, which in turn defaults to false.. [optional] if omitted the server will use the default value of False  # noqa: E501
            context (TelemetryDruidQueryContext): [optional]  # noqa: E501
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

        constant_args = {
            '_check_type': _check_type,
            '_path_to_item': _path_to_item,
            '_spec_property_naming': _spec_property_naming,
            '_configuration': _configuration,
            '_visited_composed_classes': self._visited_composed_classes,
        }
        required_args = {
            'query_type': query_type,
            'data_source': data_source,
            'intervals': intervals,
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
              TelemetryDruidBaseRequest,
              TelemetryDruidScanRequestAllOf,
          ],
          'oneOf': [
          ],
        }
