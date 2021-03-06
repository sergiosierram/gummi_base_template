#!/usr/bin/env python

import ruamel.yaml, sys #ruamel preserves comments with round_trip_XXX commands. at least some of them, which is better for us.

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    if b is None:
        return a
    elif a is None:
        return b
    else:
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

if  len(sys.argv) != 4:
    raise NameError('Function needs 3 arguments: source_yaml_file_1 source_yaml_file_2  output_yaml_file ')

with open(sys.argv[1], 'r') as stream:
    data1 = ruamel.yaml.round_trip_load(stream)

with open(sys.argv[2], 'r') as stream:
    data2 = ruamel.yaml.round_trip_load(stream)

data_both = merge(data1,data2)

stream = file(sys.argv[3], 'w')
stream.write("##########################################################################################\n")
stream.write("# This file was autogenerated by " + sys.argv[0] + " and should not be mannually editted. #\n" )
stream.write("# Edit file " + sys.argv[1] + " #\n" )
stream.write("# And file " + sys.argv[2] + " instead. #\n" )
stream.write("##########################################################################################\n")

ruamel.yaml.round_trip_dump(data_both, stream, default_flow_style=False)    # Write a YAML representation of data to 'document.yaml'.
# print ruamel.yaml.round_trip_dump(data_both, default_flow_style=False)      # Output the document to the screen.
