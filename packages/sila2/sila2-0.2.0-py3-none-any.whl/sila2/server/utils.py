from __future__ import annotations

import re
import warnings
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set, Tuple, Union

import grpc
from grpc import ServicerContext

from sila2.framework.abc.sila_error import SilaError
from sila2.framework.command.command import Command
from sila2.framework.defined_execution_error_node import DefinedExecutionErrorNode
from sila2.framework.errors.defined_execution_error import DefinedExecutionError
from sila2.framework.errors.invalid_metadata import InvalidMetadata
from sila2.framework.errors.no_metadata_allowed import NoMetadataAllowed
from sila2.framework.errors.undefined_execution_error import UndefinedExecutionError
from sila2.framework.errors.validation_error import ValidationError
from sila2.framework.fully_qualified_identifier import FullyQualifiedIdentifier
from sila2.framework.metadata import Metadata
from sila2.framework.property.property import Property
from sila2.framework.utils import FullyQualifiedIdentifierRegex, raise_as_rpc_error

if TYPE_CHECKING:
    from sila2.framework.feature import Feature
    from sila2.server.sila_server import SilaServer


def _find_allowed_defined_execution_errors(
    server: SilaServer,
    origin: Optional[Union[Command, Property]] = None,
    metadata_identifiers: Optional[Iterable[FullyQualifiedIdentifier]] = None,
) -> List[DefinedExecutionErrorNode]:
    allowed_errors = []
    if origin is not None:
        allowed_errors.extend(origin.defined_execution_errors)
    if metadata_identifiers is not None:
        for metadata_id in metadata_identifiers:
            allowed_errors.extend(server.children_by_fully_qualified_identifier[metadata_id].defined_execution_errors)
    return allowed_errors


def extract_metadata(
    context: grpc.ServicerContext, server: SilaServer, origin: Union[Property, Command]
) -> Dict[FullyQualifiedIdentifier, Any]:
    expected_metadata: Set[FullyQualifiedIdentifier] = set()
    for feature_servicer in server.feature_servicers.values():
        for meta_id, meta in feature_servicer.feature.metadata_definitions.items():
            raw_affected_calls: List[Union[Feature, Command, Property, FullyQualifiedIdentifier]] = getattr(
                feature_servicer.implementation, f"get_calls_affected_by_{meta_id}"
            )()
            affected_fqis = [
                obj if isinstance(obj, FullyQualifiedIdentifier) else obj.fully_qualified_identifier
                for obj in raw_affected_calls
            ]

            if (
                origin.fully_qualified_identifier in affected_fqis
                or origin.parent_feature.fully_qualified_identifier in affected_fqis
            ):
                expected_metadata.add(meta.fully_qualified_identifier)

    received_metadata: Dict[FullyQualifiedIdentifier, Any] = {}
    for key, value in context.invocation_metadata():
        if re.fullmatch(
            f"sila/{FullyQualifiedIdentifierRegex.MetadataIdentifier}/bin", key.replace("-", "/"), flags=re.IGNORECASE
        ):
            try:
                key = key[5:-4].replace("-", "/")
                meta: Metadata = server.children_by_fully_qualified_identifier[FullyQualifiedIdentifier(key)]
                received_metadata[meta.fully_qualified_identifier] = meta.to_native_type(value)
            except KeyError:
                raise_as_rpc_error(InvalidMetadata(f"Server has no metadata {key}"), context)
            except Exception as ex:
                raise_as_rpc_error(InvalidMetadata(f"Failed to deserialize metadata value for {key!r}: {ex}"), context)

    # local import to prevent circular imports
    from sila2.features.silaservice import SiLAServiceFeature

    if origin.parent_feature.fully_qualified_identifier == SiLAServiceFeature.fully_qualified_identifier:
        if received_metadata:
            raise_as_rpc_error(NoMetadataAllowed("Cannot use metadata with calls to the SiLAService feature"), context)
        if expected_metadata:
            warnings.warn(f"Server expects metadata for the SiLAService call {origin._identifier}. Ignoring.")
        return {}

    for expected_meta_fqi in expected_metadata:
        if expected_meta_fqi not in received_metadata:
            raise_as_rpc_error(InvalidMetadata(f"Did not receive required metadata {expected_meta_fqi}"), context)

    return received_metadata


def unpack_parameters(command: Command, request, context: ServicerContext) -> Tuple[Any, ...]:
    try:
        return command.parameters.to_native_type(request)
    except ValidationError as val_err:
        raise_as_rpc_error(val_err, context)


@contextmanager
def raises_rpc_errors(
    context: ServicerContext,
    allowed_defined_execution_errors: Optional[Iterable[DefinedExecutionErrorNode]] = None,
):
    try:
        yield
    except Exception as ex:
        if isinstance(ex, NotImplementedError):
            context.abort(grpc.StatusCode.UNIMPLEMENTED, "The requested functionality is not implemented")

        if not isinstance(ex, SilaError):
            raise_as_rpc_error(UndefinedExecutionError(ex), context)

        allowed_error_identifiers = [err.fully_qualified_identifier for err in allowed_defined_execution_errors]
        if isinstance(ex, DefinedExecutionError) and ex.fully_qualified_identifier not in allowed_error_identifiers:
            raise_as_rpc_error(UndefinedExecutionError(ex), context)

        raise_as_rpc_error(ex, context)
