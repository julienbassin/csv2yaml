import yaml
import os
import csv
import getopt
import sys


root = os.getcwd()


# takes a csvFile name and output file name/path
def csvToYaml(csvFile, output):
    csvFile.read(3)
    with open(output, 'w') as output_file:
        # https://stackoverflow.com/questions/18897029/read-csv-file-from-url-into-python-3-x-csv-error-iterator-should-return-str
        # need to decode bytes
        csvopen = csv.reader(csvFile)
        keys = next(csvopen)

        selected_row = {}
        for row in csvopen:
            if row[1] == 'in':
                hostname = row[0]
                port = row[4]
                protocol = row[5]
                if hostname not in selected_row.keys():
                    selected_row[hostname] = {protocol: [port]}
                else:
                    if protocol not in selected_row[hostname].keys():
                        selected_row[hostname][protocol] = [port]
                    else:
                        if port not in selected_row[hostname][protocol]:
                            selected_row[hostname][protocol].append(port)

        print(selected_row)
        iptables = []
        for hostname, values in selected_row.items():
            row_object = {
                            'name': hostname,
                            'tcp': values['tcp'],
                            'udp': values['udp']
            }

            iptables.append(row_object)
        yaml.dump({'iptables_rules':iptables}, output_file, default_flow_style=False)

# converts all csv file in this folder
def localCSV(folder=root):
    # print folder
    for f in os.listdir(folder):
        if f.endswith('.csv'):
            csvFile = os.path.join(folder, f)
            output = os.path.join(folder, f.replace('.csv', '.yml'))
            print(output)
            singleCSV(csvFile, output)


# converts only one csv file
def singleCSV(csvFile, output=None):
    output = output if output else root + '/' + (csvFile.split('/')[-1].replace('.csv', '.yml'))
    with open(csvFile, 'r') as csvFile:
        csvToYaml(csvFile, output)


# print -h --help
def usage():
    print(
        '\nUsage:\n-i --input: path of file \n-o --output: path name of output, if left out will convert in this folder using its name as output\n-f --folder: flag indicating input is directory/folder and should be treate as such\n-h --help: print this/help stuff.....')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:uf', ['help', 'input=', 'output=', 'url', 'folder'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    csvFile = None
    output = None
    url = False
    folder = False
    if len(opts) == 0:
        localCSV()
        exit()
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-i', '--input'):
            csvFile = a
        elif o in ('-o', '--output'):
            output = a        
        elif o in ('-f', '--folder'):
            folder = True
        else:
            print('unhandled option')
    if folder:
        localCSV(csvFile)
        exit()
    singleCSV(csvFile, output)


if __name__ in ("__main__", "csvyml"):
    main()
