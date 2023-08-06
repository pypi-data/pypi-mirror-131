from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.types import cl_types
from pycspr.types import cl_values


def encode(entity: cl_types.CL_Type) -> bytes:
    result = bytes([entity.type_key.value])

    if type(entity) in _SIMPLE_TYPES:
        return result

    elif isinstance(entity, cl_types.CL_Type_ByteArray):
        return result + cl_value_to_bytes(cl_values.CL_U32(entity.size))

    elif isinstance(entity, cl_types.CL_Type_List):
        return result + encode(entity.inner_type)

    elif isinstance(entity, cl_types.CL_Type_Map):
        return result + encode(entity.key_type) + encode(entity.value_type)

    elif isinstance(entity, cl_types.CL_Type_Option):
        return result + encode(entity.inner_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple1):
        return result + encode(entity.t0_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple2):
        return result + encode(entity.t0_type) + encode(entity.t1_type)

    elif isinstance(entity, cl_types.CL_Type_Tuple3):
        return result + encode(entity.t0_type) + encode(entity.t1_type) + encode(entity.t2_type)


_SIMPLE_TYPES = {
    cl_types.CL_Type_Any,
    cl_types.CL_Type_Bool,
    cl_types.CL_Type_I32,
    cl_types.CL_Type_I64,
    cl_types.CL_Type_Key,
    cl_types.CL_Type_PublicKey,
    cl_types.CL_Type_Result,
    cl_types.CL_Type_String,
    cl_types.CL_Type_U8,
    cl_types.CL_Type_U32,
    cl_types.CL_Type_U64,
    cl_types.CL_Type_U128,
    cl_types.CL_Type_U256,
    cl_types.CL_Type_U512,
    cl_types.CL_Type_Unit,
    cl_types.CL_Type_URef,
}
