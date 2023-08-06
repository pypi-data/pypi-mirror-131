from typing import List

import datahub.emitter.mce_builder as builder
import datahub.metadata.schema_classes as models

from dh_client.entities import Entity


class Owner(Entity):
    @staticmethod
    def create_owners_aspect(owners: List[str]) -> models.OwnershipClass:
        """Create a `models.OwnershipClass` instance based on the given list of owners.

        Args:
            owners: List of owners.

        Return:
            A `models.OwnershipClass` instance.
        """
        return models.OwnershipClass(
            owners=[
                models.OwnerClass(builder.make_user_urn(owner), type="DATAOWNER")
                for owner in owners
            ]
        )
