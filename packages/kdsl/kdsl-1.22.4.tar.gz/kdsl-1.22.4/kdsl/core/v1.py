from __future__ import annotations
import attr
import kdsl.core.v1
from typing import Any, Optional, Union, Literal, Mapping, Sequence, TypedDict, ClassVar
from kdsl.bases import OMIT, K8sObject, OmitEnum, K8sResource


def optional_list_converter_AttachedVolume(value: Union[Sequence[AttachedVolumeUnion], OmitEnum, None]) ->Union[Sequence[AttachedVolume], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_AttachedVolume(x) for x in value]


def optional_list_converter_ContainerImage(value: Union[Sequence[ContainerImageUnion], OmitEnum, None]) ->Union[Sequence[ContainerImage], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerImage(x) for x in value]


def optional_list_converter_ContainerPort(value: Union[Sequence[ContainerPortUnion], OmitEnum, None]) ->Union[Sequence[ContainerPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerPort(x) for x in value]


def optional_list_converter_ContainerStatus(value: Union[Sequence[ContainerStatusUnion], OmitEnum, None]) ->Union[Sequence[ContainerStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ContainerStatus(x) for x in value]


def optional_list_converter_DownwardAPIVolumeFile(value: Union[Sequence[DownwardAPIVolumeFileUnion], OmitEnum, None]) ->Union[Sequence[DownwardAPIVolumeFile], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_DownwardAPIVolumeFile(x) for x in value]


def optional_list_converter_EmbeddedPersistentVolumeClaim(value: Union[Sequence[EmbeddedPersistentVolumeClaimUnion], OmitEnum, None]) ->Union[Sequence[EmbeddedPersistentVolumeClaim], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EmbeddedPersistentVolumeClaim(x) for x in value]


def optional_list_converter_EndpointAddress(value: Union[Sequence[EndpointAddressUnion], OmitEnum, None]) ->Union[Sequence[EndpointAddress], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointAddress(x) for x in value]


def optional_list_converter_EndpointPort(value: Union[Sequence[EndpointPortUnion], OmitEnum, None]) ->Union[Sequence[EndpointPort], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointPort(x) for x in value]


def optional_list_converter_EndpointSubset(value: Union[Sequence[EndpointSubsetUnion], OmitEnum, None]) ->Union[Sequence[EndpointSubset], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EndpointSubset(x) for x in value]


def optional_list_converter_EnvFromSource(value: Union[Sequence[EnvFromSourceUnion], OmitEnum, None]) ->Union[Sequence[EnvFromSource], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_EnvFromSource(x) for x in value]


def optional_list_converter_HTTPHeader(value: Union[Sequence[HTTPHeaderUnion], OmitEnum, None]) ->Union[Sequence[HTTPHeader], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_HTTPHeader(x) for x in value]


def optional_list_converter_KeyToPath(value: Union[Sequence[KeyToPathUnion], OmitEnum, None]) ->Union[Sequence[KeyToPath], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_KeyToPath(x) for x in value]


def optional_list_converter_LabelSelector(value: Union[Sequence[LabelSelectorUnion], OmitEnum, None]) ->Union[Sequence[LabelSelector], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LabelSelector(x) for x in value]


def optional_list_converter_LabelSelectorRequirement(value: Union[Sequence[LabelSelectorRequirementUnion], OmitEnum, None]) ->Union[Sequence[LabelSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LabelSelectorRequirement(x) for x in value]


def optional_list_converter_LoadBalancerIngress(value: Union[Sequence[LoadBalancerIngressUnion], OmitEnum, None]) ->Union[Sequence[LoadBalancerIngress], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LoadBalancerIngress(x) for x in value]


def optional_list_converter_LocalObjectReference(value: Union[Sequence[LocalObjectReferenceUnion], OmitEnum, None]) ->Union[Sequence[LocalObjectReference], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_LocalObjectReference(x) for x in value]


def optional_list_converter_ManagedFieldsEntry(value: Union[Sequence[ManagedFieldsEntryUnion], OmitEnum, None]) ->Union[Sequence[ManagedFieldsEntry], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ManagedFieldsEntry(x) for x in value]


def optional_list_converter_NodeSelectorRequirement(value: Union[Sequence[NodeSelectorRequirementUnion], OmitEnum, None]) ->Union[Sequence[NodeSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_NodeSelectorRequirement(x) for x in value]


def optional_list_converter_ObjectReference(value: Union[Sequence[ObjectReferenceUnion], OmitEnum, None]) ->Union[Sequence[ObjectReference], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ObjectReference(x) for x in value]


def optional_list_converter_PodAffinityTerm(value: Union[Sequence[PodAffinityTermUnion], OmitEnum, None]) ->Union[Sequence[PodAffinityTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodAffinityTerm(x) for x in value]


def optional_list_converter_PodDNSConfigOption(value: Union[Sequence[PodDNSConfigOptionUnion], OmitEnum, None]) ->Union[Sequence[PodDNSConfigOption], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodDNSConfigOption(x) for x in value]


def optional_list_converter_PodIP(value: Union[Sequence[PodIPUnion], OmitEnum, None]) ->Union[Sequence[PodIP], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodIP(x) for x in value]


def optional_list_converter_PodReadinessGate(value: Union[Sequence[PodReadinessGateUnion], OmitEnum, None]) ->Union[Sequence[PodReadinessGate], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PodReadinessGate(x) for x in value]


def optional_list_converter_PortStatus(value: Union[Sequence[PortStatusUnion], OmitEnum, None]) ->Union[Sequence[PortStatus], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PortStatus(x) for x in value]


def optional_list_converter_PreferredSchedulingTerm(value: Union[Sequence[PreferredSchedulingTermUnion], OmitEnum, None]) ->Union[Sequence[PreferredSchedulingTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_PreferredSchedulingTerm(x) for x in value]


def optional_list_converter_ScopedResourceSelectorRequirement(value: Union[Sequence[ScopedResourceSelectorRequirementUnion], OmitEnum, None]) ->Union[Sequence[ScopedResourceSelectorRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_ScopedResourceSelectorRequirement(x) for x in value]


def optional_list_converter_Sysctl(value: Union[Sequence[SysctlUnion], OmitEnum, None]) ->Union[Sequence[Sysctl], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Sysctl(x) for x in value]


def optional_list_converter_Taint(value: Union[Sequence[TaintUnion], OmitEnum, None]) ->Union[Sequence[Taint], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Taint(x) for x in value]


def optional_list_converter_Toleration(value: Union[Sequence[TolerationUnion], OmitEnum, None]) ->Union[Sequence[Toleration], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_Toleration(x) for x in value]


def optional_list_converter_TopologySelectorLabelRequirement(value: Union[Sequence[TopologySelectorLabelRequirementUnion], OmitEnum, None]) ->Union[Sequence[TopologySelectorLabelRequirement], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_TopologySelectorLabelRequirement(x) for x in value]


def optional_list_converter_TopologySelectorTerm(value: Union[Sequence[TopologySelectorTermUnion], OmitEnum, None]) ->Union[Sequence[TopologySelectorTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_TopologySelectorTerm(x) for x in value]


def optional_list_converter_VolumeProjection(value: Union[Sequence[VolumeProjectionUnion], OmitEnum, None]) ->Union[Sequence[VolumeProjection], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_VolumeProjection(x) for x in value]


def optional_list_converter_WeightedPodAffinityTerm(value: Union[Sequence[WeightedPodAffinityTermUnion], OmitEnum, None]) ->Union[Sequence[WeightedPodAffinityTerm], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_WeightedPodAffinityTerm(x) for x in value]


def required_list_converter_LimitRangeItem(value: Sequence[LimitRangeItemUnion]) ->Sequence[LimitRangeItem]:
    return [required_converter_LimitRangeItem(x) for x in value]


def required_list_converter_NodeSelectorTerm(value: Sequence[NodeSelectorTermUnion]) ->Sequence[NodeSelectorTerm]:
    return [required_converter_NodeSelectorTerm(x) for x in value]


def optional_mlist_converter_ConditionItem(value: Union[Mapping[str, ConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, ConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_ContainerItem(value: Union[Mapping[str, ContainerItemUnion], OmitEnum, None]) ->Union[Mapping[str, ContainerItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ContainerItem(v) for k, v in value.items()}


def optional_mlist_converter_ContainerPortItem(value: Union[Mapping[int, ContainerPortItemUnion], OmitEnum, None]) ->Union[Mapping[int, ContainerPortItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ContainerPortItem(v) for k, v in value.items()}


def optional_mlist_converter_EnvVarItem(value: Union[Mapping[str, EnvVarItemUnion], OmitEnum, None]) ->Union[Mapping[str, EnvVarItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_EnvVarItem(v) for k, v in value.items()}


def optional_mlist_converter_EphemeralContainerItem(value: Union[Mapping[str, EphemeralContainerItemUnion], OmitEnum, None]) ->Union[Mapping[str, EphemeralContainerItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_EphemeralContainerItem(v) for k, v in value.items()}


def optional_mlist_converter_HostAliasItem(value: Union[Mapping[str, HostAliasItemUnion], OmitEnum, None]) ->Union[Mapping[str, HostAliasItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_HostAliasItem(v) for k, v in value.items()}


def optional_mlist_converter_NamespaceConditionItem(value: Union[Mapping[str, NamespaceConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, NamespaceConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_NamespaceConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_NodeAddressItem(value: Union[Mapping[str, NodeAddressItemUnion], OmitEnum, None]) ->Union[Mapping[str, NodeAddressItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_NodeAddressItem(v) for k, v in value.items()}


def optional_mlist_converter_NodeConditionItem(value: Union[Mapping[str, NodeConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, NodeConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_NodeConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_ObjectReferenceItem(value: Union[Mapping[str, ObjectReferenceItemUnion], OmitEnum, None]) ->Union[Mapping[str, ObjectReferenceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ObjectReferenceItem(v) for k, v in value.items()}


def optional_mlist_converter_OwnerReferenceItem(value: Union[Mapping[str, OwnerReferenceItemUnion], OmitEnum, None]) ->Union[Mapping[str, OwnerReferenceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_OwnerReferenceItem(v) for k, v in value.items()}


def optional_mlist_converter_PersistentVolumeClaimConditionItem(value: Union[Mapping[str, PersistentVolumeClaimConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, PersistentVolumeClaimConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_PersistentVolumeClaimConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_PodConditionItem(value: Union[Mapping[str, PodConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, PodConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_PodConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_ReplicationControllerConditionItem(value: Union[Mapping[str, ReplicationControllerConditionItemUnion], OmitEnum, None]) ->Union[Mapping[str, ReplicationControllerConditionItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ReplicationControllerConditionItem(v) for k, v in value.items()}


def optional_mlist_converter_ServicePortItem(value: Union[Mapping[int, ServicePortItemUnion], OmitEnum, None]) ->Union[Mapping[int, ServicePortItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_ServicePortItem(v) for k, v in value.items()}


def optional_mlist_converter_TopologySpreadConstraintItem(value: Union[Mapping[str, TopologySpreadConstraintItemUnion], OmitEnum, None]) ->Union[Mapping[str, TopologySpreadConstraintItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_TopologySpreadConstraintItem(v) for k, v in value.items()}


def optional_mlist_converter_VolumeDeviceItem(value: Union[Mapping[str, VolumeDeviceItemUnion], OmitEnum, None]) ->Union[Mapping[str, VolumeDeviceItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeDeviceItem(v) for k, v in value.items()}


def optional_mlist_converter_VolumeItem(value: Union[Mapping[str, VolumeItemUnion], OmitEnum, None]) ->Union[Mapping[str, VolumeItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeItem(v) for k, v in value.items()}


def optional_mlist_converter_VolumeMountItem(value: Union[Mapping[str, VolumeMountItemUnion], OmitEnum, None]) ->Union[Mapping[str, VolumeMountItem], OmitEnum, None]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_VolumeMountItem(v) for k, v in value.items()}


def required_mlist_converter_ContainerItem(value: Mapping[str, ContainerItemUnion]) ->Mapping[str, ContainerItem]:
    return {k: required_converter_ContainerItem(v) for k, v in value.items()}


def optional_converter_AWSElasticBlockStoreVolumeSource(value: Union[AWSElasticBlockStoreVolumeSourceUnion, OmitEnum, None]) ->Union[AWSElasticBlockStoreVolumeSource, OmitEnum, None]:
    return AWSElasticBlockStoreVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_Affinity(value: Union[AffinityUnion, OmitEnum, None]) ->Union[Affinity, OmitEnum, None]:
    return Affinity(**value) if isinstance(value, dict) else value


def optional_converter_AttachedVolume(value: Union[AttachedVolumeUnion, OmitEnum, None]) ->Union[AttachedVolume, OmitEnum, None]:
    return AttachedVolume(**value) if isinstance(value, dict) else value


def optional_converter_AzureDiskVolumeSource(value: Union[AzureDiskVolumeSourceUnion, OmitEnum, None]) ->Union[AzureDiskVolumeSource, OmitEnum, None]:
    return AzureDiskVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_AzureFilePersistentVolumeSource(value: Union[AzureFilePersistentVolumeSourceUnion, OmitEnum, None]) ->Union[AzureFilePersistentVolumeSource, OmitEnum, None]:
    return AzureFilePersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_AzureFileVolumeSource(value: Union[AzureFileVolumeSourceUnion, OmitEnum, None]) ->Union[AzureFileVolumeSource, OmitEnum, None]:
    return AzureFileVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_CSIPersistentVolumeSource(value: Union[CSIPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[CSIPersistentVolumeSource, OmitEnum, None]:
    return CSIPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_CSIVolumeSource(value: Union[CSIVolumeSourceUnion, OmitEnum, None]) ->Union[CSIVolumeSource, OmitEnum, None]:
    return CSIVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_Capabilities(value: Union[CapabilitiesUnion, OmitEnum, None]) ->Union[Capabilities, OmitEnum, None]:
    return Capabilities(**value) if isinstance(value, dict) else value


def optional_converter_CephFSPersistentVolumeSource(value: Union[CephFSPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[CephFSPersistentVolumeSource, OmitEnum, None]:
    return CephFSPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_CephFSVolumeSource(value: Union[CephFSVolumeSourceUnion, OmitEnum, None]) ->Union[CephFSVolumeSource, OmitEnum, None]:
    return CephFSVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_CinderPersistentVolumeSource(value: Union[CinderPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[CinderPersistentVolumeSource, OmitEnum, None]:
    return CinderPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_CinderVolumeSource(value: Union[CinderVolumeSourceUnion, OmitEnum, None]) ->Union[CinderVolumeSource, OmitEnum, None]:
    return CinderVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ClientIPConfig(value: Union[ClientIPConfigUnion, OmitEnum, None]) ->Union[ClientIPConfig, OmitEnum, None]:
    return ClientIPConfig(**value) if isinstance(value, dict) else value


def optional_converter_ConditionItem(value: Union[ConditionItemUnion, OmitEnum, None]) ->Union[ConditionItem, OmitEnum, None]:
    return ConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapEnvSource(value: Union[ConfigMapEnvSourceUnion, OmitEnum, None]) ->Union[ConfigMapEnvSource, OmitEnum, None]:
    return ConfigMapEnvSource(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapKeySelector(value: Union[ConfigMapKeySelectorUnion, OmitEnum, None]) ->Union[ConfigMapKeySelector, OmitEnum, None]:
    return ConfigMapKeySelector(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapNodeConfigSource(value: Union[ConfigMapNodeConfigSourceUnion, OmitEnum, None]) ->Union[ConfigMapNodeConfigSource, OmitEnum, None]:
    return ConfigMapNodeConfigSource(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapProjection(value: Union[ConfigMapProjectionUnion, OmitEnum, None]) ->Union[ConfigMapProjection, OmitEnum, None]:
    return ConfigMapProjection(**value) if isinstance(value, dict) else value


def optional_converter_ConfigMapVolumeSource(value: Union[ConfigMapVolumeSourceUnion, OmitEnum, None]) ->Union[ConfigMapVolumeSource, OmitEnum, None]:
    return ConfigMapVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ContainerImage(value: Union[ContainerImageUnion, OmitEnum, None]) ->Union[ContainerImage, OmitEnum, None]:
    return ContainerImage(**value) if isinstance(value, dict) else value


def optional_converter_ContainerItem(value: Union[ContainerItemUnion, OmitEnum, None]) ->Union[ContainerItem, OmitEnum, None]:
    return ContainerItem(**value) if isinstance(value, dict) else value


def optional_converter_ContainerPort(value: Union[ContainerPortUnion, OmitEnum, None]) ->Union[ContainerPort, OmitEnum, None]:
    return ContainerPort(**value) if isinstance(value, dict) else value


def optional_converter_ContainerPortItem(value: Union[ContainerPortItemUnion, OmitEnum, None]) ->Union[ContainerPortItem, OmitEnum, None]:
    return ContainerPortItem(**value) if isinstance(value, dict) else value


def optional_converter_ContainerState(value: Union[ContainerStateUnion, OmitEnum, None]) ->Union[ContainerState, OmitEnum, None]:
    return ContainerState(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStateRunning(value: Union[ContainerStateRunningUnion, OmitEnum, None]) ->Union[ContainerStateRunning, OmitEnum, None]:
    return ContainerStateRunning(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStateTerminated(value: Union[ContainerStateTerminatedUnion, OmitEnum, None]) ->Union[ContainerStateTerminated, OmitEnum, None]:
    return ContainerStateTerminated(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStateWaiting(value: Union[ContainerStateWaitingUnion, OmitEnum, None]) ->Union[ContainerStateWaiting, OmitEnum, None]:
    return ContainerStateWaiting(**value) if isinstance(value, dict) else value


def optional_converter_ContainerStatus(value: Union[ContainerStatusUnion, OmitEnum, None]) ->Union[ContainerStatus, OmitEnum, None]:
    return ContainerStatus(**value) if isinstance(value, dict) else value


def optional_converter_DaemonEndpoint(value: Union[DaemonEndpointUnion, OmitEnum, None]) ->Union[DaemonEndpoint, OmitEnum, None]:
    return DaemonEndpoint(**value) if isinstance(value, dict) else value


def optional_converter_DeleteOptions(value: Union[DeleteOptionsUnion, OmitEnum, None]) ->Union[DeleteOptions, OmitEnum, None]:
    return DeleteOptions(**value) if isinstance(value, dict) else value


def optional_converter_DownwardAPIProjection(value: Union[DownwardAPIProjectionUnion, OmitEnum, None]) ->Union[DownwardAPIProjection, OmitEnum, None]:
    return DownwardAPIProjection(**value) if isinstance(value, dict) else value


def optional_converter_DownwardAPIVolumeFile(value: Union[DownwardAPIVolumeFileUnion, OmitEnum, None]) ->Union[DownwardAPIVolumeFile, OmitEnum, None]:
    return DownwardAPIVolumeFile(**value) if isinstance(value, dict) else value


def optional_converter_DownwardAPIVolumeSource(value: Union[DownwardAPIVolumeSourceUnion, OmitEnum, None]) ->Union[DownwardAPIVolumeSource, OmitEnum, None]:
    return DownwardAPIVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_EmbeddedPersistentVolumeClaim(value: Union[EmbeddedPersistentVolumeClaimUnion, OmitEnum, None]) ->Union[EmbeddedPersistentVolumeClaim, OmitEnum, None]:
    return EmbeddedPersistentVolumeClaim(**value) if isinstance(value, dict) else value


def optional_converter_EmptyDirVolumeSource(value: Union[EmptyDirVolumeSourceUnion, OmitEnum, None]) ->Union[EmptyDirVolumeSource, OmitEnum, None]:
    return EmptyDirVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_EndpointAddress(value: Union[EndpointAddressUnion, OmitEnum, None]) ->Union[EndpointAddress, OmitEnum, None]:
    return EndpointAddress(**value) if isinstance(value, dict) else value


def optional_converter_EndpointPort(value: Union[EndpointPortUnion, OmitEnum, None]) ->Union[EndpointPort, OmitEnum, None]:
    return EndpointPort(**value) if isinstance(value, dict) else value


def optional_converter_EndpointSubset(value: Union[EndpointSubsetUnion, OmitEnum, None]) ->Union[EndpointSubset, OmitEnum, None]:
    return EndpointSubset(**value) if isinstance(value, dict) else value


def optional_converter_EnvFromSource(value: Union[EnvFromSourceUnion, OmitEnum, None]) ->Union[EnvFromSource, OmitEnum, None]:
    return EnvFromSource(**value) if isinstance(value, dict) else value


def optional_converter_EnvVarItem(value: Union[EnvVarItemUnion, OmitEnum, None]) ->Union[EnvVarItem, OmitEnum, None]:
    return EnvVarItem(**value) if isinstance(value, dict) else value


def optional_converter_EnvVarSource(value: Union[EnvVarSourceUnion, OmitEnum, None]) ->Union[EnvVarSource, OmitEnum, None]:
    return EnvVarSource(**value) if isinstance(value, dict) else value


def optional_converter_EphemeralContainerItem(value: Union[EphemeralContainerItemUnion, OmitEnum, None]) ->Union[EphemeralContainerItem, OmitEnum, None]:
    return EphemeralContainerItem(**value) if isinstance(value, dict) else value


def optional_converter_EphemeralVolumeSource(value: Union[EphemeralVolumeSourceUnion, OmitEnum, None]) ->Union[EphemeralVolumeSource, OmitEnum, None]:
    return EphemeralVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_EventSeries(value: Union[EventSeriesUnion, OmitEnum, None]) ->Union[EventSeries, OmitEnum, None]:
    return EventSeries(**value) if isinstance(value, dict) else value


def optional_converter_EventSource(value: Union[EventSourceUnion, OmitEnum, None]) ->Union[EventSource, OmitEnum, None]:
    return EventSource(**value) if isinstance(value, dict) else value


def optional_converter_ExecAction(value: Union[ExecActionUnion, OmitEnum, None]) ->Union[ExecAction, OmitEnum, None]:
    return ExecAction(**value) if isinstance(value, dict) else value


def optional_converter_FCVolumeSource(value: Union[FCVolumeSourceUnion, OmitEnum, None]) ->Union[FCVolumeSource, OmitEnum, None]:
    return FCVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_FlexPersistentVolumeSource(value: Union[FlexPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[FlexPersistentVolumeSource, OmitEnum, None]:
    return FlexPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_FlexVolumeSource(value: Union[FlexVolumeSourceUnion, OmitEnum, None]) ->Union[FlexVolumeSource, OmitEnum, None]:
    return FlexVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_FlockerVolumeSource(value: Union[FlockerVolumeSourceUnion, OmitEnum, None]) ->Union[FlockerVolumeSource, OmitEnum, None]:
    return FlockerVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_GCEPersistentDiskVolumeSource(value: Union[GCEPersistentDiskVolumeSourceUnion, OmitEnum, None]) ->Union[GCEPersistentDiskVolumeSource, OmitEnum, None]:
    return GCEPersistentDiskVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_GitRepoVolumeSource(value: Union[GitRepoVolumeSourceUnion, OmitEnum, None]) ->Union[GitRepoVolumeSource, OmitEnum, None]:
    return GitRepoVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_GlusterfsPersistentVolumeSource(value: Union[GlusterfsPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[GlusterfsPersistentVolumeSource, OmitEnum, None]:
    return GlusterfsPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_GlusterfsVolumeSource(value: Union[GlusterfsVolumeSourceUnion, OmitEnum, None]) ->Union[GlusterfsVolumeSource, OmitEnum, None]:
    return GlusterfsVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_HTTPGetAction(value: Union[HTTPGetActionUnion, OmitEnum, None]) ->Union[HTTPGetAction, OmitEnum, None]:
    return HTTPGetAction(**value) if isinstance(value, dict) else value


def optional_converter_HTTPHeader(value: Union[HTTPHeaderUnion, OmitEnum, None]) ->Union[HTTPHeader, OmitEnum, None]:
    return HTTPHeader(**value) if isinstance(value, dict) else value


def optional_converter_Handler(value: Union[HandlerUnion, OmitEnum, None]) ->Union[Handler, OmitEnum, None]:
    return Handler(**value) if isinstance(value, dict) else value


def optional_converter_HostAliasItem(value: Union[HostAliasItemUnion, OmitEnum, None]) ->Union[HostAliasItem, OmitEnum, None]:
    return HostAliasItem(**value) if isinstance(value, dict) else value


def optional_converter_HostPathVolumeSource(value: Union[HostPathVolumeSourceUnion, OmitEnum, None]) ->Union[HostPathVolumeSource, OmitEnum, None]:
    return HostPathVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ISCSIPersistentVolumeSource(value: Union[ISCSIPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[ISCSIPersistentVolumeSource, OmitEnum, None]:
    return ISCSIPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ISCSIVolumeSource(value: Union[ISCSIVolumeSourceUnion, OmitEnum, None]) ->Union[ISCSIVolumeSource, OmitEnum, None]:
    return ISCSIVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_KeyToPath(value: Union[KeyToPathUnion, OmitEnum, None]) ->Union[KeyToPath, OmitEnum, None]:
    return KeyToPath(**value) if isinstance(value, dict) else value


def optional_converter_LabelSelector(value: Union[LabelSelectorUnion, OmitEnum, None]) ->Union[LabelSelector, OmitEnum, None]:
    return LabelSelector(**value) if isinstance(value, dict) else value


def optional_converter_LabelSelectorRequirement(value: Union[LabelSelectorRequirementUnion, OmitEnum, None]) ->Union[LabelSelectorRequirement, OmitEnum, None]:
    return LabelSelectorRequirement(**value) if isinstance(value, dict) else value


def optional_converter_Lifecycle(value: Union[LifecycleUnion, OmitEnum, None]) ->Union[Lifecycle, OmitEnum, None]:
    return Lifecycle(**value) if isinstance(value, dict) else value


def optional_converter_LimitRangeItem(value: Union[LimitRangeItemUnion, OmitEnum, None]) ->Union[LimitRangeItem, OmitEnum, None]:
    return LimitRangeItem(**value) if isinstance(value, dict) else value


def optional_converter_LimitRangeSpec(value: Union[LimitRangeSpecUnion, OmitEnum, None]) ->Union[LimitRangeSpec, OmitEnum, None]:
    return LimitRangeSpec(**value) if isinstance(value, dict) else value


def optional_converter_LoadBalancerIngress(value: Union[LoadBalancerIngressUnion, OmitEnum, None]) ->Union[LoadBalancerIngress, OmitEnum, None]:
    return LoadBalancerIngress(**value) if isinstance(value, dict) else value


def optional_converter_LoadBalancerStatus(value: Union[LoadBalancerStatusUnion, OmitEnum, None]) ->Union[LoadBalancerStatus, OmitEnum, None]:
    return LoadBalancerStatus(**value) if isinstance(value, dict) else value


def optional_converter_LocalObjectReference(value: Union[LocalObjectReferenceUnion, OmitEnum, None]) ->Union[LocalObjectReference, OmitEnum, None]:
    return LocalObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_LocalVolumeSource(value: Union[LocalVolumeSourceUnion, OmitEnum, None]) ->Union[LocalVolumeSource, OmitEnum, None]:
    return LocalVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ManagedFieldsEntry(value: Union[ManagedFieldsEntryUnion, OmitEnum, None]) ->Union[ManagedFieldsEntry, OmitEnum, None]:
    return ManagedFieldsEntry(**value) if isinstance(value, dict) else value


def optional_converter_NFSVolumeSource(value: Union[NFSVolumeSourceUnion, OmitEnum, None]) ->Union[NFSVolumeSource, OmitEnum, None]:
    return NFSVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_NamespaceConditionItem(value: Union[NamespaceConditionItemUnion, OmitEnum, None]) ->Union[NamespaceConditionItem, OmitEnum, None]:
    return NamespaceConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_NamespaceSpec(value: Union[NamespaceSpecUnion, OmitEnum, None]) ->Union[NamespaceSpec, OmitEnum, None]:
    return NamespaceSpec(**value) if isinstance(value, dict) else value


def optional_converter_NamespaceStatus(value: Union[NamespaceStatusUnion, OmitEnum, None]) ->Union[NamespaceStatus, OmitEnum, None]:
    return NamespaceStatus(**value) if isinstance(value, dict) else value


def optional_converter_NodeAddressItem(value: Union[NodeAddressItemUnion, OmitEnum, None]) ->Union[NodeAddressItem, OmitEnum, None]:
    return NodeAddressItem(**value) if isinstance(value, dict) else value


def optional_converter_NodeAffinity(value: Union[NodeAffinityUnion, OmitEnum, None]) ->Union[NodeAffinity, OmitEnum, None]:
    return NodeAffinity(**value) if isinstance(value, dict) else value


def optional_converter_NodeConditionItem(value: Union[NodeConditionItemUnion, OmitEnum, None]) ->Union[NodeConditionItem, OmitEnum, None]:
    return NodeConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_NodeConfigSource(value: Union[NodeConfigSourceUnion, OmitEnum, None]) ->Union[NodeConfigSource, OmitEnum, None]:
    return NodeConfigSource(**value) if isinstance(value, dict) else value


def optional_converter_NodeConfigStatus(value: Union[NodeConfigStatusUnion, OmitEnum, None]) ->Union[NodeConfigStatus, OmitEnum, None]:
    return NodeConfigStatus(**value) if isinstance(value, dict) else value


def optional_converter_NodeDaemonEndpoints(value: Union[NodeDaemonEndpointsUnion, OmitEnum, None]) ->Union[NodeDaemonEndpoints, OmitEnum, None]:
    return NodeDaemonEndpoints(**value) if isinstance(value, dict) else value


def optional_converter_NodeSelector(value: Union[NodeSelectorUnion, OmitEnum, None]) ->Union[NodeSelector, OmitEnum, None]:
    return NodeSelector(**value) if isinstance(value, dict) else value


def optional_converter_NodeSelectorRequirement(value: Union[NodeSelectorRequirementUnion, OmitEnum, None]) ->Union[NodeSelectorRequirement, OmitEnum, None]:
    return NodeSelectorRequirement(**value) if isinstance(value, dict) else value


def optional_converter_NodeSelectorTerm(value: Union[NodeSelectorTermUnion, OmitEnum, None]) ->Union[NodeSelectorTerm, OmitEnum, None]:
    return NodeSelectorTerm(**value) if isinstance(value, dict) else value


def optional_converter_NodeSpec(value: Union[NodeSpecUnion, OmitEnum, None]) ->Union[NodeSpec, OmitEnum, None]:
    return NodeSpec(**value) if isinstance(value, dict) else value


def optional_converter_NodeStatus(value: Union[NodeStatusUnion, OmitEnum, None]) ->Union[NodeStatus, OmitEnum, None]:
    return NodeStatus(**value) if isinstance(value, dict) else value


def optional_converter_NodeSystemInfo(value: Union[NodeSystemInfoUnion, OmitEnum, None]) ->Union[NodeSystemInfo, OmitEnum, None]:
    return NodeSystemInfo(**value) if isinstance(value, dict) else value


def optional_converter_ObjectFieldSelector(value: Union[ObjectFieldSelectorUnion, OmitEnum, None]) ->Union[ObjectFieldSelector, OmitEnum, None]:
    return ObjectFieldSelector(**value) if isinstance(value, dict) else value


def optional_converter_ObjectMeta(value: Union[ObjectMetaUnion, OmitEnum, None]) ->Union[ObjectMeta, OmitEnum, None]:
    return ObjectMeta(**value) if isinstance(value, dict) else value


def optional_converter_ObjectReference(value: Union[ObjectReferenceUnion, OmitEnum, None]) ->Union[ObjectReference, OmitEnum, None]:
    return ObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_ObjectReferenceItem(value: Union[ObjectReferenceItemUnion, OmitEnum, None]) ->Union[ObjectReferenceItem, OmitEnum, None]:
    return ObjectReferenceItem(**value) if isinstance(value, dict) else value


def optional_converter_OwnerReferenceItem(value: Union[OwnerReferenceItemUnion, OmitEnum, None]) ->Union[OwnerReferenceItem, OmitEnum, None]:
    return OwnerReferenceItem(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimConditionItem(value: Union[PersistentVolumeClaimConditionItemUnion, OmitEnum, None]) ->Union[PersistentVolumeClaimConditionItem, OmitEnum, None]:
    return PersistentVolumeClaimConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimSpec(value: Union[PersistentVolumeClaimSpecUnion, OmitEnum, None]) ->Union[PersistentVolumeClaimSpec, OmitEnum, None]:
    return PersistentVolumeClaimSpec(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimStatus(value: Union[PersistentVolumeClaimStatusUnion, OmitEnum, None]) ->Union[PersistentVolumeClaimStatus, OmitEnum, None]:
    return PersistentVolumeClaimStatus(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimTemplate(value: Union[PersistentVolumeClaimTemplateUnion, OmitEnum, None]) ->Union[PersistentVolumeClaimTemplate, OmitEnum, None]:
    return PersistentVolumeClaimTemplate(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeClaimVolumeSource(value: Union[PersistentVolumeClaimVolumeSourceUnion, OmitEnum, None]) ->Union[PersistentVolumeClaimVolumeSource, OmitEnum, None]:
    return PersistentVolumeClaimVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeSpec(value: Union[PersistentVolumeSpecUnion, OmitEnum, None]) ->Union[PersistentVolumeSpec, OmitEnum, None]:
    return PersistentVolumeSpec(**value) if isinstance(value, dict) else value


def optional_converter_PersistentVolumeStatus(value: Union[PersistentVolumeStatusUnion, OmitEnum, None]) ->Union[PersistentVolumeStatus, OmitEnum, None]:
    return PersistentVolumeStatus(**value) if isinstance(value, dict) else value


def optional_converter_PhotonPersistentDiskVolumeSource(value: Union[PhotonPersistentDiskVolumeSourceUnion, OmitEnum, None]) ->Union[PhotonPersistentDiskVolumeSource, OmitEnum, None]:
    return PhotonPersistentDiskVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_PodAffinity(value: Union[PodAffinityUnion, OmitEnum, None]) ->Union[PodAffinity, OmitEnum, None]:
    return PodAffinity(**value) if isinstance(value, dict) else value


def optional_converter_PodAffinityTerm(value: Union[PodAffinityTermUnion, OmitEnum, None]) ->Union[PodAffinityTerm, OmitEnum, None]:
    return PodAffinityTerm(**value) if isinstance(value, dict) else value


def optional_converter_PodAntiAffinity(value: Union[PodAntiAffinityUnion, OmitEnum, None]) ->Union[PodAntiAffinity, OmitEnum, None]:
    return PodAntiAffinity(**value) if isinstance(value, dict) else value


def optional_converter_PodConditionItem(value: Union[PodConditionItemUnion, OmitEnum, None]) ->Union[PodConditionItem, OmitEnum, None]:
    return PodConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_PodDNSConfig(value: Union[PodDNSConfigUnion, OmitEnum, None]) ->Union[PodDNSConfig, OmitEnum, None]:
    return PodDNSConfig(**value) if isinstance(value, dict) else value


def optional_converter_PodDNSConfigOption(value: Union[PodDNSConfigOptionUnion, OmitEnum, None]) ->Union[PodDNSConfigOption, OmitEnum, None]:
    return PodDNSConfigOption(**value) if isinstance(value, dict) else value


def optional_converter_PodIP(value: Union[PodIPUnion, OmitEnum, None]) ->Union[PodIP, OmitEnum, None]:
    return PodIP(**value) if isinstance(value, dict) else value


def optional_converter_PodReadinessGate(value: Union[PodReadinessGateUnion, OmitEnum, None]) ->Union[PodReadinessGate, OmitEnum, None]:
    return PodReadinessGate(**value) if isinstance(value, dict) else value


def optional_converter_PodSecurityContext(value: Union[PodSecurityContextUnion, OmitEnum, None]) ->Union[PodSecurityContext, OmitEnum, None]:
    return PodSecurityContext(**value) if isinstance(value, dict) else value


def optional_converter_PodSpec(value: Union[PodSpecUnion, OmitEnum, None]) ->Union[PodSpec, OmitEnum, None]:
    return PodSpec(**value) if isinstance(value, dict) else value


def optional_converter_PodStatus(value: Union[PodStatusUnion, OmitEnum, None]) ->Union[PodStatus, OmitEnum, None]:
    return PodStatus(**value) if isinstance(value, dict) else value


def optional_converter_PodTemplateSpec(value: Union[PodTemplateSpecUnion, OmitEnum, None]) ->Union[PodTemplateSpec, OmitEnum, None]:
    return PodTemplateSpec(**value) if isinstance(value, dict) else value


def optional_converter_PortStatus(value: Union[PortStatusUnion, OmitEnum, None]) ->Union[PortStatus, OmitEnum, None]:
    return PortStatus(**value) if isinstance(value, dict) else value


def optional_converter_PortworxVolumeSource(value: Union[PortworxVolumeSourceUnion, OmitEnum, None]) ->Union[PortworxVolumeSource, OmitEnum, None]:
    return PortworxVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_Preconditions(value: Union[PreconditionsUnion, OmitEnum, None]) ->Union[Preconditions, OmitEnum, None]:
    return Preconditions(**value) if isinstance(value, dict) else value


def optional_converter_PreferredSchedulingTerm(value: Union[PreferredSchedulingTermUnion, OmitEnum, None]) ->Union[PreferredSchedulingTerm, OmitEnum, None]:
    return PreferredSchedulingTerm(**value) if isinstance(value, dict) else value


def optional_converter_Probe(value: Union[ProbeUnion, OmitEnum, None]) ->Union[Probe, OmitEnum, None]:
    return Probe(**value) if isinstance(value, dict) else value


def optional_converter_ProjectedVolumeSource(value: Union[ProjectedVolumeSourceUnion, OmitEnum, None]) ->Union[ProjectedVolumeSource, OmitEnum, None]:
    return ProjectedVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_QuobyteVolumeSource(value: Union[QuobyteVolumeSourceUnion, OmitEnum, None]) ->Union[QuobyteVolumeSource, OmitEnum, None]:
    return QuobyteVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_RBDPersistentVolumeSource(value: Union[RBDPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[RBDPersistentVolumeSource, OmitEnum, None]:
    return RBDPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_RBDVolumeSource(value: Union[RBDVolumeSourceUnion, OmitEnum, None]) ->Union[RBDVolumeSource, OmitEnum, None]:
    return RBDVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ReplicationControllerConditionItem(value: Union[ReplicationControllerConditionItemUnion, OmitEnum, None]) ->Union[ReplicationControllerConditionItem, OmitEnum, None]:
    return ReplicationControllerConditionItem(**value) if isinstance(value, dict) else value


def optional_converter_ReplicationControllerSpec(value: Union[ReplicationControllerSpecUnion, OmitEnum, None]) ->Union[ReplicationControllerSpec, OmitEnum, None]:
    return ReplicationControllerSpec(**value) if isinstance(value, dict) else value


def optional_converter_ReplicationControllerStatus(value: Union[ReplicationControllerStatusUnion, OmitEnum, None]) ->Union[ReplicationControllerStatus, OmitEnum, None]:
    return ReplicationControllerStatus(**value) if isinstance(value, dict) else value


def optional_converter_ResourceFieldSelector(value: Union[ResourceFieldSelectorUnion, OmitEnum, None]) ->Union[ResourceFieldSelector, OmitEnum, None]:
    return ResourceFieldSelector(**value) if isinstance(value, dict) else value


def optional_converter_ResourceQuotaSpec(value: Union[ResourceQuotaSpecUnion, OmitEnum, None]) ->Union[ResourceQuotaSpec, OmitEnum, None]:
    return ResourceQuotaSpec(**value) if isinstance(value, dict) else value


def optional_converter_ResourceQuotaStatus(value: Union[ResourceQuotaStatusUnion, OmitEnum, None]) ->Union[ResourceQuotaStatus, OmitEnum, None]:
    return ResourceQuotaStatus(**value) if isinstance(value, dict) else value


def optional_converter_ResourceRequirements(value: Union[ResourceRequirementsUnion, OmitEnum, None]) ->Union[ResourceRequirements, OmitEnum, None]:
    return ResourceRequirements(**value) if isinstance(value, dict) else value


def optional_converter_SELinuxOptions(value: Union[SELinuxOptionsUnion, OmitEnum, None]) ->Union[SELinuxOptions, OmitEnum, None]:
    return SELinuxOptions(**value) if isinstance(value, dict) else value


def optional_converter_ScaleIOPersistentVolumeSource(value: Union[ScaleIOPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[ScaleIOPersistentVolumeSource, OmitEnum, None]:
    return ScaleIOPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ScaleIOVolumeSource(value: Union[ScaleIOVolumeSourceUnion, OmitEnum, None]) ->Union[ScaleIOVolumeSource, OmitEnum, None]:
    return ScaleIOVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_ScopeSelector(value: Union[ScopeSelectorUnion, OmitEnum, None]) ->Union[ScopeSelector, OmitEnum, None]:
    return ScopeSelector(**value) if isinstance(value, dict) else value


def optional_converter_ScopedResourceSelectorRequirement(value: Union[ScopedResourceSelectorRequirementUnion, OmitEnum, None]) ->Union[ScopedResourceSelectorRequirement, OmitEnum, None]:
    return ScopedResourceSelectorRequirement(**value) if isinstance(value, dict) else value


def optional_converter_SeccompProfile(value: Union[SeccompProfileUnion, OmitEnum, None]) ->Union[SeccompProfile, OmitEnum, None]:
    return SeccompProfile(**value) if isinstance(value, dict) else value


def optional_converter_SecretEnvSource(value: Union[SecretEnvSourceUnion, OmitEnum, None]) ->Union[SecretEnvSource, OmitEnum, None]:
    return SecretEnvSource(**value) if isinstance(value, dict) else value


def optional_converter_SecretKeySelector(value: Union[SecretKeySelectorUnion, OmitEnum, None]) ->Union[SecretKeySelector, OmitEnum, None]:
    return SecretKeySelector(**value) if isinstance(value, dict) else value


def optional_converter_SecretProjection(value: Union[SecretProjectionUnion, OmitEnum, None]) ->Union[SecretProjection, OmitEnum, None]:
    return SecretProjection(**value) if isinstance(value, dict) else value


def optional_converter_SecretReference(value: Union[SecretReferenceUnion, OmitEnum, None]) ->Union[SecretReference, OmitEnum, None]:
    return SecretReference(**value) if isinstance(value, dict) else value


def optional_converter_SecretVolumeSource(value: Union[SecretVolumeSourceUnion, OmitEnum, None]) ->Union[SecretVolumeSource, OmitEnum, None]:
    return SecretVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_SecurityContext(value: Union[SecurityContextUnion, OmitEnum, None]) ->Union[SecurityContext, OmitEnum, None]:
    return SecurityContext(**value) if isinstance(value, dict) else value


def optional_converter_ServiceAccountTokenProjection(value: Union[ServiceAccountTokenProjectionUnion, OmitEnum, None]) ->Union[ServiceAccountTokenProjection, OmitEnum, None]:
    return ServiceAccountTokenProjection(**value) if isinstance(value, dict) else value


def optional_converter_ServicePortItem(value: Union[ServicePortItemUnion, OmitEnum, None]) ->Union[ServicePortItem, OmitEnum, None]:
    return ServicePortItem(**value) if isinstance(value, dict) else value


def optional_converter_ServiceSpec(value: Union[ServiceSpecUnion, OmitEnum, None]) ->Union[ServiceSpec, OmitEnum, None]:
    return ServiceSpec(**value) if isinstance(value, dict) else value


def optional_converter_ServiceStatus(value: Union[ServiceStatusUnion, OmitEnum, None]) ->Union[ServiceStatus, OmitEnum, None]:
    return ServiceStatus(**value) if isinstance(value, dict) else value


def optional_converter_SessionAffinityConfig(value: Union[SessionAffinityConfigUnion, OmitEnum, None]) ->Union[SessionAffinityConfig, OmitEnum, None]:
    return SessionAffinityConfig(**value) if isinstance(value, dict) else value


def optional_converter_StorageOSPersistentVolumeSource(value: Union[StorageOSPersistentVolumeSourceUnion, OmitEnum, None]) ->Union[StorageOSPersistentVolumeSource, OmitEnum, None]:
    return StorageOSPersistentVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_StorageOSVolumeSource(value: Union[StorageOSVolumeSourceUnion, OmitEnum, None]) ->Union[StorageOSVolumeSource, OmitEnum, None]:
    return StorageOSVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_Sysctl(value: Union[SysctlUnion, OmitEnum, None]) ->Union[Sysctl, OmitEnum, None]:
    return Sysctl(**value) if isinstance(value, dict) else value


def optional_converter_TCPSocketAction(value: Union[TCPSocketActionUnion, OmitEnum, None]) ->Union[TCPSocketAction, OmitEnum, None]:
    return TCPSocketAction(**value) if isinstance(value, dict) else value


def optional_converter_Taint(value: Union[TaintUnion, OmitEnum, None]) ->Union[Taint, OmitEnum, None]:
    return Taint(**value) if isinstance(value, dict) else value


def optional_converter_Toleration(value: Union[TolerationUnion, OmitEnum, None]) ->Union[Toleration, OmitEnum, None]:
    return Toleration(**value) if isinstance(value, dict) else value


def optional_converter_TopologySelectorLabelRequirement(value: Union[TopologySelectorLabelRequirementUnion, OmitEnum, None]) ->Union[TopologySelectorLabelRequirement, OmitEnum, None]:
    return TopologySelectorLabelRequirement(**value) if isinstance(value, dict) else value


def optional_converter_TopologySelectorTerm(value: Union[TopologySelectorTermUnion, OmitEnum, None]) ->Union[TopologySelectorTerm, OmitEnum, None]:
    return TopologySelectorTerm(**value) if isinstance(value, dict) else value


def optional_converter_TopologySpreadConstraintItem(value: Union[TopologySpreadConstraintItemUnion, OmitEnum, None]) ->Union[TopologySpreadConstraintItem, OmitEnum, None]:
    return TopologySpreadConstraintItem(**value) if isinstance(value, dict) else value


def optional_converter_TypedLocalObjectReference(value: Union[TypedLocalObjectReferenceUnion, OmitEnum, None]) ->Union[TypedLocalObjectReference, OmitEnum, None]:
    return TypedLocalObjectReference(**value) if isinstance(value, dict) else value


def optional_converter_VolumeDeviceItem(value: Union[VolumeDeviceItemUnion, OmitEnum, None]) ->Union[VolumeDeviceItem, OmitEnum, None]:
    return VolumeDeviceItem(**value) if isinstance(value, dict) else value


def optional_converter_VolumeItem(value: Union[VolumeItemUnion, OmitEnum, None]) ->Union[VolumeItem, OmitEnum, None]:
    return VolumeItem(**value) if isinstance(value, dict) else value


def optional_converter_VolumeMountItem(value: Union[VolumeMountItemUnion, OmitEnum, None]) ->Union[VolumeMountItem, OmitEnum, None]:
    return VolumeMountItem(**value) if isinstance(value, dict) else value


def optional_converter_VolumeNodeAffinity(value: Union[VolumeNodeAffinityUnion, OmitEnum, None]) ->Union[VolumeNodeAffinity, OmitEnum, None]:
    return VolumeNodeAffinity(**value) if isinstance(value, dict) else value


def optional_converter_VolumeProjection(value: Union[VolumeProjectionUnion, OmitEnum, None]) ->Union[VolumeProjection, OmitEnum, None]:
    return VolumeProjection(**value) if isinstance(value, dict) else value


def optional_converter_VsphereVirtualDiskVolumeSource(value: Union[VsphereVirtualDiskVolumeSourceUnion, OmitEnum, None]) ->Union[VsphereVirtualDiskVolumeSource, OmitEnum, None]:
    return VsphereVirtualDiskVolumeSource(**value) if isinstance(value, dict) else value


def optional_converter_WeightedPodAffinityTerm(value: Union[WeightedPodAffinityTermUnion, OmitEnum, None]) ->Union[WeightedPodAffinityTerm, OmitEnum, None]:
    return WeightedPodAffinityTerm(**value) if isinstance(value, dict) else value


def optional_converter_WindowsSecurityContextOptions(value: Union[WindowsSecurityContextOptionsUnion, OmitEnum, None]) ->Union[WindowsSecurityContextOptions, OmitEnum, None]:
    return WindowsSecurityContextOptions(**value) if isinstance(value, dict) else value


def required_converter_AWSElasticBlockStoreVolumeSource(value: AWSElasticBlockStoreVolumeSourceUnion) ->AWSElasticBlockStoreVolumeSource:
    return AWSElasticBlockStoreVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_Affinity(value: AffinityUnion) ->Affinity:
    return Affinity(**value) if isinstance(value, dict) else value


def required_converter_AttachedVolume(value: AttachedVolumeUnion) ->AttachedVolume:
    return AttachedVolume(**value) if isinstance(value, dict) else value


def required_converter_AzureDiskVolumeSource(value: AzureDiskVolumeSourceUnion) ->AzureDiskVolumeSource:
    return AzureDiskVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_AzureFilePersistentVolumeSource(value: AzureFilePersistentVolumeSourceUnion) ->AzureFilePersistentVolumeSource:
    return AzureFilePersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_AzureFileVolumeSource(value: AzureFileVolumeSourceUnion) ->AzureFileVolumeSource:
    return AzureFileVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CSIPersistentVolumeSource(value: CSIPersistentVolumeSourceUnion) ->CSIPersistentVolumeSource:
    return CSIPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CSIVolumeSource(value: CSIVolumeSourceUnion) ->CSIVolumeSource:
    return CSIVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_Capabilities(value: CapabilitiesUnion) ->Capabilities:
    return Capabilities(**value) if isinstance(value, dict) else value


def required_converter_CephFSPersistentVolumeSource(value: CephFSPersistentVolumeSourceUnion) ->CephFSPersistentVolumeSource:
    return CephFSPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CephFSVolumeSource(value: CephFSVolumeSourceUnion) ->CephFSVolumeSource:
    return CephFSVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CinderPersistentVolumeSource(value: CinderPersistentVolumeSourceUnion) ->CinderPersistentVolumeSource:
    return CinderPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_CinderVolumeSource(value: CinderVolumeSourceUnion) ->CinderVolumeSource:
    return CinderVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ClientIPConfig(value: ClientIPConfigUnion) ->ClientIPConfig:
    return ClientIPConfig(**value) if isinstance(value, dict) else value


def required_converter_ConditionItem(value: ConditionItemUnion) ->ConditionItem:
    return ConditionItem(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapEnvSource(value: ConfigMapEnvSourceUnion) ->ConfigMapEnvSource:
    return ConfigMapEnvSource(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapKeySelector(value: ConfigMapKeySelectorUnion) ->ConfigMapKeySelector:
    return ConfigMapKeySelector(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapNodeConfigSource(value: ConfigMapNodeConfigSourceUnion) ->ConfigMapNodeConfigSource:
    return ConfigMapNodeConfigSource(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapProjection(value: ConfigMapProjectionUnion) ->ConfigMapProjection:
    return ConfigMapProjection(**value) if isinstance(value, dict) else value


def required_converter_ConfigMapVolumeSource(value: ConfigMapVolumeSourceUnion) ->ConfigMapVolumeSource:
    return ConfigMapVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ContainerImage(value: ContainerImageUnion) ->ContainerImage:
    return ContainerImage(**value) if isinstance(value, dict) else value


def required_converter_ContainerItem(value: ContainerItemUnion) ->ContainerItem:
    return ContainerItem(**value) if isinstance(value, dict) else value


def required_converter_ContainerPort(value: ContainerPortUnion) ->ContainerPort:
    return ContainerPort(**value) if isinstance(value, dict) else value


def required_converter_ContainerPortItem(value: ContainerPortItemUnion) ->ContainerPortItem:
    return ContainerPortItem(**value) if isinstance(value, dict) else value


def required_converter_ContainerState(value: ContainerStateUnion) ->ContainerState:
    return ContainerState(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateRunning(value: ContainerStateRunningUnion) ->ContainerStateRunning:
    return ContainerStateRunning(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateTerminated(value: ContainerStateTerminatedUnion) ->ContainerStateTerminated:
    return ContainerStateTerminated(**value) if isinstance(value, dict) else value


def required_converter_ContainerStateWaiting(value: ContainerStateWaitingUnion) ->ContainerStateWaiting:
    return ContainerStateWaiting(**value) if isinstance(value, dict) else value


def required_converter_ContainerStatus(value: ContainerStatusUnion) ->ContainerStatus:
    return ContainerStatus(**value) if isinstance(value, dict) else value


def required_converter_DaemonEndpoint(value: DaemonEndpointUnion) ->DaemonEndpoint:
    return DaemonEndpoint(**value) if isinstance(value, dict) else value


def required_converter_DeleteOptions(value: DeleteOptionsUnion) ->DeleteOptions:
    return DeleteOptions(**value) if isinstance(value, dict) else value


def required_converter_DownwardAPIProjection(value: DownwardAPIProjectionUnion) ->DownwardAPIProjection:
    return DownwardAPIProjection(**value) if isinstance(value, dict) else value


def required_converter_DownwardAPIVolumeFile(value: DownwardAPIVolumeFileUnion) ->DownwardAPIVolumeFile:
    return DownwardAPIVolumeFile(**value) if isinstance(value, dict) else value


def required_converter_DownwardAPIVolumeSource(value: DownwardAPIVolumeSourceUnion) ->DownwardAPIVolumeSource:
    return DownwardAPIVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_EmbeddedPersistentVolumeClaim(value: EmbeddedPersistentVolumeClaimUnion) ->EmbeddedPersistentVolumeClaim:
    return EmbeddedPersistentVolumeClaim(**value) if isinstance(value, dict) else value


def required_converter_EmptyDirVolumeSource(value: EmptyDirVolumeSourceUnion) ->EmptyDirVolumeSource:
    return EmptyDirVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_EndpointAddress(value: EndpointAddressUnion) ->EndpointAddress:
    return EndpointAddress(**value) if isinstance(value, dict) else value


def required_converter_EndpointPort(value: EndpointPortUnion) ->EndpointPort:
    return EndpointPort(**value) if isinstance(value, dict) else value


def required_converter_EndpointSubset(value: EndpointSubsetUnion) ->EndpointSubset:
    return EndpointSubset(**value) if isinstance(value, dict) else value


def required_converter_EnvFromSource(value: EnvFromSourceUnion) ->EnvFromSource:
    return EnvFromSource(**value) if isinstance(value, dict) else value


def required_converter_EnvVarItem(value: EnvVarItemUnion) ->EnvVarItem:
    return EnvVarItem(**value) if isinstance(value, dict) else value


def required_converter_EnvVarSource(value: EnvVarSourceUnion) ->EnvVarSource:
    return EnvVarSource(**value) if isinstance(value, dict) else value


def required_converter_EphemeralContainerItem(value: EphemeralContainerItemUnion) ->EphemeralContainerItem:
    return EphemeralContainerItem(**value) if isinstance(value, dict) else value


def required_converter_EphemeralVolumeSource(value: EphemeralVolumeSourceUnion) ->EphemeralVolumeSource:
    return EphemeralVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_EventSeries(value: EventSeriesUnion) ->EventSeries:
    return EventSeries(**value) if isinstance(value, dict) else value


def required_converter_EventSource(value: EventSourceUnion) ->EventSource:
    return EventSource(**value) if isinstance(value, dict) else value


def required_converter_ExecAction(value: ExecActionUnion) ->ExecAction:
    return ExecAction(**value) if isinstance(value, dict) else value


def required_converter_FCVolumeSource(value: FCVolumeSourceUnion) ->FCVolumeSource:
    return FCVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_FlexPersistentVolumeSource(value: FlexPersistentVolumeSourceUnion) ->FlexPersistentVolumeSource:
    return FlexPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_FlexVolumeSource(value: FlexVolumeSourceUnion) ->FlexVolumeSource:
    return FlexVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_FlockerVolumeSource(value: FlockerVolumeSourceUnion) ->FlockerVolumeSource:
    return FlockerVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_GCEPersistentDiskVolumeSource(value: GCEPersistentDiskVolumeSourceUnion) ->GCEPersistentDiskVolumeSource:
    return GCEPersistentDiskVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_GitRepoVolumeSource(value: GitRepoVolumeSourceUnion) ->GitRepoVolumeSource:
    return GitRepoVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_GlusterfsPersistentVolumeSource(value: GlusterfsPersistentVolumeSourceUnion) ->GlusterfsPersistentVolumeSource:
    return GlusterfsPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_GlusterfsVolumeSource(value: GlusterfsVolumeSourceUnion) ->GlusterfsVolumeSource:
    return GlusterfsVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_HTTPGetAction(value: HTTPGetActionUnion) ->HTTPGetAction:
    return HTTPGetAction(**value) if isinstance(value, dict) else value


def required_converter_HTTPHeader(value: HTTPHeaderUnion) ->HTTPHeader:
    return HTTPHeader(**value) if isinstance(value, dict) else value


def required_converter_Handler(value: HandlerUnion) ->Handler:
    return Handler(**value) if isinstance(value, dict) else value


def required_converter_HostAliasItem(value: HostAliasItemUnion) ->HostAliasItem:
    return HostAliasItem(**value) if isinstance(value, dict) else value


def required_converter_HostPathVolumeSource(value: HostPathVolumeSourceUnion) ->HostPathVolumeSource:
    return HostPathVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ISCSIPersistentVolumeSource(value: ISCSIPersistentVolumeSourceUnion) ->ISCSIPersistentVolumeSource:
    return ISCSIPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ISCSIVolumeSource(value: ISCSIVolumeSourceUnion) ->ISCSIVolumeSource:
    return ISCSIVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_KeyToPath(value: KeyToPathUnion) ->KeyToPath:
    return KeyToPath(**value) if isinstance(value, dict) else value


def required_converter_LabelSelector(value: LabelSelectorUnion) ->LabelSelector:
    return LabelSelector(**value) if isinstance(value, dict) else value


def required_converter_LabelSelectorRequirement(value: LabelSelectorRequirementUnion) ->LabelSelectorRequirement:
    return LabelSelectorRequirement(**value) if isinstance(value, dict) else value


def required_converter_Lifecycle(value: LifecycleUnion) ->Lifecycle:
    return Lifecycle(**value) if isinstance(value, dict) else value


def required_converter_LimitRangeItem(value: LimitRangeItemUnion) ->LimitRangeItem:
    return LimitRangeItem(**value) if isinstance(value, dict) else value


def required_converter_LimitRangeSpec(value: LimitRangeSpecUnion) ->LimitRangeSpec:
    return LimitRangeSpec(**value) if isinstance(value, dict) else value


def required_converter_LoadBalancerIngress(value: LoadBalancerIngressUnion) ->LoadBalancerIngress:
    return LoadBalancerIngress(**value) if isinstance(value, dict) else value


def required_converter_LoadBalancerStatus(value: LoadBalancerStatusUnion) ->LoadBalancerStatus:
    return LoadBalancerStatus(**value) if isinstance(value, dict) else value


def required_converter_LocalObjectReference(value: LocalObjectReferenceUnion) ->LocalObjectReference:
    return LocalObjectReference(**value) if isinstance(value, dict) else value


def required_converter_LocalVolumeSource(value: LocalVolumeSourceUnion) ->LocalVolumeSource:
    return LocalVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ManagedFieldsEntry(value: ManagedFieldsEntryUnion) ->ManagedFieldsEntry:
    return ManagedFieldsEntry(**value) if isinstance(value, dict) else value


def required_converter_NFSVolumeSource(value: NFSVolumeSourceUnion) ->NFSVolumeSource:
    return NFSVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_NamespaceConditionItem(value: NamespaceConditionItemUnion) ->NamespaceConditionItem:
    return NamespaceConditionItem(**value) if isinstance(value, dict) else value


def required_converter_NamespaceSpec(value: NamespaceSpecUnion) ->NamespaceSpec:
    return NamespaceSpec(**value) if isinstance(value, dict) else value


def required_converter_NamespaceStatus(value: NamespaceStatusUnion) ->NamespaceStatus:
    return NamespaceStatus(**value) if isinstance(value, dict) else value


def required_converter_NodeAddressItem(value: NodeAddressItemUnion) ->NodeAddressItem:
    return NodeAddressItem(**value) if isinstance(value, dict) else value


def required_converter_NodeAffinity(value: NodeAffinityUnion) ->NodeAffinity:
    return NodeAffinity(**value) if isinstance(value, dict) else value


def required_converter_NodeConditionItem(value: NodeConditionItemUnion) ->NodeConditionItem:
    return NodeConditionItem(**value) if isinstance(value, dict) else value


def required_converter_NodeConfigSource(value: NodeConfigSourceUnion) ->NodeConfigSource:
    return NodeConfigSource(**value) if isinstance(value, dict) else value


def required_converter_NodeConfigStatus(value: NodeConfigStatusUnion) ->NodeConfigStatus:
    return NodeConfigStatus(**value) if isinstance(value, dict) else value


def required_converter_NodeDaemonEndpoints(value: NodeDaemonEndpointsUnion) ->NodeDaemonEndpoints:
    return NodeDaemonEndpoints(**value) if isinstance(value, dict) else value


def required_converter_NodeSelector(value: NodeSelectorUnion) ->NodeSelector:
    return NodeSelector(**value) if isinstance(value, dict) else value


def required_converter_NodeSelectorRequirement(value: NodeSelectorRequirementUnion) ->NodeSelectorRequirement:
    return NodeSelectorRequirement(**value) if isinstance(value, dict) else value


def required_converter_NodeSelectorTerm(value: NodeSelectorTermUnion) ->NodeSelectorTerm:
    return NodeSelectorTerm(**value) if isinstance(value, dict) else value


def required_converter_NodeSpec(value: NodeSpecUnion) ->NodeSpec:
    return NodeSpec(**value) if isinstance(value, dict) else value


def required_converter_NodeStatus(value: NodeStatusUnion) ->NodeStatus:
    return NodeStatus(**value) if isinstance(value, dict) else value


def required_converter_NodeSystemInfo(value: NodeSystemInfoUnion) ->NodeSystemInfo:
    return NodeSystemInfo(**value) if isinstance(value, dict) else value


def required_converter_ObjectFieldSelector(value: ObjectFieldSelectorUnion) ->ObjectFieldSelector:
    return ObjectFieldSelector(**value) if isinstance(value, dict) else value


def required_converter_ObjectMeta(value: ObjectMetaUnion) ->ObjectMeta:
    return ObjectMeta(**value) if isinstance(value, dict) else value


def required_converter_ObjectReference(value: ObjectReferenceUnion) ->ObjectReference:
    return ObjectReference(**value) if isinstance(value, dict) else value


def required_converter_ObjectReferenceItem(value: ObjectReferenceItemUnion) ->ObjectReferenceItem:
    return ObjectReferenceItem(**value) if isinstance(value, dict) else value


def required_converter_OwnerReferenceItem(value: OwnerReferenceItemUnion) ->OwnerReferenceItem:
    return OwnerReferenceItem(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimConditionItem(value: PersistentVolumeClaimConditionItemUnion) ->PersistentVolumeClaimConditionItem:
    return PersistentVolumeClaimConditionItem(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimSpec(value: PersistentVolumeClaimSpecUnion) ->PersistentVolumeClaimSpec:
    return PersistentVolumeClaimSpec(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimStatus(value: PersistentVolumeClaimStatusUnion) ->PersistentVolumeClaimStatus:
    return PersistentVolumeClaimStatus(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimTemplate(value: PersistentVolumeClaimTemplateUnion) ->PersistentVolumeClaimTemplate:
    return PersistentVolumeClaimTemplate(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeClaimVolumeSource(value: PersistentVolumeClaimVolumeSourceUnion) ->PersistentVolumeClaimVolumeSource:
    return PersistentVolumeClaimVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeSpec(value: PersistentVolumeSpecUnion) ->PersistentVolumeSpec:
    return PersistentVolumeSpec(**value) if isinstance(value, dict) else value


def required_converter_PersistentVolumeStatus(value: PersistentVolumeStatusUnion) ->PersistentVolumeStatus:
    return PersistentVolumeStatus(**value) if isinstance(value, dict) else value


def required_converter_PhotonPersistentDiskVolumeSource(value: PhotonPersistentDiskVolumeSourceUnion) ->PhotonPersistentDiskVolumeSource:
    return PhotonPersistentDiskVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_PodAffinity(value: PodAffinityUnion) ->PodAffinity:
    return PodAffinity(**value) if isinstance(value, dict) else value


def required_converter_PodAffinityTerm(value: PodAffinityTermUnion) ->PodAffinityTerm:
    return PodAffinityTerm(**value) if isinstance(value, dict) else value


def required_converter_PodAntiAffinity(value: PodAntiAffinityUnion) ->PodAntiAffinity:
    return PodAntiAffinity(**value) if isinstance(value, dict) else value


def required_converter_PodConditionItem(value: PodConditionItemUnion) ->PodConditionItem:
    return PodConditionItem(**value) if isinstance(value, dict) else value


def required_converter_PodDNSConfig(value: PodDNSConfigUnion) ->PodDNSConfig:
    return PodDNSConfig(**value) if isinstance(value, dict) else value


def required_converter_PodDNSConfigOption(value: PodDNSConfigOptionUnion) ->PodDNSConfigOption:
    return PodDNSConfigOption(**value) if isinstance(value, dict) else value


def required_converter_PodIP(value: PodIPUnion) ->PodIP:
    return PodIP(**value) if isinstance(value, dict) else value


def required_converter_PodReadinessGate(value: PodReadinessGateUnion) ->PodReadinessGate:
    return PodReadinessGate(**value) if isinstance(value, dict) else value


def required_converter_PodSecurityContext(value: PodSecurityContextUnion) ->PodSecurityContext:
    return PodSecurityContext(**value) if isinstance(value, dict) else value


def required_converter_PodSpec(value: PodSpecUnion) ->PodSpec:
    return PodSpec(**value) if isinstance(value, dict) else value


def required_converter_PodStatus(value: PodStatusUnion) ->PodStatus:
    return PodStatus(**value) if isinstance(value, dict) else value


def required_converter_PodTemplateSpec(value: PodTemplateSpecUnion) ->PodTemplateSpec:
    return PodTemplateSpec(**value) if isinstance(value, dict) else value


def required_converter_PortStatus(value: PortStatusUnion) ->PortStatus:
    return PortStatus(**value) if isinstance(value, dict) else value


def required_converter_PortworxVolumeSource(value: PortworxVolumeSourceUnion) ->PortworxVolumeSource:
    return PortworxVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_Preconditions(value: PreconditionsUnion) ->Preconditions:
    return Preconditions(**value) if isinstance(value, dict) else value


def required_converter_PreferredSchedulingTerm(value: PreferredSchedulingTermUnion) ->PreferredSchedulingTerm:
    return PreferredSchedulingTerm(**value) if isinstance(value, dict) else value


def required_converter_Probe(value: ProbeUnion) ->Probe:
    return Probe(**value) if isinstance(value, dict) else value


def required_converter_ProjectedVolumeSource(value: ProjectedVolumeSourceUnion) ->ProjectedVolumeSource:
    return ProjectedVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_QuobyteVolumeSource(value: QuobyteVolumeSourceUnion) ->QuobyteVolumeSource:
    return QuobyteVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_RBDPersistentVolumeSource(value: RBDPersistentVolumeSourceUnion) ->RBDPersistentVolumeSource:
    return RBDPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_RBDVolumeSource(value: RBDVolumeSourceUnion) ->RBDVolumeSource:
    return RBDVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ReplicationControllerConditionItem(value: ReplicationControllerConditionItemUnion) ->ReplicationControllerConditionItem:
    return ReplicationControllerConditionItem(**value) if isinstance(value, dict) else value


def required_converter_ReplicationControllerSpec(value: ReplicationControllerSpecUnion) ->ReplicationControllerSpec:
    return ReplicationControllerSpec(**value) if isinstance(value, dict) else value


def required_converter_ReplicationControllerStatus(value: ReplicationControllerStatusUnion) ->ReplicationControllerStatus:
    return ReplicationControllerStatus(**value) if isinstance(value, dict) else value


def required_converter_ResourceFieldSelector(value: ResourceFieldSelectorUnion) ->ResourceFieldSelector:
    return ResourceFieldSelector(**value) if isinstance(value, dict) else value


def required_converter_ResourceQuotaSpec(value: ResourceQuotaSpecUnion) ->ResourceQuotaSpec:
    return ResourceQuotaSpec(**value) if isinstance(value, dict) else value


def required_converter_ResourceQuotaStatus(value: ResourceQuotaStatusUnion) ->ResourceQuotaStatus:
    return ResourceQuotaStatus(**value) if isinstance(value, dict) else value


def required_converter_ResourceRequirements(value: ResourceRequirementsUnion) ->ResourceRequirements:
    return ResourceRequirements(**value) if isinstance(value, dict) else value


def required_converter_SELinuxOptions(value: SELinuxOptionsUnion) ->SELinuxOptions:
    return SELinuxOptions(**value) if isinstance(value, dict) else value


def required_converter_ScaleIOPersistentVolumeSource(value: ScaleIOPersistentVolumeSourceUnion) ->ScaleIOPersistentVolumeSource:
    return ScaleIOPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ScaleIOVolumeSource(value: ScaleIOVolumeSourceUnion) ->ScaleIOVolumeSource:
    return ScaleIOVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_ScopeSelector(value: ScopeSelectorUnion) ->ScopeSelector:
    return ScopeSelector(**value) if isinstance(value, dict) else value


def required_converter_ScopedResourceSelectorRequirement(value: ScopedResourceSelectorRequirementUnion) ->ScopedResourceSelectorRequirement:
    return ScopedResourceSelectorRequirement(**value) if isinstance(value, dict) else value


def required_converter_SeccompProfile(value: SeccompProfileUnion) ->SeccompProfile:
    return SeccompProfile(**value) if isinstance(value, dict) else value


def required_converter_SecretEnvSource(value: SecretEnvSourceUnion) ->SecretEnvSource:
    return SecretEnvSource(**value) if isinstance(value, dict) else value


def required_converter_SecretKeySelector(value: SecretKeySelectorUnion) ->SecretKeySelector:
    return SecretKeySelector(**value) if isinstance(value, dict) else value


def required_converter_SecretProjection(value: SecretProjectionUnion) ->SecretProjection:
    return SecretProjection(**value) if isinstance(value, dict) else value


def required_converter_SecretReference(value: SecretReferenceUnion) ->SecretReference:
    return SecretReference(**value) if isinstance(value, dict) else value


def required_converter_SecretVolumeSource(value: SecretVolumeSourceUnion) ->SecretVolumeSource:
    return SecretVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_SecurityContext(value: SecurityContextUnion) ->SecurityContext:
    return SecurityContext(**value) if isinstance(value, dict) else value


def required_converter_ServiceAccountTokenProjection(value: ServiceAccountTokenProjectionUnion) ->ServiceAccountTokenProjection:
    return ServiceAccountTokenProjection(**value) if isinstance(value, dict) else value


def required_converter_ServicePortItem(value: ServicePortItemUnion) ->ServicePortItem:
    return ServicePortItem(**value) if isinstance(value, dict) else value


def required_converter_ServiceSpec(value: ServiceSpecUnion) ->ServiceSpec:
    return ServiceSpec(**value) if isinstance(value, dict) else value


def required_converter_ServiceStatus(value: ServiceStatusUnion) ->ServiceStatus:
    return ServiceStatus(**value) if isinstance(value, dict) else value


def required_converter_SessionAffinityConfig(value: SessionAffinityConfigUnion) ->SessionAffinityConfig:
    return SessionAffinityConfig(**value) if isinstance(value, dict) else value


def required_converter_StorageOSPersistentVolumeSource(value: StorageOSPersistentVolumeSourceUnion) ->StorageOSPersistentVolumeSource:
    return StorageOSPersistentVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_StorageOSVolumeSource(value: StorageOSVolumeSourceUnion) ->StorageOSVolumeSource:
    return StorageOSVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_Sysctl(value: SysctlUnion) ->Sysctl:
    return Sysctl(**value) if isinstance(value, dict) else value


def required_converter_TCPSocketAction(value: TCPSocketActionUnion) ->TCPSocketAction:
    return TCPSocketAction(**value) if isinstance(value, dict) else value


def required_converter_Taint(value: TaintUnion) ->Taint:
    return Taint(**value) if isinstance(value, dict) else value


def required_converter_Toleration(value: TolerationUnion) ->Toleration:
    return Toleration(**value) if isinstance(value, dict) else value


def required_converter_TopologySelectorLabelRequirement(value: TopologySelectorLabelRequirementUnion) ->TopologySelectorLabelRequirement:
    return TopologySelectorLabelRequirement(**value) if isinstance(value, dict) else value


def required_converter_TopologySelectorTerm(value: TopologySelectorTermUnion) ->TopologySelectorTerm:
    return TopologySelectorTerm(**value) if isinstance(value, dict) else value


def required_converter_TopologySpreadConstraintItem(value: TopologySpreadConstraintItemUnion) ->TopologySpreadConstraintItem:
    return TopologySpreadConstraintItem(**value) if isinstance(value, dict) else value


def required_converter_TypedLocalObjectReference(value: TypedLocalObjectReferenceUnion) ->TypedLocalObjectReference:
    return TypedLocalObjectReference(**value) if isinstance(value, dict) else value


def required_converter_VolumeDeviceItem(value: VolumeDeviceItemUnion) ->VolumeDeviceItem:
    return VolumeDeviceItem(**value) if isinstance(value, dict) else value


def required_converter_VolumeItem(value: VolumeItemUnion) ->VolumeItem:
    return VolumeItem(**value) if isinstance(value, dict) else value


def required_converter_VolumeMountItem(value: VolumeMountItemUnion) ->VolumeMountItem:
    return VolumeMountItem(**value) if isinstance(value, dict) else value


def required_converter_VolumeNodeAffinity(value: VolumeNodeAffinityUnion) ->VolumeNodeAffinity:
    return VolumeNodeAffinity(**value) if isinstance(value, dict) else value


def required_converter_VolumeProjection(value: VolumeProjectionUnion) ->VolumeProjection:
    return VolumeProjection(**value) if isinstance(value, dict) else value


def required_converter_VsphereVirtualDiskVolumeSource(value: VsphereVirtualDiskVolumeSourceUnion) ->VsphereVirtualDiskVolumeSource:
    return VsphereVirtualDiskVolumeSource(**value) if isinstance(value, dict) else value


def required_converter_WeightedPodAffinityTerm(value: WeightedPodAffinityTermUnion) ->WeightedPodAffinityTerm:
    return WeightedPodAffinityTerm(**value) if isinstance(value, dict) else value


def required_converter_WindowsSecurityContextOptions(value: WindowsSecurityContextOptionsUnion) ->WindowsSecurityContextOptions:
    return WindowsSecurityContextOptions(**value) if isinstance(value, dict) else value


@attr.s(kw_only=True)
class AWSElasticBlockStoreVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={'yaml_name': 'volumeID'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    partition: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'partition'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class AWSElasticBlockStoreVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    partition: int
    readOnly: bool


class AWSElasticBlockStoreVolumeSourceTypedDict(AWSElasticBlockStoreVolumeSourceOptionalTypedDict, total=(True)):
    volumeID: str


AWSElasticBlockStoreVolumeSourceUnion = Union[AWSElasticBlockStoreVolumeSource, AWSElasticBlockStoreVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Affinity(K8sObject):
    nodeAffinity: Union[None, OmitEnum, NodeAffinity] = attr.ib(metadata={'yaml_name': 'nodeAffinity'}, converter=optional_converter_NodeAffinity, default=OMIT)
    podAffinity: Union[None, OmitEnum, PodAffinity] = attr.ib(metadata={'yaml_name': 'podAffinity'}, converter=optional_converter_PodAffinity, default=OMIT)
    podAntiAffinity: Union[None, OmitEnum, PodAntiAffinity] = attr.ib(metadata={'yaml_name': 'podAntiAffinity'}, converter=optional_converter_PodAntiAffinity, default=OMIT)


class AffinityTypedDict(TypedDict, total=(False)):
    nodeAffinity: NodeAffinity
    podAffinity: PodAffinity
    podAntiAffinity: PodAntiAffinity


AffinityUnion = Union[Affinity, AffinityTypedDict]


@attr.s(kw_only=True)
class AttachedVolume(K8sObject):
    devicePath: str = attr.ib(metadata={'yaml_name': 'devicePath'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class AttachedVolumeTypedDict(TypedDict, total=(True)):
    devicePath: str
    name: str


AttachedVolumeUnion = Union[AttachedVolume, AttachedVolumeTypedDict]


@attr.s(kw_only=True)
class AzureDiskVolumeSource(K8sObject):
    diskName: str = attr.ib(metadata={'yaml_name': 'diskName'})
    diskURI: str = attr.ib(metadata={'yaml_name': 'diskURI'})
    cachingMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'cachingMode'}, default=OMIT)
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    kind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'kind'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class AzureDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    cachingMode: str
    fsType: str
    kind: str
    readOnly: bool


class AzureDiskVolumeSourceTypedDict(AzureDiskVolumeSourceOptionalTypedDict, total=(True)):
    diskName: str
    diskURI: str


AzureDiskVolumeSourceUnion = Union[AzureDiskVolumeSource, AzureDiskVolumeSourceTypedDict]


@attr.s(kw_only=True)
class AzureFilePersistentVolumeSource(K8sObject):
    secretName: str = attr.ib(metadata={'yaml_name': 'secretName'})
    shareName: str = attr.ib(metadata={'yaml_name': 'shareName'})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretNamespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'secretNamespace'}, default=OMIT)


class AzureFilePersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool
    secretNamespace: str


class AzureFilePersistentVolumeSourceTypedDict(AzureFilePersistentVolumeSourceOptionalTypedDict, total=(True)):
    secretName: str
    shareName: str


AzureFilePersistentVolumeSourceUnion = Union[AzureFilePersistentVolumeSource, AzureFilePersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class AzureFileVolumeSource(K8sObject):
    secretName: str = attr.ib(metadata={'yaml_name': 'secretName'})
    shareName: str = attr.ib(metadata={'yaml_name': 'shareName'})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class AzureFileVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class AzureFileVolumeSourceTypedDict(AzureFileVolumeSourceOptionalTypedDict, total=(True)):
    secretName: str
    shareName: str


AzureFileVolumeSourceUnion = Union[AzureFileVolumeSource, AzureFileVolumeSourceTypedDict]


@attr.s(kw_only=True)
class CSIPersistentVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={'yaml_name': 'driver'})
    volumeHandle: str = attr.ib(metadata={'yaml_name': 'volumeHandle'})
    controllerExpandSecretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'controllerExpandSecretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    controllerPublishSecretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'controllerPublishSecretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    nodePublishSecretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'nodePublishSecretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    nodeStageSecretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'nodeStageSecretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    volumeAttributes: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'volumeAttributes'}, default=OMIT)


class CSIPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    controllerExpandSecretRef: SecretReference
    controllerPublishSecretRef: SecretReference
    fsType: str
    nodePublishSecretRef: SecretReference
    nodeStageSecretRef: SecretReference
    readOnly: bool
    volumeAttributes: Mapping[str, str]


class CSIPersistentVolumeSourceTypedDict(CSIPersistentVolumeSourceOptionalTypedDict, total=(True)):
    driver: str
    volumeHandle: str


CSIPersistentVolumeSourceUnion = Union[CSIPersistentVolumeSource, CSIPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class CSIVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={'yaml_name': 'driver'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    nodePublishSecretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'nodePublishSecretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    volumeAttributes: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'volumeAttributes'}, default=OMIT)


class CSIVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    nodePublishSecretRef: LocalObjectReference
    readOnly: bool
    volumeAttributes: Mapping[str, str]


class CSIVolumeSourceTypedDict(CSIVolumeSourceOptionalTypedDict, total=(True)):
    driver: str


CSIVolumeSourceUnion = Union[CSIVolumeSource, CSIVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Capabilities(K8sObject):
    add: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'add'}, default=OMIT)
    drop: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'drop'}, default=OMIT)


class CapabilitiesTypedDict(TypedDict, total=(False)):
    add: Sequence[str]
    drop: Sequence[str]


CapabilitiesUnion = Union[Capabilities, CapabilitiesTypedDict]


@attr.s(kw_only=True)
class CephFSPersistentVolumeSource(K8sObject):
    monitors: Sequence[str] = attr.ib(metadata={'yaml_name': 'monitors'})
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretFile: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'secretFile'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class CephFSPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    readOnly: bool
    secretFile: str
    secretRef: SecretReference
    user: str


class CephFSPersistentVolumeSourceTypedDict(CephFSPersistentVolumeSourceOptionalTypedDict, total=(True)):
    monitors: Sequence[str]


CephFSPersistentVolumeSourceUnion = Union[CephFSPersistentVolumeSource, CephFSPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class CephFSVolumeSource(K8sObject):
    monitors: Sequence[str] = attr.ib(metadata={'yaml_name': 'monitors'})
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretFile: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'secretFile'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class CephFSVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    path: str
    readOnly: bool
    secretFile: str
    secretRef: LocalObjectReference
    user: str


class CephFSVolumeSourceTypedDict(CephFSVolumeSourceOptionalTypedDict, total=(True)):
    monitors: Sequence[str]


CephFSVolumeSourceUnion = Union[CephFSVolumeSource, CephFSVolumeSourceTypedDict]


@attr.s(kw_only=True)
class CinderPersistentVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={'yaml_name': 'volumeID'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretReference, default=OMIT)


class CinderPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: SecretReference


class CinderPersistentVolumeSourceTypedDict(CinderPersistentVolumeSourceOptionalTypedDict, total=(True)):
    volumeID: str


CinderPersistentVolumeSourceUnion = Union[CinderPersistentVolumeSource, CinderPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class CinderVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={'yaml_name': 'volumeID'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)


class CinderVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: LocalObjectReference


class CinderVolumeSourceTypedDict(CinderVolumeSourceOptionalTypedDict, total=(True)):
    volumeID: str


CinderVolumeSourceUnion = Union[CinderVolumeSource, CinderVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ClientIPConfig(K8sObject):
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'timeoutSeconds'}, default=OMIT)


class ClientIPConfigTypedDict(TypedDict, total=(False)):
    timeoutSeconds: int


ClientIPConfigUnion = Union[ClientIPConfig, ClientIPConfigTypedDict]


@attr.s(kw_only=True)
class ConditionItem(K8sObject):
    lastTransitionTime: str = attr.ib(metadata={'yaml_name': 'lastTransitionTime'})
    message: str = attr.ib(metadata={'yaml_name': 'message'})
    reason: str = attr.ib(metadata={'yaml_name': 'reason'})
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)


class ConditionItemOptionalTypedDict(TypedDict, total=(False)):
    observedGeneration: int


class ConditionItemTypedDict(ConditionItemOptionalTypedDict, total=(True)):
    lastTransitionTime: str
    message: str
    reason: str
    status: str


ConditionItemUnion = Union[ConditionItem, ConditionItemTypedDict]


@attr.s(kw_only=True)
class ConfigMapEnvSource(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class ConfigMapEnvSourceTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


ConfigMapEnvSourceUnion = Union[ConfigMapEnvSource, ConfigMapEnvSourceTypedDict]


@attr.s(kw_only=True)
class ConfigMapKeySelector(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class ConfigMapKeySelectorOptionalTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


class ConfigMapKeySelectorTypedDict(ConfigMapKeySelectorOptionalTypedDict, total=(True)):
    key: str


ConfigMapKeySelectorUnion = Union[ConfigMapKeySelector, ConfigMapKeySelectorTypedDict]


@attr.s(kw_only=True)
class ConfigMapNodeConfigSource(K8sObject):
    kubeletConfigKey: str = attr.ib(metadata={'yaml_name': 'kubeletConfigKey'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    namespace: str = attr.ib(metadata={'yaml_name': 'namespace'})
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resourceVersion'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)


class ConfigMapNodeConfigSourceOptionalTypedDict(TypedDict, total=(False)):
    resourceVersion: str
    uid: str


class ConfigMapNodeConfigSourceTypedDict(ConfigMapNodeConfigSourceOptionalTypedDict, total=(True)):
    kubeletConfigKey: str
    name: str
    namespace: str


ConfigMapNodeConfigSourceUnion = Union[ConfigMapNodeConfigSource, ConfigMapNodeConfigSourceTypedDict]


@attr.s(kw_only=True)
class ConfigMapProjection(K8sObject):
    items: Union[None, OmitEnum, Sequence[KeyToPath]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_KeyToPath, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class ConfigMapProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[KeyToPath]
    name: str
    optional: bool


ConfigMapProjectionUnion = Union[ConfigMapProjection, ConfigMapProjectionTypedDict]


@attr.s(kw_only=True)
class ConfigMapVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'defaultMode'}, default=OMIT)
    items: Union[None, OmitEnum, Sequence[KeyToPath]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_KeyToPath, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class ConfigMapVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[KeyToPath]
    name: str
    optional: bool


ConfigMapVolumeSourceUnion = Union[ConfigMapVolumeSource, ConfigMapVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ContainerImage(K8sObject):
    names: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'names'}, default=OMIT)
    sizeBytes: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'sizeBytes'}, default=OMIT)


class ContainerImageTypedDict(TypedDict, total=(False)):
    names: Sequence[str]
    sizeBytes: int


ContainerImageUnion = Union[ContainerImage, ContainerImageTypedDict]


@attr.s(kw_only=True)
class ContainerItem(K8sObject):
    args: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'args'}, default=OMIT)
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'command'}, default=OMIT)
    env: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.EnvVarItem]] = attr.ib(metadata={'yaml_name': 'env', 'mlist_key': 'name'}, converter=optional_mlist_converter_EnvVarItem, default=OMIT)
    envFrom: Union[None, OmitEnum, Sequence[EnvFromSource]] = attr.ib(metadata={'yaml_name': 'envFrom'}, converter=optional_list_converter_EnvFromSource, default=OMIT)
    image: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'image'}, default=OMIT)
    imagePullPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'imagePullPolicy'}, default=OMIT)
    lifecycle: Union[None, OmitEnum, Lifecycle] = attr.ib(metadata={'yaml_name': 'lifecycle'}, converter=optional_converter_Lifecycle, default=OMIT)
    livenessProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'livenessProbe'}, converter=optional_converter_Probe, default=OMIT)
    ports: Union[None, OmitEnum, Mapping[int, kdsl.core.v1.ContainerPortItem]] = attr.ib(metadata={'yaml_name': 'ports', 'mlist_key': 'containerPort'}, converter=optional_mlist_converter_ContainerPortItem, default=OMIT)
    readinessProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'readinessProbe'}, converter=optional_converter_Probe, default=OMIT)
    resources: Union[None, OmitEnum, ResourceRequirements] = attr.ib(metadata={'yaml_name': 'resources'}, converter=optional_converter_ResourceRequirements, default=OMIT)
    securityContext: Union[None, OmitEnum, SecurityContext] = attr.ib(metadata={'yaml_name': 'securityContext'}, converter=optional_converter_SecurityContext, default=OMIT)
    startupProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'startupProbe'}, converter=optional_converter_Probe, default=OMIT)
    stdin: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'stdin'}, default=OMIT)
    stdinOnce: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'stdinOnce'}, default=OMIT)
    terminationMessagePath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'terminationMessagePath'}, default=OMIT)
    terminationMessagePolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'terminationMessagePolicy'}, default=OMIT)
    tty: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'tty'}, default=OMIT)
    volumeDevices: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeDeviceItem]] = attr.ib(metadata={'yaml_name': 'volumeDevices', 'mlist_key': 'devicePath'}, converter=optional_mlist_converter_VolumeDeviceItem, default=OMIT)
    volumeMounts: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeMountItem]] = attr.ib(metadata={'yaml_name': 'volumeMounts', 'mlist_key': 'mountPath'}, converter=optional_mlist_converter_VolumeMountItem, default=OMIT)
    workingDir: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'workingDir'}, default=OMIT)


class ContainerItemTypedDict(TypedDict, total=(False)):
    args: Sequence[str]
    command: Sequence[str]
    env: Mapping[str, kdsl.core.v1.EnvVarItem]
    envFrom: Sequence[EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: Lifecycle
    livenessProbe: Probe
    ports: Mapping[int, kdsl.core.v1.ContainerPortItem]
    readinessProbe: Probe
    resources: ResourceRequirements
    securityContext: SecurityContext
    startupProbe: Probe
    stdin: bool
    stdinOnce: bool
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    volumeMounts: Mapping[str, kdsl.core.v1.VolumeMountItem]
    workingDir: str


ContainerItemUnion = Union[ContainerItem, ContainerItemTypedDict]


@attr.s(kw_only=True)
class ContainerPort(K8sObject):
    containerPort: int = attr.ib(metadata={'yaml_name': 'containerPort'})
    hostIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostIP'}, default=OMIT)
    hostPort: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'hostPort'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)


class ContainerPortOptionalTypedDict(TypedDict, total=(False)):
    hostIP: str
    hostPort: int
    name: str
    protocol: str


class ContainerPortTypedDict(ContainerPortOptionalTypedDict, total=(True)):
    containerPort: int


ContainerPortUnion = Union[ContainerPort, ContainerPortTypedDict]


@attr.s(kw_only=True)
class ContainerPortItem(K8sObject):
    hostIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostIP'}, default=OMIT)
    hostPort: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'hostPort'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)


class ContainerPortItemTypedDict(TypedDict, total=(False)):
    hostIP: str
    hostPort: int
    name: str
    protocol: str


ContainerPortItemUnion = Union[ContainerPortItem, ContainerPortItemTypedDict]


@attr.s(kw_only=True)
class ContainerState(K8sObject):
    running: Union[None, OmitEnum, ContainerStateRunning] = attr.ib(metadata={'yaml_name': 'running'}, converter=optional_converter_ContainerStateRunning, default=OMIT)
    terminated: Union[None, OmitEnum, ContainerStateTerminated] = attr.ib(metadata={'yaml_name': 'terminated'}, converter=optional_converter_ContainerStateTerminated, default=OMIT)
    waiting: Union[None, OmitEnum, ContainerStateWaiting] = attr.ib(metadata={'yaml_name': 'waiting'}, converter=optional_converter_ContainerStateWaiting, default=OMIT)


class ContainerStateTypedDict(TypedDict, total=(False)):
    running: ContainerStateRunning
    terminated: ContainerStateTerminated
    waiting: ContainerStateWaiting


ContainerStateUnion = Union[ContainerState, ContainerStateTypedDict]


@attr.s(kw_only=True)
class ContainerStateRunning(K8sObject):
    startedAt: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'startedAt'}, default=OMIT)


class ContainerStateRunningTypedDict(TypedDict, total=(False)):
    startedAt: str


ContainerStateRunningUnion = Union[ContainerStateRunning, ContainerStateRunningTypedDict]


@attr.s(kw_only=True)
class ContainerStateTerminated(K8sObject):
    exitCode: int = attr.ib(metadata={'yaml_name': 'exitCode'})
    containerID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'containerID'}, default=OMIT)
    finishedAt: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'finishedAt'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    signal: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'signal'}, default=OMIT)
    startedAt: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'startedAt'}, default=OMIT)


class ContainerStateTerminatedOptionalTypedDict(TypedDict, total=(False)):
    containerID: str
    finishedAt: str
    message: str
    reason: str
    signal: int
    startedAt: str


class ContainerStateTerminatedTypedDict(ContainerStateTerminatedOptionalTypedDict, total=(True)):
    exitCode: int


ContainerStateTerminatedUnion = Union[ContainerStateTerminated, ContainerStateTerminatedTypedDict]


@attr.s(kw_only=True)
class ContainerStateWaiting(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class ContainerStateWaitingTypedDict(TypedDict, total=(False)):
    message: str
    reason: str


ContainerStateWaitingUnion = Union[ContainerStateWaiting, ContainerStateWaitingTypedDict]


@attr.s(kw_only=True)
class ContainerStatus(K8sObject):
    image: str = attr.ib(metadata={'yaml_name': 'image'})
    imageID: str = attr.ib(metadata={'yaml_name': 'imageID'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    ready: bool = attr.ib(metadata={'yaml_name': 'ready'})
    restartCount: int = attr.ib(metadata={'yaml_name': 'restartCount'})
    containerID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'containerID'}, default=OMIT)
    lastState: Union[None, OmitEnum, ContainerState] = attr.ib(metadata={'yaml_name': 'lastState'}, converter=optional_converter_ContainerState, default=OMIT)
    started: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'started'}, default=OMIT)
    state: Union[None, OmitEnum, ContainerState] = attr.ib(metadata={'yaml_name': 'state'}, converter=optional_converter_ContainerState, default=OMIT)


class ContainerStatusOptionalTypedDict(TypedDict, total=(False)):
    containerID: str
    lastState: ContainerState
    started: bool
    state: ContainerState


class ContainerStatusTypedDict(ContainerStatusOptionalTypedDict, total=(True)):
    image: str
    imageID: str
    name: str
    ready: bool
    restartCount: int


ContainerStatusUnion = Union[ContainerStatus, ContainerStatusTypedDict]


@attr.s(kw_only=True)
class DaemonEndpoint(K8sObject):
    Port: int = attr.ib(metadata={'yaml_name': 'Port'})


class DaemonEndpointTypedDict(TypedDict, total=(True)):
    Port: int


DaemonEndpointUnion = Union[DaemonEndpoint, DaemonEndpointTypedDict]


@attr.s(kw_only=True)
class DeleteOptions(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    dryRun: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'dryRun'}, default=OMIT)
    gracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'gracePeriodSeconds'}, default=OMIT)
    kind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'kind'}, default=OMIT)
    orphanDependents: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'orphanDependents'}, default=OMIT)
    preconditions: Union[None, OmitEnum, Preconditions] = attr.ib(metadata={'yaml_name': 'preconditions'}, converter=optional_converter_Preconditions, default=OMIT)
    propagationPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'propagationPolicy'}, default=OMIT)


class DeleteOptionsTypedDict(TypedDict, total=(False)):
    apiVersion: str
    dryRun: Sequence[str]
    gracePeriodSeconds: int
    kind: str
    orphanDependents: bool
    preconditions: Preconditions
    propagationPolicy: str


DeleteOptionsUnion = Union[DeleteOptions, DeleteOptionsTypedDict]


@attr.s(kw_only=True)
class DownwardAPIProjection(K8sObject):
    items: Union[None, OmitEnum, Sequence[DownwardAPIVolumeFile]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_DownwardAPIVolumeFile, default=OMIT)


class DownwardAPIProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[DownwardAPIVolumeFile]


DownwardAPIProjectionUnion = Union[DownwardAPIProjection, DownwardAPIProjectionTypedDict]


@attr.s(kw_only=True)
class DownwardAPIVolumeFile(K8sObject):
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    fieldRef: Union[None, OmitEnum, ObjectFieldSelector] = attr.ib(metadata={'yaml_name': 'fieldRef'}, converter=optional_converter_ObjectFieldSelector, default=OMIT)
    mode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'mode'}, default=OMIT)
    resourceFieldRef: Union[None, OmitEnum, ResourceFieldSelector] = attr.ib(metadata={'yaml_name': 'resourceFieldRef'}, converter=optional_converter_ResourceFieldSelector, default=OMIT)


class DownwardAPIVolumeFileOptionalTypedDict(TypedDict, total=(False)):
    fieldRef: ObjectFieldSelector
    mode: int
    resourceFieldRef: ResourceFieldSelector


class DownwardAPIVolumeFileTypedDict(DownwardAPIVolumeFileOptionalTypedDict, total=(True)):
    path: str


DownwardAPIVolumeFileUnion = Union[DownwardAPIVolumeFile, DownwardAPIVolumeFileTypedDict]


@attr.s(kw_only=True)
class DownwardAPIVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'defaultMode'}, default=OMIT)
    items: Union[None, OmitEnum, Sequence[DownwardAPIVolumeFile]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_DownwardAPIVolumeFile, default=OMIT)


class DownwardAPIVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[DownwardAPIVolumeFile]


DownwardAPIVolumeSourceUnion = Union[DownwardAPIVolumeSource, DownwardAPIVolumeSourceTypedDict]


@attr.s(kw_only=True)
class EmbeddedPersistentVolumeClaim(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    kind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'kind'}, default=OMIT)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PersistentVolumeClaimSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PersistentVolumeClaimSpec, default=OMIT)
    status: Union[None, OmitEnum, PersistentVolumeClaimStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PersistentVolumeClaimStatus, default=OMIT)


class EmbeddedPersistentVolumeClaimTypedDict(TypedDict, total=(False)):
    apiVersion: str
    kind: str
    metadata: ObjectMeta
    spec: PersistentVolumeClaimSpec
    status: PersistentVolumeClaimStatus


EmbeddedPersistentVolumeClaimUnion = Union[EmbeddedPersistentVolumeClaim, EmbeddedPersistentVolumeClaimTypedDict]


@attr.s(kw_only=True)
class EmptyDirVolumeSource(K8sObject):
    medium: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'medium'}, default=OMIT)
    sizeLimit: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'sizeLimit'}, default=OMIT)


class EmptyDirVolumeSourceTypedDict(TypedDict, total=(False)):
    medium: str
    sizeLimit: str


EmptyDirVolumeSourceUnion = Union[EmptyDirVolumeSource, EmptyDirVolumeSourceTypedDict]


@attr.s(kw_only=True)
class EndpointAddress(K8sObject):
    ip: str = attr.ib(metadata={'yaml_name': 'ip'})
    hostname: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostname'}, default=OMIT)
    nodeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'nodeName'}, default=OMIT)
    targetRef: Union[None, OmitEnum, ObjectReference] = attr.ib(metadata={'yaml_name': 'targetRef'}, converter=optional_converter_ObjectReference, default=OMIT)


class EndpointAddressOptionalTypedDict(TypedDict, total=(False)):
    hostname: str
    nodeName: str
    targetRef: ObjectReference


class EndpointAddressTypedDict(EndpointAddressOptionalTypedDict, total=(True)):
    ip: str


EndpointAddressUnion = Union[EndpointAddress, EndpointAddressTypedDict]


@attr.s(kw_only=True)
class EndpointPort(K8sObject):
    port: int = attr.ib(metadata={'yaml_name': 'port'})
    appProtocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'appProtocol'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)


class EndpointPortOptionalTypedDict(TypedDict, total=(False)):
    appProtocol: str
    name: str
    protocol: str


class EndpointPortTypedDict(EndpointPortOptionalTypedDict, total=(True)):
    port: int


EndpointPortUnion = Union[EndpointPort, EndpointPortTypedDict]


@attr.s(kw_only=True)
class EndpointSubset(K8sObject):
    addresses: Union[None, OmitEnum, Sequence[EndpointAddress]] = attr.ib(metadata={'yaml_name': 'addresses'}, converter=optional_list_converter_EndpointAddress, default=OMIT)
    notReadyAddresses: Union[None, OmitEnum, Sequence[EndpointAddress]] = attr.ib(metadata={'yaml_name': 'notReadyAddresses'}, converter=optional_list_converter_EndpointAddress, default=OMIT)
    ports: Union[None, OmitEnum, Sequence[EndpointPort]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_EndpointPort, default=OMIT)


class EndpointSubsetTypedDict(TypedDict, total=(False)):
    addresses: Sequence[EndpointAddress]
    notReadyAddresses: Sequence[EndpointAddress]
    ports: Sequence[EndpointPort]


EndpointSubsetUnion = Union[EndpointSubset, EndpointSubsetTypedDict]


@attr.s(kw_only=True)
class EnvFromSource(K8sObject):
    configMapRef: Union[None, OmitEnum, ConfigMapEnvSource] = attr.ib(metadata={'yaml_name': 'configMapRef'}, converter=optional_converter_ConfigMapEnvSource, default=OMIT)
    prefix: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'prefix'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretEnvSource] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretEnvSource, default=OMIT)


class EnvFromSourceTypedDict(TypedDict, total=(False)):
    configMapRef: ConfigMapEnvSource
    prefix: str
    secretRef: SecretEnvSource


EnvFromSourceUnion = Union[EnvFromSource, EnvFromSourceTypedDict]


@attr.s(kw_only=True)
class EnvVarItem(K8sObject):
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)
    valueFrom: Union[None, OmitEnum, EnvVarSource] = attr.ib(metadata={'yaml_name': 'valueFrom'}, converter=optional_converter_EnvVarSource, default=OMIT)


class EnvVarItemTypedDict(TypedDict, total=(False)):
    value: str
    valueFrom: EnvVarSource


EnvVarItemUnion = Union[EnvVarItem, EnvVarItemTypedDict]


@attr.s(kw_only=True)
class EnvVarSource(K8sObject):
    configMapKeyRef: Union[None, OmitEnum, ConfigMapKeySelector] = attr.ib(metadata={'yaml_name': 'configMapKeyRef'}, converter=optional_converter_ConfigMapKeySelector, default=OMIT)
    fieldRef: Union[None, OmitEnum, ObjectFieldSelector] = attr.ib(metadata={'yaml_name': 'fieldRef'}, converter=optional_converter_ObjectFieldSelector, default=OMIT)
    resourceFieldRef: Union[None, OmitEnum, ResourceFieldSelector] = attr.ib(metadata={'yaml_name': 'resourceFieldRef'}, converter=optional_converter_ResourceFieldSelector, default=OMIT)
    secretKeyRef: Union[None, OmitEnum, SecretKeySelector] = attr.ib(metadata={'yaml_name': 'secretKeyRef'}, converter=optional_converter_SecretKeySelector, default=OMIT)


class EnvVarSourceTypedDict(TypedDict, total=(False)):
    configMapKeyRef: ConfigMapKeySelector
    fieldRef: ObjectFieldSelector
    resourceFieldRef: ResourceFieldSelector
    secretKeyRef: SecretKeySelector


EnvVarSourceUnion = Union[EnvVarSource, EnvVarSourceTypedDict]


@attr.s(kw_only=True)
class EphemeralContainerItem(K8sObject):
    args: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'args'}, default=OMIT)
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'command'}, default=OMIT)
    env: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.EnvVarItem]] = attr.ib(metadata={'yaml_name': 'env', 'mlist_key': 'name'}, converter=optional_mlist_converter_EnvVarItem, default=OMIT)
    envFrom: Union[None, OmitEnum, Sequence[EnvFromSource]] = attr.ib(metadata={'yaml_name': 'envFrom'}, converter=optional_list_converter_EnvFromSource, default=OMIT)
    image: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'image'}, default=OMIT)
    imagePullPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'imagePullPolicy'}, default=OMIT)
    lifecycle: Union[None, OmitEnum, Lifecycle] = attr.ib(metadata={'yaml_name': 'lifecycle'}, converter=optional_converter_Lifecycle, default=OMIT)
    livenessProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'livenessProbe'}, converter=optional_converter_Probe, default=OMIT)
    ports: Union[None, OmitEnum, Sequence[ContainerPort]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_ContainerPort, default=OMIT)
    readinessProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'readinessProbe'}, converter=optional_converter_Probe, default=OMIT)
    resources: Union[None, OmitEnum, ResourceRequirements] = attr.ib(metadata={'yaml_name': 'resources'}, converter=optional_converter_ResourceRequirements, default=OMIT)
    securityContext: Union[None, OmitEnum, SecurityContext] = attr.ib(metadata={'yaml_name': 'securityContext'}, converter=optional_converter_SecurityContext, default=OMIT)
    startupProbe: Union[None, OmitEnum, Probe] = attr.ib(metadata={'yaml_name': 'startupProbe'}, converter=optional_converter_Probe, default=OMIT)
    stdin: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'stdin'}, default=OMIT)
    stdinOnce: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'stdinOnce'}, default=OMIT)
    targetContainerName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'targetContainerName'}, default=OMIT)
    terminationMessagePath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'terminationMessagePath'}, default=OMIT)
    terminationMessagePolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'terminationMessagePolicy'}, default=OMIT)
    tty: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'tty'}, default=OMIT)
    volumeDevices: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeDeviceItem]] = attr.ib(metadata={'yaml_name': 'volumeDevices', 'mlist_key': 'devicePath'}, converter=optional_mlist_converter_VolumeDeviceItem, default=OMIT)
    volumeMounts: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeMountItem]] = attr.ib(metadata={'yaml_name': 'volumeMounts', 'mlist_key': 'mountPath'}, converter=optional_mlist_converter_VolumeMountItem, default=OMIT)
    workingDir: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'workingDir'}, default=OMIT)


