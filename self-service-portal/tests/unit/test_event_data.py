import pytest

from create_event.event_data import EventData


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "unit": "u1", "name": "scanned_parcel", "description": "Scan parcel on the shop", "schema": { '
                '"properties": { "parcel_identification": { "type": "string" } } } }',
    }


@pytest.fixture()
def apigw_event_without_description():
    """ Generates API GW Event without description"""

    return {
        "body": '{ "unit": "u1", "name": "scanned_parcel", "schema": { '
                '"properties": { "parcel_identification": { "type": "string" } } } }',
    }


def test_make_event_data_from_request(apigw_event):
    expectedEventData = EventData("u1", "scanned_parcel", "Scan parcel on the shop",
                                  {'parcel_identification': {'type': 'string'}})

    event_data = EventData.from_request(apigw_event)

    assert event_data.unit == expectedEventData.unit
    assert event_data.description == expectedEventData.description
    assert event_data.name == expectedEventData.name
    assert event_data.schema_properties == expectedEventData.schema_properties


def test_make_event_data_from_request_without_description(apigw_event_without_description):
    expectedEventData = EventData("u1", "scanned_parcel", "", {'parcel_identification': {'type': 'string'}})

    event_data = EventData.from_request(apigw_event_without_description)

    assert event_data.unit == expectedEventData.unit
    assert event_data.description == expectedEventData.description
    assert event_data.name == expectedEventData.name
    assert event_data.schema_properties == expectedEventData.schema_properties
