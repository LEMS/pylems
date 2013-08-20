"""

Utilities for checking generated LEMS code

"""

def validateLEMS(file_name):

    from lxml import etree
    from urllib import urlopen
    schema_file = urlopen("https://raw.github.com/LEMS/LEMS/development/Schemas/LEMS/LEMS_v0.7.1.xsd")
    xmlschema = etree.XMLSchema(etree.parse(schema_file))
    print "Validating %s against %s" %(file_name, schema_file.geturl())
    xmlschema.assertValid(etree.parse(file_name))
    print "It's valid!"


