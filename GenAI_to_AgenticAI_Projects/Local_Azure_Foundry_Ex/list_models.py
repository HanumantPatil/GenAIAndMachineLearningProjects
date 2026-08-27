"""List models available in the local Foundry catalog."""

# The package is installed in the Foundry Local runtime environment.
from foundry_local import FoundryLocalManager  # pylint: disable=import-error  # pyright: ignore[reportMissingImports]

manager = FoundryLocalManager()

catalog = manager.catalog

for model in catalog.list_models():
    print(model.alias)