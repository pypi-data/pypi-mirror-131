"""Types of the objects contained in the OSEF stream."""
import uuid
from collections import namedtuple
from enum import IntEnum, Enum
from struct import Struct
from typing import List

import numpy as np


class OsefTypes(IntEnum):
    """Outsight Node and Leaf types."""

    AUGMENTED_CLOUD = 1
    NUMBER_POINTS = 2
    SPHERICAL_COORD_3F = 3
    REFLECTIVITIES = 4
    BACKGROUND_FLAG = 5
    CARTESIAN_COORD_3F = 6
    BGR_COLOR = 7
    OBJECT_DETECTION_FRAME = 8
    IMAGE_DIM = 9
    NUMBER_OBJECT = 10
    CLOUD_FRAME = 11
    TIMESTAMP_MICROSECOND = 12
    AZIMUTHS_COL = 13
    NUMBER_OF_LAYERS = 14
    CLOUD_PROCESSING = 15
    RANGE_AZIMUTH = 16
    BBOX_ARRAY = 17
    CLASS_ID_ARRAY = 18
    CONFIDENCE_ARRAY = 19
    TIMESTAMP_DATA = 20
    PERCEPT = 21
    CLUSTER = 22
    BGR_IMAGE = 23
    POSE = 24
    SCAN_FRAME = 25
    TRACKED_OBJECT = 26
    BOUNDING_BOX_SIZE = 27
    SPEED_VECTOR = 28
    POSE_ARRAY = 29
    OBJECT_ID = 30
    CARTESIAN_COORD_4F = 31
    SPHERICAL_COORD_4F = 32
    ZONES = 33
    ZONE = 34
    ZONE_VERTICE = 35
    ZONE_NAME = 36
    ZONE_UUID = 37
    ZONE_BINDINGS = 38
    OBJECT_PROPERTIES = 39
    IMU_PACKET = 40
    VELODYNE_TIMESTAMP = 41
    POSE_RELATIVE = 42
    GRAVITY = 43
    EGO_MOTION = 44
    PREDICTED_POSITION = 45
    GEOGRAPHIC_POSE = 46
    OBJECT_ID_32_BITS = 47
    ZONE_BINDINGS_32_BITS = 48
    BACKGROUND_BITS = 49
    GROUND_PLANE_BITS = 50
    AZIMUTHS = 51
    ELEVATIONS = 52
    DISTANCES = 53
    LIDAR_MODEL = 54
    SLAM_POSE_ARRAY = 55
    ZONE_VERTICAL_LIMITS = 56


class PerceptIds(Enum):
    """Ids of the elements classified by the percept algorithm"""

    DEFAULT = 0
    ROAD = 1
    VEGETATION = 2
    GROUND = 3
    SIGN = 4
    BUILDING = 5
    FLAT_GND = 6
    UNKNOWN = 7
    MARKING = 8
    OBJECT = 9
    WALL = 10


class TrackedObjectClassIds(Enum):
    """Ids of the objects classified by the tracking algorithm"""

    UNKNOWN = 0
    PERSON = 1
    LUGGAGE = 2
    TROLLEY = 3
    TRUCK = 4
    BUS = 5
    CAR = 6
    VAN = 7
    TWO_WHEELER = 8
    MASK = 9
    NO_MASK = 10
    LANDMARK = 11


class LidarModelIds(Enum):
    """LiDAR models enum"""

    UNKNOWN = 0
    VELODYNE_VLP16 = 1
    VELODYNE_VLP32 = 2
    VELODYNE_VLS128 = 3
    VELODYNE_HDL32 = 4
    ROBOSENSE_BPEARL_V1 = 5
    ROBOSENSE_BPEARL_V2 = 6
    ROBOSENSE_RS32 = 7
    ROBOSENSE_HELIOS = 8
    LIVOX_HORIZON = 9
    LIVOX_AVIA = 10
    LIVOX_MID70 = 11
    OUSTER = 12
    OUTSIGHT_SA01 = 13
    HESAI_PANDAR_XT = 14
    HESAI_PANDAR_QT = 15
    RANDOM = 16


