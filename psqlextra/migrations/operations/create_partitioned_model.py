from django.db.migrations.operations.models import CreateModel

from psqlextra.migrations.state import PostgresPartitionedModelState


class PostgresCreatePartitionedModel(CreateModel):
    """Creates the model as a native PostgreSQL 11.x partitioned table."""

    serialization_expand_args = [
        "fields",
        "options",
        "managers",
        "partitioning_options",
    ]

    def __init__(self, *args, partitioning_options={}, **kwargs):
        super().__init__(*args, **kwargs)

        self.partitioning_options = partitioning_options or {}

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if self.partitioning_options:
            kwargs["partitioning_options"] = self.partitioning_options

        return name, args, kwargs

    def state_forwards(self, app_label, state):
        state.add_model(
            PostgresPartitionedModelState(
                app_label=app_label,
                name=self.name,
                fields=list(self.fields),
                options=dict(self.options),
                bases=tuple(self.bases),
                managers=list(self.managers),
                partitioning_options=dict(self.partitioning_options),
            )
        )

    def describe(self):
        """Gets a human readable text describing this migration."""

        description = super().describe()
        description = description.replace("model", "partitioned model")
        return descripton

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        """Apply this migration operation forwards."""

        model = to_state.apps.get_model(app_label, self.name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.create_partitioned_model(model)

    def database_backwards(
        self, app_label, schema_editor, from_state, to_state
    ):
        """Apply this migration operation backwards."""

        model = from_state.apps.get_model(app_label, self.name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.delete_partitioned_model(model)
