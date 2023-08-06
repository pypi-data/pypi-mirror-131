from typing import List, Dict

import datahub.emitter.mce_builder as builder
import datahub.metadata.schema_classes as models

from dh_client.entities import Entity
from dh_client.entities.owners import Owner
from dh_client.entities.tags import Tag


class Dataset(Entity):
    """
    Examples:

        The standard way:

        >>> client.dataset.upsert(name="projectA.datasetB.tableC", description="A random dataset description",
        ...                       tags=["foo"], owners=["team1@domain.com", "user2@domain.com"],
        ...                       glossary_terms=["gloss_term1"], upstream_datasets=["projectA.datasetB.tableD"],
        ...                       links={"Kaggle": "https://kaggle.com/randomuser/randomdataset"},
        ...                       custom_properties={'a': 'b'}
        ... )

        Modify dataset using a JSON file:

        $ ls *.json
        dataset_definitions.json
        $ cat dataset_definitions.json
        {"name": "projectA.datasetB.tableC", "description": "A random dataset description"}
        >>> client.dataset.upsert(file_pattern="*.json")
    """

    entity_type: str = "dataset"
    aspect_name: str = "datasetProperties"

    def _create_mpc(
        self,
        name: str,
        platform: str = "bigquery",
        env: str = "DEV",
        description: str = None,
        url: str = None,
        tags: List[str] = None,
        owners: List[str] = None,
        custom_properties=None,
        glossary_terms: List[str] = None,
        upstream_datasets: List[str] = None,
        links: dict = None,
    ) -> List[dict]:
        dataset_urn: str = builder.make_dataset_urn(
            platform=platform, name=name, env=env
        )
        """Create list of mpc dictionaries for dataset modifications.
        
        Args:
            name: The dataset name.
            platform: The platform name.
            env: The environment.
            description: The dataset's description.
            url: Dataset's url.
            tags: List of tags.
            owners: List of owners.
            custom_properties: Key/value custom properties.
            glossary_terms: List of glossary terms.
            upstream_datasets: List of upstream datasets.
        
        Returns:
            a list of mpc dictionaries.
        """

        mpc = [
            dict(
                entityType=Dataset.entity_type,
                entityUrn=dataset_urn,
                aspectName=Dataset.aspect_name,
                aspect=models.DatasetPropertiesClass(
                    description=description, externalUrl=url
                ),
            )
        ]

        mpc.extend(self._add_tags(dataset_urn, tags))
        mpc.extend(self._add_owners(dataset_urn, owners))
        mpc.extend(self._add_custom_properties(dataset_urn, custom_properties))
        mpc.extend(self._add_glossary_terms(dataset_urn, glossary_terms))
        mpc.extend(self._add_upstream_datasets(dataset_urn, upstream_datasets))
        mpc.extend(self._add_links(dataset_urn, links))

        return mpc

    @staticmethod
    def _add_tags(dataset_urn, tags) -> List[dict]:
        """Associate a list of tags with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            tags: List of tags.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                dict(
                    entityType=Dataset.entity_type,
                    entityUrn=dataset_urn,
                    aspectName="globalTags",
                    aspect=Tag.create_global_tags_aspect(tags),
                )
            ]
            if tags
            else []
        )

    @staticmethod
    def _add_owners(dataset_urn, owners) -> List[dict]:
        """Associate a list of owners with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            owners: List of owners.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    entityType=Dataset.entity_type,
                    aspectName="ownership",
                    aspect=Owner.create_owners_aspect(owners),
                )
            ]
            if owners
            else []
        )

    @staticmethod
    def _add_custom_properties(dataset_urn: str, custom_properties: dict) -> List[dict]:
        """Associate multiple custom properties with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            custom_properties: Dictionary of custom properties.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    entityType=Dataset.entity_type,
                    aspectName="datasetProperties",
                    aspect=models.DatasetPropertiesClass(
                        customProperties=custom_properties
                    ),
                )
            ]
            if custom_properties
            else []
        )

    def _add_glossary_terms(
        self, dataset_urn: str, glossary_terms: List[str]
    ) -> List[dict]:
        """Associate a list of glossary terms with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            glossary_terms: List of tags.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                dict(
                    entityUrn=dataset_urn,
                    aspectName="glossaryTerms",
                    entityType=Dataset.entity_type,
                    aspect=models.GlossaryTermsClass(
                        terms=[
                            models.GlossaryTermAssociationClass(
                                f"urn:li:glossaryTerm:{term}"
                            )
                            for term in glossary_terms
                        ],
                        auditStamp=models.AuditStampClass(
                            time=0, actor=self.emmiter.datahub_actor
                        ),
                    ),
                )
            ]
            if glossary_terms
            else []
        )

    def _add_upstream_datasets(
        self, dataset_urn: str, upstream_datasets: List[str]
    ) -> List[dict]:
        """Associate a list of upstream datasets with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            upstream_datasets: List of upstream datasets.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                {
                    "entityUrn": dataset_urn,
                    "aspectName": "upstreamLineage",
                    "entityType": Dataset.entity_type,
                    "aspect": models.UpstreamLineageClass(
                        upstreams=[
                            models.UpstreamClass(
                                dataset=self._create_resource_urn(upstream_dataset),
                                type=models.DatasetLineageTypeClass.TRANSFORMED,
                            )
                            for upstream_dataset in upstream_datasets
                        ]
                    ),
                }
            ]
            if upstream_datasets
            else []
        )

    def _add_links(self, dataset_urn: str, links: Dict[str, str]) -> List[dict]:
        """Associate a dictinary of links with the given dataset.

        Args:
            dataset_urn: The dataset URN.
            links: Dictionary of links.

        Returns:
            A list with a single mpc dictionary.
        """
        return (
            [
                {
                    "entityUrn": dataset_urn,
                    "entityType": Dataset.entity_type,
                    "aspectName": "institutionalMemory",
                    "aspect": models.InstitutionalMemoryClass(
                        elements=[
                            models.InstitutionalMemoryMetadataClass(
                                url=links[desc],
                                description=desc,
                                createStamp=models.AuditStampClass(
                                    time=0, actor=self.emmiter.datahub_actor
                                ),
                            )
                            for desc in links.keys()
                        ]
                    ),
                }
            ]
            if links
            else []
        )

    def delete_tag(self, dataset_urn: str, tag: str) -> None:
        """Delete tag from a dataset TODO: debug this

        Examples:

            >>> client.dataset.delete_tag("projectA.datasetB.tableC", "foo")
        """
        body = {
            "query": "mutation removeTag($input: TagAssociationInput!) {removeTag(input: $input)}",
            "variables": {
                "input": {
                    "tagUrn": builder.make_tag_urn(tag),
                    "resourceUrn": self._create_resource_urn(dataset_urn),
                }
            },
        }
        self._apply_mcp(None, [body], use_graphql=True)

    def _create_resource_urn(self, dataset: str) -> str:
        """Create the dataset urn using emitters' attributes.

        Args:
            dataset: dataset name

        Returns:
            The dataset URN.
        """
        return builder.make_dataset_urn(
            self.emmiter.dataset_platform, dataset, self.emmiter.env
        )
