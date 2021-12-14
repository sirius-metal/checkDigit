
#!/usr/bin/env python3
#unitTest_checkDigit.py
"""Unit tests for check digit formula classes
    SumOfWeightsCDF
    NricCDF
"""

from checkDigit import SumOfWeightsCDF
from sgNRIC import NricCDF
import unittest


class NricCDFTest(unittest.TestCase):
    """
        Tests for verifyCD method to return True or False
        generateCD method is implicitly tested as verifyCD calls generateCD

        Mock data for NRIC and FIN unit tests data were created using spreadsheet formula (SUMPRODUCT, MOD, etc).
        Any similarity to true NRIC/FIN ID that may have been issued/yet to be issued to real people, living or dead,
        or yet to be born (in the case of T44 series) are purely coincidental;
        and are WITHOUT any intention of malice/invasion of privacy.
        Test cases does not include the M series issued from 2022 onwards.
    """

    def test(self):
        NricObject = NricCDF()
        print('Single NRIC/FIN tests for generating checksum letter')
        self.assertEqual(NricObject.generateCD('S4444441'),'J')
        self.assertEqual(NricObject.generateCD('T4444484'),'J')
        self.assertEqual(NricObject.generateCD('F4444441'),'X')
        self.assertEqual(NricObject.generateCD('G4444484'),'X')

        print('Single NRIC/FIN tests expecting True for verification')
        self.assertTrue(NricObject.verifyCD('S4444441J'))
        self.assertTrue(NricObject.verifyCD('T4444484J'))
        self.assertTrue(NricObject.verifyCD('F4444441X'))
        self.assertTrue(NricObject.verifyCD('G4444484X'))

        print('Single NRIC/FIN tests expecting False for verification')
        self.assertFalse(NricObject.verifyCD('S4444441A'))
        self.assertFalse(NricObject.verifyCD('T4444484A'))
        self.assertFalse(NricObject.verifyCD('F4444441B'))
        self.assertFalse(NricObject.verifyCD('G4444484B'))

    def testAllChecksumLetters(self):

        NricObject = NricCDF()
        validSseries = ['S4444441J','S4444447Z','S4444442I','S4444448H','S4444443G','S4444449F','S4444444E','S4444484D','S4444445C','S4444440B','S4444446A']
        validTseries = ['T4444484J','T4444445Z','T4444440I','T4444446H','T4444441G','T4444447F','T4444442E','T4444448D','T4444443C','T4444449B','T4444444A']
        validFseries = ['F4444441X','F4444447W','F4444442U','F4444448T','F4444443R','F4444449Q','F4444444P','F4444484N','F4444445M','F4444440L','F4444446K']
        validGseries = ['G4444484X','G4444445W','G4444440U','G4444446T','G4444441R','G4444447Q','G4444442P','G4444448N','G4444443M','G4444449L','G4444444K']

        invalidSseries = ['S4444441X','S4444447X','S4444442X','S4444448X','S4444443X','S4444449X','S4444444X','S4444484X','S4444445X','S4444440X','S4444446X']
        invalidTseries = ['T4444484X','T4444445X','T4444440X','T4444446X','T4444441X','T4444447X','T4444442X','T4444448X','T4444443X','T4444449X','T4444444X']
        invalidFseries = ['F4444441A','F4444447A','F4444442A','F4444448A','F4444443A','F4444449A','F4444444A','F4444484A','F4444445A','F4444440A','F4444446A']
        invalidGseries = ['G4444484A','G4444445A','G4444440A','G4444446A','G4444441A','G4444447A','G4444442A','G4444448A','G4444443A','G4444449A','G4444444A']

        print("testing S series NRIC expecting True")
        for testData in validSseries:
            with self.subTest(testData):
                self.assertTrue(NricObject.verifyCD(testData))

        print("testing T series NRIC expecting True")
        for testData in validTseries:
            with self.subTest(testData):
                self.assertTrue(NricObject.verifyCD(testData))

        print("testing F series NRIC expecting True")
        for testData in validFseries:
            with self.subTest(testData):
                self.assertTrue(NricObject.verifyCD(testData))

        print("testing G series NRIC expecting True")
        for testData in validGseries:
            with self.subTest(testData):
                self.assertTrue(NricObject.verifyCD(testData))

        print("testing S series NRIC expecting False")
        for testData in invalidSseries:
            with self.subTest(testData):
                self.assertFalse(NricObject.verifyCD(testData))

        print("testing T series NRIC expecting False")
        for testData in invalidTseries:
            with self.subTest(testData):
                self.assertFalse(NricObject.verifyCD(testData))

        print("testing F series NRIC expecting False")
        for testData in invalidFseries:
            with self.subTest(testData):
                self.assertFalse(NricObject.verifyCD(testData))

        print("testing G series NRIC expecting False")
        for testData in invalidGseries:
            with self.subTest(testData):
                self.assertFalse(NricObject.verifyCD(testData))

