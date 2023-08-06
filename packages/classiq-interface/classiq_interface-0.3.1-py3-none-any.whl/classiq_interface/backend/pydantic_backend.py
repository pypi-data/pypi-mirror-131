from datetime import timedelta
from typing import TYPE_CHECKING

import pydantic

AZURE_QUANTUM_RESOURCE_ID_REGEX = r"^/subscriptions/([a-fA-F0-9-]*)/resourceGroups/([^\s/]*)/providers/Microsoft\.Quantum/Workspaces/([^\s/]*)$"  # noqa: F722

_IONQ_API_KEY_LENGTH: int = 32
INVALID_API_KEY: str = _IONQ_API_KEY_LENGTH * "a"
MAX_EXECUTION_TIMEOUT_SECONDS = timedelta(hours=4).total_seconds()

if TYPE_CHECKING:
    pydanticAWSAccessKeyID = str
    pydanticAWSSecretAccessKey = str
    pydanticExecutionTimeout = int
    pydanticRegionName = str
    pydanticS3BucketKey = str
    pydanticS3BucketName = str
    pydanticAzureResourceIDType = str
    pydanticIonQApiKeyType = str
    pydanticArgumentNameType = str
else:
    # TODO Simplify regular expressions in this file

    pydanticAWSAccessKeyID = pydantic.constr(
        strip_whitespace=True,
        min_length=20,
        max_length=20,
        regex=r"(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])",
    )

    pydanticAWSSecretAccessKey = pydantic.constr(
        strip_whitespace=True,
        min_length=40,
        max_length=40,
        regex=r"(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])",
    )

    pydanticRegionName = pydantic.constr(strip_whitespace=True, min_length=1)

    pydanticS3BucketName = pydantic.constr(strip_whitespace=True, min_length=3)

    pydanticS3BucketKey = pydantic.constr(strip_whitespace=True, min_length=1)

    pydanticAzureResourceIDType = pydantic.constr(regex=AZURE_QUANTUM_RESOURCE_ID_REGEX)

    pydanticIonQApiKeyType = pydantic.constr(
        regex=f"[A-Za-z0-9]{{{_IONQ_API_KEY_LENGTH}}}"
    )
    pydanticExecutionTimeout = pydantic.conint(gt=0, le=MAX_EXECUTION_TIMEOUT_SECONDS)

    pydanticArgumentNameType = pydantic.constr(regex="[_a-zA-Z][_a-zA-Z0-9]*")
