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
        ("/customers/{customer_id}/plans", "GET"),
        ("/customers/{customer_id}/plans/status", "GET"),
        ("/customers/{customer_id}/plans/{plan_id}", "POST"),
        ("/customers/{customer_id}/plans/{plan_id}", "PATCH"),
        ("/transactions", "POST"),
        ("/transactions", "GET"),
        ("/invoices", "POST"),
        ("/plans", "POST"),
        ("/plans", "GET"),


    }

    assert registered_endpoints == expected_endpoints