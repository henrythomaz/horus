"""
HORUS - Geração do mapa de áreas de risco da missão.

Entrada:
    tests/mission_001/results/risk_result.json

Saídas:
    tests/mission_001/results/risk_map.html
    tests/mission_001/results/risk_map.geojson

Nesta versão:
- o risco é representado por POLÍGONOS/ÁREAS, e não por bolinhas;
- imagens próximas com o mesmo nível de risco são agrupadas em uma zona;
- a zona é formada pelo contorno dos pontos + uma margem;
- VERY_LOW continua como ponto, pois não representa uma zona prioritária;
- LOW/MEDIUM/HIGH geram zonas;
- percurso, fotos detectadas e fotos sem detecção continuam separados;
- resumo fica no canto superior esquerdo;
- controle de camadas fica no canto superior direito.

IMPORTANTE:
As zonas são uma representação de priorização do MVP.
Não são o footprint real da câmera e não representam a posição
geográfica exata de cada objeto detectado.
"""

from __future__ import annotations

import html
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import folium
except ImportError:
    print("Erro: a biblioteca 'folium' não está instalada.")
    print("Instale com: pip install folium")
    sys.exit(1)

try:
    from shapely.geometry import MultiPoint, Point, Polygon, mapping
    from shapely.ops import unary_union
except ImportError:
    print("Erro: a biblioteca 'shapely' não está instalada.")
    print("Instale com: pip install shapely")
    sys.exit(1)


MVP_DIR = Path(__file__).resolve().parent.parent
MISSION_DIR = MVP_DIR / "tests" / "mission_001"
RESULTS_DIR = MISSION_DIR / "results"

INPUT_FILE = RESULTS_DIR / "risk_result.json"
OUTPUT_HTML = RESULTS_DIR / "risk_map.html"
OUTPUT_GEOJSON = RESULTS_DIR / "risk_map.geojson"


RISK_COLORS = {
    "VERY_LOW": "#2E7D32",
    "LOW": "#F9A825",
    "MEDIUM": "#EF6C00",
    "HIGH": "#C62828",
}

RISK_LABELS = {
    "VERY_LOW": "Muito baixo",
    "LOW": "Baixo",
    "MEDIUM": "Médio",
    "HIGH": "Alto",
}

# Somente LOW, MEDIUM e HIGH geram áreas.
AREA_LEVELS = ("HIGH", "MEDIUM", "LOW")

# Margem adicionada ao redor do contorno das fotos.
# É pequena propositalmente: a ideia é criar um hotspot visual,
# não fingir que conhecemos o footprint da câmera.
ZONE_MARGIN_M = {
    "LOW": 7.0,
    "MEDIUM": 10.0,
    "HIGH": 12.0,
}

