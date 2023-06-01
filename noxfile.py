"""Nox automation file."""

from nox import Session, session

python_versions = ["3.9"]


@session(python=["3.9"])
def export_ts(session: Session) -> None:
    """Export Pydantic model as TypeScript object."""
    session.install("-r", "requirements-dev.txt")
    session.run(
        "pydantic2ts",
        "--module",
        "microjson.py",
        "--output",
        "microjsonschema.ts",
    )