#!/usr/bin/env python3
#checkDigit.py
"""Library for check digit formula to either generate or verify check digit for identification strings
Contains a parent class SumOfWeightsCDF which is intended as a customisable implementation of the Sum of Weights check digit formula
"""

import re

class SumOfWeightsCDF(object):
    """
    Provides a generic way to implement sum of weights check digit formula
    Input values should not have whitespaces or formatting such as dashes (typical in bank account numbers)

    Required properties:
        weighString (str) - a string of numeric digits representing weights to be applied on the input from left to right
        modulusValue (int) - the modulus value to applied after the sum of weights is calculated
        modulusLambda (lambda expr) - the lambda expression that determines what is done with the remainder (e.g. if remainder is 10, what is done, etc)
    
    Optional properties:
        identifierPattern (str) - a regex pattern that can be used to validate an input value that has the check digit, IGNORECASE is used for matching
        idenfifierPatternWithoutCD (str) - a regex pattern that can be used to validate an input value that requires check digit generation, IGNORECASE is used for matching
        
    Example Usage: ISBN 10 check digit https://en.wikipedia.org/wiki/Check_digit#ISBN_10

        Isbn10CD = SumOfWeightsCDF()
        Isbn10CD.weightString = '123456789'
        Isbn10CD.modulusValue = 11
        Isbn10CD.modulusLambda = lambda remainder : 'X' if (remainder == 10) else remainder
        print(Isbn10CD.generateCD('020153082')) # output is '1'
        print(Isbn10CD.verifyCD('0201530822'))  # output is False
        print(Isbn10CD.generateCD('020153083')) # output is 'X'
        print(Isbn10CD.verifyCD('020153083X'))  # output is True

        # Example passing required properties in constructor
        #
        # Note the lambda is passed as eval to a string of a lambda expression instead of simply passing a lambda expression
        # This eval method will make the lambda function to be in the instantiated object instead of where the object was instantiated.
        #
        Isbn10CDctor = SumofWeightsCDF(weights = '123456789', modulusValue = 11, modulusLambda = eval("lambda remainder : 'X' if (remainder == 10) else remainder"))
    """

    def __init__(self, weightString = None, modulusValue = None, modulusLambda = None, identifierPattern = None, identifierPatternWithoutCD = None):
        self.modulusValue = modulusValue
        self.weightString = weightString
        self.modulusLambda = modulusLambda
        self.identifierPattern = identifierPattern
        self.identifierPatternWithoutCD = identifierPattern
        self._reqMissing = (self.weightString is None and self.modulusValue is None and self.modulusLambda is None) or self.modulusValue <= 0

    """
    weightString(str):
    contains the weight string that is used for the check digit formula
    a simple check is done that all the characters in the input are numeric
    exception ValueError('weighString property should be a string containing numeric digit values') is raised when the weightString non-numeric characters
    an internal list is created with the individual digits converted to int value for calculation
    """
    @property
    def weightString(self):
        return self.__weighString
    
    @weightString.setter
    def weightString(self, value):
        self.__weighString = value
        if value is None:
            self._weightValues = None
            self._reqMissing = True
        else:
            matched = re.search(r'^([\d]+)$', value)
            if not matched:
                raise ValueError('weighString property should be a string containing numeric digit values')
            self._weightValues = [int(weight) for weight in value]

    """
    modulusValue(int):
    contains the modulus used for the check digit formula
    simple check that modulusValue is not negative or zero
    """
    @property
    def modulusValue(self):
        return self.__modulusValue
    
    @modulusValue.setter
    def modulusValue(self, value):
        if value is None:
            self.__modulusValue = value
            self._reqMissing = True
        elif value <= 0:
            raise ValueError('modulusValue property cannot be negative or zero')
        else:
            self.__modulusValue = value

    """
    modulusLambda(lambda expr):
    contains the modulus used for the check digit formula
    simple check that modulusValue is None or not
    """
    @property
    def modulusValue(self):
        return self.__modulusLambda
    
    @modulusValue.setter
    def modulusValue(self, value):
        self.__modulusLambda = value
        if value is None:
            self._reqMissing = True

    """
    identifierPattern(str):
    contains the regex string pattern that is used to check whether the input value that has a check digit matches the expected format
    when set, the pattern is also compiled in a RegEx object
    """
    @property
    def identifierPattern(self):
        return self._identifierPattern
    
    @identifierPattern.setter
    def identifierPattern(self, value):
        self._identifierPattern = value
        if value is None:
            self._regExPattern = None
        else:
            self._regExPattern = re.compile(value, re.IGNORECASE)


    """
    identifierPatternWithoutCD(str):
    contains the regex string pattern that is used to check whether the input value that does not have check digit matches the expected format
    when set, the pattern is also compiled in a RegEx object
    """
    @property
    def identifierPatternWithoutCD(self):
        return self._identifierPatternWithoutCD

    @identifierPatternWithoutCD.setter
    def identifierPatternWithoutCD(self, value):
        self._identifierPatternWithoutCD = value
        if value is None:
            self._regExPatternWithoutCD = None
        else:
            self._regExPatternWithoutCD = re.compile(value, re.IGNORECASE)

    def generateCD(self, value):
        """
        returns a check digit (str) of the value (str) passed; calculated using the weightString and modulusValue
        the modulusLambda operates on the remainder as typically this is where check digit formula would differ
        when the identifierPatternWithoutCD property is set, the input value is verified against the RegEx pattern
        otherwise a simple check that the length of the input is the same as the length of the weightString
        exceptions that can be raised
            ValueError('weighString property is not set.')
            ValueError('modulusValue property is not set.')
            NotImplementedError('modulusLambda expression is required')   
            ValueError('Input value length does not match weightString length')
            ValueError('ValueError('modulusValue property cannot be negative or zero')
            ValueError('Input value with check digit does not match expected pattern')
        This method is also called internally by the verifyCD method
        """

        if self._reqMissing:
            if self.__weighString is None:
                raise ValueError('weighString property is not set.')
            if self.modulusValue is None:
                raise ValueError('modulusValue property is not set.')
            if self.modulusValue <= 0:
                raise ValueError('modulusValue property cannot be negative or zero')
            if self.modulusLambda is None:
                raise NotImplementedError('modulusLambda expression is required')
            #if required properties individually set instead of from constructor the self.__reqMissing may still be True
            #so if it got to this point (i.e. no Exceptions raised) this should set it to False and next round won't have to check
            self._reqMissing = (self.weightString is None and self.modulusValue is None and self.modulusLambda is None) or self.modulusValue <= 0
        if self._identifierPatternWithoutCD is None:
            #if no regEx pattern is set, check whether length of the weighString matches input value
            if len(value) != len(self.__weighString):
                raise ValueError('Input value length does not match weightString length')
        else:
            matched = self._regExPatternWithoutCD.match(value)
            if not matched:
                raise ValueError('Input value does not match expected pattern')

        valueAsNumbers = [int(digit) for digit in value]
        remainder = sum(digit * weight for digit, weight in zip(valueAsNumbers, self._weightValues)) % self.modulusValue
        return str(self.modulusLambda(remainder))

    def verifyCD(self, value):
        """
        returns a True or False whether the check digit in the input passed verification or not
        assumes that the check digit is the last digit on the right
        if the check digit is not on this assumed position,
        alternative is to call generateCD without the check digit and compare the generated value with input
        when the optional identifierPattern property is set, the input value is verified against the RegEx pattern
        and Exceptions ValueError('Input value with check digit does not match expected pattern') can be raised
        otherwise no check is made on the validity of the input and it is assumed the user of this class does it during end-user input
        """
        if self._regExPattern is not None:
            matched = self._regExPattern.match(value)
            if not matched:
                raise ValueError('Input value with check digit does not match expected pattern')
        return self.generateCD(value[:-1]) == value[-1]
    