# Distância máxima para considerar duas imagens do mesmo nível
# como pertencentes ao mesmo hotspot.
CLUSTER_DISTANCE_M = 22.0


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido em {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("O conteúdo do JSON deve ser um objeto.")

    return data


def valid_location(record: dict[str, Any]) -> bool:
    location = record.get("location")

    if not isinstance(location, dict):
        return False

    lat = location.get("latitude")
    lon = location.get("longitude")

    return (
        isinstance(lat, (int, float))
        and isinstance(lon, (int, float))
        and -90 <= float(lat) <= 90
        and -180 <= float(lon) <= 180
    )


def risk_label(level: str) -> str:
    return RISK_LABELS.get(level, level)


def class_counts(record: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for detection in record.get("detections", []):
        if not isinstance(detection, dict):
            continue

        class_name = str(detection.get("class", "unknown"))
        counts[class_name] = counts.get(class_name, 0) + 1

    return counts


def popup_html(record: dict[str, Any]) -> str:
    filename = html.escape(str(record.get("filename", "desconhecido")))
    location = record.get("location", {})
    detections = record.get("detections", [])
    risk_score = float(record.get("risk_score", 0.0))
    risk_level = str(record.get("risk_level", "VERY_LOW"))

    latitude = float(location["latitude"])
    longitude = float(location["longitude"])
    altitude = location.get("altitude")

    altitude_text = (
        "Não informado"
        if altitude is None
        else f"{float(altitude):.2f} m"
    )

    counts = class_counts(record)

    if counts:
        rows = "".join(
            f"""
            <tr>
                <td style="padding:3px 0;">{html.escape(name)}</td>
                <td style="padding:3px 0;text-align:right;">{count}</td>
            </tr>
            """
            for name, count in sorted(counts.items())
        )

        detections_html = f"""
        <table style="width:100%;border-collapse:collapse;font-size:12px;">
            <thead>
                <tr>
                    <th style="text-align:left;border-bottom:1px solid #ddd;">
                        Classe
                    </th>
                    <th style="text-align:right;border-bottom:1px solid #ddd;">
                        Qtd.
                    </th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """
    else:
        detections_html = "<p style='margin:4px 0;'>Nenhuma detecção.</p>"

    return f"""
    <div style="width:315px;font-family:Arial,sans-serif;">
        <h4 style="margin:0 0 8px 0;">{filename}</h4>

        <div style="
            padding:8px;
            border-radius:6px;
            background:#f5f5f5;
            margin-bottom:8px;
        ">
            <b>Risco:</b> {html.escape(risk_label(risk_level))}<br>
            <b>Score:</b> {risk_score:.4f}
        </div>

        <b>Localização da imagem</b>
        <div style="margin:4px 0 8px 0;">
            Latitude: {latitude:.7f}<br>
            Longitude: {longitude:.7f}<br>
            Altitude: {altitude_text}
        </div>

        <b>Detecções</b>
        {detections_html}

        <div style="
            margin-top:8px;
            padding-top:6px;
            border-top:1px solid #ddd;
            color:#666;
            font-size:10px;
        ">
            A área representa um hotspot de priorização do MVP.
            Não representa o footprint real da câmera.
        </div>
    </div>
    """


def local_xy(
    lon: float,
    lat: float,
    origin_lat: float,
) -> tuple[float, float]:
    """
    Converte lon/lat para coordenadas locais em metros.
    Suficiente para a pequena área de uma missão.
    """
    meters_lat = 110_540.0
    meters_lon = 111_320.0 * math.cos(math.radians(origin_lat))

    return lon * meters_lon, lat * meters_lat


def haversine_m(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    radius = 6_371_000.0

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    )

    return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def cluster_records(
    records: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    """
    Agrupa registros por proximidade.

    Dois pontos pertencem ao mesmo cluster quando existe conexão
    entre eles por pontos cuja distância seja <= CLUSTER_DISTANCE_M.
    """
    if not records:
        return []

    clusters: list[list[dict[str, Any]]] = []
    unused = set(range(len(records)))

    while unused:
        seed = unused.pop()
        cluster_indices = {seed}
        changed = True

        while changed:
            changed = False

            for index in list(unused):
                record = records[index]
                location = record["location"]
                lat = float(location["latitude"])
                lon = float(location["longitude"])

                belongs = False

                for cluster_index in cluster_indices:
                    anchor = records[cluster_index]
                    anchor_location = anchor["location"]

                    distance = haversine_m(
                        lat,
                        lon,
                        float(anchor_location["latitude"]),
                        float(anchor_location["longitude"]),
                    )

                    if distance <= CLUSTER_DISTANCE_M:
                        belongs = True
                        break

                if belongs:
                    cluster_indices.add(index)
                    unused.remove(index)
                    changed = True

        clusters.append([records[index] for index in sorted(cluster_indices)])

    return clusters


def xy_to_lon_lat(
    x: float,
    y: float,
    origin_lat: float,
) -> tuple[float, float]:
    meters_lat = 110_540.0
    meters_lon = 111_320.0 * math.cos(math.radians(origin_lat))

    return x / meters_lon, y / meters_lat


def geometry_to_geojson(geometry, origin_lat: float) -> dict[str, Any]:
    """
    Converte uma geometria Shapely em coordenadas GeoJSON.

    As geometrias são calculadas em um plano local métrico.
    Antes de escrever o GeoJSON, cada vértice é convertido de volta para
    longitude/latitude, na ordem exigida pelo padrão: [longitude, latitude].
    """
    if geometry.geom_type == "Polygon":
        rings = []

        exterior = []
        for x, y in geometry.exterior.coords:
            lon, lat = xy_to_lon_lat(x, y, origin_lat)
            exterior.append([lon, lat])
        rings.append(exterior)

        for interior in geometry.interiors:
            ring = []
            for x, y in interior.coords:
                lon, lat = xy_to_lon_lat(x, y, origin_lat)
                ring.append([lon, lat])
            rings.append(ring)

        return {
            "type": "Polygon",
            "coordinates": rings,
        }

    if geometry.geom_type == "MultiPolygon":
        polygons = [
            geometry_to_geojson(polygon, origin_lat)["coordinates"]
            for polygon in geometry.geoms
        ]
        return {
            "type": "MultiPolygon",
            "coordinates": polygons,
        }

    raise ValueError(
        f"Geometria não suportada para GeoJSON: {geometry.geom_type}"
    )


def build_zone_data(
    records: list[dict[str, Any]],
    level: str,
    origin_lat: float,
) -> tuple[Any, dict[str, Any]]:
    """
    Cria a geometria e os metadados de um hotspot.

    A geometria inicial continua sendo:
        pontos -> convex hull -> margem

    A resolução de sobreposição entre níveis acontece em build_zones().
    """
    xy_points = []

    total_score = 0.0
    total_detections = 0
    images = []
    detection_classes: Counter[str] = Counter()

    for record in records:
        location = record["location"]
        lat = float(location["latitude"])
        lon = float(location["longitude"])

        x, y = local_xy(lon, lat, origin_lat)
        xy_points.append((x, y))

        total_score += float(record.get("risk_score", 0.0))
        total_detections += len(record.get("detections", []))
        images.append(record.get("filename"))

        for class_name, count in class_counts(record).items():
            detection_classes[class_name] += count

    geometry = MultiPoint(xy_points)
    margin = ZONE_MARGIN_M[level]
    polygon = geometry.convex_hull.buffer(margin, resolution=32)

    centroid = polygon.centroid
    center_lon, center_lat = xy_to_lon_lat(
        centroid.x,
        centroid.y,
        origin_lat,
    )

    properties = {
        "feature_type": "risk_zone",
        "risk_level": level,
        "risk_label": risk_label(level),
        "images": images,
        "images_count": len(images),
        "detections": total_detections,
        "risk_score": round(total_score, 4),
        "detections_by_class": dict(detection_classes),
        "zone_margin_m": margin,
        "center": {
            "latitude": center_lat,
            "longitude": center_lon,
        },
    }

    return polygon, properties


def geometry_components(geometry) -> list[Any]:
    """Retorna Polygon(s) individuais de uma geometria Shapely."""
    if geometry.is_empty:
        return []

    if geometry.geom_type == "Polygon":
        return [geometry]

    if geometry.geom_type == "MultiPolygon":
        return list(geometry.geoms)

    return [part for part in getattr(geometry, "geoms", []) if not part.is_empty]


def merge_same_level_zones(
    raw_zones: list[tuple[Any, dict[str, Any]]],
    origin_lat: float,
) -> list[tuple[Any, dict[str, Any]]]:
    """
    Une hotspots que se encostam ou se sobrepõem dentro do mesmo nível.

    Isso evita duas áreas HIGH, por exemplo, desenhadas uma sobre a outra
    por causa da margem do buffer.
    """
    if not raw_zones:
        return []

    merged_geometry = unary_union([geometry for geometry, _ in raw_zones])
    components = geometry_components(merged_geometry)

    merged_zones: list[tuple[Any, dict[str, Any]]] = []

    for component in components:
        related = [
            props
            for geometry, props in raw_zones
            if geometry.intersects(component)
        ]

        images: list[Any] = []
        detection_classes: Counter[str] = Counter()
        total_score = 0.0
        total_detections = 0
        margin = 0.0

        for props in related:
            images.extend(props.get("images", []))
            total_score += float(props.get("risk_score", 0.0))
            total_detections += int(props.get("detections", 0))
            margin = max(margin, float(props.get("zone_margin_m", 0.0)))
            detection_classes.update(props.get("detections_by_class", {}))

        level = related[0]["risk_level"] if related else "LOW"
        centroid = component.centroid
        center_lon, center_lat = xy_to_lon_lat(
            centroid.x,
            centroid.y,
            origin_lat,
        )

        merged_zones.append(
            (
                component,
                {
                    "feature_type": "risk_zone",
                    "risk_level": level,
                    "risk_label": risk_label(level),
                    "images": images,
                    "images_count": len(images),
                    "detections": total_detections,
                    "risk_score": round(total_score, 4),
                    "detections_by_class": dict(detection_classes),
                    "zone_margin_m": margin,
                    "center": {
                        "latitude": center_lat,
                        "longitude": center_lon,
                    },
                },
            )
        )

    return merged_zones


def make_zone_feature(
    geometry,
    properties: dict[str, Any],
    origin_lat: float,
) -> dict[str, Any]:
    """Cria um Feature GeoJSON a partir de uma geometria Shapely."""
    return {
        "type": "Feature",
        "geometry": geometry_to_geojson(geometry, origin_lat),
        "properties": dict(properties),
    }


def build_zones(
    images: list[dict[str, Any]],
    origin_lat: float,
) -> list[dict[str, Any]]:
    """
    Gera zonas finais sem sobreposição entre níveis de risco.

    Regra espacial:
        HIGH > MEDIUM > LOW

    Portanto:
        MEDIUM = MEDIUM - HIGH
        LOW    = LOW - HIGH - MEDIUM

    Dentro do mesmo nível, geometrias que se encostam/sobrepõem são
    dissolvidas antes da etapa de prioridade.
    """
    raw_by_level: dict[str, list[tuple[Any, dict[str, Any]]]] = {
        level: [] for level in AREA_LEVELS
    }

    for level in AREA_LEVELS:
        records = [
            record
            for record in images
            if str(record.get("risk_level", "VERY_LOW")) == level
            and len(record.get("detections", [])) > 0
        ]

        for cluster in cluster_records(records):
            geometry, properties = build_zone_data(
                cluster,
                level,
                origin_lat,
            )
            raw_by_level[level].append((geometry, properties))

    merged_by_level = {
        level: merge_same_level_zones(raw_by_level[level], origin_lat)
        for level in AREA_LEVELS
    }

    zones: list[dict[str, Any]] = []
    covered = None
    priority = ("HIGH", "MEDIUM", "LOW")

    for level in priority:
        for geometry, properties in merged_by_level[level]:
            final_geometry = geometry

            if covered is not None:
                final_geometry = geometry.difference(covered)

            for component in geometry_components(final_geometry):
                if component.is_empty or component.area <= 0:
                    continue

                zones.append(
                    make_zone_feature(
                        component,
                        properties,
                        origin_lat,
                    )
                )

        level_geometry = unary_union(
            [geometry for geometry, _ in merged_by_level[level]]
        ) if merged_by_level[level] else None

        if level_geometry is not None:
            if covered is None:
                covered = level_geometry
            else:
                covered = unary_union([covered, level_geometry])

    return zones


def popup_for_zone(zone: dict[str, Any]) -> str:
    props = zone["properties"]
    level = props["risk_level"]

    classes = props.get("detections_by_class", {})

    class_html = ""
    if classes:
        class_html = "<ul style='margin:5px 0;padding-left:18px;'>"
        for name, count in sorted(classes.items()):
            class_html += (
                f"<li>{html.escape(str(name))}: {int(count)}</li>"
            )
        class_html += "</ul>"

    images = props.get("images", [])
    images_html = "<br>".join(
        html.escape(str(filename))
        for filename in images
    )

    return f"""
    <div style="width:320px;font-family:Arial,sans-serif;">
        <h4 style="margin:0 0 8px 0;">
            Área de risco — {html.escape(risk_label(level))}
        </h4>

        <div style="
            padding:8px;
            background:#f5f5f5;
            border-radius:6px;
            margin-bottom:8px;
        ">
            <b>Score da zona:</b> {props["risk_score"]:.4f}<br>
            <b>Imagens:</b> {props["images_count"]}<br>
            <b>Detecções:</b> {props["detections"]}
        </div>

        <b>Classes detectadas</b>
        {class_html}

        <b>Imagens da zona</b>
        <div style="margin-top:4px;font-size:11px;">
            {images_html}
        </div>

        <div style="
            margin-top:8px;
            padding-top:6px;
            border-top:1px solid #ddd;
            color:#666;
            font-size:10px;
        ">
            Hotspot de priorização do MVP.
        </div>
    </div>
    """


def add_risk_zones(
    fmap: folium.Map,
    zones: list[dict[str, Any]],
) -> None:
    layer = folium.FeatureGroup(
        name="Áreas de risco",
        show=True,
    )

    # Renderiza primeiro as zonas mais fortes.
    priority = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    zones_sorted = sorted(
        zones,
        key=lambda z: priority[z["properties"]["risk_level"]],
    )

    for zone in zones_sorted:
        level = zone["properties"]["risk_level"]
        color = RISK_COLORS[level]

        folium.GeoJson(
            zone,
            style_function=lambda feature, c=color: {
                "color": c,
                "weight": 2,
                "fillColor": c,
                "fillOpacity": 0.32,
            },
            highlight_function=lambda feature, c=color: {
                "color": c,
                "weight": 3,
                "fillColor": c,
                "fillOpacity": 0.45,
            },
            popup=folium.Popup(
                popup_for_zone(zone),
                max_width=390,
            ),
            tooltip=(
                f"Área {risk_label(level)} — "
                f"{zone['properties']['detections']} detecções"
            ),
        ).add_to(layer)

    layer.add_to(fmap)


def add_photo_layers(
    fmap: folium.Map,
    images: list[dict[str, Any]],
) -> None:
    detected_layer = folium.FeatureGroup(
        name="Fotos com detecção",
        show=True,
    )

    no_detection_layer = folium.FeatureGroup(
        name="Fotos sem detecção",
        show=False,
    )

    for record in images:
        if not valid_location(record):
            continue

        location = record["location"]
        lat = float(location["latitude"])
        lon = float(location["longitude"])

        detections = record.get("detections", [])
        level = str(record.get("risk_level", "VERY_LOW"))
        color = RISK_COLORS.get(level, "#757575")

        if detections:
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color="#212121",
                weight=2,
                fill=True,
                fill_color=color,
                fill_opacity=1,
                popup=folium.Popup(
                    popup_html(record),
                    max_width=390,
                ),
                tooltip=(
                    f"{record.get('filename', '')} — "
                    f"{risk_label(level)}"
                ),
            ).add_to(detected_layer)

        else:
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                color="#616161",
                weight=1,
                fill=True,
                fill_color="#BDBDBD",
                fill_opacity=0.85,
                popup=folium.Popup(
                    popup_html(record),
                    max_width=390,
                ),
                tooltip=(
                    f"{record.get('filename', '')} — Sem detecção"
                ),
            ).add_to(no_detection_layer)

    detected_layer.add_to(fmap)
    no_detection_layer.add_to(fmap)


def add_very_low_points(
    fmap: folium.Map,
    images: list[dict[str, Any]],
) -> None:
    """
    VERY_LOW com detecção fica em uma camada própria.

    Assim continua sendo possível enxergar onde houve detecção,
    sem transformar cada detecção fraca em uma área.
    """
    layer = folium.FeatureGroup(
        name="Detecções muito baixas",
        show=False,
    )

    for record in images:
        if not valid_location(record):
            continue

        if str(record.get("risk_level", "VERY_LOW")) != "VERY_LOW":
            continue

        detections = record.get("detections", [])
        if not detections:
            continue

        location = record["location"]

        folium.CircleMarker(
            location=[
                float(location["latitude"]),
                float(location["longitude"]),
            ],
            radius=4,
            color=RISK_COLORS["VERY_LOW"],
            weight=2,
            fill=True,
            fill_color=RISK_COLORS["VERY_LOW"],
            fill_opacity=0.85,
            popup=folium.Popup(
                popup_html(record),
                max_width=390,
            ),
            tooltip=(
                f"{record.get('filename', '')} — Muito baixo"
            ),
        ).add_to(layer)

    layer.add_to(fmap)


def add_trajectory(
    fmap: folium.Map,
    images: list[dict[str, Any]],
) -> None:
    coordinates = []

    for record in images:
        if not valid_location(record):
            continue

        location = record["location"]

        coordinates.append(
            [
                float(location["latitude"]),
                float(location["longitude"]),
            ]
        )

    layer = folium.FeatureGroup(
        name="Percurso aproximado",
        show=True,
    )

    if len(coordinates) >= 2:
        folium.PolyLine(
            coordinates,
            color="#1976D2",
            weight=3,
            opacity=0.70,
            dash_array="8,6",
            tooltip="Percurso aproximado pelas imagens",
        ).add_to(layer)

    layer.add_to(fmap)


def add_title(fmap: folium.Map) -> None:
    content = """
    <div style="
        position:fixed;
        top:10px;
        left:50%;
        transform:translateX(-50%);
        z-index:9999;
        background:rgba(255,255,255,.96);
        padding:9px 16px;
        border-radius:8px;
        box-shadow:0 1px 6px rgba(0,0,0,.25);
        font-family:Arial,sans-serif;
        font-size:16px;
        font-weight:bold;
        white-space:nowrap;
    ">
        HORUS — Mapa de áreas de risco
    </div>
    """

    fmap.get_root().html.add_child(
        folium.Element(content)
    )


def add_summary(
    fmap: folium.Map,
    data: dict[str, Any],
    zones: list[dict[str, Any]],
) -> None:
    summary = data.get("risk_summary", {})

    panel = f"""
    <div style="
        position:fixed;
        top:62px;
        left:10px;
        z-index:9999;
        background:rgba(255,255,255,.96);
        border:1px solid #aaa;
        border-radius:8px;
        padding:10px;
        width:190px;
        box-shadow:0 1px 6px rgba(0,0,0,.20);
        font-family:Arial,sans-serif;
        font-size:12px;
    ">
        <div style="
            font-size:14px;
            font-weight:bold;
            margin-bottom:7px;
        ">
            Resumo da missão
        </div>

        <div>
            Imagens: <b>{int(data.get("images_processed", 0))}</b>
        </div>

        <div>
            Detecções: <b>{int(data.get("total_detections", 0))}</b>
        </div>

        <div>
            Score total:
            <b>{float(data.get("total_risk_score", 0.0)):.4f}</b>
        </div>

        <div>
            Áreas geradas: <b>{len(zones)}</b>
        </div>

        <hr style="
            border:none;
            border-top:1px solid #ddd;
            margin:7px 0;
        ">

        <div>
            Muito baixo: <b>{summary.get("VERY_LOW", 0)}</b>
        </div>

        <div>
            Baixo: <b>{summary.get("LOW", 0)}</b>
        </div>

        <div>
            Médio: <b>{summary.get("MEDIUM", 0)}</b>
        </div>

        <div>
            Alto: <b>{summary.get("HIGH", 0)}</b>
        </div>
    </div>
    """

    fmap.get_root().html.add_child(
        folium.Element(panel)
    )


def add_legend(fmap: folium.Map) -> None:
    items = ""

    for level in ("HIGH", "MEDIUM", "LOW", "VERY_LOW"):
        color = RISK_COLORS[level]
        label = RISK_LABELS[level]

        items += f"""
        <div style="margin:4px 0;">
            <span style="
                display:inline-block;
                width:13px;
                height:13px;
                border-radius:3px;
                background:{color};
                margin-right:6px;
                vertical-align:middle;
            "></span>
            {label}
        </div>
        """

    legend = f"""
    <div style="
        position:fixed;
        bottom:30px;
        left:10px;
        z-index:9999;
        background:rgba(255,255,255,.96);
        border:1px solid #aaa;
        border-radius:8px;
        padding:10px;
        min-width:150px;
        box-shadow:0 1px 6px rgba(0,0,0,.20);
        font-family:Arial,sans-serif;
        font-size:12px;
    ">
        <div style="
            font-weight:bold;
            margin-bottom:7px;
        ">
            Legenda
        </div>
        {items}
        <hr style="
            border:none;
            border-top:1px solid #ddd;
            margin:7px 0;
        ">
        <div style="
            font-size:10px;
            color:#666;
        ">
            Áreas = hotspots de priorização
        </div>
    </div>
    """

    fmap.get_root().html.add_child(
        folium.Element(legend)
    )


def make_geojson(
    images: list[dict[str, Any]],
    zones: list[dict[str, Any]],
) -> dict[str, Any]:
    features: list[dict[str, Any]] = []

    for record in images:
        if not valid_location(record):
            continue

        location = record["location"]
        detections = record.get("detections", [])
        level = str(record.get("risk_level", "VERY_LOW"))

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(location["longitude"]),
                        float(location["latitude"]),
                    ],
                },
                "properties": {
                    "feature_type": "image",
                    "filename": record.get("filename"),
                    "latitude": float(location["latitude"]),
                    "longitude": float(location["longitude"]),
                    "altitude": location.get("altitude"),
                    "risk_score": float(record.get("risk_score", 0.0)),
                    "risk_level": level,
                    "risk_label": risk_label(level),
                    "detections": len(detections),
                    "detections_by_class": class_counts(record),
                    "annotated_image": record.get("annotated_image"),
                },
            }
        )

    features.extend(zones)

    return {
        "type": "FeatureCollection",
        "features": features,
    }


