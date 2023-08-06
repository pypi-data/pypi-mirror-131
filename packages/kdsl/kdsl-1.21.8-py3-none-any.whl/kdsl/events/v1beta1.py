from __future__ import annotations
import attr
import kdsl.core.v1
import kdsl.events.v1beta1
from typing import Sequence, Optional, Any, Mapping, TypedDict, Union, ClassVar, Literal
from kdsl.bases import OMIT, K8sResource, OmitEnum, K8sObject


def optional_converter_EventSeries(value: Union[EventSeriesUnion, OmitEnum, None]) ->Union[EventSeries, OmitEnum, None]:
    return EventSeries(**value) if isinstance(value, dict) else value


def required_converter_EventSeries(value: EventSeriesUnion) ->EventSeries:
    return EventSeries(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class EventSeries(K8sObject):
    count: int = attr.ib(metadata={'yaml_name': 'count'})
    lastObservedTime: str = attr.ib(metadata={'yaml_name': 'lastObservedTime'})


class EventSeriesTypedDict(TypedDict, total=(True)):
    count: int
    lastObservedTime: str


EventSeriesUnion = Union[EventSeries, EventSeriesTypedDict]


@attr.s(kw_only=True)
class Event(K8sResource):
    apiVersion: ClassVar[str] = 'events.k8s.io/v1beta1'
    kind: ClassVar[str] = 'Event'
    eventTime: str = attr.ib(metadata={'yaml_name': 'eventTime'})
    action: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'action'}, default=OMIT)
    deprecatedCount: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'deprecatedCount'}, default=OMIT)
    deprecatedFirstTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'deprecatedFirstTimestamp'}, default=OMIT)
    deprecatedLastTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'deprecatedLastTimestamp'}, default=OMIT)
    deprecatedSource: Union[None, OmitEnum, kdsl.core.v1.EventSource] = attr.ib(metadata={'yaml_name': 'deprecatedSource'}, converter=kdsl.core.v1.optional_converter_EventSource, default=OMIT)
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=kdsl.core.v1.optional_converter_ObjectMeta, default=OMIT)
    note: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'note'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    regarding: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(metadata={'yaml_name': 'regarding'}, converter=kdsl.core.v1.optional_converter_ObjectReference, default=OMIT)
    related: Union[None, OmitEnum, kdsl.core.v1.ObjectReference] = attr.ib(metadata={'yaml_name': 'related'}, converter=kdsl.core.v1.optional_converter_ObjectReference, default=OMIT)
    reportingController: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reportingController'}, default=OMIT)
    reportingInstance: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reportingInstance'}, default=OMIT)
    series: Union[None, OmitEnum, EventSeries] = attr.ib(metadata={'yaml_name': 'series'}, converter=optional_converter_EventSeries, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)
