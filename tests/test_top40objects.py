import arrow

__author__ = 'dan'
from codefurther import top40

from expects import *
from booby.errors import FieldError
from arrow import Arrow


class TestValidation:

    def test_should_fail_validation_if_null_dictionary_supplied(self):
        def callback():
            top40.Entry({})

        expect(callback).to(raise_error(TypeError))

    def test_should_fail_artist_validation_if_incorrect_field_supplied(self):
        def create_artist():
            top40.Entry(artistz="")

        expect(create_artist).to(raise_error(FieldError))

    def test_should_fail_entry_validation_if_incorrect_field_supplied(self):
        def create_entry():
            top40.Entry(artistz="")

        expect(create_entry).to(raise_error(FieldError))

    def test_should_fail_change_validation_if_incorrect_field_supplied(self):

        def create_change():
            top40.Entry(artistz="")

        expect(create_change).to(raise_error(FieldError))

    def test_should_pass_validation_for_artist_type(self):
        artist = top40.Chart(
            date=Arrow.utcnow().timestamp,
            retrieved=Arrow.utcnow().timestamp,
            entries={
                "position": 1,
                "previousPosition": 2,
                "numWeeks": 4,
                "artist": "An artist",
                "title": "A title",
                "change": {
                    "direction": "down",
                    "amount": 2,
                    "actual": -2
                },
            }
        )

        expect(artist).to(be(artist))

    def test_should_pass_validation_for_entry_type(self):
        entry = top40.Entry(
            position=1,
            previousPosition=2,
            numWeeks=4,
            artist="An artist",
            title="A title",
            change={
                "direction": "down",
                "amount": 2,
                "actual": -2
            }
        )

        expect(entry).to(be(entry))

    def test_should_pass_validation_for_entry_type_with_status_field(self):
        entry = top40.Entry(
            position=1,
            previousPosition=2,
            numWeeks=4,
            artist="An artist",
            title="A title",
            change={
                "direction": "down",
                "amount": 2,
                "actual": -2
            },
            status="up 2"
        )

        expect(entry).to(be(entry))

    def test_should_pass_validation_for_entry_type_with_current_field(self):
        chart = top40.Chart(
            date = arrow.utcnow().timestamp,
            retrieved = arrow.utcnow().timestamp,
            entries=[
                {
                    "position": 1,
                    "previousPosition": 2,
                    "numWeeks": 4,
                    "artist": "An artist",
                    "title": "A title",
                    "change": {
                        "direction": "down",
                        "amount": 2,
                        "actual": -2
                    },
                    "status": "up 2"
                }
            ],
            current=False
        )

        expect(chart).to(be(chart))
        expect(chart.date).to(be_an(int))
        expect(chart["date"]).to(be_an(int))
        expect(chart.current).to(be_a(bool))
        expect(chart["current"]).to(be_a(bool))

    def test_should_pass_validation_for_change_type(self):
        change = top40.Change(direction="down", amount=2, actual=-2)

        expect(change).to(be(change))

