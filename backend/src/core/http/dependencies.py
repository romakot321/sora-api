from src.core.http.client import AsyncHttpClient, IHttpClient


def get_http_client() -> IHttpClient:
    return AsyncHttpClient()