def main() -> None:
    print("=" * 70)
    print("HORUS - GERAÇÃO DO MAPA DE ÁREAS DE RISCO")
    print("=" * 70)
    print()
    print(f"Lendo:\n{INPUT_FILE}")
    print()

    try:
        data = read_json(INPUT_FILE)

        images = data.get("images", [])

        if not isinstance(images, list):
            raise ValueError("O campo 'images' deve ser uma lista.")

        valid_images = [
            record
            for record in images
            if isinstance(record, dict) and valid_location(record)
        ]

        if not valid_images:
            raise ValueError(
                "Nenhuma imagem com latitude/longitude válidas foi encontrada."
            )

        origin_lat = (
            sum(
                float(record["location"]["latitude"])
                for record in valid_images
            )
            / len(valid_images)
        )

        zones = build_zones(
            valid_images,
            origin_lat,
        )

        center_lat = (
            sum(
                float(record["location"]["latitude"])
                for record in valid_images
            )
            / len(valid_images)
        )

        center_lon = (
            sum(
                float(record["location"]["longitude"])
                for record in valid_images
            )
            / len(valid_images)
        )

        fmap = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=19,
            control_scale=True,
            tiles="OpenStreetMap",
        )

        # Ordem visual.
        add_trajectory(fmap, valid_images)
        add_risk_zones(fmap, zones)
        add_photo_layers(fmap, valid_images)
        add_very_low_points(fmap, valid_images)

        folium.LayerControl(
            collapsed=False,
            position="topright",
        ).add_to(fmap)

        add_title(fmap)
        add_summary(fmap, data, zones)
        add_legend(fmap)

        fmap.save(OUTPUT_HTML)

        geojson = make_geojson(
            valid_images,
            zones,
        )

        OUTPUT_GEOJSON.write_text(
            json.dumps(
                geojson,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    except (
        FileNotFoundError,
        ValueError,
        OSError,
    ) as exc:
        print(f"Erro: {exc}")
        sys.exit(1)

    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    print(f"Imagens com GPS: {len(valid_images)}")
    print(f"Imagens ignoradas: {len(images) - len(valid_images)}")
    print(f"Áreas de risco geradas: {len(zones)}")
    print()
    print(f"Mapa HTML salvo em:\n{OUTPUT_HTML}")
    print()
    print(f"GeoJSON salvo em:\n{OUTPUT_GEOJSON}")
    print()
    print("Camadas disponíveis:")
    print("  - Áreas de risco")
    print("  - Fotos com detecção")
    print("  - Fotos sem detecção")
    print("  - Detecções muito baixas")
    print("  - Percurso aproximado")
    print()
    print("Para abrir o mapa:")
    print(f"  xdg-open {OUTPUT_HTML}")


if __name__ == "__main__":
    main()

