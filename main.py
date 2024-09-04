import sys
import json
import argparse
from datetime import datetime, timedelta, timezone

import simplekml
from tqdm import tqdm

fileName = ""

parser = argparse.ArgumentParser(description="no -e option only 1 day data")
parser.add_argument("-t", "--timeline", help="JSON file path", type=str, required=True)
parser.add_argument("-s", "--start", help="start date:2024-01-01", type=str, required=True)
parser.add_argument("-e", "--end", help="end date:2024-01-01", type=str)

args = parser.parse_args()
if args.end == None:
    args.end = args.start
    fileName = args.start + ".kml"
else:
    fileName = args.start + "_" + args.end + ".kml"

def main():
    allHistory = json.load(open(args.timeline, 'r'))

    kml = simplekml.Kml()
    style = simplekml.Style()
    style.iconstyle.icon.href = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
    style.iconstyle.color = simplekml.Color.orangered
    style.linestyle.width = 4
    style.linestyle.color = simplekml.Color.deepskyblue

    longDateFormat = '%Y-%m-%dT%H:%M'
    dateFormat = '%Y-%m-%d'
    sDate = datetime.strptime(args.start, dateFormat)
    eDate = datetime.strptime(args.end, dateFormat)

    print("KML Create for", fileName)
    for i in tqdm(range((eDate - sDate).days + 1)):
        date = sDate.strftime(dateFormat)
        line = kml.newlinestring(name=date)

        for parse in allHistory:
            startDate = parse['startTime'][0:10]
            if date == startDate and parse.get('visit') != None:
                spotID = parse['visit']['topCandidate']['placeID']
                geo = parse['visit']['topCandidate']['placeLocation'][4:].split(',')
                point = kml.newpoint(name="spot", description=spotID, coords=[(geo[1], geo[0])])
                point.style = style

            startDate = datetime.strptime(parse['startTime'][0:16], longDateFormat).replace(tzinfo=timezone.utc).astimezone().strftime(longDateFormat)[0:10]
            if date == startDate and parse.get('timelinePath') != None:
                for points in parse['timelinePath']:
                    geo = points['point'][4:].split(',')
                    line.coords.addcoordinates([(geo[1], geo[0])])
                    line.style = style

        sDate += timedelta(1)

    kml.save(fileName)
    sys.exit()

if __name__ == "__main__":
    main()