LeafInfo = namedtuple("Leaf", "parsing_function")
InternalNodeInfo = namedtuple("InternalNode", "type")
TypeInfo = namedtuple("Type", "name node_info")


def _get_value_parser(pack_format: str):
    def _parse_value(value: bytes) -> object:
        return (Struct(pack_format).unpack(value))[0]

    return _parse_value


def _get_array_parser(dtype: np.dtype):
    def _parse_array(value: bytes) -> np.ndarray:
        return np.frombuffer(value, dtype=dtype)

    return _parse_array


def _get_structured_array_parser(dtype: np.dtype):
    def _parse_structured_array(value: bytes) -> np.ndarray:
        array = np.frombuffer(value, dtype=dtype)
        names = array.dtype.names
        if "__todrop" in names:
            names.remove("__todrop")
            array = array[names]
        return array

    return _parse_structured_array


def _get_bytes_parser():
    def _parse_bytes(value: bytes) -> bytes:
        return value

    return _parse_bytes


def _get_dict_parser(pack_format: str, fields_names: List[str]):
    def _parse_dict(value: bytes) -> dict:
        array = list(Struct(pack_format).iter_unpack(value))
        return dict(zip(fields_names, array[0]))

    return _parse_dict


def _get_string_parser():
    def _parse_string(value: bytes) -> str:
        return value.decode("ascii")[:-1]

    return _parse_string


def _processing_bitfield_parser(value: bytes) -> dict:
    background_deleted = 1
    bitfield = Struct("<Q").unpack(value)[0]
    return {"background_deleted": (bitfield & (1 << background_deleted) != 0)}


def _bool_bitfield_parser(value: bytes) -> np.ndarray:
    if len(value) == 0:
        return np.array([])
    np_8bit = np.frombuffer(value, dtype=np.uint8)
    return np.unpackbits(np_8bit).astype(bool)


def _percept_class_parser(value: bytes) -> np.ndarray:
    dtype = [("class_code", int), ("class_name", "<U12")]
    if len(value) == 0:
        return np.array(np.array([], dtype=dtype))

    classes_iter = Struct("<H").iter_unpack(value)

    data_list = [(code[0], PerceptIds(code[0]).name) for code in classes_iter]
    return np.array(data_list, dtype=dtype)


def _class_array_parser(value: bytes) -> np.ndarray:
    dtype = [("class_code", int), ("class_name", "<U12")]
    if len(value) == 0:
        return np.array([], dtype=dtype)

    classes_iter = Struct("<L").iter_unpack(value)
    data_list = [
        (code[0], TrackedObjectClassIds(code[0]).name) for code in classes_iter
    ]
    return np.array(data_list, dtype=dtype)


LidarModel = namedtuple("LidarModel", ("id", "name"))


def _lidar_model_parser(value: bytes) -> LidarModel:

    if len(value) == 0:
        return LidarModel(0, LidarModelIds.UNKNOWN.name)

    model_code = Struct("<B").unpack(value)[0]
    data_list = LidarModel(model_code, LidarModelIds(model_code).name)
    return data_list


def _parse_timestamp(value: bytes) -> float:
    seconds, micro_seconds = Struct("<LL").unpack(value)
    return seconds + micro_seconds * 10 ** -6


def _pose_parser(value: bytes) -> dict:
    """Values to parse: tx ty tz Vxx Vyx Vzx Vxy Vyy Vzy Vxz Vyz Vzz

    Where rotation matrices should be at the end:
        | Vxx Vxy Vxz |
    R = | Vyx Vyy Vyz |
        | Vzx Vzy Vzz |
    """
    floats = Struct("<ffffffffffff").unpack(value)
    # we have to transpose rotation matrices because values
    # are received column by column and not line by line
    return {
        "translation": np.array(floats[0:3]),
        "rotation": np.transpose(np.reshape(np.array(floats[3:]), (3, 3))),
    }


