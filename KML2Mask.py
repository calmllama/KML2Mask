import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import sys
import re

def parseArguments():
    parser = argparse.ArgumentParser()
    #Optional Arguments
    parser.add_argument("-g", "--graphical", help="Starts this sript in graphical mode", action='store_true')
    parser.add_argument("-i", "--input", help="KML or KMZ file to be converted", type=str, default="")
    parser.add_argument("-o", "--output", help="TXT file to be created", type=str, default="")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args=parseArguments()

    # only done for windows exe. comment out otherwise
    args.graphical=True

    if args.graphical:
        Tk().withdraw()
        filename=askopenfilename()
    else:
        if args.input and args.output:
            filename=args.input
            outputFilename=args.output
        else:
            print ("Using this tool in headless mode requires the -i and -o arguments for the input and output files respectively")
            sys.exit()
    
    # Intake input file and parse out lat/long
    with open (filename, "r") as inputFile:
        data = inputFile.read().replace('\n', '')
        pointList = re.search('<coordinates>(.*)</coordinates>', data).group(1).split()

        points = []
        for entry in pointList:
            lon = entry.split(',')[0]
            lat = entry.split(',')[1]
            data = lat, lon
            points.append(data)

    # Save as new file
    if args.graphical:
        outputFilename = asksaveasfilename()

    with open(outputFilename, 'w') as file:
        file.write("# Lat/long polygon defines where we want to process video.")
        file.write('\n')
        file.write("# Video will be eliminated outside of this polygon.")
        file.write('\n')
        file.write('default LUT')
        file.write('\n')
        file.write('originLatLong' + ' ' + points[0][0] + ' ' + points[0][1])
        file.write('\n')
        file.write('polylatlong \'video-area\' THRO')
        file.write('\n')
        for point in points:
            file.write(point[0] + ' ' + point[1])
            file.write('\n')
        file.write('endpoly')

        if args.graphical:
            messagebox.showinfo(title='KML-2-Mask', message='Your file has been created sucessfully.\n Thanks for using this lovely app')
        else:
            print ("\nYour file has been crated sucessfully.\n Thanks for using this lovely app\n")
            
    sys.exit()