class NricCDFExceptionTest(unittest.TestCase):
    """
    Unit tests for NricCDF class instance that the expected Exceptions are thrown based on invalid input
    These are also tests for the correctness of the regex patterns initialised in the constructor.
    """
    def testExceptions(self):
        NricObject = NricCDF()

        try:
            print('Pass invalid NRIC value A4444441 for checksum letter generation')
            NricObject.generateCD('A4444441')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print('Pass invalid NRIC value A4444441J for checksum letter verification')
            NricObject.verifyCD('A4444441J')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print('Pass valid NRIC value S4444441 inside another string value ABCDS4444441777 for checksum letter generation')
            NricObject.generateCD('ABCDS4444441777')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print('Pass valid NRIC value S4444441J inside another string value ABCDS4444441JEFG for checksum letter verification')
            NricObject.verifyCD('ABCDS4444441JEFG')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

class SumOfWeightsCDFTest(unittest.TestCase):
    """
    Unit test for SumOfWeightsCDF using ISBN10 and ISBN13 check digit as simple test case
    Note that the lambda expression and regex pattern correctness is not verified in this unit test.
    The data set for this test case is also not exhaustive.
    This unit test is primarily for code coverage.
    The exhaustive data set (and by consequence, lambda expression and regex patterns correctness) is best
    tested by function(s)/modules(s) that use this class or class(es) that inherit from this class
    """
    def test(self):
        IsbnCD = SumOfWeightsCDF()

        try:
            print("Using class methods without setting weightString")
            IsbnCD.generateCD('020153082')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print("Using class methods by setting weightString with alpha char")
            IsbnCD.weightString = '12345678A'
            IsbnCD.generateCD('020153082')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print("Using class methods without setting modulusValue")
            IsbnCD.weightString = '123456789'
            IsbnCD.generateCD('020153082')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        try:
            print("Using class methods with setting modulusValue to 0")
            IsbnCD.weightString = '123456789'
            IsbnCD.modulusValue = 0
            IsbnCD.generateCD('020153082')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')
        
        try:
            print("Using class methods without setting modulusLambda expression")
            IsbnCD.modulusValue = 11
            IsbnCD.generateCD('020153082')
        except Exception as e:
            print('Expected exception received: ', e.args[0])
        else:
            self.fail('Exception was not raised')

        IsbnCD.modulusLambda = lambda remainder : 'X' if remainder == 10 else remainder

        print("All 3 required properties are set for ISBN10, methods should work as expected")
        self.assertEqual(IsbnCD.generateCD('020153082'),'1')
        self.assertEqual(IsbnCD.generateCD('020153083'),'X')
        self.assertNotEqual(IsbnCD.generateCD('020153083'),'4')
        self.assertTrue(IsbnCD.verifyCD('020153083X'))
        self.assertFalse(IsbnCD.verifyCD('0201530834'))

        print("Change all 3 properties to handle ISBN13, methods should work as expected")
        IsbnCD.weightString = '131313131313'
        IsbnCD.modulusValue = 10
        IsbnCD.modulusLambda = lambda x : (10 - x) if (10 - x < 10) else 0
        self.assertEqual(IsbnCD.generateCD('978030640615'),'7')
        self.assertNotEqual(IsbnCD.generateCD('978030640615'),'4')
        self.assertTrue(IsbnCD.verifyCD('9780306406157'))
        self.assertFalse(IsbnCD.verifyCD('9780306406154'))

