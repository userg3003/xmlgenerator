from loguru import logger
def get_all_value_from_facet(node_type):
    all_facets_types = [item.split("}")[1] for item in node_type.facets if item is not None]
    logger.trace(f"all_facets_types: {all_facets_types}")
    type_=dict()
    for attr in all_facets_types:
        type_[attr] = get_value_from_facet(node_type.facets, attr)

    return type_


def get_value_from_facet(facet, name_value):
    name_key = f'{{http://www.w3.org/2001/XMLSchema}}{name_value}'
    value = None
    if name_value == "pattern":
        value = getattr(facet[name_key], "patterns", None) if facet.get(name_key, None) else None
        value = value[0] if value is not None else None
    elif name_value == "enumeration":
        value = getattr(facet[name_key], "enumeration", None) if facet.get(name_key, None) else None
        value = value if value is not None else None
    else:
        value = getattr(facet[name_key], "value", None)
    return value

def get_value_from_base_type_facet(node_type, name_value):
    name_key = f'{{http://www.w3.org/2001/XMLSchema}}{name_value}'
    value = None
    value = getattr(node_type.base_type, name_value, None)
    return value
