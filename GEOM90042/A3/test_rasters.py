# Author:       Bingkun Chen
# StudentID:    992113
# UserName:     BINGKUNC
# Description:  This is the test_code for Geom90042 Assigment3.
# Written:      8/5/2020
# Last updated: 15/5/2020

import os
import unittest
import rasters
import ProjectModules


class TestTaskOne(unittest.TestCase):
    def setUp(self):
        ''' Sets up a few variables to run test cases in Task 1'''
        self.filename = os.path.join(os.path.curdir, 'DEM', 'CLIP.tif')
        self.tested_dict = rasters.summary_dem(self.filename, 3111)

    def test_summary_dem(self):
        '''Tests the output of Task1.1'''
        # Tests the type of output
        self.assertTrue(isinstance(self.tested_dict, dict),
                        "Output not a dictionary.")

        # Tests the bound value(lat/lon) of CLIP.tif
        # the test data is from "readme_metadata.html"
        self.assertAlmostEqual(round(self.tested_dict['Min Lon']['value'], 5),
                               145.45486, places=3)
        self.assertAlmostEqual(round(self.tested_dict['Max Lon']['value'], 5),
                               146.44638, places=3)
        self.assertAlmostEqual(round(self.tested_dict['Min Lat']['value'], 5),
                               -37.97885, places=3)
        self.assertAlmostEqual(round(self.tested_dict['Max Lat']['value'], 5),
                               -37.43670, places=3)
        # Tests the units of (lat/lon)
        self.assertEqual(self.tested_dict['Min Lon']['units'], 'degree',
                         "The unit of Min_lon is not degree.")
        self.assertEqual(self.tested_dict['Max Lon']['units'], 'degree',
                         "The unit of Max_lon is not degree.")
        self.assertEqual(self.tested_dict['Min Lat']['units'], 'degree',
                         "The unit of Min_lat is not degree.")
        self.assertEqual(self.tested_dict['Max Lat']['units'], 'degree',
                         "The unit of Max_lat is not degree.")
        # Tests the utm_coordinate of bound
        # the test data is computed from QGIS
        self.assertAlmostEqual(self.tested_dict['Min x']['value'],
                               2539962.6883884235)
        self.assertAlmostEqual(self.tested_dict['Max x']['value'],
                               2627972.334948602)
        self.assertAlmostEqual(self.tested_dict['Min y']['value'],
                               2390417.722480248)
        self.assertAlmostEqual(self.tested_dict['Max y']['value'],
                               2451433.2929335157)
        # Tests the units of utm_coordinate
        self.assertEqual(self.tested_dict['Min x']['units'], 'metre',
                         "The unit of Min_x is not metre.")
        self.assertEqual(self.tested_dict['Max x']['units'], 'metre',
                         "The unit of Max_x is not metre.")
        self.assertEqual(self.tested_dict['Min y']['units'], 'metre',
                         "The unit of Min_y is not metre.")
        self.assertEqual(self.tested_dict['Max y']['units'], 'metre',
                         "The unit of Max_y is not metre.")

    def test_display_summary(self):
        ''' Test Task1.2'''
        # Test Task1.2: whether using PrettyTable.py to output the table
        tested_table = rasters.display_summary(self.tested_dict)
        self.assertTrue(isinstance(tested_table,
                                   ProjectModules.PrettyTable.PrettyTable),
                        "Not using PrettyTable to display the data.")

    def test_plot_highest_value_cell(self):
        ''' Test Task1.4'''
        # Tests the returned coordinate by plot_highest_value_cell function
        tested_coordinate = rasters.plot_highest_value_cell(self.filename)
        for coordinate in tested_coordinate:
            self.assertTrue(isinstance(coordinate, tuple),
                            "Coordinate not a tuple.")
            self.assertEqual(len(coordinate), 2,
                             "The number of coordinate is not 2.")
            self.assertTrue(isinstance(coordinate[0], float),
                            "X coordinate not a float, seems unlikely")
            self.assertTrue(isinstance(coordinate[1], float),
                            "Y coordinate not a float, seems unlikely")


if __name__ == '__main__':
    unittest.main()
