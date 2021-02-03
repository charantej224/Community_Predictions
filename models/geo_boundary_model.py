from utilities.file_utils import read_json


class BoundaryMapper:
    def __init__(self, input_block_group, input_neighborhood, police_boundary, council_boundary):
        self.input_block_group = read_json(input_block_group)
        self.input_neighborhood = read_json(input_neighborhood)
        self.police_boundary = read_json(police_boundary)
        self.council_boundary = read_json(council_boundary)

    def map_block_group(self, latitude, longitude, response):
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
                    response["block_id"] = each
                    return
        return

    def map_neighborhood(self, input_boundary, latitude, longitude, key_list, response):
        for each in input_boundary['features']:
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
                    for key in key_list:
                        if key in each["properties"]:
                            response[key] = each["properties"][key]
                    return
        return

    def get_boundaries(self, in_latitude, in_longitude):
        key_list = ["nbhname", "block_id", "nbhid", "division", "divisionname", "indistrict", "atlarge", "district"]
        response = {}
        for key in key_list:
            response[key] = "N/A"
        self.map_block_group(in_latitude, in_longitude, response)
        self.map_neighborhood(self.input_neighborhood, in_latitude, in_longitude, key_list, response)
        self.map_neighborhood(self.police_boundary, in_latitude, in_longitude, key_list, response)
        self.map_neighborhood(self.council_boundary, in_latitude, in_longitude, key_list, response)
        return response
