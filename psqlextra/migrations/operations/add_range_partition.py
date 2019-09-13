from .partition import PostgresPartitionOperation


class PostgresAddRangePartition(PostgresPartitionOperation):
    """Adds a new range partition to a :see:PartitionedPostgresModel."""

    def __init__(self, model_name: str, name: str, from_values, to_values):
        """Initializes new instance of :see:AddRangePartition.

        Arguments:
            model_name:
                The name of the :see:PartitionedPostgresModel.

            name:
                The name to give to the new partition table.

            from_values:
                Start of the partitioning key range of
                values that need to be stored in this
                partition.

            to_values:
                End of the partitioning key range of
                values that need to be stored in this
                partition.
        """

        super().__init__(model_name, name)

        self.from_values = from_values
        self.to_values = to_values

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.add_range_partition(
                model, self.name, self.from_values, self.to_values
            )

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        kwargs["from_values"] = self.from_values
        kwargs["to_values"] = self.to_values

        return name, args, kwargs
