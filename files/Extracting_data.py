#!/usr/bin/python3
def get_ranges_from_file(filename):
    data = {'ports': {}}
    ranges = {}
    with open(filename, 'r') as f:
        for line in f:
            if "parameter" in line:
                line = line.replace(',', '')
                _, param, _, value = line.split(maxsplit=3)
                try:
                    value = int(value)
                except ValueError:
                    pass
                ranges[param] = value
            if "input" in line or "output" in line:
                parts = line.strip().split()
                port_type = parts[0]
                if parts[-2] == "input":
                    port_range = "None"
                else:
                    port_range = parts[-2]

                if (port_range != 'None' and parts[-2] != 'reg'):
                    port_name = parts[-1].rstrip(',')
                    data['ports'][port_name] = {    
                        'type': port_type,
                        'range': '['+str((ranges[port_range[1:len(port_range)-5]])-1)+port_range[len(port_range)-3:]
                    }
                else:
                    port_name = parts[-1].rstrip(',')
                    data['ports'][port_name] = {
                        'type': port_type,
                        'range': 'None'
                    }
    return data