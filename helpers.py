import csv
from io import TextIOWrapper
from typing import Union, Dict, Any, BinaryIO

from django.core.files.uploadedfile import UploadedFile

from graph_dijkstra import Graph


def graph_loader(file: Union[str, BinaryIO, UploadedFile] = "routes.csv") -> Graph:
    """Reads the CSV and creates a Graph object."""
    graph = Graph()
    if isinstance(file, str):
        with open(file, "r") as file_object:
            _populate_rows(file_object, graph)
    else:
        file_object = TextIOWrapper(file, "utf-8")
        _populate_rows(file_object, graph)
    return graph


def _populate_rows(file_object, graph):
    rows = csv.DictReader(file_object)
    for row in rows:
        try:
            graph.add_vertex(
                source=row["source"],
                destination=row["destination"],
                cost=float(row["cost"]),
                time=float(row["time"]),
                mode=row["type"],
            )
        except KeyError as e:
            raise ValueError(f"Missing required field in row: {row}") from e
        except ValueError as e:
            raise ValueError(f"Invalid data in row: {row}") from e


def load_coordinates() -> Dict[str, Any]:
    coordinates = {}
    try:
        with open("cities.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                coordinates[row["city"]] = {
                    "lat": float(row["latitude"]),
                    "lon": float(row["longitude"]),
                }
    except FileNotFoundError:
        return {}
    return coordinates
