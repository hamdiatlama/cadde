"""Meilisearch search client (adapter pattern)."""
from typing import Optional
import meilisearch

from src.config import MEILISEARCH_URL, MEILISEARCH_API_KEY


class SearchClient:
    def __init__(self, url: str = MEILISEARCH_URL, api_key: str = MEILISEARCH_API_KEY):
        self._client = meilisearch.Client(url, api_key)

    def index(self, index_name: str):
        return self._client.index(index_name)

    def add_documents(self, index_name: str, documents: list[dict], primary_key: Optional[str] = None):
        return self.index(index_name).add_documents(documents, primary_key=primary_key)

    def update_documents(self, index_name: str, documents: list[dict]):
        return self.index(index_name).update_documents(documents)

    def delete_document(self, index_name: str, document_id: str | int):
        return self.index(index_name).delete_document(str(document_id))

    def search(self, index_name: str, query: str, **kwargs) -> dict:
        return self.index(index_name).search(query, kwargs)

    def create_index(self, index_name: str, primary_key: Optional[str] = None):
        try:
            self._client.create_index(index_name, {"primaryKey": primary_key})
        except meilisearch.errors.MeilisearchApiError:
            pass

    def delete_index(self, index_name: str):
        try:
            self._client.delete_index(index_name)
        except meilisearch.errors.MeilisearchApiError:
            pass


search = SearchClient()
