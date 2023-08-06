"""Generate Raindrop Trace path using NLDI and user-defined point."""
import geojson

from .utils import geom_to_geojson
from .utils import get_coordsys
from .utils import get_flowgrid
from .utils import get_intersection_point
from .utils import get_local_catchment
from .utils import get_local_flowline
from .utils import get_on_flowline
from .utils import get_raindrop_path
from .utils import get_reach_measure
from .utils import project_point
from .utils import split_flowline


class Flowtrace:
    """Define inputs and outputs for the main Flowtrace class."""

    def __init__(self, x: float, y: float, raindroptrace: bool, direction: str) -> None:
        """Initialize Flowtrace."""
        self.x = x
        self.y = y
        self.raindropTrace = raindroptrace
        self.direction = direction
        self.catchmentIdentifier = None
        self.flowline = None
        self.flw = None
        self.flwdir_transform = None
        self.projected_xy = None
        self.onFlowline = bool

        # geoms
        self.catchmentGeom = None
        self.splitCatchmentGeom = None
        self.upstreamBasinGeom = None
        self.mergedCatchmentGeom = None
        self.intersectionPointGeom = None
        self.raindropPathGeom = None
        self.nhdFlowlineGeom = None
        self.upstreamFlowlineGeom = None
        self.downstreamFlowlineGeom = None
        self.downstreamPathGeom = None

        # outputs
        self.catchment = None
        self.splitCatchment = None
        self.upstreamBasin = None
        self.mergedCatchment = None
        self.intersectionPoint = None
        self.raindropPath = None
        self.nhdFlowline = None
        self.streamInfo = None
        self.upstreamFlowline = None
        self.downstreamFlowline = None
        self.downstreamPath = None

        # create transform
        self.transformToRaster = None
        self.transformToWGS84 = None

        # kick off
        self.run()

    def serialize(self) -> geojson.feature.FeatureCollection:  # noqa C901
        """Convert returns to GeoJSON to be exported."""
        if self.onFlowline is True:
            if self.direction == "up":
                feature1 = geojson.Feature(
                    geometry=self.upstreamFlowline,
                    id="upstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "down":
                feature1 = geojson.Feature(
                    geometry=self.downstreamFlowline,
                    id="downstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "none":
                feature1 = geojson.Feature(
                    geometry=self.nhdFlowline,
                    id="nhdFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

        if self.onFlowline is False:
            if self.direction == "up" and self.raindropTrace is True:
                feature1 = geojson.Feature(
                    geometry=self.upstreamFlowline,
                    id="upstreamFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

            if self.direction == "down" and self.raindropTrace is True:
                feature1 = geojson.Feature(
                    geometry=self.downstreamFlowline,
                    id="downstreamFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

            if self.direction == "none" and self.raindropTrace is True:
                feature1 = geojson.Feature(
                    geometry=self.nhdFlowline,
                    id="nhdFlowline",
                    properties=self.streamInfo,
                )
                feature2 = geojson.Feature(
                    geometry=self.raindropPath, id="raindropPath"
                )
                featurecollection = geojson.FeatureCollection([feature1, feature2])

            if self.direction == "up" and self.raindropTrace is False:
                feature1 = geojson.Feature(
                    geometry=self.upstreamFlowline,
                    id="upstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "down" and self.raindropTrace is False:
                feature1 = geojson.Feature(
                    geometry=self.downstreamFlowline,
                    id="downstreamFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

            if self.direction == "none" and self.raindropTrace is False:
                feature1 = geojson.Feature(
                    geometry=self.nhdFlowline,
                    id="nhdFlowline",
                    properties=self.streamInfo,
                )
                featurecollection = geojson.FeatureCollection([feature1])

        # print('featurecollection', type(featurecollection))
        return featurecollection

    # main functions
    def run(self) -> None:  # noqa C901
        """Run FLowtrace module."""
        # Order of these functions is important!
        self.catchmentIdentifier, self.catchmentGeom = get_local_catchment(
            self.x, self.y
        )
        self.flowline, self.nhdFlowlineGeom = get_local_flowline(
            self.catchmentIdentifier
        )
        self.transformToRaster, self.transformToWGS84 = get_coordsys()
        self.projected_xy = project_point(self.x, self.y, self.transformToRaster)
        self.flw, self.flwdir_transform = get_flowgrid(
            self.catchmentGeom, self.transformToRaster
        )
        self.onFlowline = get_on_flowline(
            self.projected_xy, self.flowline, self.transformToRaster
        )
        self.catchment = geom_to_geojson(self.catchmentGeom)

        if self.onFlowline is True:
            self.intersectionPointGeom = get_intersection_point(
                self.x, self.y, self.onFlowline
            )
            self.streamInfo = get_reach_measure(
                self.intersectionPointGeom, self.flowline
            )
            self.upstreamFlowlineGeom, self.downstreamFlowlineGeom = split_flowline(
                self.intersectionPointGeom, self.flowline
            )

            # Outputs
            if self.direction == "up":
                self.upstreamFlowline = geom_to_geojson(self.upstreamFlowlineGeom)

            if self.direction == "down":
                self.downstreamFlowline = geom_to_geojson(self.downstreamFlowlineGeom)

            if self.direction == "none":
                self.nhdFlowline = geom_to_geojson(self.nhdFlowlineGeom)

        if self.onFlowline is False:
            self.raindropPathGeom = get_raindrop_path(
                self.flw,
                self.projected_xy,
                self.nhdFlowlineGeom,
                self.flowline,
                self.transformToRaster,
                self.transformToWGS84,
            )
            self.intersectionPointGeom = get_intersection_point(
                self.x, self.y, self.onFlowline, self.raindropPathGeom
            )
            # self.streamInfo = get_reach_measure(self.intersectionPointGeom, self.flowline)
            self.upstreamFlowlineGeom, self.downstreamFlowlineGeom = split_flowline(
                self.intersectionPointGeom, self.flowline
            )

            # Outputs
            if self.direction == "up" and self.raindropTrace is True:
                self.upstreamFlowline = geom_to_geojson(self.upstreamFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            if self.direction == "down" and self.raindropTrace is True:
                self.downstreamFlowline = geom_to_geojson(self.downstreamFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            if self.direction == "none" and self.raindropTrace is True:
                self.nhdFlowline = geom_to_geojson(self.nhdFlowlineGeom)
                self.raindropPath = geom_to_geojson(self.raindropPathGeom)

            if self.direction == "up" and self.raindropTrace is False:
                self.upstreamFlowline = geom_to_geojson(self.upstreamFlowlineGeom)

            if self.direction == "down" and self.raindropTrace is False:
                self.downstreamFlowline = geom_to_geojson(self.downstreamFlowlineGeom)

            if self.direction == "none" and self.raindropTrace is False:
                self.nhdFlowline = geom_to_geojson(self.nhdFlowlineGeom)

            if self.raindropTrace is True:
                self.streamInfo = get_reach_measure(
                    self.intersectionPointGeom, self.flowline, self.raindropPathGeom
                )
            if self.raindropTrace is False:
                self.streamInfo = get_reach_measure(
                    self.intersectionPointGeom, self.flowline
                )
