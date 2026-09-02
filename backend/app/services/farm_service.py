import json
from typing import Any

from geoalchemy2.elements import WKTElement
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.models import Farm, Farmer


class FarmServiceError(Exception):
    pass


class FarmerNotFoundError(FarmServiceError):
    pass


class FarmNotFoundError(FarmServiceError):
    pass


class InvalidGeometryError(FarmServiceError):
    pass


def _coordinate_pair(value: Any) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise InvalidGeometryError("Coordinates must be longitude/latitude pairs.")
    longitude, latitude = value
    if isinstance(longitude, bool) or isinstance(latitude, bool) or not isinstance(longitude, (int, float)) or not isinstance(latitude, (int, float)):
        raise InvalidGeometryError("Coordinates must be numeric longitude/latitude pairs.")
    longitude, latitude = float(longitude), float(latitude)
    if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
        raise InvalidGeometryError("Coordinates are outside valid longitude/latitude ranges.")
    return longitude, latitude


def _polygon_wkt(session: Session, geometry: dict[str, Any]) -> str:
    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) != 1 or not isinstance(coordinates[0], list):
        raise InvalidGeometryError("Polygon geometry must contain one linear ring.")

    ring = [_coordinate_pair(value) for value in coordinates[0]]
    if len(ring) < 2 or ring[0] != ring[-1]:
        raise InvalidGeometryError("Polygon linear rings must be closed.")
    vertices = ring[:-1]
    if len(vertices) < 6:
        raise InvalidGeometryError("Polygon geometry must contain at least six vertices.")

    wkt = "POLYGON((" + ", ".join(f"{longitude} {latitude}" for longitude, latitude in ring) + "))"
    is_valid = session.execute(text("SELECT ST_IsValid(ST_GeomFromText(:wkt, 4326))"), {"wkt": wkt}).scalar_one()
    if not is_valid:
        raise InvalidGeometryError("Polygon geometry is invalid.")
    return wkt


def _point_radius_wkt(session: Session, geometry: dict[str, Any], radius_meters: float | None) -> str:
    if radius_meters is None:
        raise InvalidGeometryError("Point geometry requires radius_meters.")
    longitude, latitude = _coordinate_pair(geometry.get("coordinates"))
    return session.execute(
        text(
            "SELECT ST_AsText("
            "ST_Buffer(ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography, :radius_meters)::geometry"
            ")"
        ),
        {"longitude": longitude, "latitude": latitude, "radius_meters": radius_meters},
    ).scalar_one()


def _geometry_wkt(session: Session, geometry: dict[str, Any], radius_meters: float | None) -> str:
    geometry_type = geometry.get("type") if isinstance(geometry, dict) else None
    if geometry_type == "Polygon":
        if radius_meters is not None:
            raise InvalidGeometryError("radius_meters is only permitted with Point geometry.")
        return _polygon_wkt(session, geometry)
    if geometry_type == "Point":
        return _point_radius_wkt(session, geometry, radius_meters)
    raise InvalidGeometryError("Geometry type must be Polygon or Point.")


def create_farm(session: Session, *, farmer_id: int, geometry: dict[str, Any], radius_meters: float | None) -> Farm:
    if session.query(Farmer).filter(Farmer.farmer_id == farmer_id).one_or_none() is None:
        raise FarmerNotFoundError(f"Farmer {farmer_id} not found.")

    polygon_wkt = _geometry_wkt(session, geometry, radius_meters)
    farm = Farm(
        farmer_id=farmer_id,
        polygon_geom=WKTElement(polygon_wkt, srid=4326),
        area_hectares=None,
        eudr_risk_flag=None,
    )
    session.add(farm)
    session.commit()
    validate_farm(session, farm.farm_id)
    return farm


def validate_farm(session: Session, farm_id: int) -> Farm:
    farm = session.query(Farm).filter(Farm.farm_id == farm_id).one_or_none()
    if farm is None:
        raise FarmNotFoundError(f"Farm {farm_id} not found.")
    area_hectares = session.execute(
        text("SELECT ST_Area(polygon_geom::geography) / 10000 FROM farms WHERE farm_id = :farm_id"),
        {"farm_id": farm_id},
    ).scalar_one()
    if area_hectares is None or area_hectares <= 0:
        raise InvalidGeometryError("Farm geometry has no calculable area.")
    farm.area_hectares = area_hectares
    farm.eudr_risk_flag = area_hectares > 10
    session.commit()
    session.refresh(farm)
    return farm


def get_farm(session: Session, farm_id: int) -> tuple[Farm, dict[str, Any]]:
    row = session.execute(
        select(Farm, text("ST_AsGeoJSON(farms.polygon_geom)")).where(Farm.farm_id == farm_id)
    ).one_or_none()
    if row is None:
        raise FarmNotFoundError(f"Farm {farm_id} not found.")
    farm, geometry_json = row
    return farm, json.loads(geometry_json)