class EphemeralContainerItemTypedDict(TypedDict, total=(False)):
    args: Sequence[str]
    command: Sequence[str]
    env: Mapping[str, kdsl.core.v1.EnvVarItem]
    envFrom: Sequence[EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: Lifecycle
    livenessProbe: Probe
    ports: Sequence[ContainerPort]
    readinessProbe: Probe
    resources: ResourceRequirements
    securityContext: SecurityContext
    startupProbe: Probe
    stdin: bool
    stdinOnce: bool
    targetContainerName: str
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: Mapping[str, kdsl.core.v1.VolumeDeviceItem]
    volumeMounts: Mapping[str, kdsl.core.v1.VolumeMountItem]
    workingDir: str


EphemeralContainerItemUnion = Union[EphemeralContainerItem, EphemeralContainerItemTypedDict]


@attr.s(kw_only=True)
class EphemeralVolumeSource(K8sObject):
    volumeClaimTemplate: Union[None, OmitEnum, PersistentVolumeClaimTemplate] = attr.ib(metadata={'yaml_name': 'volumeClaimTemplate'}, converter=optional_converter_PersistentVolumeClaimTemplate, default=OMIT)


class EphemeralVolumeSourceTypedDict(TypedDict, total=(False)):
    volumeClaimTemplate: PersistentVolumeClaimTemplate


EphemeralVolumeSourceUnion = Union[EphemeralVolumeSource, EphemeralVolumeSourceTypedDict]


@attr.s(kw_only=True)
class EventSeries(K8sObject):
    count: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'count'}, default=OMIT)
    lastObservedTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastObservedTime'}, default=OMIT)


