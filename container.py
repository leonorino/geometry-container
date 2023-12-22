'''
Container for Points and Vectors.

Usage example:
    point = Point(0, 0, 0)
    vector = Vector(2, 2, 2)

    container = Container(point, vector)
    container.append(Vector(5, 6, 7))
    container.append(3) # ValueError - can't contain anything other
        than Points or Vectors.
'''

from __future__ import annotations
import json

from point import Point
from vector import Vector


class Container(list):
    '''Container which can only contain Points and Vectors
    '''

    @classmethod
    def from_json(cls: Container,json_string: str = None,
                  json_dict: dict = None) -> Container:
        '''Class method that creates a Container object from JSON.

        Args:
            (optional) str json_string: String which if specified will be
                parsed with json.parse method.
                Default: None
            (optional) dict json_dict: Already parsed JSON dictionary.
        Either json_string or json_dict should be specified.
        Parsed or specified JSON dictionary should contain key 'element' with
            array of Point or Vector dictionaries.

        Returns:
            Container object from JSON data.

        Raises:
            ValueError: json_dict is unspecified or can't be parsed from
                json_string.
            ValueError: elements in dictionary can't be converted to float
                or Point.
            KeyError: json_dict doesn't contain necessary elements.
        '''
        if json_string:
            json_dict = json.loads(json_string)

        if not json_dict:
            raise ValueError('Illegal Container JSON format')

        approved_elements = []
        try:
            elements = json_dict['elements']
            for element in elements:
                if element['type'] == 'Vector':
                    approved_elements.append(
                        Vector.from_json(json_dict=element))
                elif element['type'] == 'Point':
                    approved_elements.append(
                        Point.from_json(json_dict=element))
        except (KeyError, ValueError) as exception:
            raise ValueError('Illegal Container JSON format') from exception

        return Container(*approved_elements)


    def __init__(self: Container, *elements: [Vector | Point]):
        '''Container initializer.

        Checks if all specified elements are Vector or Point and adds them to
        inner list. Non-conforming elements are skipped.

        Args:
            [Vector|Point] elements: Collection of elements to be added
                to Container.
        '''
        approved_elements = list(filter(
            lambda el: isinstance(el, (Vector, Point)),
            elements
        ))
        for arg in elements:
            if isinstance(arg, (Point, Vector)):
                approved_elements.append(arg)

        super().__init__(approved_elements)

    @override
    def append(self: Container, element: Vector | Point):
        '''List append override.

        Only allows Vector and Point elements to be appended.

        Args:
            Vector|Point element

        Raises:
            ValueError: Illegal argument type.
        '''
        if not isinstance(element, (Vector, Point)):
            raise ValueError('Can only add Vector or Point to Container')

        return super().append(element)

    @override
    def extend(self: Container, elements: [Vector | Point]):
        ''' List extend override.

        Only allows extensiton with Point or Vector elements.
        Skips non-conforming elements.

        Args:
            [Vector|Point] elements: Collection of elements for extension.
        '''
        approved_elements = list(filter(
            lambda el: isinstance(el, (Vector, Point)),
            elements
        ))

        return super().extend(approved_elements)

    @override
    def insert(self: Container, index: int, element: Vector | Point):
        '''List insert override.

        Only allows Vector and Point elements to be inserted.

        Args:
            Vector|Point element

        Raises:
            ValueError: Illegal argument type.
        '''
        if not isinstance(element, (Vector, Point)):
            raise ValueError('Can only add Vector or Point to Container')

        return super().insert(index, element)

    def to_json(self: Container, to_dict: bool = False) -> str:
        '''Converts Container to JSON string or dict.

        Args:
            (optional) bool to_dict: Flag to convert Container to dict instead
            of string. Default: False.

        Returns:
            If to_dict is set to True, returns a dict. Otherwise returns
            the same dict converted to string with json.dumps.
        '''
        json_dict = {
            'elements': [element.to_json(True) for element in self],
            'type': 'Container'
        }
        if to_dict:
            return json_dict
        return json.dumps(json_dict)