def _pose_array_parser(value: bytes) -> List:
    """Values to parse: tx ty tz Vxx Vyx Vzx Vxy Vyy Vzy Vxz Vyz Vzz

    Where rotation matrices should be at the end:
        | Vxx Vxy Vxz |
    R = | Vyx Vyy Vyz |
        | Vzx Vzy Vzz |
    """
    floats = np.array(list(Struct("<ffffffffffff").iter_unpack(value)), ndmin=2)
    translations = floats[:, 0:3]
    rotations = np.transpose(floats[:, 3:].reshape((-1, 3, 3)), axes=[0, 2, 1])
    # we have to transpose rotation matrices because values
    # are received column by column and not line by line
    return [{"translation": t, "rotation": r} for t, r in zip(translations, rotations)]


def _object_properties_parser(value: bytes) -> np.ndarray:
    dtype = [
        ("oriented", bool),
        ("extrapolated", bool),
        ("has_valid_slam_pose", bool),
        ("is_static", bool),
    ]
    if len(value) == 0:
        return np.array([], dtype=dtype)

    object_iter = Struct("<B").iter_unpack(value)
    property_list = [
        (bool(c[0] & 0x1), bool(c[0] & 0x2), bool(c[0] & 0x4), bool(c[0] & 0x8))
        for c in object_iter
    ]
    return np.array(property_list, dtype=dtype)


def _imu_parser(value: bytes) -> dict:
    value = Struct("<LLffffff").unpack(value)
    return {
        "timestamp": {"unix_s": value[0], "remaining_us": value[1]},
        "acceleration": value[2:5],
        "angular_velocity": value[5:8],
    }


