# Copyright (c) 2001-2015, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

import requests
import logging


class _NavitiaWrapper(object):

    def __init__(self, url, token=None):
        self.url = url
        self.token = token
        self.timeout = 1

    def query(self, query, q=None):
        """
        query the API and return
        * the response as a python dict
        * the http status code
        """
        logging.getLogger(__name__).debug('query {}'.format(self.url + query))
        try:
            response = requests.get(self.url + query, auth=(self.token, None), timeout=self.timeout, params=q)
        except requests.exceptions.RequestException:
            logging.getLogger(__name__).exception('call to navitia failed')
            #currently we reraise the previous exceptions
            raise Exception('call to navitia failed, query: {}'.format(query))

        if response.status_code not in (200, 404):
            raise NavitiaException('invalid call to navitia: {res} | {code}'
                                   .format(res=response.text, code=response.status_code))
        json = {}
        try:
            json = response.json()
        except Exception:
            logging.getLogger(__name__).exception('impossible to load the response as json')

        return json, response.status_code


class Navitia(_NavitiaWrapper):
    def instance(self, name):
        return Instance('{url}v1/coverage/{name}/'.format(url=self.url, name=name), self.token)


class Instance(_NavitiaWrapper):
    def _collection(self, col, uri=None, q=None):
        """
        call navitia on one collection API
        return the list of found object (not the whole navitia response)
        """
        url = col + '/'
        if uri is not None:
            url += uri + '/'

        res, status = self.query(url, q)

        if status == 200:
            return res[col]
        return []

    def vehicle_journeys(self, uri=None, q=None):
        return self._collection('vehicle_journeys', uri, q)

    def stop_areas(self, uri=None, q=None):
        return self._collection('stop_areas', uri, q)


class NavitiaException(Exception):
    pass