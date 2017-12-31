def func_key_val(self, key, value):
    """
    Get the number inputted by the user.
    For example, after pressing r to rotate, the user can input a 
    rotation amount (in degrees) by pressing numbers on the keyboard
    """
    numbers = {
        'NUMPAD_0' : '0',
        'NUMPAD_1' : '1',
        'NUMPAD_2' : '2',
        'NUMPAD_3' : '3',
        'NUMPAD_4' : '4',
        'NUMPAD_5' : '5',
        'NUMPAD_6' : '6',
        'NUMPAD_7' : '7',
        'NUMPAD_8' : '8',
        'NUMPAD_9' : '9',
        'ZERO' : '0',
        'ONE' : '1',
        'TWO' : '2',
        'THREE' : '3',
        'FOUR' : '4',
        'FIVE' : '5',
        'SIX' : '6',
        'SEVEN' : '7',
        'EIGHT' : '8',
        'NINE' : '9',
        'PERIOD' : '.',
        'NUMPAD_PERIOD' : '.',
    }
    if key in numbers.keys() and value == 'PRESS':
        if key in ['NUMPAD_PERIOD', 'PERIOD']:
            if self.key_val.count('.') == 0:
                self.key_val += '.'
        else:
            self.key_val += numbers[key]
                        
    if key in ['NUMPAD_MINUS', 'MINUS'] and value == 'PRESS':
        self.key_val = self.key_val.replace('+','-') if self.key_val[0] == '+' else self.key_val.replace('-','+')