outsight_types = {
    OsefTypes.AUGMENTED_CLOUD.value: TypeInfo(
        "augmented_cloud", InternalNodeInfo(dict)
    ),
    OsefTypes.NUMBER_POINTS.value: TypeInfo(
        "number_of_points", LeafInfo(_get_value_parser("<L"))
    ),
    OsefTypes.SPHERICAL_COORD_3F.value: TypeInfo(
        "spherical_coordinates",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("azimuth", np.float32),
                            ("elevation", np.float32),
                            ("distance", np.float32),
                        ]
                    ),
                )
            )
        ),
    ),
    OsefTypes.REFLECTIVITIES.value: TypeInfo(
        "reflectivities", LeafInfo(_get_array_parser(np.dtype(np.uint8)))
    ),
    OsefTypes.BACKGROUND_FLAG.value: TypeInfo(
        "background_flags", LeafInfo(_get_array_parser(np.dtype(bool)))
    ),
    OsefTypes.CARTESIAN_COORD_3F.value: TypeInfo(
        "cartesian_coordinates",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    ([("x", np.float32), ("y", np.float32), ("z", np.float32)]),
                )
            )
        ),
    ),
    OsefTypes.BGR_COLOR.value: TypeInfo("bgr_colors", LeafInfo(_get_bytes_parser())),
    OsefTypes.OBJECT_DETECTION_FRAME.value: TypeInfo(
        "object_detection_frame", InternalNodeInfo(dict)
    ),
    OsefTypes.IMAGE_DIM.value: TypeInfo(
        "image_dimension",
        LeafInfo(_get_dict_parser("<LL", ["image_width", "image_height"])),
    ),
    OsefTypes.NUMBER_OBJECT.value: TypeInfo(
        "number_of_objects", LeafInfo(_get_value_parser("<L"))
    ),
    OsefTypes.CLOUD_FRAME.value: TypeInfo("cloud_frame", InternalNodeInfo(dict)),
    OsefTypes.TIMESTAMP_MICROSECOND.value: TypeInfo(
        "timestamp_microsecond",
        LeafInfo(_parse_timestamp),
    ),
    OsefTypes.AZIMUTHS_COL.value: TypeInfo(
        "azimuths_column", LeafInfo(_get_array_parser(np.dtype(np.float32)))
    ),
    OsefTypes.NUMBER_OF_LAYERS.value: TypeInfo(
        "number_of_layers", LeafInfo(_get_value_parser("<L"))
    ),
    OsefTypes.CLOUD_PROCESSING.value: TypeInfo(
        "cloud_processing",
        LeafInfo(_processing_bitfield_parser),
    ),
    OsefTypes.RANGE_AZIMUTH.value: TypeInfo(
        "range_azimuth",
        LeafInfo(_get_dict_parser("<ff", ["azimuth_begin_deg", "azimuth_end_deg"])),
    ),
    OsefTypes.BBOX_ARRAY.value: TypeInfo(
        "bounding_boxes_array",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("x_min", np.float32),
                            ("y_min", np.float32),
                            ("x_max", np.float32),
                            ("y_max", np.float32),
                        ]
                    ),
                )
            )
        ),
    ),
    OsefTypes.CLASS_ID_ARRAY.value: TypeInfo(
        "class_id_array", LeafInfo(_class_array_parser)
    ),
    OsefTypes.CONFIDENCE_ARRAY.value: TypeInfo(
        "confidence_array",
        LeafInfo(_get_array_parser(np.dtype(np.float32))),
    ),
    OsefTypes.TIMESTAMP_DATA.value: TypeInfo(
        "timestamped_data", InternalNodeInfo(dict)
    ),
    OsefTypes.PERCEPT.value: TypeInfo("percept", LeafInfo(_percept_class_parser)),
    OsefTypes.CLUSTER.value: TypeInfo(
        "cluster", LeafInfo(_get_array_parser(np.dtype(np.uint16)))
    ),
    OsefTypes.BGR_IMAGE.value: TypeInfo("bgr_image_frame", InternalNodeInfo(dict)),
    OsefTypes.POSE.value: TypeInfo("pose", LeafInfo(_pose_parser)),
    OsefTypes.SCAN_FRAME.value: TypeInfo("scan_frame", InternalNodeInfo(dict)),
    OsefTypes.TRACKED_OBJECT.value: TypeInfo("tracked_objects", InternalNodeInfo(dict)),
    OsefTypes.BOUNDING_BOX_SIZE.value: TypeInfo(
        "bbox_sizes",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("bbox_x", np.float32),
                            ("bbox_y", np.float32),
                            ("bbox_z", np.float32),
                        ]
                    ),
                ),
            )
        ),
    ),
    OsefTypes.SPEED_VECTOR.value: TypeInfo(
        "speed_vectors",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    ([("Vx", np.float32), ("Vy", np.float32), ("Vz", np.float32)]),
                ),
            )
        ),
    ),
    OsefTypes.POSE_ARRAY.value: TypeInfo("pose_array", LeafInfo(_pose_array_parser)),
    OsefTypes.OBJECT_ID.value: TypeInfo(
        "object_id", LeafInfo(_get_array_parser(np.dtype(np.ulonglong)))
    ),
    OsefTypes.CARTESIAN_COORD_4F.value: TypeInfo(
        "cartesian_coordinates_4f",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("x", np.float32),
                            ("y", np.float32),
                            ("z", np.float32),
                            ("__todrop", np.float32),
                        ]
                    ),
                )
            )
        ),
    ),
    # __todrop are unused columns that are here to
    # have 4 floats in the TLV which is more cpu efficient.
    OsefTypes.SPHERICAL_COORD_4F.value: TypeInfo(
        "spherical_coordinates_4f",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("azimuth", np.float32),
                            ("elevation", np.float32),
                            ("distance", np.float32),
                            ("__todrop", np.float32),
                        ]
                    ),
                )
            )
        ),
    ),
    OsefTypes.ZONES.value: TypeInfo("zones_def", InternalNodeInfo(list)),
    OsefTypes.ZONE.value: TypeInfo("zone", InternalNodeInfo(dict)),
    OsefTypes.ZONE_VERTICE.value: TypeInfo(
        "zone_vertices",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(([("x", np.float32), ("y", np.float32)])),
            )
        ),
    ),
    OsefTypes.ZONE_NAME.value: TypeInfo("zone_name", LeafInfo(_get_string_parser())),
    OsefTypes.ZONE_UUID.value: TypeInfo(
        "zone_uuid", LeafInfo(lambda v: uuid.UUID(bytes=v))
    ),
    OsefTypes.ZONE_BINDINGS.value: TypeInfo(
        "zones_objects_binding",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    ([("object_id", np.uint64), ("zone_idx", np.uint32)]),
                ),
            )
        ),
    ),
    OsefTypes.OBJECT_PROPERTIES.value: TypeInfo(
        "object_properties", LeafInfo(_object_properties_parser)
    ),
    OsefTypes.IMU_PACKET.value: TypeInfo("imu_packet", LeafInfo(_imu_parser)),
    OsefTypes.VELODYNE_TIMESTAMP.value: TypeInfo(
        "timestamp_lidar_velodyne",
        LeafInfo(_get_dict_parser("<LL", ["unix_s", "remaining_us"])),
    ),
    OsefTypes.POSE_RELATIVE.value: TypeInfo("pose_relative", LeafInfo(_pose_parser)),
    OsefTypes.GRAVITY.value: TypeInfo(
        "gravity", LeafInfo(_get_dict_parser("<fff", ["x", "y", "z"]))
    ),
    OsefTypes.EGO_MOTION.value: TypeInfo("ego_motion", InternalNodeInfo(dict)),
    OsefTypes.PREDICTED_POSITION.value: TypeInfo(
        "predicted_position",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    ([("x", np.float32), ("y", np.float32), ("z", np.float32)]),
                ),
            )
        ),
    ),
    OsefTypes.GEOGRAPHIC_POSE.value: TypeInfo(
        "geographic_pose",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    (
                        [
                            ("lat", np.float32),
                            ("long", np.float32),
                            ("heading", np.float32),
                        ]
                    )
                )
            )
        ),
    ),
    OsefTypes.OBJECT_ID_32_BITS.value: TypeInfo(
        "object_id_32_bits", LeafInfo(_get_array_parser(np.dtype(np.uint32)))
    ),
    OsefTypes.ZONE_BINDINGS_32_BITS.value: TypeInfo(
        "zones_objects_binding_32_bits",
        LeafInfo(
            _get_structured_array_parser(
                np.dtype(
                    ([("object_id", np.uint32), ("zone_idx", np.uint32)]),
                ),
            )
        ),
    ),
    OsefTypes.BACKGROUND_BITS.value: TypeInfo(
        "background_bits", LeafInfo(_bool_bitfield_parser)
    ),
    OsefTypes.GROUND_PLANE_BITS.value: TypeInfo(
        "ground_plane_bits", LeafInfo(_bool_bitfield_parser)
    ),
    OsefTypes.AZIMUTHS.value: TypeInfo(
        "azimuths", LeafInfo(_get_array_parser(np.dtype(np.float32)))
    ),
    OsefTypes.ELEVATIONS.value: TypeInfo(
        "elevations", LeafInfo(_get_array_parser(np.dtype(np.float32)))
    ),
    OsefTypes.DISTANCES.value: TypeInfo(
        "distances", LeafInfo(_get_array_parser(np.dtype(np.float32)))
    ),
    OsefTypes.LIDAR_MODEL.value: TypeInfo("lidar_model", LeafInfo(_lidar_model_parser)),
    OsefTypes.SLAM_POSE_ARRAY.value: TypeInfo(
        "slam_pose_array", LeafInfo(_pose_array_parser)
    ),
    OsefTypes.ZONE_VERTICAL_LIMITS.value: TypeInfo(
        "zone_vertical_limits", LeafInfo(_get_array_parser(np.dtype(np.float32)))
    ),
}


def get_type_info_by_id(type_code):
    """Get TypeInfo for a given type code.

    :param type_code: Int value in OsefTypes
    :return:
    """
    if type_code in outsight_types:
        return outsight_types[type_code]

    return TypeInfo(f"Unknown type ({type_code})", LeafInfo(None))


def get_type_info_by_key(type_name: str) -> TypeInfo:
    """Get TypeInfo for a given key/name.

    :param type_name: Int value in OsefTypes
    :return:
    """
    for value in outsight_types.values():
        if value.name == type_name:
            return value
    return TypeInfo(f"Unknown type ({type_name})", LeafInfo(None))
