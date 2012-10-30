"""
Component simulation-spec storage.

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import LEMSBase
from lems.base.errors import ModelError

from lems.base.util import merge_dict

class Run(LEMSBase):
    """
    Stores the description of an object to be run according to an independent
    variable (usually time).
    """

    def __init__(self, component, variable, increment, total):
        """
        Constructor.

        @param component: Name of the target component to be run according to
        the specification given for an independent state variable.
        @type component: string

        @param variable: The name of an independent state variable according
        to which the target component will be run.
        @type variable: string

        @param increment: Increment of the state variable on each step.
        @type increment: string

        @param total: Final value of the state variable.
        @type total: string
        """

        self.component = component
        """ Name of the target component to be run according to the
        specification given for an independent state variable.
        @type: string """

        self.variable = variable
        """ The name of an independent state variable according to which the
        target component will be run.
        @type: string """

        self.increment = increment
        """ Increment of the state variable on each step.
        @type: string """

        self.total = total
        """ Final value of the state variable.
        @type: string """

class Record(LEMSBase):
    """
    Stores the parameters of a <Record> statement.
    """

    def __init__(self, quantity, scale, color):
        self.quantity = quantity
        self.scale = scale
        self.color = color

        self.numeric_scale = None

class Simulation(LEMSBase):
    """
    Stores the simulation-related aspects for a component type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.runs = {}
        """ Dictionary of runs in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.Run) """

        self.records = {}
        """ Dictionary of recorded variables in this dynamics regime.
        @type: dict(string -> lems.model.dynamics.Record """

        self.data_displays = {}
        """ Dictionary of data displays mapping titles to regions.
        @type: dict(string -> string) """

    def add_run(self, component, variable, increment, total):
        """
        Adds a runnable target component definition to the list of runnable
        components stored in this context.

        @param component: Name of the target component to be run.
        @type component: string

        @param variable: Name of an indendent state variable used to control
        the target component (usually time).
        @type variable: string

        @param increment: Value by which the control variable is to be
        incremented in each step.
        @type increment: string

        @param total: End value for the control variable.
        @type total: string
        """

        if component in self.runs:
            raise ModelError('Duplicate run for ' + component)

        self.runs[component] = Run(component, variable, increment, total)

    def add_record(self, quantity, scale, color):
        """
        Adds a record objects to the list of record objects in this dynamics
        regime.

        @param quantity: Path to the quantity to be recorded
        @type quantity: string

        @param scale: Scale of the quantity to be recorded
        @type scale: string

        @param color: Color of the quantity to be recorded as a 24-bit hex
        RGB value (#RRGGBB)
        @type color: string
        """

        if quantity in self.records:
            raise ModelError('Duplicate record {0}'.format(quantity))

        self.records[quantity] = Record(quantity, scale, color)

    def add_data_display(self, title, data_region):
        """
        Adds a data display to this simulation section.

        @param title: Title of the display.
        @type title: string

        @param data_region: Region of the display used for the plot.
        @type data_region: string
        """

        if title in self.data_displays:
            raise ModelError("Redefinition of data display '{0}'".format(title))

        self.data_displays[title] = data_region

    def merge(self, other):
        """
        Merge another set of simulation specs into this one.

        @param other: Simulation specs
        @type other: lems.model.simulation.Simulation
        """

        merge_dict(self.runs, other.runs)
        merge_dict(self.records, other.records)
        merge_dict(self.data_displays, other.data_displays)
