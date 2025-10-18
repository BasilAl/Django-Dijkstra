from django.shortcuts import render

from routes.forms import UploadCSVForm, DijkstraForm
from dijkstra import dijkstra
from graph_dijkstra import Graph
from helpers import graph_loader, load_coordinates


def upload_csv(request):
    upload_form = UploadCSVForm()
    dijkstra_form = None
    results = None

    if "graph" in request.session:
        graph = Graph.from_dict(request.session["graph"])
    else:
        print("No graph found in session.")
        graph = None

    if request.method == "POST":
        if "upload_csv" in request.POST:
            upload_form = UploadCSVForm(request.POST, request.FILES)
            if upload_form.is_valid():
                csv_file = request.FILES["csv_file"]
                graph = graph_loader(csv_file)
                dijkstra_form = DijkstraForm(graph_nodes=list(graph.nodes.keys()))
        elif "calculate_dijkstra" in request.POST:
            if graph:
                dijkstra_form = DijkstraForm(
                    request.POST, graph_nodes=list(graph.nodes.keys())
                )
                if dijkstra_form.is_valid():
                    source = dijkstra_form.cleaned_data["source"]
                    destination = dijkstra_form.cleaned_data["destination"]
                    optimise_by = dijkstra_form.cleaned_data["optimise_by"]
                    results = dijkstra(
                        graph,
                        source,
                        destination,
                        optimise=optimise_by,
                    )

    if graph:
        request.session["graph"] = graph.to_dict()
    coordinates = load_coordinates()
    route_coordinates = None
    if coordinates:
        route_coordinates = (
            [coordinates[node[0].name] for node in results["path"]] if results else None
        )
    return render(
        request,
        "main.html",
        {
            "upload_form": upload_form,
            "dijkstra_form": dijkstra_form if graph else None,
            "results": results,
            "graph": graph if graph else None,
            "route_coordinates": route_coordinates if coordinates else None,
        },
    )
