from typing import List
from napari.layers.image.image import Image
from napari.layers.points.points import Points
from napari.layers.tracks.tracks import Tracks
from koil.qt import FutureWrapper
from mikro.schema import Representation, RepresentationVariety, Sample, Table
from napari import Viewer
import xarray as xr
from qtpy import QtWidgets
from qtpy.QtCore import Signal, QObject
import logging
from mikro import gql
import pandas as pd
import numpy as np
import dask.array as da

logger = logging.getLogger(__name__)


class DownloadIndicator(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel("Downloading")

    def setLabel(self, rep: Representation):
        self.label.setText(f"Downloading {rep.name}")


class StageHelper(QObject):
    openStack = Signal(xr.DataArray, Representation)
    openMultiStack = Signal(list, Representation)
    openPoints = Signal(np.ndarray, str)
    openLabels = Signal(xr.DataArray, Representation)
    openImage = Signal(xr.DataArray, Representation)
    downloadingImage = Signal(Representation)
    downloadingDone = Signal(Representation)

    def __init__(self, viewer: Viewer, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.viewer = viewer

        self.downloadingDialog = DownloadIndicator()

        self.openImage.connect(self.open_xarray_as_rgb)
        self.openStack.connect(self.open_xarray_as_stack)
        self.openMultiStack.connect(self.open_xarray_as_multiview)
        self.openPoints.connect(self.open_array_as_points)
        self.openLabels.connect(self.open_xarray_as_labels)

        self.downloadingImage.connect(self.on_image_download)
        self.downloadingDone.connect(self.on_image_downloaded)

    def on_image_download(self, rep: Representation):
        self.downloadingDialog.setLabel(rep)
        self.downloadingDialog.show()

    def on_image_downloaded(self, rep: Representation):
        self.downloadingDialog.hide()

    def open_xarray_as_multiview(self, items: list, rep: Representation):
        self.viewer.add_image(
            items,
            name=rep.name,
            multiscale=True,
            metadata={"rep": rep},
        )

    def open_xarray_as_stack(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_image(
            array,
            rgb=False,
            name=rep.name,
            metadata={"rep": rep},
        )

    def open_array_as_points(self, array: np.ndarray, name="Points"):
        self.viewer.add_points(
            array,
            name=name,
        )

    def open_xarray_as_rgb(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_image(
            array,
            rgb=True,
            name=rep.name,
            metadata={"rep": rep},
        )  # why this werid transposing... hate napari

    def open_xarray_as_labels(self, array: xr.DataArray, rep: Representation):
        self.viewer.add_labels(
            rep,
            rgb=False,
            name=rep.name,
            metadata={"rep": rep},
        )  # why this werid transposing... hate napari

    def open_as_layer(self, rep: Representation, stream=True):
        array = rep.data.squeeze()

        if (
            rep.variety == RepresentationVariety.VOXEL
            or rep.variety == RepresentationVariety.UNKNOWN
        ):
            if "t" in array.dims:
                raise NotImplementedError("Time series are not supported yet")

            elif "z" in array.dims:
                if "c" in array.dims:
                    array = array.transpose(*list("zxyc"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openStack.emit(array, rep)
                else:
                    array = array.transpose(*list("zxy"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openStack.emit(array, rep)

            elif "c" in array.dims:
                if array.sizes["c"] == 3:
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)

                    self.openImage.emit(array, rep)
                else:
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)
                    self.openStack.emit(array, rep)
            elif "x" in array.dims and "y" in array.dims:
                if not stream:
                    self.downloadingImage.emit(rep)
                    array = array.compute()
                    self.downloadingDone.emit(rep)
                self.openStack.emit(array, rep)
            else:
                raise NotImplementedError(f"What the fuck??? {array.dims}")

        elif rep.variety == RepresentationVariety.MASK:
            if "t" in array.dims:
                raise NotImplementedError("Time series are not supported yet")

            if "z" in array.dims:
                if "c" in array.dims:
                    raise NotImplementedError("We have not managed to do things yet...")
                else:
                    array = array.transpose(*list("zxy"))
                    if not stream:
                        self.downloadingImage.emit(rep)
                        array = array.compute()
                        self.downloadingDone.emit(rep)
                    self.openLabels.emit(array, rep)
        else:
            raise NotImplementedError(
                f"Cannot open Representation of Variety {rep.variety}"
            )

    def open_multiscale(self, rep: Representation):

        query = gql(
            """
            query DetailRep($id: ID!) {
                representation(id: $id){
                    name
                    store
                    derived(tags: ["multiscale"]) {
                        name
                        tags
                        meta 
                        store
                    }
                }
            }
            """
        ).run(id=rep.id)

        parent = query.representation

        childrens = [rep.data.squeeze() for rep in query.representation.derived]

        self.openMultiStack.emit([parent.data.squeeze()] + childrens, parent)

    def open_aside(self, reps: List[Representation]):

        query = gql(
            """
            query DetailRep($ids: [String]) {
                representations(ids: $ids){
                    name
                    store
                }
            }
            """
        ).run(ids=reps)

        max_shape = np.max([rep.data.shape for rep in reps], axis=0)
        arrays = [da.zeros(max_shape) for rep in reps]
        for index, array in enumerate(arrays):
            array[
                : reps[index].data.shape[0],
                : reps[index].data.shape[1],
                : reps[index].data.shape[2],
                : reps[index].data.shape[3],
                : reps[index].data.shape[4],
            ] = reps[index].data

        concatz = xr.DataArray(da.concatenate(arrays, axis=4)).compute()

        self.openStack.emit(concatz, reps[0])

    def open_with_localizations(self, rep: Representation):

        query = gql(
            """
            query Representation($id: ID!){
                representation(id: $id){
                    store
                    name
                    tables(tags: ["localization"]) {
                        id
                        store
                    }
                }
            }
            """
        ).run(id=rep.id)

        rep = query.representation
        localizations = rep.tables[0].data
        localizations = localizations[
            [
                "Plane",
                "CentroidY(px)",
                "CentroidX(px)",
            ]
        ]
        locs = localizations.to_numpy()

        self.openStack.emit(rep.data.compute(), rep)
        self.openPoints.emit(locs, "localizations")

    def upload_everything(self, image_name: str = None, sample: Sample = None):

        assert len(self.viewer.layers.selection) > 0, "No Image Was Selected"

        image_layers = [
            layer for layer in self.viewer.layers.selection if isinstance(layer, Image)
        ]

        assert len(image_layers) != 0, "You need to select only one image to upload"
        assert (
            len(image_layers) == 1
        ), "You can only have one and only one Image selected (points are okay)"

        image_layer = image_layers[0]

        image_layer.data
        image_layer.ndim

        assert image_layer.ndim >= 2, "This is not an Image"

        if image_layer.ndim == 2:
            if image_layer.rgb:
                xarray = (
                    xr.DataArray(image_layer.data, dims=list("xyc"))
                    .expand_dims("z")
                    .expand_dims("t")
                )
            else:
                xarray = (
                    xr.DataArray(image_layer.data, dims=list("xy"))
                    .expand_dims("c")
                    .expand_dims("z")
                    .expand_dims("t")
                )

        if image_layer.ndim == 3:
            xarray = (
                xr.DataArray(image_layer.data, dims=list("zxy"))
                .expand_dims("c")
                .expand_dims("t")
            )

        if image_layer.ndim == 4:
            xarray = xr.DataArray(image_layer.data, dims=list("tzxy")).expand_dims("c")

        if image_layer.ndim == 5:
            xarray = xr.DataArray(image_layer.data, dims=list("tzxyc"))

        rep = Representation.objects.from_xarray(
            xarray, name=image_name or image_layer.name, sample=sample
        )

        point_layers = [
            layer for layer in self.viewer.layers.selection if isinstance(layer, Points)
        ]

        for layer in point_layers:

            layer_data = layer.data
            point_dims = layer_data.shape[1]

            if point_dims == 3:
                points_df = pd.DataFrame(
                    data=layer_data, columns=["IndexZ", "IndexX", "IndexY"]
                )
            if point_dims == 2:
                points_df = pd.DataFrame(data=layer_data, columns=["IndexX", "IndexY"])

            table = Table.objects.from_df(
                points_df, name=layer.name, representation=rep, tags=["roi:points"]
            )

        track_layers = [
            layer for layer in self.viewer.layers.selection if isinstance(layer, Tracks)
        ]

        return rep

    def get_active_layer_as_xarray(self):
        layer = self.viewer.layers[0]

        data = layer.data
        ndim = layer.ndim

        if ndim == 2:
            # first two dimensions is x,y and then channel
            if layer.rgb:
                # We are dealing with an rgb image
                stack = (
                    xr.DataArray(data, dims=list("xyc"))
                    .expand_dims("z")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )
            else:
                stack = (
                    xr.DataArray(data, dims=list("xy"))
                    .expand_dims("c")
                    .expand_dims("z")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )

        if ndim == 3:
            # first three dimensios is z,x,y and then channel?
            if len(data.shape) == 3:
                stack = (
                    xr.DataArray(data, dims=list("zxy"))
                    .expand_dims("c")
                    .expand_dims("t")
                    .transpose(*list("xyczt"))
                )
            else:
                raise NotImplementedError("Dont know")

        return stack, layer.name
