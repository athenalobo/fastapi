import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.body_multiple_params.tutorial003_an_py39 import app

    client = TestClient(app)
    return client


# Test required and embedded body parameters with no bodies sent
@needs_py39
@pytest.mark.parametrize(
    "path,body,expected_status,expected_response",
    [
        (
            "/items/5",
            {
                "importance": 2,
                "item": {"name": "Foo", "price": 50.5},
                "user": {"username": "Dave"},
            },
            200,
            {
                "item_id": 5,
                "importance": 2,
                "item": {
                    "name": "Foo",
                    "price": 50.5,
                    "description": None,
                    "tax": None,
                },
                "user": {"username": "Dave", "full_name": None},
            },
        ),
        (
            "/items/5",
            None,
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "item"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "importance"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
        (
            "/items/5",
            [],
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "item"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "user"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                    {
                        "loc": ["body", "importance"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    },
                ]
            },
        ),
    ],
)
def test_post_body(path, body, expected_status, expected_response, client: TestClient):
    response = client.put(path, json=body)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "put": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                    "summary": "Update Item",
                    "operationId": "update_item_items__item_id__put",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"title": "Item Id", "type": "integer"},
                            "name": "item_id",
                            "in": "path",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_update_item_items__item_id__put"
                                }
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Item": {
                    "title": "Item",
                    "required": ["name", "price"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                        "description": {"title": "Description", "type": "string"},
                        "tax": {"title": "Tax", "type": "number"},
                    },
                },
                "User": {
                    "title": "User",
                    "required": ["username"],
                    "type": "object",
                    "properties": {
                        "username": {"title": "Username", "type": "string"},
                        "full_name": {"title": "Full Name", "type": "string"},
                    },
                },
                "Body_update_item_items__item_id__put": {
                    "title": "Body_update_item_items__item_id__put",
                    "required": ["item", "user", "importance"],
                    "type": "object",
                    "properties": {
                        "item": {"$ref": "#/components/schemas/Item"},
                        "user": {"$ref": "#/components/schemas/User"},
                        "importance": {"title": "Importance", "type": "integer"},
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }
