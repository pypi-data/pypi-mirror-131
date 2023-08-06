from datetime import timedelta
from typing import Union

import pydantic

from classiq_interface.backend import pydantic_backend
from classiq_interface.backend.quantum_backend_providers import (
    EXACT_SIMULATORS,
    AWSBackendNames,
    AzureQuantumBackendNames,
    IBMQBackendNames,
    IonqBackendNames,
    ProviderTypeVendor,
    ProviderVendor,
)


class BackendPreferences(pydantic.BaseModel):
    backend_service_provider: str = pydantic.Field(
        description="Provider company for the requested backend."
    )
    backend_name: str = pydantic.Field(description="Name of the requested backend.")


AWS_DEFAULT_JOB_TIMEOUT_SECONDS = timedelta(minutes=5).total_seconds()


class AwsBackendPreferences(BackendPreferences):
    backend_service_provider: ProviderTypeVendor.AWS_BRAKET = ProviderVendor.AWS_BRAKET
    # Allow running any backend supported by the vendor
    backend_name: Union[AWSBackendNames, str]
    aws_access_key_id: pydantic_backend.pydanticAWSAccessKeyID = pydantic.Field(
        description="AWS Access Key ID"
    )
    aws_secret_access_key: pydantic_backend.pydanticAWSSecretAccessKey = pydantic.Field(
        description="AWS Secret Access Key"
    )
    region_name: pydantic_backend.pydanticRegionName = pydantic.Field(
        description="AWS Region name"
    )
    s3_bucket_name: pydantic_backend.pydanticS3BucketName = pydantic.Field(
        description="S3 Bucket Name"
    )
    s3_bucket_key: pydantic_backend.pydanticS3BucketKey = pydantic.Field(
        description="S3 Bucket Key"
    )
    job_timeout: pydantic_backend.pydanticExecutionTimeout = pydantic.Field(
        description="Timeout for Jobs sent for execution in seconds.",
        default=AWS_DEFAULT_JOB_TIMEOUT_SECONDS,
    )


class IBMBackendPreferences(BackendPreferences):
    backend_service_provider: ProviderTypeVendor.IBMQ = ProviderVendor.IBMQ
    backend_name: IBMQBackendNames


class AzureCredential(pydantic.BaseSettings):
    tenant_id: str = pydantic.Field(..., description="Azure Tenant ID")
    client_id: str = pydantic.Field(..., description="Azure Client ID")
    client_secret: str = pydantic.Field(..., description="Azure Client Secret")

    class Config:
        title = "Azure Service Principal Credential"
        env_prefix = "AZURE_"
        case_sensitive = False


class AzureBackendPreferences(BackendPreferences):
    backend_service_provider: ProviderTypeVendor.AZURE_QUANTUM = (
        ProviderVendor.AZURE_QUANTUM
    )
    # Allow running any backend supported by the vendor
    backend_name: Union[AzureQuantumBackendNames, str]

    resource_id: pydantic_backend.pydanticAzureResourceIDType = pydantic.Field(
        ...,
        description="Azure Resource ID (including Azure subscription ID, resource "
        "group and workspace)",
    )

    location: str = pydantic.Field(..., description="Azure Region")

    credential: AzureCredential = pydantic.Field(
        default_factory=AzureCredential,
        description="The service principal credential to access the quantum workspace",
    )


class IonqBackendPreferences(BackendPreferences):
    backend_service_provider: ProviderTypeVendor.IONQ = ProviderVendor.IONQ
    backend_name: IonqBackendNames = pydantic.Field(
        default=IonqBackendNames.SIMULATOR,
        description="IonQ backend for quantum programs execution.",
    )
    api_key: pydantic_backend.pydanticIonQApiKeyType = pydantic.Field(
        ..., description="IonQ API key"
    )


def is_exact_simulator(backend_preferences: BackendPreferences):
    return backend_preferences.backend_name in EXACT_SIMULATORS
