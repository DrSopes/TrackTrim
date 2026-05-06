class TrackTrimError(Exception):
    """Base exception for TrackTrim."""


class NoContentDetectedError(TrackTrimError):
    """Raised when no non-silent content is detected."""


class InvalidFormatError(TrackTrimError):
    """Raised when input or output format is not supported."""