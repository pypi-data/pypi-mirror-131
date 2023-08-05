
import os
from pathlib import Path

import h5py
import trimesh
from collections import defaultdict
import numpy as np


def get_interaction_coordinates_from_track_file(filename):
    # if Path(filename).is_file():
    track = h5py.File(filename)
    # other useful info is also in attributes but not needed
    # n_particles = track.attrs["n_particles"]
    # n_coords = track.attrs["n_coords"]
    coords = track["coordinates_1"]
    return [i for i in coords]

def get_all_track_files_in_folder(dir="."):
    unsorted_paths = list(Path(dir).glob("track_*.h5"))
    unsorted_strings = []
    for entry in unsorted_paths:
        unsorted_strings.append(str(entry))
    return sorted(unsorted_strings)

def get_distance_between_two_coords(coordinate_1, coordinate_2):

#     point_a: Tuple[float, float], point_b: Tuple[float, float]
# ) -> float:
#     """Computes the distance between two points.
#     Args:
#         point_a (float, float): X, Y coordinates of the first point
#         point_b (float, float): X, Y coordinates of the second point
#     Returns:
#         float: distance between A and B
#     """

    return np.linalg.norm(coordinate_1 - coordinate_2)


def get_distance_between_iterable_of_coords(coordinates):
    distances = []
    for counter, coord in enumerate(coordinates[:-1]):
        # print('distance between', coords[counter], coords[counter+1])
        distance = get_distance_between_two_coords(coordinates[counter], coordinates[counter + 1])
        distances.append(distance)
    return sum(distances)

def convert_track_files_to_vtk(h5_filename, vtk_filename=''):
    if vtk_filename == '':
        if isinstance(h5_filename, str):
            h5_filename=Path(h5_filename)
        vtk_filename = h5_filename.with_suffix('')
        
    os.system(f"openmc-track-to-vtk {h5_filename} -o {vtk_filename}")

def load_geomtry_into_mesh_volume(filename):
    trimesh_mesh = trimesh.load_mesh(filename)
    # mesh.fill_holes()
    if not trimesh_mesh.is_watertight:
        print(filename, 'is not watertight=')
    return trimesh_mesh

def query_coordinate_inside_mesh_volume(
    trimesh_mesh,
    coordinate,
):

    return trimesh_mesh.contains(coordinate)
    # inside_or_not = is_interaction_inside_mesh(coordinate, trimesh_mesh)
    # if True in inside_or_not:
    #     return True
    # return False

def query_coordinates_inside_mesh_volume(
    trimesh_mesh,
    coordinates,
):
    ture_false_list = []
    coordinate_indexes_that_interact = []
    for counter, coordinate in enumerate(coordinates):
        inside_or_not = query_coordinate_inside_mesh_volume(trimesh_mesh, coordinate)
        if True in inside_or_not:
            ture_false_list.append(True)
            coordinate_indexes_that_interact.append(counter)
        else:
            ture_false_list.append(False)
    return ture_false_list, coordinate_indexes_that_interact

def query_track_file_interacts_inside_mesh_volume(
    track_file,
    trimesh_mesh
):
    coordinates = get_interaction_coordinates_from_track_file(track_file)
    inside_or_not = query_coordinates_inside_mesh_volume(trimesh_mesh, coordinates)
    return inside_or_not

def query_track_file_interact_inside_mesh_file(
    track_file,
    mesh_file
):
    trimesh_mesh = load_geomtry_into_mesh_volume(mesh_file)
    inside_or_not = query_track_file_interacts_inside_mesh_volume(track_file, trimesh_mesh)
    return inside_or_not

    # results_dict = {}
    # results_dict['interacted'] = []
    # results_dict['missed'] = []

    # results_dict = defaultdict()
    # for counter, coord in enumerate(coordinates):
    #     inside_or_not = is_interaction_inside_mesh(coord, trimesh_mesh)
    #     if True in inside_or_not:
    #         results_dict['interacted'].append(coord)
    #     else:
    #         results_dict['missed'].append(coord)
