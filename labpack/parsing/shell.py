''' a package of functions for parsing STDOUT and STDERR '''
__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = 'MIT'

def convert_table(shell_output, delimiter='\t|\s{2,}', output='dict'):

    '''
        a method to convert a STDOUT shell table into a python data structure
        
    :param shell_output: string from STDOUT with headers
    :param delimiter: string with regex pattern delimiting headers
    :param output: string with type of structure to output (dict, list or csv)
    :return: list of dictionaries or list of lists or string with csv format
    '''
    
# retrieve header columns 
    import re
    gap_pattern = re.compile(delimiter)
    output_lines = shell_output.splitlines()
    column_headers = gap_pattern.split(output_lines[0])
    blank_index = column_headers.index('')
    if blank_index > -1:
        column_headers.pop(blank_index)

# generate indices tuples
    indices = []
    for i in range(len(column_headers)):
        if i + 1 < len(column_headers):
            indices.append(( 
                output_lines[0].find(column_headers[i]), 
                output_lines[0].find(column_headers[i + 1]) 
            ))
        else:
            indices.append((
                output_lines[0].find(column_headers[i]),
                -1
            ))

# add headers to output
    python_list = []
    csv_string = ''
    if output == 'dict':
        pass
    elif output == 'list':
        python_list.append(column_headers)
    elif output == 'csv':
        for i in range(len(column_headers)):
            if i:
                csv_string += ','
            csv_string += column_headers[i]
    else:
        raise ValueError('output argument must be one of dict, list or csv values.')

# add rows to output
    for i in range(1, len(output_lines)):
        if output == 'dict':
            row_details = {}
            for j in range(len(column_headers)):
                row_details[column_headers[j]] = output_lines[i][indices[j][0]:indices[j][1]].rstrip()
            python_list.append(row_details)
        elif output == 'list':
            row_list = []
            for j in range(len(column_headers)):
                row_list.append(output_lines[i][indices[j][0]:indices[j][1]]).rstrip()
            python_list.append(row_list)
        elif output == 'csv':
            csv_string += '\n'
            for j in range(len(column_headers)):
                if j:
                    csv_string += ','
                csv_string += output_lines[i][indices[j][0]:indices[j][1]].rstrip()

# return output
    if csv_string:
        return csv_string
    
    return python_list