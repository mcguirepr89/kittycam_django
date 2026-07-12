from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class DiagnosticResult:
    """
    The normalized result produced by a single diagnostic.

    Every diagnostic in the engine returns one of these.
    """

    #
    # Name of the diagnostic that produced this result.
    #
    name: str

    #
    # Did the diagnostic itself complete successfully?
    #
    success: bool

    #
    # Machine-readable status.
    #
    status: str

    #
    # Short human-readable summary.
    #
    summary: str

    #
    # Optional additional information.
    #
    details: str | None = None

    #
    # Arbitrary structured data useful for debugging.
    #
    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        """
        Convert the result into a JSON-serializable dictionary.
        """

        return asdict(self)
