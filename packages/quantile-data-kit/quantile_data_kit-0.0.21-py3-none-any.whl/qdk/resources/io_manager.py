from dagster.core.storage.io_manager import IOManager
from dagster.core.storage.io_manager import io_manager as dagster_io_manager
from qdk.materialization import Materializer


class QDKIOManager(IOManager):
    def __init__(self):
        self.values = {}

    def handle_output(self, context, obj):
        key = tuple(context.get_output_identifier())
        self.values[key] = obj

        # Create a materializer for the object
        asset_materialization = Materializer(
            asset_key=[
                context.pipeline_name,
                context.solid_def.name,
                key[-1],
            ],
            object=obj,
        ).materialize()

        # If the asset was materialized, yield the asset
        if asset_materialization:
            yield asset_materialization

    def load_input(self, context):
        key = tuple(context.upstream_output.get_output_identifier())

        if key not in self.values:
            raise KeyError(
                "The key was not found. Make sure the io_manager lives between execution processes."
            )

        obj = self.values[key]
        return obj


@dagster_io_manager
def qdk_io_manager(_):
    return QDKIOManager()