class EventSeriesTypedDict(TypedDict, total=(False)):
    count: int
    lastObservedTime: str


EventSeriesUnion = Union[EventSeries, EventSeriesTypedDict]


@attr.s(kw_only=True)
class EventSource(K8sObject):
    component: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'component'}, default=OMIT)
    host: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'host'}, default=OMIT)


class EventSourceTypedDict(TypedDict, total=(False)):
    component: str
    host: str


EventSourceUnion = Union[EventSource, EventSourceTypedDict]


@attr.s(kw_only=True)
class ExecAction(K8sObject):
    command: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'command'}, default=OMIT)


class ExecActionTypedDict(TypedDict, total=(False)):
    command: Sequence[str]


ExecActionUnion = Union[ExecAction, ExecActionTypedDict]


@attr.s(kw_only=True)
class FCVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    lun: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'lun'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    targetWWNs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'targetWWNs'}, default=OMIT)
    wwids: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'wwids'}, default=OMIT)


class FCVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    lun: int
    readOnly: bool
    targetWWNs: Sequence[str]
    wwids: Sequence[str]


FCVolumeSourceUnion = Union[FCVolumeSource, FCVolumeSourceTypedDict]


@attr.s(kw_only=True)
class FlexPersistentVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={'yaml_name': 'driver'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    options: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'options'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretReference, default=OMIT)


class FlexPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    options: Mapping[str, str]
    readOnly: bool
    secretRef: SecretReference


class FlexPersistentVolumeSourceTypedDict(FlexPersistentVolumeSourceOptionalTypedDict, total=(True)):
    driver: str


FlexPersistentVolumeSourceUnion = Union[FlexPersistentVolumeSource, FlexPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class FlexVolumeSource(K8sObject):
    driver: str = attr.ib(metadata={'yaml_name': 'driver'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    options: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'options'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)


class FlexVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    options: Mapping[str, str]
    readOnly: bool
    secretRef: LocalObjectReference


class FlexVolumeSourceTypedDict(FlexVolumeSourceOptionalTypedDict, total=(True)):
    driver: str


FlexVolumeSourceUnion = Union[FlexVolumeSource, FlexVolumeSourceTypedDict]


@attr.s(kw_only=True)
class FlockerVolumeSource(K8sObject):
    datasetName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'datasetName'}, default=OMIT)
    datasetUUID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'datasetUUID'}, default=OMIT)


class FlockerVolumeSourceTypedDict(TypedDict, total=(False)):
    datasetName: str
    datasetUUID: str


FlockerVolumeSourceUnion = Union[FlockerVolumeSource, FlockerVolumeSourceTypedDict]


@attr.s(kw_only=True)
class GCEPersistentDiskVolumeSource(K8sObject):
    pdName: str = attr.ib(metadata={'yaml_name': 'pdName'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    partition: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'partition'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class GCEPersistentDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    partition: int
    readOnly: bool


class GCEPersistentDiskVolumeSourceTypedDict(GCEPersistentDiskVolumeSourceOptionalTypedDict, total=(True)):
    pdName: str


GCEPersistentDiskVolumeSourceUnion = Union[GCEPersistentDiskVolumeSource, GCEPersistentDiskVolumeSourceTypedDict]


@attr.s(kw_only=True)
class GitRepoVolumeSource(K8sObject):
    repository: str = attr.ib(metadata={'yaml_name': 'repository'})
    directory: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'directory'}, default=OMIT)
    revision: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'revision'}, default=OMIT)


class GitRepoVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    directory: str
    revision: str


class GitRepoVolumeSourceTypedDict(GitRepoVolumeSourceOptionalTypedDict, total=(True)):
    repository: str


GitRepoVolumeSourceUnion = Union[GitRepoVolumeSource, GitRepoVolumeSourceTypedDict]


@attr.s(kw_only=True)
class GlusterfsPersistentVolumeSource(K8sObject):
    endpoints: str = attr.ib(metadata={'yaml_name': 'endpoints'})
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    endpointsNamespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'endpointsNamespace'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class GlusterfsPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    endpointsNamespace: str
    readOnly: bool


class GlusterfsPersistentVolumeSourceTypedDict(GlusterfsPersistentVolumeSourceOptionalTypedDict, total=(True)):
    endpoints: str
    path: str


GlusterfsPersistentVolumeSourceUnion = Union[GlusterfsPersistentVolumeSource, GlusterfsPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class GlusterfsVolumeSource(K8sObject):
    endpoints: str = attr.ib(metadata={'yaml_name': 'endpoints'})
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class GlusterfsVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class GlusterfsVolumeSourceTypedDict(GlusterfsVolumeSourceOptionalTypedDict, total=(True)):
    endpoints: str
    path: str


GlusterfsVolumeSourceUnion = Union[GlusterfsVolumeSource, GlusterfsVolumeSourceTypedDict]


@attr.s(kw_only=True)
class HTTPGetAction(K8sObject):
    port: Union[int, str] = attr.ib(metadata={'yaml_name': 'port'})
    host: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'host'}, default=OMIT)
    httpHeaders: Union[None, OmitEnum, Sequence[HTTPHeader]] = attr.ib(metadata={'yaml_name': 'httpHeaders'}, converter=optional_list_converter_HTTPHeader, default=OMIT)
    path: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'path'}, default=OMIT)
    scheme: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'scheme'}, default=OMIT)


class HTTPGetActionOptionalTypedDict(TypedDict, total=(False)):
    host: str
    httpHeaders: Sequence[HTTPHeader]
    path: str
    scheme: str


class HTTPGetActionTypedDict(HTTPGetActionOptionalTypedDict, total=(True)):
    port: Union[int, str]


HTTPGetActionUnion = Union[HTTPGetAction, HTTPGetActionTypedDict]


@attr.s(kw_only=True)
class HTTPHeader(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    value: str = attr.ib(metadata={'yaml_name': 'value'})


class HTTPHeaderTypedDict(TypedDict, total=(True)):
    name: str
    value: str


HTTPHeaderUnion = Union[HTTPHeader, HTTPHeaderTypedDict]


@attr.s(kw_only=True)
class Handler(K8sObject):
    exec: Union[None, OmitEnum, ExecAction] = attr.ib(metadata={'yaml_name': 'exec'}, converter=optional_converter_ExecAction, default=OMIT)
    httpGet: Union[None, OmitEnum, HTTPGetAction] = attr.ib(metadata={'yaml_name': 'httpGet'}, converter=optional_converter_HTTPGetAction, default=OMIT)
    tcpSocket: Union[None, OmitEnum, TCPSocketAction] = attr.ib(metadata={'yaml_name': 'tcpSocket'}, converter=optional_converter_TCPSocketAction, default=OMIT)


class HandlerTypedDict(TypedDict, total=(False)):
    exec: ExecAction
    httpGet: HTTPGetAction
    tcpSocket: TCPSocketAction


HandlerUnion = Union[Handler, HandlerTypedDict]


@attr.s(kw_only=True)
class HostAliasItem(K8sObject):
    hostnames: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'hostnames'}, default=OMIT)


class HostAliasItemTypedDict(TypedDict, total=(False)):
    hostnames: Sequence[str]


HostAliasItemUnion = Union[HostAliasItem, HostAliasItemTypedDict]


@attr.s(kw_only=True)
class HostPathVolumeSource(K8sObject):
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class HostPathVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    type: str


class HostPathVolumeSourceTypedDict(HostPathVolumeSourceOptionalTypedDict, total=(True)):
    path: str


HostPathVolumeSourceUnion = Union[HostPathVolumeSource, HostPathVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ISCSIPersistentVolumeSource(K8sObject):
    iqn: str = attr.ib(metadata={'yaml_name': 'iqn'})
    lun: int = attr.ib(metadata={'yaml_name': 'lun'})
    targetPortal: str = attr.ib(metadata={'yaml_name': 'targetPortal'})
    chapAuthDiscovery: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'chapAuthDiscovery'}, default=OMIT)
    chapAuthSession: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'chapAuthSession'}, default=OMIT)
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    initiatorName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'initiatorName'}, default=OMIT)
    iscsiInterface: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'iscsiInterface'}, default=OMIT)
    portals: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'portals'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretReference, default=OMIT)


class ISCSIPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iscsiInterface: str
    portals: Sequence[str]
    readOnly: bool
    secretRef: SecretReference


class ISCSIPersistentVolumeSourceTypedDict(ISCSIPersistentVolumeSourceOptionalTypedDict, total=(True)):
    iqn: str
    lun: int
    targetPortal: str


ISCSIPersistentVolumeSourceUnion = Union[ISCSIPersistentVolumeSource, ISCSIPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ISCSIVolumeSource(K8sObject):
    iqn: str = attr.ib(metadata={'yaml_name': 'iqn'})
    lun: int = attr.ib(metadata={'yaml_name': 'lun'})
    targetPortal: str = attr.ib(metadata={'yaml_name': 'targetPortal'})
    chapAuthDiscovery: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'chapAuthDiscovery'}, default=OMIT)
    chapAuthSession: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'chapAuthSession'}, default=OMIT)
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    initiatorName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'initiatorName'}, default=OMIT)
    iscsiInterface: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'iscsiInterface'}, default=OMIT)
    portals: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'portals'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)


class ISCSIVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iscsiInterface: str
    portals: Sequence[str]
    readOnly: bool
    secretRef: LocalObjectReference


class ISCSIVolumeSourceTypedDict(ISCSIVolumeSourceOptionalTypedDict, total=(True)):
    iqn: str
    lun: int
    targetPortal: str


ISCSIVolumeSourceUnion = Union[ISCSIVolumeSource, ISCSIVolumeSourceTypedDict]


@attr.s(kw_only=True)
class KeyToPath(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    mode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'mode'}, default=OMIT)


class KeyToPathOptionalTypedDict(TypedDict, total=(False)):
    mode: int


class KeyToPathTypedDict(KeyToPathOptionalTypedDict, total=(True)):
    key: str
    path: str


KeyToPathUnion = Union[KeyToPath, KeyToPathTypedDict]


@attr.s(kw_only=True)
class LabelSelector(K8sObject):
    matchExpressions: Union[None, OmitEnum, Sequence[LabelSelectorRequirement]] = attr.ib(metadata={'yaml_name': 'matchExpressions'}, converter=optional_list_converter_LabelSelectorRequirement, default=OMIT)
    matchLabels: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'matchLabels'}, default=OMIT)


class LabelSelectorTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[LabelSelectorRequirement]
    matchLabels: Mapping[str, str]


LabelSelectorUnion = Union[LabelSelector, LabelSelectorTypedDict]


@attr.s(kw_only=True)
class LabelSelectorRequirement(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist'] = attr.ib(metadata={'yaml_name': 'operator'})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'values'}, default=OMIT)


class LabelSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class LabelSelectorRequirementTypedDict(LabelSelectorRequirementOptionalTypedDict, total=(True)):
    key: str
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist']


LabelSelectorRequirementUnion = Union[LabelSelectorRequirement, LabelSelectorRequirementTypedDict]


@attr.s(kw_only=True)
class Lifecycle(K8sObject):
    postStart: Union[None, OmitEnum, Handler] = attr.ib(metadata={'yaml_name': 'postStart'}, converter=optional_converter_Handler, default=OMIT)
    preStop: Union[None, OmitEnum, Handler] = attr.ib(metadata={'yaml_name': 'preStop'}, converter=optional_converter_Handler, default=OMIT)


class LifecycleTypedDict(TypedDict, total=(False)):
    postStart: Handler
    preStop: Handler


LifecycleUnion = Union[Lifecycle, LifecycleTypedDict]


@attr.s(kw_only=True)
class LimitRangeItem(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    default: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'default'}, default=OMIT)
    defaultRequest: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'defaultRequest'}, default=OMIT)
    max: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'max'}, default=OMIT)
    maxLimitRequestRatio: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'maxLimitRequestRatio'}, default=OMIT)
    min: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'min'}, default=OMIT)


class LimitRangeItemOptionalTypedDict(TypedDict, total=(False)):
    default: Mapping[str, str]
    defaultRequest: Mapping[str, str]
    max: Mapping[str, str]
    maxLimitRequestRatio: Mapping[str, str]
    min: Mapping[str, str]


class LimitRangeItemTypedDict(LimitRangeItemOptionalTypedDict, total=(True)):
    type: str


LimitRangeItemUnion = Union[LimitRangeItem, LimitRangeItemTypedDict]


@attr.s(kw_only=True)
class LimitRangeSpec(K8sObject):
    limits: Sequence[LimitRangeItem] = attr.ib(metadata={'yaml_name': 'limits'}, converter=required_list_converter_LimitRangeItem)


class LimitRangeSpecTypedDict(TypedDict, total=(True)):
    limits: Sequence[LimitRangeItem]


LimitRangeSpecUnion = Union[LimitRangeSpec, LimitRangeSpecTypedDict]


@attr.s(kw_only=True)
class LoadBalancerIngress(K8sObject):
    hostname: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostname'}, default=OMIT)
    ip: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'ip'}, default=OMIT)
    ports: Union[None, OmitEnum, Sequence[PortStatus]] = attr.ib(metadata={'yaml_name': 'ports'}, converter=optional_list_converter_PortStatus, default=OMIT)


class LoadBalancerIngressTypedDict(TypedDict, total=(False)):
    hostname: str
    ip: str
    ports: Sequence[PortStatus]


LoadBalancerIngressUnion = Union[LoadBalancerIngress, LoadBalancerIngressTypedDict]


@attr.s(kw_only=True)
class LoadBalancerStatus(K8sObject):
    ingress: Union[None, OmitEnum, Sequence[LoadBalancerIngress]] = attr.ib(metadata={'yaml_name': 'ingress'}, converter=optional_list_converter_LoadBalancerIngress, default=OMIT)


class LoadBalancerStatusTypedDict(TypedDict, total=(False)):
    ingress: Sequence[LoadBalancerIngress]


LoadBalancerStatusUnion = Union[LoadBalancerStatus, LoadBalancerStatusTypedDict]


@attr.s(kw_only=True)
class LocalObjectReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)


class LocalObjectReferenceTypedDict(TypedDict, total=(False)):
    name: str


LocalObjectReferenceUnion = Union[LocalObjectReference, LocalObjectReferenceTypedDict]


@attr.s(kw_only=True)
class LocalVolumeSource(K8sObject):
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)


class LocalVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str


class LocalVolumeSourceTypedDict(LocalVolumeSourceOptionalTypedDict, total=(True)):
    path: str


LocalVolumeSourceUnion = Union[LocalVolumeSource, LocalVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ManagedFieldsEntry(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    fieldsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fieldsType'}, default=OMIT)
    fieldsV1: Union[None, OmitEnum, Mapping[str, Any]] = attr.ib(metadata={'yaml_name': 'fieldsV1'}, default=OMIT)
    manager: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'manager'}, default=OMIT)
    operation: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'operation'}, default=OMIT)
    subresource: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'subresource'}, default=OMIT)
    time: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'time'}, default=OMIT)


class ManagedFieldsEntryTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldsType: str
    fieldsV1: Mapping[str, Any]
    manager: str
    operation: str
    subresource: str
    time: str


ManagedFieldsEntryUnion = Union[ManagedFieldsEntry, ManagedFieldsEntryTypedDict]


@attr.s(kw_only=True)
class NFSVolumeSource(K8sObject):
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    server: str = attr.ib(metadata={'yaml_name': 'server'})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class NFSVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class NFSVolumeSourceTypedDict(NFSVolumeSourceOptionalTypedDict, total=(True)):
    path: str
    server: str


NFSVolumeSourceUnion = Union[NFSVolumeSource, NFSVolumeSourceTypedDict]


@attr.s(kw_only=True)
class NamespaceConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class NamespaceConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class NamespaceConditionItemTypedDict(NamespaceConditionItemOptionalTypedDict, total=(True)):
    status: str


NamespaceConditionItemUnion = Union[NamespaceConditionItem, NamespaceConditionItemTypedDict]


@attr.s(kw_only=True)
class NamespaceSpec(K8sObject):
    finalizers: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'finalizers'}, default=OMIT)


class NamespaceSpecTypedDict(TypedDict, total=(False)):
    finalizers: Sequence[str]


NamespaceSpecUnion = Union[NamespaceSpec, NamespaceSpecTypedDict]


@attr.s(kw_only=True)
class NamespaceStatus(K8sObject):
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.NamespaceConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_NamespaceConditionItem, default=OMIT)
    phase: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'phase'}, default=OMIT)


class NamespaceStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.NamespaceConditionItem]
    phase: str


NamespaceStatusUnion = Union[NamespaceStatus, NamespaceStatusTypedDict]


@attr.s(kw_only=True)
class NodeAddressItem(K8sObject):
    address: str = attr.ib(metadata={'yaml_name': 'address'})


class NodeAddressItemTypedDict(TypedDict, total=(True)):
    address: str


NodeAddressItemUnion = Union[NodeAddressItem, NodeAddressItemTypedDict]


@attr.s(kw_only=True)
class NodeAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, Sequence[PreferredSchedulingTerm]] = attr.ib(metadata={'yaml_name': 'preferredDuringSchedulingIgnoredDuringExecution'}, converter=optional_list_converter_PreferredSchedulingTerm, default=OMIT)
    requiredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, NodeSelector] = attr.ib(metadata={'yaml_name': 'requiredDuringSchedulingIgnoredDuringExecution'}, converter=optional_converter_NodeSelector, default=OMIT)


class NodeAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[PreferredSchedulingTerm]
    requiredDuringSchedulingIgnoredDuringExecution: NodeSelector


NodeAffinityUnion = Union[NodeAffinity, NodeAffinityTypedDict]


@attr.s(kw_only=True)
class NodeConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastHeartbeatTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastHeartbeatTime'}, default=OMIT)
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class NodeConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastHeartbeatTime: str
    lastTransitionTime: str
    message: str
    reason: str


class NodeConditionItemTypedDict(NodeConditionItemOptionalTypedDict, total=(True)):
    status: str


NodeConditionItemUnion = Union[NodeConditionItem, NodeConditionItemTypedDict]


@attr.s(kw_only=True)
class NodeConfigSource(K8sObject):
    configMap: Union[None, OmitEnum, ConfigMapNodeConfigSource] = attr.ib(metadata={'yaml_name': 'configMap'}, converter=optional_converter_ConfigMapNodeConfigSource, default=OMIT)


class NodeConfigSourceTypedDict(TypedDict, total=(False)):
    configMap: ConfigMapNodeConfigSource


NodeConfigSourceUnion = Union[NodeConfigSource, NodeConfigSourceTypedDict]


@attr.s(kw_only=True)
class NodeConfigStatus(K8sObject):
    active: Union[None, OmitEnum, NodeConfigSource] = attr.ib(metadata={'yaml_name': 'active'}, converter=optional_converter_NodeConfigSource, default=OMIT)
    assigned: Union[None, OmitEnum, NodeConfigSource] = attr.ib(metadata={'yaml_name': 'assigned'}, converter=optional_converter_NodeConfigSource, default=OMIT)
    error: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'error'}, default=OMIT)
    lastKnownGood: Union[None, OmitEnum, NodeConfigSource] = attr.ib(metadata={'yaml_name': 'lastKnownGood'}, converter=optional_converter_NodeConfigSource, default=OMIT)


class NodeConfigStatusTypedDict(TypedDict, total=(False)):
    active: NodeConfigSource
    assigned: NodeConfigSource
    error: str
    lastKnownGood: NodeConfigSource


NodeConfigStatusUnion = Union[NodeConfigStatus, NodeConfigStatusTypedDict]


@attr.s(kw_only=True)
class NodeDaemonEndpoints(K8sObject):
    kubeletEndpoint: Union[None, OmitEnum, DaemonEndpoint] = attr.ib(metadata={'yaml_name': 'kubeletEndpoint'}, converter=optional_converter_DaemonEndpoint, default=OMIT)


class NodeDaemonEndpointsTypedDict(TypedDict, total=(False)):
    kubeletEndpoint: DaemonEndpoint


NodeDaemonEndpointsUnion = Union[NodeDaemonEndpoints, NodeDaemonEndpointsTypedDict]


@attr.s(kw_only=True)
class NodeSelector(K8sObject):
    nodeSelectorTerms: Sequence[NodeSelectorTerm] = attr.ib(metadata={'yaml_name': 'nodeSelectorTerms'}, converter=required_list_converter_NodeSelectorTerm)


class NodeSelectorTypedDict(TypedDict, total=(True)):
    nodeSelectorTerms: Sequence[NodeSelectorTerm]


NodeSelectorUnion = Union[NodeSelector, NodeSelectorTypedDict]


@attr.s(kw_only=True)
class NodeSelectorRequirement(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist', 'Gt', 'Lt'] = attr.ib(metadata={'yaml_name': 'operator'})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'values'}, default=OMIT)


class NodeSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class NodeSelectorRequirementTypedDict(NodeSelectorRequirementOptionalTypedDict, total=(True)):
    key: str
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist', 'Gt', 'Lt']


NodeSelectorRequirementUnion = Union[NodeSelectorRequirement, NodeSelectorRequirementTypedDict]


@attr.s(kw_only=True)
class NodeSelectorTerm(K8sObject):
    matchExpressions: Union[None, OmitEnum, Sequence[NodeSelectorRequirement]] = attr.ib(metadata={'yaml_name': 'matchExpressions'}, converter=optional_list_converter_NodeSelectorRequirement, default=OMIT)
    matchFields: Union[None, OmitEnum, Sequence[NodeSelectorRequirement]] = attr.ib(metadata={'yaml_name': 'matchFields'}, converter=optional_list_converter_NodeSelectorRequirement, default=OMIT)


class NodeSelectorTermTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[NodeSelectorRequirement]
    matchFields: Sequence[NodeSelectorRequirement]


NodeSelectorTermUnion = Union[NodeSelectorTerm, NodeSelectorTermTypedDict]


@attr.s(kw_only=True)
class NodeSpec(K8sObject):
    configSource: Union[None, OmitEnum, NodeConfigSource] = attr.ib(metadata={'yaml_name': 'configSource'}, converter=optional_converter_NodeConfigSource, default=OMIT)
    externalID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'externalID'}, default=OMIT)
    podCIDR: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'podCIDR'}, default=OMIT)
    podCIDRs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'podCIDRs'}, default=OMIT)
    providerID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'providerID'}, default=OMIT)
    taints: Union[None, OmitEnum, Sequence[Taint]] = attr.ib(metadata={'yaml_name': 'taints'}, converter=optional_list_converter_Taint, default=OMIT)
    unschedulable: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'unschedulable'}, default=OMIT)


class NodeSpecTypedDict(TypedDict, total=(False)):
    configSource: NodeConfigSource
    externalID: str
    podCIDR: str
    podCIDRs: Sequence[str]
    providerID: str
    taints: Sequence[Taint]
    unschedulable: bool


NodeSpecUnion = Union[NodeSpec, NodeSpecTypedDict]


@attr.s(kw_only=True)
class NodeStatus(K8sObject):
    addresses: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.NodeAddressItem]] = attr.ib(metadata={'yaml_name': 'addresses', 'mlist_key': 'type'}, converter=optional_mlist_converter_NodeAddressItem, default=OMIT)
    allocatable: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'allocatable'}, default=OMIT)
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'capacity'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.NodeConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_NodeConditionItem, default=OMIT)
    config: Union[None, OmitEnum, NodeConfigStatus] = attr.ib(metadata={'yaml_name': 'config'}, converter=optional_converter_NodeConfigStatus, default=OMIT)
    daemonEndpoints: Union[None, OmitEnum, NodeDaemonEndpoints] = attr.ib(metadata={'yaml_name': 'daemonEndpoints'}, converter=optional_converter_NodeDaemonEndpoints, default=OMIT)
    images: Union[None, OmitEnum, Sequence[ContainerImage]] = attr.ib(metadata={'yaml_name': 'images'}, converter=optional_list_converter_ContainerImage, default=OMIT)
    nodeInfo: Union[None, OmitEnum, NodeSystemInfo] = attr.ib(metadata={'yaml_name': 'nodeInfo'}, converter=optional_converter_NodeSystemInfo, default=OMIT)
    phase: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'phase'}, default=OMIT)
    volumesAttached: Union[None, OmitEnum, Sequence[AttachedVolume]] = attr.ib(metadata={'yaml_name': 'volumesAttached'}, converter=optional_list_converter_AttachedVolume, default=OMIT)
    volumesInUse: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'volumesInUse'}, default=OMIT)


