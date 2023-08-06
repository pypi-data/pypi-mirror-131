from .CatsParseException import CatsParseException
from .CompositeTypeParser import CompositeTypeParser
from .parserutils import TypeNameChecker, parse_builtin, parse_dec_or_hex
from .RegexParserFactory import RegexParserFactory


class EnumParser(CompositeTypeParser):
    """Parser for `enum` statements"""
    def __init__(self, regex):
        super().__init__(regex, [EnumValueParserFactory()])

    def process_line(self, line):
        match = self.regex.match(line)
        self.type_name = TypeNameChecker.require_user_type(match.group('enum_type_name'))

        base_type = TypeNameChecker.require_primitive(match.group('underlying_type_name'))
        builtin_type_descriptor = parse_builtin(base_type)
        self.type_descriptor = {
            'type': 'enum',
            'size': builtin_type_descriptor['size'],
            'signedness': builtin_type_descriptor['signedness'],
            'values': []
        }

    def append(self, property_value_descriptor):
        self._require_unknown_property(property_value_descriptor['name'])

        self.type_descriptor['values'].append(property_value_descriptor)

    def _require_unknown_property(self, property_name):
        if any(property_name == property_type_descriptor['name'] for property_type_descriptor in self.type_descriptor['values']):
            raise CatsParseException('duplicate definition for enum value "{}"'.format(property_name))


class EnumParserFactory(RegexParserFactory):
    """Factory for creating enum parsers"""
    def __init__(self):
        super().__init__(r'enum (?P<enum_type_name>\S+) : (?P<underlying_type_name>u?int\d+)', EnumParser)


class EnumValueParser:
    """Parser for enum values"""
    def __init__(self, regex):
        self.regex = regex

    def process_line(self, line):
        match = self.regex.match(line)
        return {
            'name': TypeNameChecker.require_const_property(match.group('name')),
            'value': parse_dec_or_hex(match.group('value'))
        }


class EnumValueParserFactory(RegexParserFactory):
    """Factory for creating enum value parsers"""
    def __init__(self):
        super().__init__(r'(?P<name>\S+) = (?P<value>\S+)', EnumValueParser)
