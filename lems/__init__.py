"""
:author: Gautham Ganapathy
:organization: LEMS (https://github.com/organizations/LEMS)
"""

import logging

logger = logging.getLogger('LEMS')

__version__ = '0.5.5'

__schema_version__ = '0.7.6'
__schema_branch__ = "development"
__schema_location__ = 'https://raw.githubusercontent.com/LEMS/LEMS/{0}/Schemas/LEMS/LEMS_v{1}.xsd'.format(__schema_branch__, __schema_version__)
