"""Common utilities for use by Doni CLI."""
import yaml
from cliff.columns import FormattableColumn
from osc_lib import utils as osc_utils


class YamlColumn(FormattableColumn):
    def human_readable(self):
        return yaml.dump(self._value)


class HardwareSerializer(object):
    def serialize_hardware(self, hw_dict: "dict", columns: "list[str]"):
        return osc_utils.get_dict_properties(
            hw_dict,
            columns,
            formatters={
                "properties": YamlColumn,
                "workers": YamlColumn,
            },
        )
