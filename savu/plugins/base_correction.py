# -*- coding: utf-8 -*-
# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: base_correction
   :platform: Unix
   :synopsis: A base class for dark and flat field corrections

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""
import logging

from savu.plugins.plugin import Plugin


class BaseCorrection(Plugin):
    """
    A base class for dark and flat field correction plugins.

    :param in_datasets: Create a list of the dataset(s) to \
        process. Default: [].
    :param out_datasets: Create a list of the dataset(s) to \
        create. Default: [].
    """

    def __init__(self, name='BaseCorrection'):
        super(BaseCorrection, self).__init__(name)

    def process_frames(self, data, slice_list):
        """
        Perform the correction
        """
        self.slice_list = slice_list[0]
        return self.correct(data[0])

    def correct(self, data):
        """
        This is the main processing method for all plugins that inherit from
        base correction.  The plugin must implement this method.
        """
        logging.error("process needs to be implemented")
        raise NotImplementedError("process needs to be implemented")

    def setup(self):
        """
        Initial setup of all datasets required as input and output to the
        plugin.  This method is called before the process method in the plugin
        chain.
        """
        # set up the output dataset that is created by the plugin
        in_dataset, out_dataset = self.get_datasets()
        # copy all required information from in_dataset[0]
        out_dataset[0].create_dataset(in_dataset[0])
        # set information relating to the plugin data
        in_pData, out_pData = self.get_plugin_datasets()
        # set pattern_name and nframes to process for all datasets
        if 'pattern' in self.parameters.keys():
            pattern = self.parameters['pattern']
        else:
            pattern = 'PROJECTION'

        flag = self.fixed_flag()

        in_pData[0].plugin_data_setup(pattern, self.get_max_frames(),
                                      fixed=flag)
        out_pData[0].plugin_data_setup(pattern, self.get_max_frames(),
                                       fixed=flag)

    def fixed_flag(self):
        return False

    def nInput_datasets(self):
        return 1

    def nOutput_datasets(self):
        return 1

    def get_max_frames(self):
        """
        Should be overridden to define the max number of frames to process at
        a time.

        :returns:  an integer of the number of frames
        """
        return 16
