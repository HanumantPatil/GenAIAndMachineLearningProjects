"""List models available in the local Foundry catalog."""

from foundry_local_sdk import Configuration, FoundryLocalManager


def main() -> None:
    """Print the aliases available in the Foundry Local model catalog."""
    config = Configuration(app_name="foundry_local_samples")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    for model in manager.catalog.list_models():
        print(model.alias)


if __name__ == "__main__":
    main()