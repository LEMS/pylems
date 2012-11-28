"""
@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

class Options:
    """
    PyLEMS command line options
    """

    def __init__(self):
        """
        Constructor.
        """

        self.include_dirs = ['.']
        """ List of directories that PyLEMS will search in addition to the
        working directory for included LEMS files.
        @type: list(string) """

        self.xsl_include_dirs = ['.', './xsl']
        """ List of directories that PyLEMS will search in addition to the
        working directory for XSL files.
        @type: list(string) """

    def add_include_directory(self, include_dir):
        """
        Add a directory to the list of include directories for LEMS files.

        @param include_dir: Directory to be included
        @type include_dir: string
        """

        if include_dir not in self.include_dirs:
            self.include_dirs.append(include_dir)

    def add_xsl_include_directory(self, include_dir):
        """
        Add a directory to the list of include directories for XSL files.

        @param include_dir: Directory to be included
        @type include_dir: string
        """

        if include_dir not in self.xsl_include_dirs:
            self.xsl_include_dirs.append(include_dir)

    def __str__(self):
        return '<{0}> <{1}>'.format(self.include_dirs,
                                    self.xsl_include_dirs)

options_param_count = {
    '-I':1,
    '-include':1,

    '-XI':1,
    '-xsl-include':1
    }

def parse_options(argv):
    options = Options()

    while argv:
        option = argv[0]
        argv = argv[1:]

        params = []
        print option
        if option in options_param_count:
            for i in xrange(options_param_count[option]):
                if len(argv) > 0:
                    params.append(argv[0])
                else:
                   raise Exception("Option '{0}' needs {1} parameters".format(
                       arg, options_param_count[option]))
            argv = argv[1:]

        if option == '-I' or option == '-include':
            options.add_include_directory(params[0])
        elif option == '-XI' or option == '-xsl-include':
            options.add_xsl_include_directory(params[0])

    return options

print parse_options(['-I', 'path1',
                     '-XI', 'path2',
                     '-include', 'path3',
                     '-xsl-include', 'path4'])
