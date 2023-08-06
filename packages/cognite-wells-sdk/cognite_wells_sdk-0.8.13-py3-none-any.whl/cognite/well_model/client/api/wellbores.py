import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.merge_rules.wellbores import WellboreMergeRulesAPI
from cognite.well_model.client.models.resource_list import WellboreList
from cognite.well_model.client.utils._identifier_list import identifier_items, identifier_items_single
from cognite.well_model.models import (
    IdentifierItems,
    Wellbore,
    WellboreIngestion,
    WellboreIngestionItems,
    WellboreItems,
)

logger = logging.getLogger(__name__)


class WellboresAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)
        self.merge_rules = WellboreMergeRulesAPI(client)

    def ingest(self, ingestions: List[WellboreIngestion]) -> WellboreList:
        """Ingest wellbores

        Args:
            ingestions (List[WellboreIngestion]):

        Returns:
            WellboreList:
        """
        path = self._get_path("/wellbores")
        json = WellboreIngestionItems(items=ingestions).json()
        response: Response = self.client.post(path, json)
        wellbore_items: WellboreItems = WellboreItems.parse_obj(response.json())
        wellbores: List[Wellbore] = wellbore_items.items
        return WellboreList(wellbores)

    # guranteed to be non-empty list
    def _retrieve_multiple(self, identifiers: IdentifierItems) -> List[Wellbore]:
        path: str = self._get_path("/wellbores/byids")
        response: Response = self.client.post(url_path=path, json=identifiers.json())
        wellbore_items: WellboreItems = WellboreItems.parse_raw(response.text)
        wellbores: List[Wellbore] = wellbore_items.items
        return wellbores

    def retrieve(self, asset_external_id: Optional[str] = None, matching_id: Optional[str] = None) -> Wellbore:
        """Get wellbore by asset external id or matching id.

        Args:
            asset_external_id (Optional[str], optional)
            matching_id (Optional[str], optional)

        Returns:
            Wellbore:
        """
        identifiers = identifier_items_single(asset_external_id, matching_id)
        return self._retrieve_multiple(identifiers)[0]

    def retrieve_multiple(
        self, asset_external_ids: Optional[List[str]] = None, matching_ids: Optional[List[str]] = None
    ) -> WellboreList:
        """Get wellbores by a list assets external ids and matching ids

        Args:
            asset_external_ids (Optional[List[str]]): list of wellbore asset external ids
            matching_ids (Optional[List[str]]): List of wellbore matching ids
        Returns:
            WellboreList:
        """
        identifiers = identifier_items(asset_external_ids, matching_ids)
        return WellboreList(self._retrieve_multiple(identifiers))
