import os

basePath = os.path.dirname(os.path.abspath(__file__))
serviceContoursPath = f'{basePath}\\data\\FM_service_contour_current.txt'

class ServiceContour():
    def __init__(self, data):
        self.id = data["ID"]
        self.service = data["service"]
        self.geom = self.create_geom(data["coords"])

    def as_tuple(self):
        return (self.id, self.service, self.geom)

    def create_geom(self, coords):
        # Create a list of coordinates in this format: 'lat lng' to
        # build a wkt linestring
        coordList = []
        for coord in coords:
            try:
                c = coord.split(',')
                coordList.append(f'{c[1].strip()} {c[0].strip()}')
            except:
                pass

        # Build wkt linestring
        outputCoords = ''
        for coord in coordList:
            outputCoords += f'{coord}, '
        
        # Must end on same coord as begin
        outputCoords += f'{coordList[0]}'

        outputWKT = f'LINESTRING({outputCoords})'
        outputGEOM = f"ST_Polygon('{outputWKT}'::geometry, 4326)"
        
        return outputGEOM
        
        


with open(serviceContoursPath, 'r') as file:
    print("Loading service contours...")
    # Load values as list of tuples
    values = []
    for i, line in enumerate(file.readlines()[1:]):
        # try:
            row = line.split("|")
            data = {
                "ID": row[0].strip(),
                "service": row[1].strip(),
                "coords": row[5:-1]
            }
            record = ServiceContour(data)
            values.append(record.as_tuple())

            
        except:
            print(f'Error on {row}.')

    # Insert values list to stations table
    sql = "insert into servicecontours values %s"
    psycopg2.extras.execute_values(cur, sql, values)
    print("Done\n")
        