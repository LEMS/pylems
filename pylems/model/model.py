"""
Model storage

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

class Model:
    """
    Store the model read from a LEMS file.
    """

    default_run = ''
    """ Name of the default simulation to run.
    @type: string """

    def set_default_run(self, default_run):
        """ Set the name of the default simulation to run.
        @param default_run: Name of a simulation to run by default
        @type default_run: string """
        self.default_run = default_run

    def __str__(self):
        s = ''

        s += 'Default run: ' + self.default_run + '\n'

        return s
