import pkgutil
from itertools import repeat
from sympy import flatten


def string_list(strlist):
    return ", ".join(strlist) if isinstance(strlist, list) else strlist


class MetricData(dict):
    def __init__(self, doc):
        import yaml

        super().__init__(yaml.safe_load(doc))
        doc_items = [string_list(val) for val in self.values()]
        self.__doc__ = "\n".join(doc_items)


metric_data = []

for module_info in pkgutil.iter_modules(__path__, __name__ + "."):
    module = __import__(module_info.name, fromlist="dummy")
    if module.__doc__:
        entry = MetricData(module.__doc__.lower())
        entry["metric"] = module.metric
        entry["coords"] = module.coords
        entry["variables"] = module.variables
        entry["functions"] = module.functions
        metric_data.append(entry)


def compare_filter(entries, value, key):
    if not value:
        return entries

    def select(entry):
        return value.lower() in string_list(entry.get(key, ""))

    return filter(select, entries)


def find(sub=None, symmetries=None, coords=None, notes=None):
    entries = metric_data

    if symmetries:
        for symmetry in flatten([symmetries]):
            entries = compare_filter(entries, symmetry, "symmetry")

    if coords:
        entries = compare_filter(entries, coords, "coordinates")

    if notes:
        for note in flatten([notes]):
            entries = compare_filter(entries, note, "notes")

    if sub is None:
        retval = map(MetricData.__getitem__, entries, repeat("name"))
    else:
        retval = [entry["name"] for entry in entries if sub.lower() in entry.__doc__]

    retval = list(set(retval))
    retval.sort()
    return retval


def data(name, coords=None, notes=None):
    entries = [metric for metric in metric_data if metric["name"] == name.lower()]
    if not entries:
        raise KeyError("metric {} not found".format(name))

    if coords:
        entries = compare_filter(entries, coords, "coordinates")

    if notes:
        for note in flatten([notes]):
            entries = compare_filter(entries, note, "notes")

    entries = list(entries)
    if len(entries) == 1:
        return entries[0]
    return entries


def coordinate_types(name, notes=None):
    entries = data(name, notes=notes)
    if not isinstance(entries, list):
        return entries.get("coordinates")
    return set([entry.get("coordinates") for entry in entries])


def variations(name, coords=None):
    entries = data(name, coords=coords)
    if not isinstance(entries, list):
        return entries.get("notes")
    return set([entry.get("notes") for entry in entries])
