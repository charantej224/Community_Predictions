from utilities.file_utils import read_json


class BoundaryMapper:
    def __init__(self, input_block_group, input_neighborhood):
        self.input_block_group = read_json(input_block_group)
        self.input_neighborhood = read_json(input_neighborhood)

    def map_block_group(self, latitude, longitude):
        for each in self.input_block_group.keys():
            right_top, right_bottom = False, False
            left_top, left_bottom = False, False
            list_geo_points = self.input_block_group[each]['BOUNDARIES']
            for each_point in list_geo_points:
                if latitude < each_point[0] and longitude < each_point[1]:
                    right_top = True
                if latitude < each_point[0] and longitude > each_point[1]:
                    right_bottom = True
                if latitude > each_point[0] and longitude > each_point[1]:
                    left_bottom = True
                if latitude > each_point[0] and longitude < each_point[1]:
                    left_top = True
                if right_top and right_bottom and left_top and left_bottom:
                    print(f'block id : {each}')
                    return each
        return "N/A"

    def map_neighborhood(self, latitude, longitude):
        for each in self.input_neighborhood['features']:
            right_top, right_bottom = False, False
            left_top, left_bottom = False, False
            list_geo_points = each['geometry']['coordinates'][0][0]
            for each_point in list_geo_points:
                if latitude < each_point[1] and longitude < each_point[0]:
                    right_top = True
                if latitude < each_point[1] and longitude > each_point[0]:
                    right_bottom = True
                if latitude > each_point[1] and longitude > each_point[0]:
                    left_bottom = True
                if latitude > each_point[1] and longitude < each_point[0]:
                    left_top = True
                if right_top and right_bottom and left_top and left_bottom:
                    return each["properties"]["nbhname"], each["properties"]['nbhid']
        return "N/A", "N/A"

    def get_boundaries(self, in_latitude, in_longitude):
        block_id = self.map_block_group(in_latitude, in_longitude)
        nbh_name, nbh_id = self.map_neighborhood(in_latitude, in_longitude)
        return {"block_id": block_id, "nbh_name": nbh_name, "nbh_id": nbh_id}