class NodeStatusTypedDict(TypedDict, total=(False)):
    addresses: Mapping[str, kdsl.core.v1.NodeAddressItem]
    allocatable: Mapping[str, str]
    capacity: Mapping[str, str]
    conditions: Mapping[str, kdsl.core.v1.NodeConditionItem]
    config: NodeConfigStatus
    daemonEndpoints: NodeDaemonEndpoints
    images: Sequence[ContainerImage]
    nodeInfo: NodeSystemInfo
    phase: str
    volumesAttached: Sequence[AttachedVolume]
    volumesInUse: Sequence[str]


NodeStatusUnion = Union[NodeStatus, NodeStatusTypedDict]


@attr.s(kw_only=True)
class NodeSystemInfo(K8sObject):
    architecture: str = attr.ib(metadata={'yaml_name': 'architecture'})
    bootID: str = attr.ib(metadata={'yaml_name': 'bootID'})
    containerRuntimeVersion: str = attr.ib(metadata={'yaml_name': 'containerRuntimeVersion'})
    kernelVersion: str = attr.ib(metadata={'yaml_name': 'kernelVersion'})
    kubeProxyVersion: str = attr.ib(metadata={'yaml_name': 'kubeProxyVersion'})
    kubeletVersion: str = attr.ib(metadata={'yaml_name': 'kubeletVersion'})
    machineID: str = attr.ib(metadata={'yaml_name': 'machineID'})
    operatingSystem: str = attr.ib(metadata={'yaml_name': 'operatingSystem'})
    osImage: str = attr.ib(metadata={'yaml_name': 'osImage'})
    systemUUID: str = attr.ib(metadata={'yaml_name': 'systemUUID'})


class NodeSystemInfoTypedDict(TypedDict, total=(True)):
    architecture: str
    bootID: str
    containerRuntimeVersion: str
    kernelVersion: str
    kubeProxyVersion: str
    kubeletVersion: str
    machineID: str
    operatingSystem: str
    osImage: str
    systemUUID: str


NodeSystemInfoUnion = Union[NodeSystemInfo, NodeSystemInfoTypedDict]


@attr.s(kw_only=True)
class ObjectFieldSelector(K8sObject):
    fieldPath: str = attr.ib(metadata={'yaml_name': 'fieldPath'})
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)


class ObjectFieldSelectorOptionalTypedDict(TypedDict, total=(False)):
    apiVersion: str


class ObjectFieldSelectorTypedDict(ObjectFieldSelectorOptionalTypedDict, total=(True)):
    fieldPath: str


ObjectFieldSelectorUnion = Union[ObjectFieldSelector, ObjectFieldSelectorTypedDict]


@attr.s(kw_only=True)
class ObjectMeta(K8sObject):
    annotations: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'annotations'}, default=OMIT)
    clusterName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'clusterName'}, default=OMIT)
    creationTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'creationTimestamp'}, default=OMIT)
    deletionGracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'deletionGracePeriodSeconds'}, default=OMIT)
    deletionTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'deletionTimestamp'}, default=OMIT)
    finalizers: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'finalizers'}, default=OMIT)
    generateName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'generateName'}, default=OMIT)
    generation: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'generation'}, default=OMIT)
    labels: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'labels'}, default=OMIT)
    managedFields: Union[None, OmitEnum, Sequence[ManagedFieldsEntry]] = attr.ib(metadata={'yaml_name': 'managedFields'}, converter=optional_list_converter_ManagedFieldsEntry, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    ownerReferences: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.OwnerReferenceItem]] = attr.ib(metadata={'yaml_name': 'ownerReferences', 'mlist_key': 'uid'}, converter=optional_mlist_converter_OwnerReferenceItem, default=OMIT)
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resourceVersion'}, default=OMIT)
    selfLink: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'selfLink'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)


class ObjectMetaTypedDict(TypedDict, total=(False)):
    annotations: Mapping[str, str]
    clusterName: str
    creationTimestamp: str
    deletionGracePeriodSeconds: int
    deletionTimestamp: str
    finalizers: Sequence[str]
    generateName: str
    generation: int
    labels: Mapping[str, str]
    managedFields: Sequence[ManagedFieldsEntry]
    name: str
    namespace: str
    ownerReferences: Mapping[str, kdsl.core.v1.OwnerReferenceItem]
    resourceVersion: str
    selfLink: str
    uid: str


ObjectMetaUnion = Union[ObjectMeta, ObjectMetaTypedDict]


@attr.s(kw_only=True)
class ObjectReference(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    fieldPath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fieldPath'}, default=OMIT)
    kind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'kind'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resourceVersion'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)


class ObjectReferenceTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldPath: str
    kind: str
    name: str
    namespace: str
    resourceVersion: str
    uid: str


ObjectReferenceUnion = Union[ObjectReference, ObjectReferenceTypedDict]


@attr.s(kw_only=True)
class ObjectReferenceItem(K8sObject):
    apiVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiVersion'}, default=OMIT)
    fieldPath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fieldPath'}, default=OMIT)
    kind: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'kind'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resourceVersion'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)


class ObjectReferenceItemTypedDict(TypedDict, total=(False)):
    apiVersion: str
    fieldPath: str
    kind: str
    namespace: str
    resourceVersion: str
    uid: str


ObjectReferenceItemUnion = Union[ObjectReferenceItem, ObjectReferenceItemTypedDict]


@attr.s(kw_only=True)
class OwnerReferenceItem(K8sObject):
    apiVersion: str = attr.ib(metadata={'yaml_name': 'apiVersion'})
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    blockOwnerDeletion: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'blockOwnerDeletion'}, default=OMIT)
    controller: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'controller'}, default=OMIT)


class OwnerReferenceItemOptionalTypedDict(TypedDict, total=(False)):
    blockOwnerDeletion: bool
    controller: bool


class OwnerReferenceItemTypedDict(OwnerReferenceItemOptionalTypedDict, total=(True)):
    apiVersion: str
    kind: str
    name: str


OwnerReferenceItemUnion = Union[OwnerReferenceItem, OwnerReferenceItemTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastProbeTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastProbeTime'}, default=OMIT)
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class PersistentVolumeClaimConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class PersistentVolumeClaimConditionItemTypedDict(PersistentVolumeClaimConditionItemOptionalTypedDict, total=(True)):
    status: str


PersistentVolumeClaimConditionItemUnion = Union[PersistentVolumeClaimConditionItem, PersistentVolumeClaimConditionItemTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimSpec(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'accessModes'}, default=OMIT)
    dataSource: Union[None, OmitEnum, TypedLocalObjectReference] = attr.ib(metadata={'yaml_name': 'dataSource'}, converter=optional_converter_TypedLocalObjectReference, default=OMIT)
    dataSourceRef: Union[None, OmitEnum, TypedLocalObjectReference] = attr.ib(metadata={'yaml_name': 'dataSourceRef'}, converter=optional_converter_TypedLocalObjectReference, default=OMIT)
    resources: Union[None, OmitEnum, ResourceRequirements] = attr.ib(metadata={'yaml_name': 'resources'}, converter=optional_converter_ResourceRequirements, default=OMIT)
    selector: Union[None, OmitEnum, LabelSelector] = attr.ib(metadata={'yaml_name': 'selector'}, converter=optional_converter_LabelSelector, default=OMIT)
    storageClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storageClassName'}, default=OMIT)
    volumeMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeMode'}, default=OMIT)
    volumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeName'}, default=OMIT)


class PersistentVolumeClaimSpecTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    dataSource: TypedLocalObjectReference
    dataSourceRef: TypedLocalObjectReference
    resources: ResourceRequirements
    selector: LabelSelector
    storageClassName: str
    volumeMode: str
    volumeName: str


PersistentVolumeClaimSpecUnion = Union[PersistentVolumeClaimSpec, PersistentVolumeClaimSpecTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimStatus(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'accessModes'}, default=OMIT)
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'capacity'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_PersistentVolumeClaimConditionItem, default=OMIT)
    phase: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'phase'}, default=OMIT)


class PersistentVolumeClaimStatusTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    capacity: Mapping[str, str]
    conditions: Mapping[str, kdsl.core.v1.PersistentVolumeClaimConditionItem]
    phase: str


PersistentVolumeClaimStatusUnion = Union[PersistentVolumeClaimStatus, PersistentVolumeClaimStatusTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimTemplate(K8sObject):
    spec: PersistentVolumeClaimSpec = attr.ib(metadata={'yaml_name': 'spec'}, converter=required_converter_PersistentVolumeClaimSpec)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)


class PersistentVolumeClaimTemplateOptionalTypedDict(TypedDict, total=(False)):
    metadata: ObjectMeta


class PersistentVolumeClaimTemplateTypedDict(PersistentVolumeClaimTemplateOptionalTypedDict, total=(True)):
    spec: PersistentVolumeClaimSpec


PersistentVolumeClaimTemplateUnion = Union[PersistentVolumeClaimTemplate, PersistentVolumeClaimTemplateTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeClaimVolumeSource(K8sObject):
    claimName: str = attr.ib(metadata={'yaml_name': 'claimName'})
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class PersistentVolumeClaimVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    readOnly: bool


class PersistentVolumeClaimVolumeSourceTypedDict(PersistentVolumeClaimVolumeSourceOptionalTypedDict, total=(True)):
    claimName: str


PersistentVolumeClaimVolumeSourceUnion = Union[PersistentVolumeClaimVolumeSource, PersistentVolumeClaimVolumeSourceTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeSpec(K8sObject):
    accessModes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'accessModes'}, default=OMIT)
    awsElasticBlockStore: Union[None, OmitEnum, AWSElasticBlockStoreVolumeSource] = attr.ib(metadata={'yaml_name': 'awsElasticBlockStore'}, converter=optional_converter_AWSElasticBlockStoreVolumeSource, default=OMIT)
    azureDisk: Union[None, OmitEnum, AzureDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'azureDisk'}, converter=optional_converter_AzureDiskVolumeSource, default=OMIT)
    azureFile: Union[None, OmitEnum, AzureFilePersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'azureFile'}, converter=optional_converter_AzureFilePersistentVolumeSource, default=OMIT)
    capacity: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'capacity'}, default=OMIT)
    cephfs: Union[None, OmitEnum, CephFSPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'cephfs'}, converter=optional_converter_CephFSPersistentVolumeSource, default=OMIT)
    cinder: Union[None, OmitEnum, CinderPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'cinder'}, converter=optional_converter_CinderPersistentVolumeSource, default=OMIT)
    claimRef: Union[None, OmitEnum, ObjectReference] = attr.ib(metadata={'yaml_name': 'claimRef'}, converter=optional_converter_ObjectReference, default=OMIT)
    csi: Union[None, OmitEnum, CSIPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'csi'}, converter=optional_converter_CSIPersistentVolumeSource, default=OMIT)
    fc: Union[None, OmitEnum, FCVolumeSource] = attr.ib(metadata={'yaml_name': 'fc'}, converter=optional_converter_FCVolumeSource, default=OMIT)
    flexVolume: Union[None, OmitEnum, FlexPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'flexVolume'}, converter=optional_converter_FlexPersistentVolumeSource, default=OMIT)
    flocker: Union[None, OmitEnum, FlockerVolumeSource] = attr.ib(metadata={'yaml_name': 'flocker'}, converter=optional_converter_FlockerVolumeSource, default=OMIT)
    gcePersistentDisk: Union[None, OmitEnum, GCEPersistentDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'gcePersistentDisk'}, converter=optional_converter_GCEPersistentDiskVolumeSource, default=OMIT)
    glusterfs: Union[None, OmitEnum, GlusterfsPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'glusterfs'}, converter=optional_converter_GlusterfsPersistentVolumeSource, default=OMIT)
    hostPath: Union[None, OmitEnum, HostPathVolumeSource] = attr.ib(metadata={'yaml_name': 'hostPath'}, converter=optional_converter_HostPathVolumeSource, default=OMIT)
    iscsi: Union[None, OmitEnum, ISCSIPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'iscsi'}, converter=optional_converter_ISCSIPersistentVolumeSource, default=OMIT)
    local: Union[None, OmitEnum, LocalVolumeSource] = attr.ib(metadata={'yaml_name': 'local'}, converter=optional_converter_LocalVolumeSource, default=OMIT)
    mountOptions: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'mountOptions'}, default=OMIT)
    nfs: Union[None, OmitEnum, NFSVolumeSource] = attr.ib(metadata={'yaml_name': 'nfs'}, converter=optional_converter_NFSVolumeSource, default=OMIT)
    nodeAffinity: Union[None, OmitEnum, VolumeNodeAffinity] = attr.ib(metadata={'yaml_name': 'nodeAffinity'}, converter=optional_converter_VolumeNodeAffinity, default=OMIT)
    persistentVolumeReclaimPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'persistentVolumeReclaimPolicy'}, default=OMIT)
    photonPersistentDisk: Union[None, OmitEnum, PhotonPersistentDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'photonPersistentDisk'}, converter=optional_converter_PhotonPersistentDiskVolumeSource, default=OMIT)
    portworxVolume: Union[None, OmitEnum, PortworxVolumeSource] = attr.ib(metadata={'yaml_name': 'portworxVolume'}, converter=optional_converter_PortworxVolumeSource, default=OMIT)
    quobyte: Union[None, OmitEnum, QuobyteVolumeSource] = attr.ib(metadata={'yaml_name': 'quobyte'}, converter=optional_converter_QuobyteVolumeSource, default=OMIT)
    rbd: Union[None, OmitEnum, RBDPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'rbd'}, converter=optional_converter_RBDPersistentVolumeSource, default=OMIT)
    scaleIO: Union[None, OmitEnum, ScaleIOPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'scaleIO'}, converter=optional_converter_ScaleIOPersistentVolumeSource, default=OMIT)
    storageClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storageClassName'}, default=OMIT)
    storageos: Union[None, OmitEnum, StorageOSPersistentVolumeSource] = attr.ib(metadata={'yaml_name': 'storageos'}, converter=optional_converter_StorageOSPersistentVolumeSource, default=OMIT)
    volumeMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeMode'}, default=OMIT)
    vsphereVolume: Union[None, OmitEnum, VsphereVirtualDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'vsphereVolume'}, converter=optional_converter_VsphereVirtualDiskVolumeSource, default=OMIT)


class PersistentVolumeSpecTypedDict(TypedDict, total=(False)):
    accessModes: Sequence[str]
    awsElasticBlockStore: AWSElasticBlockStoreVolumeSource
    azureDisk: AzureDiskVolumeSource
    azureFile: AzureFilePersistentVolumeSource
    capacity: Mapping[str, str]
    cephfs: CephFSPersistentVolumeSource
    cinder: CinderPersistentVolumeSource
    claimRef: ObjectReference
    csi: CSIPersistentVolumeSource
    fc: FCVolumeSource
    flexVolume: FlexPersistentVolumeSource
    flocker: FlockerVolumeSource
    gcePersistentDisk: GCEPersistentDiskVolumeSource
    glusterfs: GlusterfsPersistentVolumeSource
    hostPath: HostPathVolumeSource
    iscsi: ISCSIPersistentVolumeSource
    local: LocalVolumeSource
    mountOptions: Sequence[str]
    nfs: NFSVolumeSource
    nodeAffinity: VolumeNodeAffinity
    persistentVolumeReclaimPolicy: str
    photonPersistentDisk: PhotonPersistentDiskVolumeSource
    portworxVolume: PortworxVolumeSource
    quobyte: QuobyteVolumeSource
    rbd: RBDPersistentVolumeSource
    scaleIO: ScaleIOPersistentVolumeSource
    storageClassName: str
    storageos: StorageOSPersistentVolumeSource
    volumeMode: str
    vsphereVolume: VsphereVirtualDiskVolumeSource


PersistentVolumeSpecUnion = Union[PersistentVolumeSpec, PersistentVolumeSpecTypedDict]


@attr.s(kw_only=True)
class PersistentVolumeStatus(K8sObject):
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    phase: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'phase'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class PersistentVolumeStatusTypedDict(TypedDict, total=(False)):
    message: str
    phase: str
    reason: str


PersistentVolumeStatusUnion = Union[PersistentVolumeStatus, PersistentVolumeStatusTypedDict]


@attr.s(kw_only=True)
class PhotonPersistentDiskVolumeSource(K8sObject):
    pdID: str = attr.ib(metadata={'yaml_name': 'pdID'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)


class PhotonPersistentDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str


class PhotonPersistentDiskVolumeSourceTypedDict(PhotonPersistentDiskVolumeSourceOptionalTypedDict, total=(True)):
    pdID: str


PhotonPersistentDiskVolumeSourceUnion = Union[PhotonPersistentDiskVolumeSource, PhotonPersistentDiskVolumeSourceTypedDict]


@attr.s(kw_only=True)
class PodAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, Sequence[WeightedPodAffinityTerm]] = attr.ib(metadata={'yaml_name': 'preferredDuringSchedulingIgnoredDuringExecution'}, converter=optional_list_converter_WeightedPodAffinityTerm, default=OMIT)
    requiredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, Sequence[PodAffinityTerm]] = attr.ib(metadata={'yaml_name': 'requiredDuringSchedulingIgnoredDuringExecution'}, converter=optional_list_converter_PodAffinityTerm, default=OMIT)


class PodAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[WeightedPodAffinityTerm]
    requiredDuringSchedulingIgnoredDuringExecution: Sequence[PodAffinityTerm]


PodAffinityUnion = Union[PodAffinity, PodAffinityTypedDict]


@attr.s(kw_only=True)
class PodAffinityTerm(K8sObject):
    topologyKey: str = attr.ib(metadata={'yaml_name': 'topologyKey'})
    labelSelector: Union[None, OmitEnum, LabelSelector] = attr.ib(metadata={'yaml_name': 'labelSelector'}, converter=optional_converter_LabelSelector, default=OMIT)
    namespaceSelector: Union[None, OmitEnum, LabelSelector] = attr.ib(metadata={'yaml_name': 'namespaceSelector'}, converter=optional_converter_LabelSelector, default=OMIT)
    namespaces: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'namespaces'}, default=OMIT)


class PodAffinityTermOptionalTypedDict(TypedDict, total=(False)):
    labelSelector: LabelSelector
    namespaceSelector: LabelSelector
    namespaces: Sequence[str]


class PodAffinityTermTypedDict(PodAffinityTermOptionalTypedDict, total=(True)):
    topologyKey: str


PodAffinityTermUnion = Union[PodAffinityTerm, PodAffinityTermTypedDict]


@attr.s(kw_only=True)
class PodAntiAffinity(K8sObject):
    preferredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, Sequence[WeightedPodAffinityTerm]] = attr.ib(metadata={'yaml_name': 'preferredDuringSchedulingIgnoredDuringExecution'}, converter=optional_list_converter_WeightedPodAffinityTerm, default=OMIT)
    requiredDuringSchedulingIgnoredDuringExecution: Union[None, OmitEnum, Sequence[PodAffinityTerm]] = attr.ib(metadata={'yaml_name': 'requiredDuringSchedulingIgnoredDuringExecution'}, converter=optional_list_converter_PodAffinityTerm, default=OMIT)


class PodAntiAffinityTypedDict(TypedDict, total=(False)):
    preferredDuringSchedulingIgnoredDuringExecution: Sequence[WeightedPodAffinityTerm]
    requiredDuringSchedulingIgnoredDuringExecution: Sequence[PodAffinityTerm]


PodAntiAffinityUnion = Union[PodAntiAffinity, PodAntiAffinityTypedDict]


@attr.s(kw_only=True)
class PodConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastProbeTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastProbeTime'}, default=OMIT)
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class PodConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastProbeTime: str
    lastTransitionTime: str
    message: str
    reason: str


class PodConditionItemTypedDict(PodConditionItemOptionalTypedDict, total=(True)):
    status: str


PodConditionItemUnion = Union[PodConditionItem, PodConditionItemTypedDict]


@attr.s(kw_only=True)
class PodDNSConfig(K8sObject):
    nameservers: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'nameservers'}, default=OMIT)
    options: Union[None, OmitEnum, Sequence[PodDNSConfigOption]] = attr.ib(metadata={'yaml_name': 'options'}, converter=optional_list_converter_PodDNSConfigOption, default=OMIT)
    searches: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'searches'}, default=OMIT)


class PodDNSConfigTypedDict(TypedDict, total=(False)):
    nameservers: Sequence[str]
    options: Sequence[PodDNSConfigOption]
    searches: Sequence[str]


PodDNSConfigUnion = Union[PodDNSConfig, PodDNSConfigTypedDict]


@attr.s(kw_only=True)
class PodDNSConfigOption(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)


class PodDNSConfigOptionTypedDict(TypedDict, total=(False)):
    name: str
    value: str


PodDNSConfigOptionUnion = Union[PodDNSConfigOption, PodDNSConfigOptionTypedDict]


@attr.s(kw_only=True)
class PodIP(K8sObject):
    ip: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'ip'}, default=OMIT)


class PodIPTypedDict(TypedDict, total=(False)):
    ip: str


PodIPUnion = Union[PodIP, PodIPTypedDict]


@attr.s(kw_only=True)
class PodReadinessGate(K8sObject):
    conditionType: str = attr.ib(metadata={'yaml_name': 'conditionType'})


class PodReadinessGateTypedDict(TypedDict, total=(True)):
    conditionType: str


PodReadinessGateUnion = Union[PodReadinessGate, PodReadinessGateTypedDict]


@attr.s(kw_only=True)
class PodSecurityContext(K8sObject):
    fsGroup: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'fsGroup'}, default=OMIT)
    fsGroupChangePolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsGroupChangePolicy'}, default=OMIT)
    runAsGroup: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'runAsGroup'}, default=OMIT)
    runAsNonRoot: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'runAsNonRoot'}, default=OMIT)
    runAsUser: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'runAsUser'}, default=OMIT)
    seLinuxOptions: Union[None, OmitEnum, SELinuxOptions] = attr.ib(metadata={'yaml_name': 'seLinuxOptions'}, converter=optional_converter_SELinuxOptions, default=OMIT)
    seccompProfile: Union[None, OmitEnum, SeccompProfile] = attr.ib(metadata={'yaml_name': 'seccompProfile'}, converter=optional_converter_SeccompProfile, default=OMIT)
    supplementalGroups: Union[None, OmitEnum, Sequence[int]] = attr.ib(metadata={'yaml_name': 'supplementalGroups'}, default=OMIT)
    sysctls: Union[None, OmitEnum, Sequence[Sysctl]] = attr.ib(metadata={'yaml_name': 'sysctls'}, converter=optional_list_converter_Sysctl, default=OMIT)
    windowsOptions: Union[None, OmitEnum, WindowsSecurityContextOptions] = attr.ib(metadata={'yaml_name': 'windowsOptions'}, converter=optional_converter_WindowsSecurityContextOptions, default=OMIT)


class PodSecurityContextTypedDict(TypedDict, total=(False)):
    fsGroup: int
    fsGroupChangePolicy: str
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: SELinuxOptions
    seccompProfile: SeccompProfile
    supplementalGroups: Sequence[int]
    sysctls: Sequence[Sysctl]
    windowsOptions: WindowsSecurityContextOptions


PodSecurityContextUnion = Union[PodSecurityContext, PodSecurityContextTypedDict]


@attr.s(kw_only=True)
class PodSpec(K8sObject):
    containers: Mapping[str, kdsl.core.v1.ContainerItem] = attr.ib(metadata={'yaml_name': 'containers', 'mlist_key': 'name'}, converter=required_mlist_converter_ContainerItem)
    activeDeadlineSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'activeDeadlineSeconds'}, default=OMIT)
    affinity: Union[None, OmitEnum, Affinity] = attr.ib(metadata={'yaml_name': 'affinity'}, converter=optional_converter_Affinity, default=OMIT)
    automountServiceAccountToken: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'automountServiceAccountToken'}, default=OMIT)
    dnsConfig: Union[None, OmitEnum, PodDNSConfig] = attr.ib(metadata={'yaml_name': 'dnsConfig'}, converter=optional_converter_PodDNSConfig, default=OMIT)
    dnsPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'dnsPolicy'}, default=OMIT)
    enableServiceLinks: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'enableServiceLinks'}, default=OMIT)
    ephemeralContainers: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.EphemeralContainerItem]] = attr.ib(metadata={'yaml_name': 'ephemeralContainers', 'mlist_key': 'name'}, converter=optional_mlist_converter_EphemeralContainerItem, default=OMIT)
    hostAliases: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.HostAliasItem]] = attr.ib(metadata={'yaml_name': 'hostAliases', 'mlist_key': 'ip'}, converter=optional_mlist_converter_HostAliasItem, default=OMIT)
    hostIPC: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostIPC'}, default=OMIT)
    hostNetwork: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostNetwork'}, default=OMIT)
    hostPID: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostPID'}, default=OMIT)
    hostname: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostname'}, default=OMIT)
    imagePullSecrets: Union[None, OmitEnum, Sequence[LocalObjectReference]] = attr.ib(metadata={'yaml_name': 'imagePullSecrets'}, converter=optional_list_converter_LocalObjectReference, default=OMIT)
    initContainers: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.ContainerItem]] = attr.ib(metadata={'yaml_name': 'initContainers', 'mlist_key': 'name'}, converter=optional_mlist_converter_ContainerItem, default=OMIT)
    nodeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'nodeName'}, default=OMIT)
    nodeSelector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'nodeSelector'}, default=OMIT)
    overhead: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'overhead'}, default=OMIT)
    preemptionPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'preemptionPolicy'}, default=OMIT)
    priority: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'priority'}, default=OMIT)
    priorityClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'priorityClassName'}, default=OMIT)
    readinessGates: Union[None, OmitEnum, Sequence[PodReadinessGate]] = attr.ib(metadata={'yaml_name': 'readinessGates'}, converter=optional_list_converter_PodReadinessGate, default=OMIT)
    restartPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'restartPolicy'}, default=OMIT)
    runtimeClassName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'runtimeClassName'}, default=OMIT)
    schedulerName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'schedulerName'}, default=OMIT)
    securityContext: Union[None, OmitEnum, PodSecurityContext] = attr.ib(metadata={'yaml_name': 'securityContext'}, converter=optional_converter_PodSecurityContext, default=OMIT)
    serviceAccount: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'serviceAccount'}, default=OMIT)
    serviceAccountName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'serviceAccountName'}, default=OMIT)
    setHostnameAsFQDN: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'setHostnameAsFQDN'}, default=OMIT)
    shareProcessNamespace: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'shareProcessNamespace'}, default=OMIT)
    subdomain: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'subdomain'}, default=OMIT)
    terminationGracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'terminationGracePeriodSeconds'}, default=OMIT)
    tolerations: Union[None, OmitEnum, Sequence[Toleration]] = attr.ib(metadata={'yaml_name': 'tolerations'}, converter=optional_list_converter_Toleration, default=OMIT)
    topologySpreadConstraints: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.TopologySpreadConstraintItem]] = attr.ib(metadata={'yaml_name': 'topologySpreadConstraints', 'mlist_key': 'topologyKey'}, converter=optional_mlist_converter_TopologySpreadConstraintItem, default=OMIT)
    volumes: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.VolumeItem]] = attr.ib(metadata={'yaml_name': 'volumes', 'mlist_key': 'name'}, converter=optional_mlist_converter_VolumeItem, default=OMIT)


