import pytest

from create_event.event_data import EventData


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "application": "demo", "connection_type": "HTTPS", "event_type": "received_parcel", "description": "Received parcel on the workshop",'
                '"schema": { "properties": { "parcel_identification": { "type": "string" } } } }',
    }


@pytest.fixture()
def apigw_event_without_description():
    """ Generates API GW Event without description"""

    return {
        "body": '{ "application": "demo", "event_type": "received_parcel", "connection_type": "HTTPS",'
                '"schema": { "properties": { "parcel_identification": { "type": "string" } } } }',
    }


def test_make_event_data_from_request(apigw_event):
    # Arrange
    expectedEventData = EventData("demo", "HTTPS", "received_parcel", "Received parcel on the workshop",
        {'parcel_identification': {'type': 'string'}}
    )

    # Act
    event_data = EventData.from_request(apigw_event)

    # Assert
    assert event_data.application == expectedEventData.application
    assert event_data.connection_type == expectedEventData.connection_type
    assert event_data.event_type == expectedEventData.event_type
    assert event_data.description == expectedEventData.description
    assert event_data.schema_properties == expectedEventData.schema_properties


def test_make_event_data_from_request_without_description(apigw_event_without_description):
    # Arrange
    expectedEventData = EventData("demo",  "HTTPS", "received_parcel", "",
        {'parcel_identification': {'type': 'string'}}
    )
    
    # Act
    event_data = EventData.from_request(apigw_event_without_description)

    # Assert
    assert event_data.application == expectedEventData.application
    assert event_data.connection_type == expectedEventData.connection_type
    assert event_data.event_type == expectedEventData.event_type
    assert event_data.description == expectedEventData.description
    assert event_data.schema_properties == expectedEventData.schema_properties
