import pkgutil
import yaml
import riccipy.metrics as metrics


class MetricData (dict):
    def __init__(self, doc):
        super().__init__(yaml.safe_load(doc.lower()))


metric_data = []

for module_info in pkgutil.iter_modules(metrics.__path__, metrics.__name__ + '.'):
    module = __import__(module_info.name, fromlist='dummy')
    if module.__doc__:
        metric_data.append(MetricData(module.__doc__))
