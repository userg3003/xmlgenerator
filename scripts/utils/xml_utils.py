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