class PodSpecOptionalTypedDict(TypedDict, total=(False)):
    activeDeadlineSeconds: int
    affinity: Affinity
    automountServiceAccountToken: bool
    dnsConfig: PodDNSConfig
    dnsPolicy: str
    enableServiceLinks: bool
    ephemeralContainers: Mapping[str, kdsl.core.v1.EphemeralContainerItem]
    hostAliases: Mapping[str, kdsl.core.v1.HostAliasItem]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostname: str
    imagePullSecrets: Sequence[LocalObjectReference]
    initContainers: Mapping[str, kdsl.core.v1.ContainerItem]
    nodeName: str
    nodeSelector: Mapping[str, str]
    overhead: Mapping[str, str]
    preemptionPolicy: str
    priority: int
    priorityClassName: str
    readinessGates: Sequence[PodReadinessGate]
    restartPolicy: str
    runtimeClassName: str
    schedulerName: str
    securityContext: PodSecurityContext
    serviceAccount: str
    serviceAccountName: str
    setHostnameAsFQDN: bool
    shareProcessNamespace: bool
    subdomain: str
    terminationGracePeriodSeconds: int
    tolerations: Sequence[Toleration]
    topologySpreadConstraints: Mapping[str, kdsl.core.v1.TopologySpreadConstraintItem]
    volumes: Mapping[str, kdsl.core.v1.VolumeItem]


class PodSpecTypedDict(PodSpecOptionalTypedDict, total=(True)):
    containers: Mapping[str, kdsl.core.v1.ContainerItem]


PodSpecUnion = Union[PodSpec, PodSpecTypedDict]


@attr.s(kw_only=True)
class PodStatus(K8sObject):
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.PodConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_PodConditionItem, default=OMIT)
    containerStatuses: Union[None, OmitEnum, Sequence[ContainerStatus]] = attr.ib(metadata={'yaml_name': 'containerStatuses'}, converter=optional_list_converter_ContainerStatus, default=OMIT)
    ephemeralContainerStatuses: Union[None, OmitEnum, Sequence[ContainerStatus]] = attr.ib(metadata={'yaml_name': 'ephemeralContainerStatuses'}, converter=optional_list_converter_ContainerStatus, default=OMIT)
    hostIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'hostIP'}, default=OMIT)
    initContainerStatuses: Union[None, OmitEnum, Sequence[ContainerStatus]] = attr.ib(metadata={'yaml_name': 'initContainerStatuses'}, converter=optional_list_converter_ContainerStatus, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    nominatedNodeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'nominatedNodeName'}, default=OMIT)
    phase: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'phase'}, default=OMIT)
    podIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'podIP'}, default=OMIT)
    podIPs: Union[None, OmitEnum, Sequence[PodIP]] = attr.ib(metadata={'yaml_name': 'podIPs'}, converter=optional_list_converter_PodIP, default=OMIT)
    qosClass: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'qosClass'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    startTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'startTime'}, default=OMIT)


class PodStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.PodConditionItem]
    containerStatuses: Sequence[ContainerStatus]
    ephemeralContainerStatuses: Sequence[ContainerStatus]
    hostIP: str
    initContainerStatuses: Sequence[ContainerStatus]
    message: str
    nominatedNodeName: str
    phase: str
    podIP: str
    podIPs: Sequence[PodIP]
    qosClass: str
    reason: str
    startTime: str


PodStatusUnion = Union[PodStatus, PodStatusTypedDict]


@attr.s(kw_only=True)
class PodTemplateSpec(K8sObject):
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PodSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PodSpec, default=OMIT)


class PodTemplateSpecTypedDict(TypedDict, total=(False)):
    metadata: ObjectMeta
    spec: PodSpec


PodTemplateSpecUnion = Union[PodTemplateSpec, PodTemplateSpecTypedDict]


@attr.s(kw_only=True)
class PortStatus(K8sObject):
    port: int = attr.ib(metadata={'yaml_name': 'port'})
    protocol: str = attr.ib(metadata={'yaml_name': 'protocol'})
    error: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'error'}, default=OMIT)


class PortStatusOptionalTypedDict(TypedDict, total=(False)):
    error: str


class PortStatusTypedDict(PortStatusOptionalTypedDict, total=(True)):
    port: int
    protocol: str


PortStatusUnion = Union[PortStatus, PortStatusTypedDict]


@attr.s(kw_only=True)
class PortworxVolumeSource(K8sObject):
    volumeID: str = attr.ib(metadata={'yaml_name': 'volumeID'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)


class PortworxVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool


class PortworxVolumeSourceTypedDict(PortworxVolumeSourceOptionalTypedDict, total=(True)):
    volumeID: str


PortworxVolumeSourceUnion = Union[PortworxVolumeSource, PortworxVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Preconditions(K8sObject):
    resourceVersion: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'resourceVersion'}, default=OMIT)
    uid: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'uid'}, default=OMIT)


class PreconditionsTypedDict(TypedDict, total=(False)):
    resourceVersion: str
    uid: str


PreconditionsUnion = Union[Preconditions, PreconditionsTypedDict]


@attr.s(kw_only=True)
class PreferredSchedulingTerm(K8sObject):
    preference: NodeSelectorTerm = attr.ib(metadata={'yaml_name': 'preference'}, converter=required_converter_NodeSelectorTerm)
    weight: int = attr.ib(metadata={'yaml_name': 'weight'})


class PreferredSchedulingTermTypedDict(TypedDict, total=(True)):
    preference: NodeSelectorTerm
    weight: int


PreferredSchedulingTermUnion = Union[PreferredSchedulingTerm, PreferredSchedulingTermTypedDict]


@attr.s(kw_only=True)
class Probe(K8sObject):
    exec: Union[None, OmitEnum, ExecAction] = attr.ib(metadata={'yaml_name': 'exec'}, converter=optional_converter_ExecAction, default=OMIT)
    failureThreshold: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'failureThreshold'}, default=OMIT)
    httpGet: Union[None, OmitEnum, HTTPGetAction] = attr.ib(metadata={'yaml_name': 'httpGet'}, converter=optional_converter_HTTPGetAction, default=OMIT)
    initialDelaySeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'initialDelaySeconds'}, default=OMIT)
    periodSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'periodSeconds'}, default=OMIT)
    successThreshold: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'successThreshold'}, default=OMIT)
    tcpSocket: Union[None, OmitEnum, TCPSocketAction] = attr.ib(metadata={'yaml_name': 'tcpSocket'}, converter=optional_converter_TCPSocketAction, default=OMIT)
    terminationGracePeriodSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'terminationGracePeriodSeconds'}, default=OMIT)
    timeoutSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'timeoutSeconds'}, default=OMIT)


class ProbeTypedDict(TypedDict, total=(False)):
    exec: ExecAction
    failureThreshold: int
    httpGet: HTTPGetAction
    initialDelaySeconds: int
    periodSeconds: int
    successThreshold: int
    tcpSocket: TCPSocketAction
    terminationGracePeriodSeconds: int
    timeoutSeconds: int


ProbeUnion = Union[Probe, ProbeTypedDict]


@attr.s(kw_only=True)
class ProjectedVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'defaultMode'}, default=OMIT)
    sources: Union[None, OmitEnum, Sequence[VolumeProjection]] = attr.ib(metadata={'yaml_name': 'sources'}, converter=optional_list_converter_VolumeProjection, default=OMIT)


class ProjectedVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    sources: Sequence[VolumeProjection]


ProjectedVolumeSourceUnion = Union[ProjectedVolumeSource, ProjectedVolumeSourceTypedDict]


@attr.s(kw_only=True)
class QuobyteVolumeSource(K8sObject):
    registry: str = attr.ib(metadata={'yaml_name': 'registry'})
    volume: str = attr.ib(metadata={'yaml_name': 'volume'})
    group: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'group'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    tenant: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'tenant'}, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class QuobyteVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    group: str
    readOnly: bool
    tenant: str
    user: str


class QuobyteVolumeSourceTypedDict(QuobyteVolumeSourceOptionalTypedDict, total=(True)):
    registry: str
    volume: str


QuobyteVolumeSourceUnion = Union[QuobyteVolumeSource, QuobyteVolumeSourceTypedDict]


@attr.s(kw_only=True)
class RBDPersistentVolumeSource(K8sObject):
    image: str = attr.ib(metadata={'yaml_name': 'image'})
    monitors: Sequence[str] = attr.ib(metadata={'yaml_name': 'monitors'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    keyring: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'keyring'}, default=OMIT)
    pool: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'pool'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, SecretReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_SecretReference, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class RBDPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    keyring: str
    pool: str
    readOnly: bool
    secretRef: SecretReference
    user: str


class RBDPersistentVolumeSourceTypedDict(RBDPersistentVolumeSourceOptionalTypedDict, total=(True)):
    image: str
    monitors: Sequence[str]


RBDPersistentVolumeSourceUnion = Union[RBDPersistentVolumeSource, RBDPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class RBDVolumeSource(K8sObject):
    image: str = attr.ib(metadata={'yaml_name': 'image'})
    monitors: Sequence[str] = attr.ib(metadata={'yaml_name': 'monitors'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    keyring: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'keyring'}, default=OMIT)
    pool: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'pool'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class RBDVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    keyring: str
    pool: str
    readOnly: bool
    secretRef: LocalObjectReference
    user: str


class RBDVolumeSourceTypedDict(RBDVolumeSourceOptionalTypedDict, total=(True)):
    image: str
    monitors: Sequence[str]


RBDVolumeSourceUnion = Union[RBDVolumeSource, RBDVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ReplicationControllerConditionItem(K8sObject):
    status: str = attr.ib(metadata={'yaml_name': 'status'})
    lastTransitionTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTransitionTime'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)


class ReplicationControllerConditionItemOptionalTypedDict(TypedDict, total=(False)):
    lastTransitionTime: str
    message: str
    reason: str


class ReplicationControllerConditionItemTypedDict(ReplicationControllerConditionItemOptionalTypedDict, total=(True)):
    status: str


ReplicationControllerConditionItemUnion = Union[ReplicationControllerConditionItem, ReplicationControllerConditionItemTypedDict]


@attr.s(kw_only=True)
class ReplicationControllerSpec(K8sObject):
    minReadySeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'minReadySeconds'}, default=OMIT)
    replicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'replicas'}, default=OMIT)
    selector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'selector'}, default=OMIT)
    template: Union[None, OmitEnum, PodTemplateSpec] = attr.ib(metadata={'yaml_name': 'template'}, converter=optional_converter_PodTemplateSpec, default=OMIT)


class ReplicationControllerSpecTypedDict(TypedDict, total=(False)):
    minReadySeconds: int
    replicas: int
    selector: Mapping[str, str]
    template: PodTemplateSpec


ReplicationControllerSpecUnion = Union[ReplicationControllerSpec, ReplicationControllerSpecTypedDict]


@attr.s(kw_only=True)
class ReplicationControllerStatus(K8sObject):
    replicas: int = attr.ib(metadata={'yaml_name': 'replicas'})
    availableReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'availableReplicas'}, default=OMIT)
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.ReplicationControllerConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_ReplicationControllerConditionItem, default=OMIT)
    fullyLabeledReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'fullyLabeledReplicas'}, default=OMIT)
    observedGeneration: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'observedGeneration'}, default=OMIT)
    readyReplicas: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'readyReplicas'}, default=OMIT)


class ReplicationControllerStatusOptionalTypedDict(TypedDict, total=(False)):
    availableReplicas: int
    conditions: Mapping[str, kdsl.core.v1.ReplicationControllerConditionItem]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int


class ReplicationControllerStatusTypedDict(ReplicationControllerStatusOptionalTypedDict, total=(True)):
    replicas: int


ReplicationControllerStatusUnion = Union[ReplicationControllerStatus, ReplicationControllerStatusTypedDict]


@attr.s(kw_only=True)
class ResourceFieldSelector(K8sObject):
    resource: str = attr.ib(metadata={'yaml_name': 'resource'})
    containerName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'containerName'}, default=OMIT)
    divisor: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'divisor'}, default=OMIT)


class ResourceFieldSelectorOptionalTypedDict(TypedDict, total=(False)):
    containerName: str
    divisor: str


class ResourceFieldSelectorTypedDict(ResourceFieldSelectorOptionalTypedDict, total=(True)):
    resource: str


ResourceFieldSelectorUnion = Union[ResourceFieldSelector, ResourceFieldSelectorTypedDict]


@attr.s(kw_only=True)
class ResourceQuotaSpec(K8sObject):
    hard: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'hard'}, default=OMIT)
    scopeSelector: Union[None, OmitEnum, ScopeSelector] = attr.ib(metadata={'yaml_name': 'scopeSelector'}, converter=optional_converter_ScopeSelector, default=OMIT)
    scopes: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'scopes'}, default=OMIT)


class ResourceQuotaSpecTypedDict(TypedDict, total=(False)):
    hard: Mapping[str, str]
    scopeSelector: ScopeSelector
    scopes: Sequence[str]


ResourceQuotaSpecUnion = Union[ResourceQuotaSpec, ResourceQuotaSpecTypedDict]


@attr.s(kw_only=True)
class ResourceQuotaStatus(K8sObject):
    hard: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'hard'}, default=OMIT)
    used: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'used'}, default=OMIT)


class ResourceQuotaStatusTypedDict(TypedDict, total=(False)):
    hard: Mapping[str, str]
    used: Mapping[str, str]


ResourceQuotaStatusUnion = Union[ResourceQuotaStatus, ResourceQuotaStatusTypedDict]


@attr.s(kw_only=True)
class ResourceRequirements(K8sObject):
    limits: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'limits'}, default=OMIT)
    requests: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'requests'}, default=OMIT)


class ResourceRequirementsTypedDict(TypedDict, total=(False)):
    limits: Mapping[str, str]
    requests: Mapping[str, str]


ResourceRequirementsUnion = Union[ResourceRequirements, ResourceRequirementsTypedDict]


@attr.s(kw_only=True)
class SELinuxOptions(K8sObject):
    level: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'level'}, default=OMIT)
    role: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'role'}, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)
    user: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'user'}, default=OMIT)


class SELinuxOptionsTypedDict(TypedDict, total=(False)):
    level: str
    role: str
    type: str
    user: str


SELinuxOptionsUnion = Union[SELinuxOptions, SELinuxOptionsTypedDict]


@attr.s(kw_only=True)
class ScaleIOPersistentVolumeSource(K8sObject):
    gateway: str = attr.ib(metadata={'yaml_name': 'gateway'})
    secretRef: SecretReference = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=required_converter_SecretReference)
    system: str = attr.ib(metadata={'yaml_name': 'system'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    protectionDomain: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protectionDomain'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    sslEnabled: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'sslEnabled'}, default=OMIT)
    storageMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storageMode'}, default=OMIT)
    storagePool: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storagePool'}, default=OMIT)
    volumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeName'}, default=OMIT)


class ScaleIOPersistentVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    protectionDomain: str
    readOnly: bool
    sslEnabled: bool
    storageMode: str
    storagePool: str
    volumeName: str


class ScaleIOPersistentVolumeSourceTypedDict(ScaleIOPersistentVolumeSourceOptionalTypedDict, total=(True)):
    gateway: str
    secretRef: SecretReference
    system: str


ScaleIOPersistentVolumeSourceUnion = Union[ScaleIOPersistentVolumeSource, ScaleIOPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ScaleIOVolumeSource(K8sObject):
    gateway: str = attr.ib(metadata={'yaml_name': 'gateway'})
    secretRef: LocalObjectReference = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=required_converter_LocalObjectReference)
    system: str = attr.ib(metadata={'yaml_name': 'system'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    protectionDomain: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protectionDomain'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    sslEnabled: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'sslEnabled'}, default=OMIT)
    storageMode: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storageMode'}, default=OMIT)
    storagePool: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storagePool'}, default=OMIT)
    volumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeName'}, default=OMIT)


class ScaleIOVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    protectionDomain: str
    readOnly: bool
    sslEnabled: bool
    storageMode: str
    storagePool: str
    volumeName: str


class ScaleIOVolumeSourceTypedDict(ScaleIOVolumeSourceOptionalTypedDict, total=(True)):
    gateway: str
    secretRef: LocalObjectReference
    system: str


ScaleIOVolumeSourceUnion = Union[ScaleIOVolumeSource, ScaleIOVolumeSourceTypedDict]


@attr.s(kw_only=True)
class ScopeSelector(K8sObject):
    matchExpressions: Union[None, OmitEnum, Sequence[ScopedResourceSelectorRequirement]] = attr.ib(metadata={'yaml_name': 'matchExpressions'}, converter=optional_list_converter_ScopedResourceSelectorRequirement, default=OMIT)


class ScopeSelectorTypedDict(TypedDict, total=(False)):
    matchExpressions: Sequence[ScopedResourceSelectorRequirement]


ScopeSelectorUnion = Union[ScopeSelector, ScopeSelectorTypedDict]


@attr.s(kw_only=True)
class ScopedResourceSelectorRequirement(K8sObject):
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist'] = attr.ib(metadata={'yaml_name': 'operator'})
    scopeName: str = attr.ib(metadata={'yaml_name': 'scopeName'})
    values: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'values'}, default=OMIT)


class ScopedResourceSelectorRequirementOptionalTypedDict(TypedDict, total=(False)):
    values: Sequence[str]


class ScopedResourceSelectorRequirementTypedDict(ScopedResourceSelectorRequirementOptionalTypedDict, total=(True)):
    operator: Literal['In', 'NotIn', 'Exists', 'DoesNotExist']
    scopeName: str


ScopedResourceSelectorRequirementUnion = Union[ScopedResourceSelectorRequirement, ScopedResourceSelectorRequirementTypedDict]


@attr.s(kw_only=True)
class SeccompProfile(K8sObject):
    type: str = attr.ib(metadata={'yaml_name': 'type'})
    localhostProfile: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'localhostProfile'}, default=OMIT)


class SeccompProfileOptionalTypedDict(TypedDict, total=(False)):
    localhostProfile: str


class SeccompProfileTypedDict(SeccompProfileOptionalTypedDict, total=(True)):
    type: str


SeccompProfileUnion = Union[SeccompProfile, SeccompProfileTypedDict]


@attr.s(kw_only=True)
class SecretEnvSource(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class SecretEnvSourceTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


SecretEnvSourceUnion = Union[SecretEnvSource, SecretEnvSourceTypedDict]


@attr.s(kw_only=True)
class SecretKeySelector(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class SecretKeySelectorOptionalTypedDict(TypedDict, total=(False)):
    name: str
    optional: bool


class SecretKeySelectorTypedDict(SecretKeySelectorOptionalTypedDict, total=(True)):
    key: str


SecretKeySelectorUnion = Union[SecretKeySelector, SecretKeySelectorTypedDict]


@attr.s(kw_only=True)
class SecretProjection(K8sObject):
    items: Union[None, OmitEnum, Sequence[KeyToPath]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_KeyToPath, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)


class SecretProjectionTypedDict(TypedDict, total=(False)):
    items: Sequence[KeyToPath]
    name: str
    optional: bool


SecretProjectionUnion = Union[SecretProjection, SecretProjectionTypedDict]


@attr.s(kw_only=True)
class SecretReference(K8sObject):
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    namespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'namespace'}, default=OMIT)


class SecretReferenceTypedDict(TypedDict, total=(False)):
    name: str
    namespace: str


SecretReferenceUnion = Union[SecretReference, SecretReferenceTypedDict]


@attr.s(kw_only=True)
class SecretVolumeSource(K8sObject):
    defaultMode: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'defaultMode'}, default=OMIT)
    items: Union[None, OmitEnum, Sequence[KeyToPath]] = attr.ib(metadata={'yaml_name': 'items'}, converter=optional_list_converter_KeyToPath, default=OMIT)
    optional: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'optional'}, default=OMIT)
    secretName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'secretName'}, default=OMIT)


class SecretVolumeSourceTypedDict(TypedDict, total=(False)):
    defaultMode: int
    items: Sequence[KeyToPath]
    optional: bool
    secretName: str


SecretVolumeSourceUnion = Union[SecretVolumeSource, SecretVolumeSourceTypedDict]


@attr.s(kw_only=True)
class SecurityContext(K8sObject):
    allowPrivilegeEscalation: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'allowPrivilegeEscalation'}, default=OMIT)
    capabilities: Union[None, OmitEnum, Capabilities] = attr.ib(metadata={'yaml_name': 'capabilities'}, converter=optional_converter_Capabilities, default=OMIT)
    privileged: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'privileged'}, default=OMIT)
    procMount: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'procMount'}, default=OMIT)
    readOnlyRootFilesystem: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnlyRootFilesystem'}, default=OMIT)
    runAsGroup: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'runAsGroup'}, default=OMIT)
    runAsNonRoot: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'runAsNonRoot'}, default=OMIT)
    runAsUser: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'runAsUser'}, default=OMIT)
    seLinuxOptions: Union[None, OmitEnum, SELinuxOptions] = attr.ib(metadata={'yaml_name': 'seLinuxOptions'}, converter=optional_converter_SELinuxOptions, default=OMIT)
    seccompProfile: Union[None, OmitEnum, SeccompProfile] = attr.ib(metadata={'yaml_name': 'seccompProfile'}, converter=optional_converter_SeccompProfile, default=OMIT)
    windowsOptions: Union[None, OmitEnum, WindowsSecurityContextOptions] = attr.ib(metadata={'yaml_name': 'windowsOptions'}, converter=optional_converter_WindowsSecurityContextOptions, default=OMIT)


class SecurityContextTypedDict(TypedDict, total=(False)):
    allowPrivilegeEscalation: bool
    capabilities: Capabilities
    privileged: bool
    procMount: str
    readOnlyRootFilesystem: bool
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: SELinuxOptions
    seccompProfile: SeccompProfile
    windowsOptions: WindowsSecurityContextOptions


SecurityContextUnion = Union[SecurityContext, SecurityContextTypedDict]


@attr.s(kw_only=True)
class ServiceAccountTokenProjection(K8sObject):
    path: str = attr.ib(metadata={'yaml_name': 'path'})
    audience: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'audience'}, default=OMIT)
    expirationSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'expirationSeconds'}, default=OMIT)


class ServiceAccountTokenProjectionOptionalTypedDict(TypedDict, total=(False)):
    audience: str
    expirationSeconds: int


class ServiceAccountTokenProjectionTypedDict(ServiceAccountTokenProjectionOptionalTypedDict, total=(True)):
    path: str


ServiceAccountTokenProjectionUnion = Union[ServiceAccountTokenProjection, ServiceAccountTokenProjectionTypedDict]


@attr.s(kw_only=True)
class ServicePortItem(K8sObject):
    appProtocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'appProtocol'}, default=OMIT)
    name: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'name'}, default=OMIT)
    nodePort: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'nodePort'}, default=OMIT)
    protocol: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'protocol'}, default=OMIT)
    targetPort: Union[None, OmitEnum, Union[int, str]] = attr.ib(metadata={'yaml_name': 'targetPort'}, default=OMIT)


class ServicePortItemTypedDict(TypedDict, total=(False)):
    appProtocol: str
    name: str
    nodePort: int
    protocol: str
    targetPort: Union[int, str]


ServicePortItemUnion = Union[ServicePortItem, ServicePortItemTypedDict]


@attr.s(kw_only=True)
class ServiceSpec(K8sObject):
    allocateLoadBalancerNodePorts: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'allocateLoadBalancerNodePorts'}, default=OMIT)
    clusterIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'clusterIP'}, default=OMIT)
    clusterIPs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'clusterIPs'}, default=OMIT)
    externalIPs: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'externalIPs'}, default=OMIT)
    externalName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'externalName'}, default=OMIT)
    externalTrafficPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'externalTrafficPolicy'}, default=OMIT)
    healthCheckNodePort: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'healthCheckNodePort'}, default=OMIT)
    internalTrafficPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'internalTrafficPolicy'}, default=OMIT)
    ipFamilies: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'ipFamilies'}, default=OMIT)
    ipFamilyPolicy: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'ipFamilyPolicy'}, default=OMIT)
    loadBalancerClass: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'loadBalancerClass'}, default=OMIT)
    loadBalancerIP: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'loadBalancerIP'}, default=OMIT)
    loadBalancerSourceRanges: Union[None, OmitEnum, Sequence[str]] = attr.ib(metadata={'yaml_name': 'loadBalancerSourceRanges'}, default=OMIT)
    ports: Union[None, OmitEnum, Mapping[int, kdsl.core.v1.ServicePortItem]] = attr.ib(metadata={'yaml_name': 'ports', 'mlist_key': 'port'}, converter=optional_mlist_converter_ServicePortItem, default=OMIT)
    publishNotReadyAddresses: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'publishNotReadyAddresses'}, default=OMIT)
    selector: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'selector'}, default=OMIT)
    sessionAffinity: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'sessionAffinity'}, default=OMIT)
    sessionAffinityConfig: Union[None, OmitEnum, SessionAffinityConfig] = attr.ib(metadata={'yaml_name': 'sessionAffinityConfig'}, converter=optional_converter_SessionAffinityConfig, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


class ServiceSpecTypedDict(TypedDict, total=(False)):
    allocateLoadBalancerNodePorts: bool
    clusterIP: str
    clusterIPs: Sequence[str]
    externalIPs: Sequence[str]
    externalName: str
    externalTrafficPolicy: str
    healthCheckNodePort: int
    internalTrafficPolicy: str
    ipFamilies: Sequence[str]
    ipFamilyPolicy: str
    loadBalancerClass: str
    loadBalancerIP: str
    loadBalancerSourceRanges: Sequence[str]
    ports: Mapping[int, kdsl.core.v1.ServicePortItem]
    publishNotReadyAddresses: bool
    selector: Mapping[str, str]
    sessionAffinity: str
    sessionAffinityConfig: SessionAffinityConfig
    type: str


ServiceSpecUnion = Union[ServiceSpec, ServiceSpecTypedDict]


@attr.s(kw_only=True)
class ServiceStatus(K8sObject):
    conditions: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.ConditionItem]] = attr.ib(metadata={'yaml_name': 'conditions', 'mlist_key': 'type'}, converter=optional_mlist_converter_ConditionItem, default=OMIT)
    loadBalancer: Union[None, OmitEnum, LoadBalancerStatus] = attr.ib(metadata={'yaml_name': 'loadBalancer'}, converter=optional_converter_LoadBalancerStatus, default=OMIT)


