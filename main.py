from enum import Enum
from point import Point
from vector import Vector
from container import Container

class State(Enum):
    '''
    Enumeration of program states.
    '''

    INPUT = 0
    POINT_INPUT = 1
    VECTOR_INPUT = 2
    OUTPUT = 3
    FILE_OUTPUT = 4
    CLEAR = 5
    EXIT = 6


if __name__ == '__main__':
    print('Select one of the following options:')
    print('1: Add Point to Container')
    print('2: Add Vector to Container')
    print('3: Print out a Container')
    print('4: Export Container to JSON')
    print('5: Clear a Container')
    print('6: Exit')

    with open('output.json') as file:
        container = Container.from_json(file.read())
    state = State.INPUT

    while True:
        match state:
            case State.INPUT:
                user_input = input('> ').strip()
                if user_input in ('1', '2', '3', '4', '5', '6'):
                    state = State(int(user_input))
                else:
                    print('Illegal input')
            case State.POINT_INPUT:
                print('Input a point: (%f;%f;%f)')
                point_string = input('> ')
                try:
                    point = Point.from_str(point_string)
                    container.append(point)
                    state = State.INPUT
                except ValueError as exception:
                    print(exception)
            case State.VECTOR_INPUT:
                print('Input a vector: {%f;%f;%f};{%f;%f;%f}')
                vector_string = input('> ')
                try:
                    vector = Vector.from_str(vector_string)
                    container.append(vector)
                    state = state.INPUT
                except ValueError as exception:
                    print(exception)
            case State.OUTPUT:
                print(container)
                state = State.INPUT
            case State.FILE_OUTPUT:
                with open('output.json', 'w') as file:
                    file.write(container.to_json())
                state = State.INPUT
            case State.CLEAR:
                container.clear()
                state = State.INPUT
            case State.EXIT:
                break
