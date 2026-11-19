from fastapi import FastAPI
from fastapi.routing import APIRoute

from src.api.router import api_router


def test_given_api_router_when_included_then_registers_all_context_endpoints() -> None:
    app = FastAPI()
    app.include_router(api_router)

    registered_endpoints = {
        (route.path, method)
        for route in app.routes
        if isinstance(route, APIRoute)
        for method in route.methods
    }

    expected_endpoints = {
        ("/customers", "POST"),
        ("/customers", "GET"),
        ("/customers/{id}", "GET"),
        ("/customers/{id}", "DELETE"),
        ("/customers/{id}", "PATCH"),
        ("/transactions", "POST"),
        ("/invoices", "POST"),
    }

    assert registered_endpoints == expected_endpoints