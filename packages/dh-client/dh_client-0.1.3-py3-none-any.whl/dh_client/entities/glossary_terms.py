from typing import List

import datahub.metadata.schema_classes as models
from datahub.ingestion.source.metadata import business_glossary

from . import Entity


class GlossaryTerm(Entity):
    """

    Examples:

        >>> client.glossary_term.upsert(name="glossary term y")
    """

    entity_type: str = "glossaryTerm"
    aspect_name: str = "glossaryTermInfo"

    def _create_mpc(self, name: str, source: str = "INTERNAL") -> List[dict]:
        """Create a tag mpc.

        Args:
            name: glossary term name.
            source: The source.

        Returns: A list with a single mpc dictionary.
        """
        return [
            dict(
                entityType=GlossaryTerm.entity_type,
                entityUrn=business_glossary.make_glossary_term_urn([name]),
                aspectName=GlossaryTerm.aspect_name,
                aspect=models.GlossaryTermInfoClass(definition=name, termSource=source),
            )
        ]
