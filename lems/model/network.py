"""
Basic support of networks.

@author: Gautham Ganapathy, Dominik Krzeminski (dokato)
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.map import Map
from lems.base.errors import ModelError,ParseError
from lems.parser.expr import ExprParser


class Population(LEMSBase):
    """
    Store the specification of a population.
    """

    def __init__(self, id_, component, size):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.id = id_
        """ ID of the population.
        @type: str """

        self.dimension = dimension
        """Component of the population.
        @type: str """

        self.size = str(size)
        """Size name for the population.
        @type: str/int """

    def __str__(self):
        return 'Population id="{0}" component="{1}"' +\
           'size="{2}"'.format(self.id_, self.component, self.size)

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        return '<Population id="{0}" component="{1}"' +\
           'size="{2}"'.format(self.id_, self.component, self.size) +\
           '/>'

class Network(LEMSBase):
    """
    Store the specification of a network.
    """

    def __init__(self, id_):
        """
        Constructor.

        See instance variable documentation for more info on parameters.
        """

        self.id = id_
        """  ID of the component.
        @type: str """
        
        self.populations = list()
        """ List of populations related to this Network.
        @type: list(lems.model.network.Population) """

        
    def add_population(self, population):
        """
        Adds a population to this network.

        @param case: Population to be added.
        @type case: lems.model.network.Population
        """

        self.populations.append(population)

    def add(self, child):
        """
        Adds a typed child object to the conditional derived variable.

        @param child: Child object to be added.
        """

        if isinstance(child, Population):
            self.add_population(child)
        else:
            raise ModelError('Unsupported child element')


    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """

        xmlstr = '<network id="{0}"'.format(self.id)

        chxmlstr = ''

        for population in self.populations:
            chxmlstr += population.toxml()

        if chxmlstr:
            xmlstr += '>' + chxmlstr + '</network>'
        else:
            xmlstr += '/>'
            
        return xmlstr