class ServiceStatusTypedDict(TypedDict, total=(False)):
    conditions: Mapping[str, kdsl.core.v1.ConditionItem]
    loadBalancer: LoadBalancerStatus


ServiceStatusUnion = Union[ServiceStatus, ServiceStatusTypedDict]


@attr.s(kw_only=True)
class SessionAffinityConfig(K8sObject):
    clientIP: Union[None, OmitEnum, ClientIPConfig] = attr.ib(metadata={'yaml_name': 'clientIP'}, converter=optional_converter_ClientIPConfig, default=OMIT)


class SessionAffinityConfigTypedDict(TypedDict, total=(False)):
    clientIP: ClientIPConfig


SessionAffinityConfigUnion = Union[SessionAffinityConfig, SessionAffinityConfigTypedDict]


@attr.s(kw_only=True)
class StorageOSPersistentVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, ObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_ObjectReference, default=OMIT)
    volumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeName'}, default=OMIT)
    volumeNamespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeNamespace'}, default=OMIT)


class StorageOSPersistentVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: ObjectReference
    volumeName: str
    volumeNamespace: str


StorageOSPersistentVolumeSourceUnion = Union[StorageOSPersistentVolumeSource, StorageOSPersistentVolumeSourceTypedDict]


@attr.s(kw_only=True)
class StorageOSVolumeSource(K8sObject):
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    secretRef: Union[None, OmitEnum, LocalObjectReference] = attr.ib(metadata={'yaml_name': 'secretRef'}, converter=optional_converter_LocalObjectReference, default=OMIT)
    volumeName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeName'}, default=OMIT)
    volumeNamespace: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'volumeNamespace'}, default=OMIT)


class StorageOSVolumeSourceTypedDict(TypedDict, total=(False)):
    fsType: str
    readOnly: bool
    secretRef: LocalObjectReference
    volumeName: str
    volumeNamespace: str


StorageOSVolumeSourceUnion = Union[StorageOSVolumeSource, StorageOSVolumeSourceTypedDict]


@attr.s(kw_only=True)
class Sysctl(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    value: str = attr.ib(metadata={'yaml_name': 'value'})


class SysctlTypedDict(TypedDict, total=(True)):
    name: str
    value: str


SysctlUnion = Union[Sysctl, SysctlTypedDict]


@attr.s(kw_only=True)
class TCPSocketAction(K8sObject):
    port: Union[int, str] = attr.ib(metadata={'yaml_name': 'port'})
    host: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'host'}, default=OMIT)


class TCPSocketActionOptionalTypedDict(TypedDict, total=(False)):
    host: str


class TCPSocketActionTypedDict(TCPSocketActionOptionalTypedDict, total=(True)):
    port: Union[int, str]


TCPSocketActionUnion = Union[TCPSocketAction, TCPSocketActionTypedDict]


@attr.s(kw_only=True)
class Taint(K8sObject):
    effect: str = attr.ib(metadata={'yaml_name': 'effect'})
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    timeAdded: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'timeAdded'}, default=OMIT)
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)


class TaintOptionalTypedDict(TypedDict, total=(False)):
    timeAdded: str
    value: str


class TaintTypedDict(TaintOptionalTypedDict, total=(True)):
    effect: str
    key: str


TaintUnion = Union[Taint, TaintTypedDict]


@attr.s(kw_only=True)
class Toleration(K8sObject):
    effect: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'effect'}, default=OMIT)
    key: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'key'}, default=OMIT)
    operator: Union[None, OmitEnum, Literal['Exists', 'Equal']] = attr.ib(metadata={'yaml_name': 'operator'}, default=OMIT)
    tolerationSeconds: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'tolerationSeconds'}, default=OMIT)
    value: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'value'}, default=OMIT)


class TolerationTypedDict(TypedDict, total=(False)):
    effect: str
    key: str
    operator: Literal['Exists', 'Equal']
    tolerationSeconds: int
    value: str


TolerationUnion = Union[Toleration, TolerationTypedDict]


@attr.s(kw_only=True)
class TopologySelectorLabelRequirement(K8sObject):
    key: str = attr.ib(metadata={'yaml_name': 'key'})
    values: Sequence[str] = attr.ib(metadata={'yaml_name': 'values'})


class TopologySelectorLabelRequirementTypedDict(TypedDict, total=(True)):
    key: str
    values: Sequence[str]


TopologySelectorLabelRequirementUnion = Union[TopologySelectorLabelRequirement, TopologySelectorLabelRequirementTypedDict]


@attr.s(kw_only=True)
class TopologySelectorTerm(K8sObject):
    matchLabelExpressions: Union[None, OmitEnum, Sequence[TopologySelectorLabelRequirement]] = attr.ib(metadata={'yaml_name': 'matchLabelExpressions'}, converter=optional_list_converter_TopologySelectorLabelRequirement, default=OMIT)


class TopologySelectorTermTypedDict(TypedDict, total=(False)):
    matchLabelExpressions: Sequence[TopologySelectorLabelRequirement]


TopologySelectorTermUnion = Union[TopologySelectorTerm, TopologySelectorTermTypedDict]


@attr.s(kw_only=True)
class TopologySpreadConstraintItem(K8sObject):
    maxSkew: int = attr.ib(metadata={'yaml_name': 'maxSkew'})
    whenUnsatisfiable: str = attr.ib(metadata={'yaml_name': 'whenUnsatisfiable'})
    labelSelector: Union[None, OmitEnum, LabelSelector] = attr.ib(metadata={'yaml_name': 'labelSelector'}, converter=optional_converter_LabelSelector, default=OMIT)


class TopologySpreadConstraintItemOptionalTypedDict(TypedDict, total=(False)):
    labelSelector: LabelSelector


class TopologySpreadConstraintItemTypedDict(TopologySpreadConstraintItemOptionalTypedDict, total=(True)):
    maxSkew: int
    whenUnsatisfiable: str


TopologySpreadConstraintItemUnion = Union[TopologySpreadConstraintItem, TopologySpreadConstraintItemTypedDict]


@attr.s(kw_only=True)
class TypedLocalObjectReference(K8sObject):
    kind: str = attr.ib(metadata={'yaml_name': 'kind'})
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    apiGroup: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'apiGroup'}, default=OMIT)


class TypedLocalObjectReferenceOptionalTypedDict(TypedDict, total=(False)):
    apiGroup: str


class TypedLocalObjectReferenceTypedDict(TypedLocalObjectReferenceOptionalTypedDict, total=(True)):
    kind: str
    name: str


TypedLocalObjectReferenceUnion = Union[TypedLocalObjectReference, TypedLocalObjectReferenceTypedDict]


@attr.s(kw_only=True)
class VolumeDeviceItem(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})


class VolumeDeviceItemTypedDict(TypedDict, total=(True)):
    name: str


VolumeDeviceItemUnion = Union[VolumeDeviceItem, VolumeDeviceItemTypedDict]


@attr.s(kw_only=True)
class VolumeItem(K8sObject):
    awsElasticBlockStore: Union[None, OmitEnum, AWSElasticBlockStoreVolumeSource] = attr.ib(metadata={'yaml_name': 'awsElasticBlockStore'}, converter=optional_converter_AWSElasticBlockStoreVolumeSource, default=OMIT)
    azureDisk: Union[None, OmitEnum, AzureDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'azureDisk'}, converter=optional_converter_AzureDiskVolumeSource, default=OMIT)
    azureFile: Union[None, OmitEnum, AzureFileVolumeSource] = attr.ib(metadata={'yaml_name': 'azureFile'}, converter=optional_converter_AzureFileVolumeSource, default=OMIT)
    cephfs: Union[None, OmitEnum, CephFSVolumeSource] = attr.ib(metadata={'yaml_name': 'cephfs'}, converter=optional_converter_CephFSVolumeSource, default=OMIT)
    cinder: Union[None, OmitEnum, CinderVolumeSource] = attr.ib(metadata={'yaml_name': 'cinder'}, converter=optional_converter_CinderVolumeSource, default=OMIT)
    configMap: Union[None, OmitEnum, ConfigMapVolumeSource] = attr.ib(metadata={'yaml_name': 'configMap'}, converter=optional_converter_ConfigMapVolumeSource, default=OMIT)
    csi: Union[None, OmitEnum, CSIVolumeSource] = attr.ib(metadata={'yaml_name': 'csi'}, converter=optional_converter_CSIVolumeSource, default=OMIT)
    downwardAPI: Union[None, OmitEnum, DownwardAPIVolumeSource] = attr.ib(metadata={'yaml_name': 'downwardAPI'}, converter=optional_converter_DownwardAPIVolumeSource, default=OMIT)
    emptyDir: Union[None, OmitEnum, EmptyDirVolumeSource] = attr.ib(metadata={'yaml_name': 'emptyDir'}, converter=optional_converter_EmptyDirVolumeSource, default=OMIT)
    ephemeral: Union[None, OmitEnum, EphemeralVolumeSource] = attr.ib(metadata={'yaml_name': 'ephemeral'}, converter=optional_converter_EphemeralVolumeSource, default=OMIT)
    fc: Union[None, OmitEnum, FCVolumeSource] = attr.ib(metadata={'yaml_name': 'fc'}, converter=optional_converter_FCVolumeSource, default=OMIT)
    flexVolume: Union[None, OmitEnum, FlexVolumeSource] = attr.ib(metadata={'yaml_name': 'flexVolume'}, converter=optional_converter_FlexVolumeSource, default=OMIT)
    flocker: Union[None, OmitEnum, FlockerVolumeSource] = attr.ib(metadata={'yaml_name': 'flocker'}, converter=optional_converter_FlockerVolumeSource, default=OMIT)
    gcePersistentDisk: Union[None, OmitEnum, GCEPersistentDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'gcePersistentDisk'}, converter=optional_converter_GCEPersistentDiskVolumeSource, default=OMIT)
    gitRepo: Union[None, OmitEnum, GitRepoVolumeSource] = attr.ib(metadata={'yaml_name': 'gitRepo'}, converter=optional_converter_GitRepoVolumeSource, default=OMIT)
    glusterfs: Union[None, OmitEnum, GlusterfsVolumeSource] = attr.ib(metadata={'yaml_name': 'glusterfs'}, converter=optional_converter_GlusterfsVolumeSource, default=OMIT)
    hostPath: Union[None, OmitEnum, HostPathVolumeSource] = attr.ib(metadata={'yaml_name': 'hostPath'}, converter=optional_converter_HostPathVolumeSource, default=OMIT)
    iscsi: Union[None, OmitEnum, ISCSIVolumeSource] = attr.ib(metadata={'yaml_name': 'iscsi'}, converter=optional_converter_ISCSIVolumeSource, default=OMIT)
    nfs: Union[None, OmitEnum, NFSVolumeSource] = attr.ib(metadata={'yaml_name': 'nfs'}, converter=optional_converter_NFSVolumeSource, default=OMIT)
    persistentVolumeClaim: Union[None, OmitEnum, PersistentVolumeClaimVolumeSource] = attr.ib(metadata={'yaml_name': 'persistentVolumeClaim'}, converter=optional_converter_PersistentVolumeClaimVolumeSource, default=OMIT)
    photonPersistentDisk: Union[None, OmitEnum, PhotonPersistentDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'photonPersistentDisk'}, converter=optional_converter_PhotonPersistentDiskVolumeSource, default=OMIT)
    portworxVolume: Union[None, OmitEnum, PortworxVolumeSource] = attr.ib(metadata={'yaml_name': 'portworxVolume'}, converter=optional_converter_PortworxVolumeSource, default=OMIT)
    projected: Union[None, OmitEnum, ProjectedVolumeSource] = attr.ib(metadata={'yaml_name': 'projected'}, converter=optional_converter_ProjectedVolumeSource, default=OMIT)
    quobyte: Union[None, OmitEnum, QuobyteVolumeSource] = attr.ib(metadata={'yaml_name': 'quobyte'}, converter=optional_converter_QuobyteVolumeSource, default=OMIT)
    rbd: Union[None, OmitEnum, RBDVolumeSource] = attr.ib(metadata={'yaml_name': 'rbd'}, converter=optional_converter_RBDVolumeSource, default=OMIT)
    scaleIO: Union[None, OmitEnum, ScaleIOVolumeSource] = attr.ib(metadata={'yaml_name': 'scaleIO'}, converter=optional_converter_ScaleIOVolumeSource, default=OMIT)
    secret: Union[None, OmitEnum, SecretVolumeSource] = attr.ib(metadata={'yaml_name': 'secret'}, converter=optional_converter_SecretVolumeSource, default=OMIT)
    storageos: Union[None, OmitEnum, StorageOSVolumeSource] = attr.ib(metadata={'yaml_name': 'storageos'}, converter=optional_converter_StorageOSVolumeSource, default=OMIT)
    vsphereVolume: Union[None, OmitEnum, VsphereVirtualDiskVolumeSource] = attr.ib(metadata={'yaml_name': 'vsphereVolume'}, converter=optional_converter_VsphereVirtualDiskVolumeSource, default=OMIT)


class VolumeItemTypedDict(TypedDict, total=(False)):
    awsElasticBlockStore: AWSElasticBlockStoreVolumeSource
    azureDisk: AzureDiskVolumeSource
    azureFile: AzureFileVolumeSource
    cephfs: CephFSVolumeSource
    cinder: CinderVolumeSource
    configMap: ConfigMapVolumeSource
    csi: CSIVolumeSource
    downwardAPI: DownwardAPIVolumeSource
    emptyDir: EmptyDirVolumeSource
    ephemeral: EphemeralVolumeSource
    fc: FCVolumeSource
    flexVolume: FlexVolumeSource
    flocker: FlockerVolumeSource
    gcePersistentDisk: GCEPersistentDiskVolumeSource
    gitRepo: GitRepoVolumeSource
    glusterfs: GlusterfsVolumeSource
    hostPath: HostPathVolumeSource
    iscsi: ISCSIVolumeSource
    nfs: NFSVolumeSource
    persistentVolumeClaim: PersistentVolumeClaimVolumeSource
    photonPersistentDisk: PhotonPersistentDiskVolumeSource
    portworxVolume: PortworxVolumeSource
    projected: ProjectedVolumeSource
    quobyte: QuobyteVolumeSource
    rbd: RBDVolumeSource
    scaleIO: ScaleIOVolumeSource
    secret: SecretVolumeSource
    storageos: StorageOSVolumeSource
    vsphereVolume: VsphereVirtualDiskVolumeSource


VolumeItemUnion = Union[VolumeItem, VolumeItemTypedDict]


@attr.s(kw_only=True)
class VolumeMountItem(K8sObject):
    name: str = attr.ib(metadata={'yaml_name': 'name'})
    mountPropagation: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'mountPropagation'}, default=OMIT)
    readOnly: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'readOnly'}, default=OMIT)
    subPath: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'subPath'}, default=OMIT)
    subPathExpr: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'subPathExpr'}, default=OMIT)


class VolumeMountItemOptionalTypedDict(TypedDict, total=(False)):
    mountPropagation: str
    readOnly: bool
    subPath: str
    subPathExpr: str


class VolumeMountItemTypedDict(VolumeMountItemOptionalTypedDict, total=(True)):
    name: str


VolumeMountItemUnion = Union[VolumeMountItem, VolumeMountItemTypedDict]


@attr.s(kw_only=True)
class VolumeNodeAffinity(K8sObject):
    required: Union[None, OmitEnum, NodeSelector] = attr.ib(metadata={'yaml_name': 'required'}, converter=optional_converter_NodeSelector, default=OMIT)


class VolumeNodeAffinityTypedDict(TypedDict, total=(False)):
    required: NodeSelector


VolumeNodeAffinityUnion = Union[VolumeNodeAffinity, VolumeNodeAffinityTypedDict]


@attr.s(kw_only=True)
class VolumeProjection(K8sObject):
    configMap: Union[None, OmitEnum, ConfigMapProjection] = attr.ib(metadata={'yaml_name': 'configMap'}, converter=optional_converter_ConfigMapProjection, default=OMIT)
    downwardAPI: Union[None, OmitEnum, DownwardAPIProjection] = attr.ib(metadata={'yaml_name': 'downwardAPI'}, converter=optional_converter_DownwardAPIProjection, default=OMIT)
    secret: Union[None, OmitEnum, SecretProjection] = attr.ib(metadata={'yaml_name': 'secret'}, converter=optional_converter_SecretProjection, default=OMIT)
    serviceAccountToken: Union[None, OmitEnum, ServiceAccountTokenProjection] = attr.ib(metadata={'yaml_name': 'serviceAccountToken'}, converter=optional_converter_ServiceAccountTokenProjection, default=OMIT)


class VolumeProjectionTypedDict(TypedDict, total=(False)):
    configMap: ConfigMapProjection
    downwardAPI: DownwardAPIProjection
    secret: SecretProjection
    serviceAccountToken: ServiceAccountTokenProjection


VolumeProjectionUnion = Union[VolumeProjection, VolumeProjectionTypedDict]


@attr.s(kw_only=True)
class VsphereVirtualDiskVolumeSource(K8sObject):
    volumePath: str = attr.ib(metadata={'yaml_name': 'volumePath'})
    fsType: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'fsType'}, default=OMIT)
    storagePolicyID: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storagePolicyID'}, default=OMIT)
    storagePolicyName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'storagePolicyName'}, default=OMIT)


class VsphereVirtualDiskVolumeSourceOptionalTypedDict(TypedDict, total=(False)):
    fsType: str
    storagePolicyID: str
    storagePolicyName: str


class VsphereVirtualDiskVolumeSourceTypedDict(VsphereVirtualDiskVolumeSourceOptionalTypedDict, total=(True)):
    volumePath: str


VsphereVirtualDiskVolumeSourceUnion = Union[VsphereVirtualDiskVolumeSource, VsphereVirtualDiskVolumeSourceTypedDict]


@attr.s(kw_only=True)
class WeightedPodAffinityTerm(K8sObject):
    podAffinityTerm: PodAffinityTerm = attr.ib(metadata={'yaml_name': 'podAffinityTerm'}, converter=required_converter_PodAffinityTerm)
    weight: int = attr.ib(metadata={'yaml_name': 'weight'})


class WeightedPodAffinityTermTypedDict(TypedDict, total=(True)):
    podAffinityTerm: PodAffinityTerm
    weight: int


WeightedPodAffinityTermUnion = Union[WeightedPodAffinityTerm, WeightedPodAffinityTermTypedDict]


@attr.s(kw_only=True)
class WindowsSecurityContextOptions(K8sObject):
    gmsaCredentialSpec: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'gmsaCredentialSpec'}, default=OMIT)
    gmsaCredentialSpecName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'gmsaCredentialSpecName'}, default=OMIT)
    hostProcess: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'hostProcess'}, default=OMIT)
    runAsUserName: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'runAsUserName'}, default=OMIT)


class WindowsSecurityContextOptionsTypedDict(TypedDict, total=(False)):
    gmsaCredentialSpec: str
    gmsaCredentialSpecName: str
    hostProcess: bool
    runAsUserName: str


WindowsSecurityContextOptionsUnion = Union[WindowsSecurityContextOptions, WindowsSecurityContextOptionsTypedDict]


@attr.s(kw_only=True)
class Binding(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Binding'
    target: ObjectReference = attr.ib(metadata={'yaml_name': 'target'}, converter=required_converter_ObjectReference)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class ConfigMap(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'ConfigMap'
    binaryData: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'binaryData'}, default=OMIT)
    data: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'data'}, default=OMIT)
    immutable: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'immutable'}, default=OMIT)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)


@attr.s(kw_only=True)
class Endpoints(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Endpoints'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    subsets: Union[None, OmitEnum, Sequence[EndpointSubset]] = attr.ib(metadata={'yaml_name': 'subsets'}, converter=optional_list_converter_EndpointSubset, default=OMIT)


@attr.s(kw_only=True)
class Event(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Event'
    involvedObject: ObjectReference = attr.ib(metadata={'yaml_name': 'involvedObject'}, converter=required_converter_ObjectReference)
    metadata: ObjectMeta = attr.ib(metadata={'yaml_name': 'metadata'}, converter=required_converter_ObjectMeta)
    action: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'action'}, default=OMIT)
    count: Union[None, OmitEnum, int] = attr.ib(metadata={'yaml_name': 'count'}, default=OMIT)
    eventTime: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'eventTime'}, default=OMIT)
    firstTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'firstTimestamp'}, default=OMIT)
    lastTimestamp: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'lastTimestamp'}, default=OMIT)
    message: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'message'}, default=OMIT)
    reason: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reason'}, default=OMIT)
    related: Union[None, OmitEnum, ObjectReference] = attr.ib(metadata={'yaml_name': 'related'}, converter=optional_converter_ObjectReference, default=OMIT)
    reportingComponent: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reportingComponent'}, default=OMIT)
    reportingInstance: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'reportingInstance'}, default=OMIT)
    series: Union[None, OmitEnum, EventSeries] = attr.ib(metadata={'yaml_name': 'series'}, converter=optional_converter_EventSeries, default=OMIT)
    source: Union[None, OmitEnum, EventSource] = attr.ib(metadata={'yaml_name': 'source'}, converter=optional_converter_EventSource, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


@attr.s(kw_only=True)
class LimitRange(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'LimitRange'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, LimitRangeSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_LimitRangeSpec, default=OMIT)


@attr.s(kw_only=True)
class Namespace(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Namespace'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, NamespaceSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_NamespaceSpec, default=OMIT)
    status: Union[None, OmitEnum, NamespaceStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_NamespaceStatus, default=OMIT)


@attr.s(kw_only=True)
class Node(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Node'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, NodeSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_NodeSpec, default=OMIT)
    status: Union[None, OmitEnum, NodeStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_NodeStatus, default=OMIT)


@attr.s(kw_only=True)
class PersistentVolume(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'PersistentVolume'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PersistentVolumeSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PersistentVolumeSpec, default=OMIT)
    status: Union[None, OmitEnum, PersistentVolumeStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PersistentVolumeStatus, default=OMIT)


@attr.s(kw_only=True)
class PersistentVolumeClaim(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'PersistentVolumeClaim'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PersistentVolumeClaimSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PersistentVolumeClaimSpec, default=OMIT)
    status: Union[None, OmitEnum, PersistentVolumeClaimStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PersistentVolumeClaimStatus, default=OMIT)


@attr.s(kw_only=True)
class Pod(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Pod'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, PodSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_PodSpec, default=OMIT)
    status: Union[None, OmitEnum, PodStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_PodStatus, default=OMIT)


@attr.s(kw_only=True)
class PodTemplate(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'PodTemplate'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    template: Union[None, OmitEnum, PodTemplateSpec] = attr.ib(metadata={'yaml_name': 'template'}, converter=optional_converter_PodTemplateSpec, default=OMIT)


@attr.s(kw_only=True)
class ReplicationController(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'ReplicationController'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, ReplicationControllerSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_ReplicationControllerSpec, default=OMIT)
    status: Union[None, OmitEnum, ReplicationControllerStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_ReplicationControllerStatus, default=OMIT)


@attr.s(kw_only=True)
class ResourceQuota(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'ResourceQuota'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, ResourceQuotaSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_ResourceQuotaSpec, default=OMIT)
    status: Union[None, OmitEnum, ResourceQuotaStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_ResourceQuotaStatus, default=OMIT)


@attr.s(kw_only=True)
class Secret(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Secret'
    data: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'data'}, default=OMIT)
    immutable: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'immutable'}, default=OMIT)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    stringData: Union[None, OmitEnum, Mapping[str, str]] = attr.ib(metadata={'yaml_name': 'stringData'}, default=OMIT)
    type: Union[None, OmitEnum, str] = attr.ib(metadata={'yaml_name': 'type'}, default=OMIT)


@attr.s(kw_only=True)
class Service(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'Service'
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    spec: Union[None, OmitEnum, ServiceSpec] = attr.ib(metadata={'yaml_name': 'spec'}, converter=optional_converter_ServiceSpec, default=OMIT)
    status: Union[None, OmitEnum, ServiceStatus] = attr.ib(metadata={'yaml_name': 'status'}, converter=optional_converter_ServiceStatus, default=OMIT)


@attr.s(kw_only=True)
class ServiceAccount(K8sResource):
    apiVersion: ClassVar[str] = 'v1'
    kind: ClassVar[str] = 'ServiceAccount'
    automountServiceAccountToken: Union[None, OmitEnum, bool] = attr.ib(metadata={'yaml_name': 'automountServiceAccountToken'}, default=OMIT)
    imagePullSecrets: Union[None, OmitEnum, Sequence[LocalObjectReference]] = attr.ib(metadata={'yaml_name': 'imagePullSecrets'}, converter=optional_list_converter_LocalObjectReference, default=OMIT)
    metadata: Union[None, OmitEnum, ObjectMeta] = attr.ib(metadata={'yaml_name': 'metadata'}, converter=optional_converter_ObjectMeta, default=OMIT)
    secrets: Union[None, OmitEnum, Mapping[str, kdsl.core.v1.ObjectReferenceItem]] = attr.ib(metadata={'yaml_name': 'secrets', 'mlist_key': 'name'}, converter=optional_mlist_converter_ObjectReferenceItem, default=OMIT)
