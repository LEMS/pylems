"""
Simulation specification classes.

@author: Gautham Ganapathy
@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)
@contact: gautham@lisphacker.org
"""

from lems.base import LEMSBase

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
        @type: str """

        self.variable = variable
        """ The name of an independent state variable according to which the
        target component will be run.
        @type: str """

        self.increment = increment
        """ Increment of the state variable on each step.
        @type: str """

        self.total = total
        """ Final value of the state variable.
        @type: str """

class Record(LEMSBase):
    """
    Stores the parameters of a <Record> statement.
    """

    def __init__(self, quantity, scale = '1', color = '#000000'):
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """

        self.quantity = quantity
        """ Path to the quantity to be recorded.
        @type: str """

        self.scale = scale
        """ Text parameter to be used for scaling the quantity before display.
        @type: str """

        self.color = color
        """ Text parameter to be used to specify the color for display.
        @type: str """

class DataOutput(LEMSBase):
    """
    Generic data output specification class.
    """

    def __init__(self):
        """
        Constuctor.
        """

        pass

class DataDisplay(DataOutput):
    """
    Stores specification for a data display.
    """

    def __init__(self, title, data_region):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """

        DataOutput.__init__(self)

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

        DataOutput.__init__(self)
        
        self.path = path
        """ Path to the quantity to be saved to file.
        @type: string """

        self.file_path = file_path
        """ Text parameter to be used for the path to the file for
        saving this quantity
        @type: string """

class Simulation(LEMSBase):
    """
    Stores the simulation-related attributes of a component-type.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.runs = {}
        """ Map of runs in this dynamics regime.
        @type: Map(string -> lems.model.simulation.Run) """

        self.records = {}
        """ Map of recorded variables in this dynamics regime.
        @type: Map(string -> lems.model.simulation.Record """

        self.data_displays = {}
        """ Map of data displays mapping titles to regions.
        @type: Map(string -> string) """

        self.data_writers = {}
        """ Map of recorded variables to data writers.
        @type: Map(string -> lems.model.simulation.DataWriter """

    def add_run(self, run):
        """
        Adds a runnable target component definition to the list of runnable
        components stored in this context.

        @param run: Run specification
        @type run: lems.model.simulation.Run
        """

        self.runs[run.component] = run

    def add_record(self, record):
        """
        Adds a record object to the list of record objects in this dynamics
        regime.

        @param record: Record object to be added.
        @type record: lems.model.simulation.Record
        """

        self.records[record.quantity] = record

    def add_data_display(self, data_display):
        """
        Adds a data display to this simulation section.

        @param data_display: Data display to be added.
        @type data_display: lems.model.simulation.DataDisplay
        """

        self.data_displays[data_display.title] = data_display

    def add_data_writer(self, data_writer):
        """
        Adds a data writer to this simulation section.

        @param data_writer: Data writer to be added.
        @type data_writer: lems.model.simulation.DataWriter
        """

        self.data_writers[data_writer.path] = data_writer
