from pytest import fixture

from famistudio_convert.conversion import DefaultConversionTypes
from famistudio_convert.engine import Envelope, EnvelopeType


@fixture
def envelop() -> Envelope:
    return Envelope(EnvelopeType.VOLUME, None, None, False, [0, 1, 2, 3, 4])


def test_envelope_conversion_simple(envelop: Envelope):
    envelop.solve(DefaultConversionTypes.FAMISTUDIO_TEXT, 0)
