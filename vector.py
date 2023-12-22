'''
3-Dimensional Vector module.

Usage example:
    vector = Vector(2, 3, 2) # Coordinates: (2, 3, 2), Start point: (0, 0, 0)

    point1 = Point(1, 1, 1)
    point2 = Point(2, 2, 2)

    vector = Vector(2, 3, 2, start_point) # Coordinates: (2, 3, 2), Start point: (1, 1, 1)
    vector = Vector(start_point=point1, end_point=point2) # Coordinates: (1, 1, 1), Start point: (1, 1, 1)

    vector = Vector.from_string('(1;1;1):(2;2;2)') # Coordinates: (1, 1, 1), Start point: (1, 1, 1)
'''

from __future__ import annotations
import json

from point import Point


class Vector(Point):
    '''3-dimensional Geometric Vector.

    Attributes:
        float x, y, z: Vector coordinates.
        Point start_point: Vector start point.
        Point end_point: Vector end point.
    '''

    @classmethod
    def from_str(cls: Vector, string: str) -> Vector:
        '''Class method that returns Vector object from string.

        Args:
            str string: Input string consisting of 2 point strings separated
                by colon.

        Returns:
            Vector object from 2 specified points.

        Raises:
            ValueError: string doesn't conform to input format.
        '''
        try:
            start_string, end_string = string.split(':')

            start_point = Point.from_str(start_string)
            end_point = Point.from_str(end_string)
        except (IndexError, ValueError) as exception:
            raise ValueError('Illegal Vector string format') from exception

        return cls(start_point=start_point, end_point=end_point)

    @classmethod
    def from_json(json_string: str = None, json_dict: dict = None) -> Vector:
        '''Class method that creates a Vector object from JSON.

        Args:
            (optional) str json_string: String which if specified will be
                parsed with json.parse.
            (optional) str json_dict: Already parsed JSON dictionary.
        Either json_string or json_dict should be specified.
        Parsed or specified JSON dictionary should contain keys 'x', 'y', 'z'
            with values convertible to float and 'start_point', 'end_point'
            with values convertible to Point.

        Returns:
            Vector object from JSON data.

        Raises:
            ValueError: json_dict is unspecified or can't be parsed from
                json_string.
            ValueError: elements in dictionary can't be converted to float
                or Point.
            KeyError: dictionary doesn't contain necessary elements.
        '''
        if json_string:
            json_dict = json.loads(json_string)

        if not json_dict:
            raise ValueError('Illegal Vector JSON format')

        try:
            start_dict = json_dict['start_point']
            start_point = Point.from_json(json_dict=start_dict)
            end_dict = json_dict['end_point']
            end_point = Point.from_json(json_dict=end_dict)
        except (KeyError, ValueError) as exception:
            raise ValueError('Illegal Vector JSON format') from exception

        return cls(start_point=start_point, end_point=end_point)

    @classmethod
    def cross(cls: Vector, first: Vector, second: Vector) -> Vector:
        '''Cross-product of 2 vectors.

        Args:
            Vector first, second

        Returns:
            Cross-product of first by second.
        '''
        if not isinstance(first, Vector) or not isinstance(second, Vector):
            raise ValueError("Can't find cross-product of non-vectors")

        x = first.y * second.z - first.z * second.y
        y = first.x * second.z - first.z * second.x
        z = first.x * second.y - first.y * second.x

        return cls(x, y, z, start_point=first.start_point)

    @classmethod
    def mixed(cls: Vector, first: Vector, second: Vector,
              third: Vector) -> Vector:
        '''Mixed product of 3 vectors.

        Args:
            Vector first, second, third

        Returns:
            Mixed product of first by second by third.
        '''
        return cls.cross(first, second) * third

    @classmethod
    def collinear(first: Vector, second: Vector) -> bool:
        '''Checks if 2 vectors are collinear.

        Args:
            Vector first, second

        Returns:
            True if 2 specified Vectors are collinear, otherwise False.

        Raises:
            ValueError: one of specified arguments is not Vector.
        '''
        if not isinstance(first, Vector) or not isinstance(second, Vector):
            raise ValueError("Can't check if non-vectors are collinear")

        return first.x / second.x == first.y / second.y == first.z / second.z

    def __init__(self: Vector, x: float | int = None, y: float | int = None,
                 z: float | int = None, start_point: Point = Point(0, 0, 0),
                 end_point: Point = None):
        '''Vector initializer.

        Args:
            (optional) float x, y, z
                Default: None
            (optional) Point start_point
                Default: Point at (0, 0, 0)
            (optional) Point end_point
        x, y, z coordinates are passed to

        Raises:
            ValueError: Not enough values specified to initialize a Vector.
        '''
        if end_point is None:
            if x is None or y is None or z is None:
                raise ValueError("Can't create a Vector from provided args")
            super().__init__(x, y, z)
            self.end_point = Point(
                start_point.x + x,
                start_point.y + y,
                start_point.z + z
            )
            self.start_point = start_point
        else:
            super().__init__(
                end_point.x - start_point.x,
                end_point.y - start_point.y,
                end_point.z - start_point.z
            )
            self.start_point = start_point
            self.end_point = end_point

    def __setattr__(self: Vector, name: str, value: int | float | Point):
        '''Vector attribute setter.

        Args:
            str name: Name of attribute to be set. One of 'x', 'y', 'z',
                'start_point', 'end_point'.
            int|float|Point value: New value to be set.

        Raises:
            AttributeError: Vector doesn't have a specified attribute.
            ValueError: Illegal value type.
        '''
        if name in ('x', 'y', 'z'):
            super().__setattr__(name, value)
        elif name in ('start_point', 'end_point'):
            if not isinstance(value, Point):
                raise ValueError(f'Illegal Point: {value}')

            self.__dict__[name] = value
        else:
            raise AttributeError(f'Vector has no attribute: {name}')

    def __mul__(self: Vector, other: Vector | int | float) -> Vector | float:
        '''Multiplies current Vector by other Vector or number.

        Args:
            Vector|int|float other

        Returns:
            If other is number, current Vector scaled by other.
            If other si Vector, scalar product of 2 Vectors.

        Raises:
            ValueError: Illegal argument type.
        '''
        if isinstance(other, (float, int)):
            return Vector(
                self.x * other, self.y * other, self.z * other,
                start_point=self.start_point
            )
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z
        raise ValueError(f"Can't multiply Vector by {type(other)}")

    def __add__(self: Vector, other: Vector) -> Vector:
        '''Adds current Vector to other.

        Args:
            Vector other: other Vector.

        Returns:
            New Vector which is a result of addition.

        Raises:
            ValueError: Illegal argument type.
        '''
        if not isinstance(other, Vector):
            raise ValueError(f"Can't add {type(other)} to Vector")

        return Vector(
            self.x + other.x, self.y + other.y, self.z + other.z,
            start_point=self.start_point
        )

    def __sub__(self: Vector, other: Vector) -> Vector:
        '''Substracts current Vector from other.

        Args:
            Vector other: other Vector.

        Returns:
            New Vector which is a result of substraction.

        Raises:
            ValueError: Illegal argument type.
        '''

        if not isinstance(other, Vector):
            raise ValueError(f"Can't substract {type(other)} from Vector")

        return self + -other

    def __eq__(self: Vector, other: Vector) -> bool:
        '''Checks if Vector is equal to other Vector.

        Args:
            Vector other: other Vector.

        Returns:
            True if point coordinates are equal in pairs.
            False if coordinates are not equal, or other object is not a Vector.
        '''
        if not isinstance(other, Vector):
            return False

        return self.start_point == other.start_point and \
                self.end_point == other.end_point

    def __str__(self: Vector) -> str:
        '''Converts Vector to its string representation.

        Returns:
            String formatted as '{start_point}:{end_point}'
        '''
        return f'{self.start_point}:{self.end_point}'

    def __repr__(self: Vector) -> str:
        '''
        Override to return same format as __str__.
        '''
        return str(self)

    def to_json(self: Vector, to_dict: bool = False) -> str:
        '''Converts Vector to JSON string or dict.

        Args:
            (optional) bool to_dict: Flag to convert Vector to dict instead of
            string. Default: False.

        Returns:
            If to_dict is set to True, returns a dict. Otherwise returns
            the same dict converted to string with json.dumps.
        '''

        json_dict = {
            'start_point': self.start_point.to_json(True),
            'end_point': self.end_point.to_json(True),
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'type': 'Vector'
        }

        if to_dict:
            return json_dict
        return json.dumps(json_dict)
