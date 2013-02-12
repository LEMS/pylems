"""
Component simulation-spec storage.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
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

        See instance variable documentation for information on parameters.
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
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """

        self.quantity = quantity
        """ Path to the quantity to be recorded.
        @type: string """

        self.scale = scale
        """ Text parameter to be used for scaling the quantity before display.
        @type: string """

        self.color = color
        """ Text parameter to be used to specify the color for display.
        @type: string """

        self.numeric_scale = None

class DataOutput(LEMSBase):
    """
    Generic data output specification class.
    """

    DISPLAY = 0
    FILE = 1

    def __init__(self, type_):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """

        self.type = type_
        """ Type of output.
        @type: string """

class DataDisplay(DataOutput):
    """
    Stores specification for a data display.
    """

    def __init__(self, title, data_region):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """

        DataOutput.__init__(self, DataOutput.DISPLAY)

        self.title = title
        """ Title for the display.
        @type: string """

        self.data_region = data_region
        """ Display position
        @type: string """

class DataWriter(DataOutput):
    """
    Stores specification for a data writer.
    """

    def __init__(self, path, file_path):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """

        DataOutput.__init__(self, DataOutput.FILE)
        
        self.path = path
        """ Path to the quantity to be saved to file.
        @type: string """

        self.file_path = file_path
        """ Text parameter to be used for the path to the file for
        saving this quantity
        @type: string """

class Simulation(LEMSBase):
    """
    Stores the simulation-related aspects for a component type.
    """

    def __init__(self):
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """

        self.runs = {}
        """ Dictionary of runs in this dynamics regime.
        @type: dict(string -> lems.model.simulation.Run) """

        self.records = {}
        """ Dictionary of recorded variables in this dynamics regime.
        @type: dict(string -> lems.model.simulation.Record """

        self.data_displays = {}
        """ Dictionary of data displays mapping titles to regions.
        @type: dict(string -> string) """

        self.data_writers = {}
        """ Dictionary of recorded variables to data writers.
        @type: dict(string -> lems.model.simulation.DataWriter """

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

        self.data_displays[title] = DataDisplay(title, data_region)

    def add_data_writer(self, path, file_path):
        """
        Adds a data writer to this simulation section.

        @param path: Path to the quantity.
        @type path: string

        @param file_path: Path to the file to be used for recording the quantity.
        @type file_path: string
        """

        if path in self.data_writers:
            raise ModelError("Redefinition of data writer '{0}'".format(path))

        self.data_writers[path] = DataWriter(path, file_path)

    def merge(self, other):
        """
        Merge another set of simulation specs into this one.

        @param other: Simulation specs
        @type other: lems.model.simulation.Simulation
        """

        merge_dict(self.runs, other.runs)
        merge_dict(self.records, other.records)
        merge_dict(self.data_displays, other.data_displays)
        merge_dict(self.data_writers, other.data_writers)
