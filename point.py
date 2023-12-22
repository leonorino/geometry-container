'''3-Dimensional Point module.

Usage example:
    point = Point(1, 2, 3)
    point = Point.from_string('(1;2;3)')
'''

from __future__ import annotations
import re
import json

POINT_REGEX = r'\([+-]?([0-9]*[.])?[0-9]+;[+-]?([0-9]*[.])?[0-9]+;' + \
        r'[+-]?([0-9]*[.])?[0-9]+\)'
POINT_SPLITTERS = r'[\(;\)]'


class Point:
    '''3-dimensional Geometric Point.

    Attributes:
        float x, y, z: Point coordinates.
    '''

    @classmethod
    def from_str(cls: Point, string: str) -> Point:
        '''Class method that creates a Point object from formatted string.

        Args:
            str string: String in the following format: (%f;%f;%f)

        Returns:
            Point object with parameters described in input string.

        Raises:
            ValueError: String doesn't conform to input format.
        '''
        if not re.match(POINT_REGEX, string):
            raise ValueError('Illegal Point string format')

        x, y, z = filter(None, re.split(POINT_SPLITTERS, string))

        return cls(float(x), float(y), float(z))

    @classmethod
    def from_json(cls: Point, json_string: str = None,
                  json_dict: dict = None) -> Point:
        '''Class method that returns a Point object from JSON.

        Args:
            (optional) str json_string: String which if specified will be
                parsed with json.parse method.
                Default: None
            (optional) dict json_dict: Already parsed JSON dictionary.
        Either json_string or json_dict should be specified.
        Parsed or specified JSON dict should contain keys 'x', 'y', 'z' with
            values convertible to float.

        Returns:
            Point object from JSON data.

        Raises:
            ValueError: json_dict is unspecified or can't be parsed from
                json_string.
            ValueError: elements in dictionary can't be converted to float.
            KeyError: json_dict doesn't contain necessary elements.
        '''
        if json_string:
            json_dict = json.loads(json_string)

        if not json_dict:
            raise ValueError('Illegal Point JSON format')

        try:
            x = float(json_dict['x'])
            y = float(json_dict['y'])
            z = float(json_dict['z'])
        except (KeyError, ValueError) as exception:
            raise ValueError('Illegal Point JSON format') from exception

        return cls(x, y, z)

    def __init__(self: Point, x: float | int, y: float | int, z: float | int):
        '''Point initializer.

        Args:
            float|int x, y, z: Point coordinates.

        Raises:
            ValueError: Illegal coordinate type.
        '''
        for value in (x, y, z):
            if not isinstance(value, (float, int)):
                raise ValueError(f'Illegal coordinate: {value}')

        self.x = x
        self.y = y
        self.z = z

    def __setattr__(self: Point, name: str, value: int | float):
        '''Point attribute setter.

        Args:
            str name: Name of attribute to be set. One of 'x', 'y', 'z'.
            int|float value: New value to be set.

        Raises:
            AttributeError: Point doesn't have a specified attribute.
            ValueError: Illegal value type.
        '''
        if name not in ('x', 'y', 'z'):
            raise AttributeError(f'Point has no attribute {name}')

        if not isinstance(value, (float, int)):
            raise ValueError(f'Illegal coordinate: {value}')

        self.__dict__[name] = value

    def __eq__(self: Point, other: Point) -> bool:
        '''Checks if Point is equal to other Point.

        Args:
            Point other: other Point.

        Returns:
            True if point coordinates are equal in pairs.
            False if coordinates are not equal, or other object is not a Point.
        '''
        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self: Point) -> str:
        '''Converts Point to its string representation.

        Returns:
            String formatted as '({point.x};{point.y};{point.z})'
        '''
        return f'({self.x};{self.y};{self.z})'

    def __repr__(self: Point) -> str:
        '''Override to return same format as __str__.
        '''

        return str(self)

    def to_json(self: Point, to_dict: bool = False) -> str | dict:
        '''Converts Point to JSON string or dict.

        Args:
            (optional) bool to_dict: Flag to convert Point to dict instead of
            string. Default: False.

        Returns:
            If to_dict is set to True, returns a dict. Otherwise returns
            the same dict converted to string with json.dumps.
        '''
        json_dict = {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'type': 'Point'
        }
        if to_dict:
            return json_dict
        return json.dumps(json_dict)
