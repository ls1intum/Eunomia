import enum
from dataclasses import dataclass, field
from email.message import Message
from typing import List, Optional


class InboxType(enum.Enum):
    All = 'ALL'
    Unseen = 'UNSEEN'


@dataclass
class EmailDTO:
    delivered_to: Optional[str] = None
    received_by: List[str] = field(default_factory=list)
    received_date_time: List[str] = field(default_factory=list)
    x_google_smtp_source: Optional[str] = None
    x_received_by: List[str] = field(default_factory=list)
    x_received_date_time: List[str] = field(default_factory=list)
    arc_seal: List[str] = field(default_factory=list)
    arc_message_signature: List[str] = field(default_factory=list)
    arc_authentication_results: List[str] = field(default_factory=list)
    return_path: Optional[str] = None
    received_spf: Optional[str] = None
    authentication_results: List[str] = field(default_factory=list)
    dkim_signature: Optional[str] = None
    from_address: Optional[str] = None
    content_type: Optional[str] = None
    charset: Optional[str] = None
    content_transfer_encoding: Optional[str] = None
    subject: Optional[str] = None
    message_id: Optional[str] = None
    date: Optional[str] = None
    to: Optional[str] = None
    x_mailer: Optional[str] = None
    x_tmn: Optional[str] = None
    x_client_proxied_by: Optional[str] = None
    x_microsoft_original_message_id: Optional[str] = None
    mime_version: Optional[str] = None
    x_ms_exchange_message_sent_representing_type: Optional[str] = None
    x_ms_public_traffic_type: Optional[str] = None
    x_ms_traffic_type_diagnostic: Optional[str] = None
    x_ms_office365_filtering_correlation_id: Optional[str] = None
    x_microsoft_antispam: Optional[str] = None
    x_microsoft_antispam_message_info: Optional[str] = None
    x_ms_exchange_antispam_message_data_chunk_count: Optional[int] = None
    x_ms_exchange_antispam_message_data: List[str] = field(default_factory=list)
    x_originator_org: Optional[str] = None
    x_ms_exchange_cross_tenant_network_message_id: Optional[str] = None
    x_ms_exchange_cross_tenant_auth_source: Optional[str] = None
    x_ms_exchange_cross_tenant_auth_as: Optional[str] = None
    x_ms_exchange_cross_tenant_original_arrival_time: Optional[str] = None
    x_ms_exchange_cross_tenant_from_entity_header: Optional[str] = None
    x_ms_exchange_cross_tenant_id: Optional[str] = None
    x_ms_exchange_cross_tenant_rms_persisted_consumer_org: Optional[str] = None
    x_ms_exchange_transport_cross_tenant_headers_stamped: Optional[str] = None
    body: Optional[str] = None
    sensitive: Optional[bool] = True

    @classmethod
    def from_email_message(cls, msg: Message):
        headers = {key: msg.get_all(key) for key in msg.keys()}

        email_data = {
            "delivered_to": headers.get("Delivered-To", [None])[0],
            "received_by": headers.get("Received", []),
            "received_date_time": headers.get("Received", []),
            "x_google_smtp_source": headers.get("X-Google-Smtp-Source", [None])[0],
            "x_received_by": headers.get("X-Received", []),
            "x_received_date_time": headers.get("X-Received", []),
            "arc_seal": headers.get("ARC-Seal", []),
            "arc_message_signature": headers.get("ARC-Message-Signature", []),
            "arc_authentication_results": headers.get("ARC-Authentication-Results", []),
            "return_path": headers.get("Return-Path", [None])[0],
            "received_spf": headers.get("Received-SPF", [None])[0],
            "authentication_results": headers.get("Authentication-Results", []),
            "dkim_signature": headers.get("DKIM-Signature", [None])[0],
            "from_address": headers.get("From", [None])[0],
            "content_type": msg.get_content_type(),
            "charset": msg.get_content_charset(),
            "content_transfer_encoding": headers.get("Content-Transfer-Encoding", [None])[0],
            "subject": headers.get("Subject", [None])[0],
            "message_id": headers.get("Message-Id", [None])[0],
            "date": headers.get("Date", [None])[0],
            "to": headers.get("To", [None])[0],
            "x_mailer": headers.get("X-Mailer", [None])[0],
            "x_tmn": headers.get("X-TMN", [None])[0],
            "x_client_proxied_by": headers.get("X-ClientProxiedBy", [None])[0],
            "x_microsoft_original_message_id": headers.get("X-Microsoft-Original-Message-ID", [None])[0],
            "mime_version": headers.get("MIME-Version", [None])[0],
            "x_ms_exchange_message_sent_representing_type":
                headers.get("X-MS-Exchange-MessageSentRepresentingType", [None])[0],
            "x_ms_public_traffic_type": headers.get("X-MS-PublicTrafficType", [None])[0],
            "x_ms_traffic_type_diagnostic": headers.get("X-MS-TrafficTypeDiagnostic", [None])[0],
            "x_ms_office365_filtering_correlation_id": headers.get("X-MS-Office365-Filtering-Correlation-Id", [None])[
                0],
            "x_microsoft_antispam": headers.get("X-Microsoft-Antispam", [None])[0],
            "x_microsoft_antispam_message_info": headers.get("X-Microsoft-Antispam-Message-Info", [None])[0],
            "x_ms_exchange_antispam_message_data_chunk_count": int(
                headers.get("X-MS-Exchange-AntiSpam-MessageData-ChunkCount", [0])[0]),
            "x_ms_exchange_antispam_message_data": headers.get("X-MS-Exchange-AntiSpam-MessageData", []),
            "x_originator_org": headers.get("X-OriginatorOrg", [None])[0],
            "x_ms_exchange_cross_tenant_network_message_id":
                headers.get("X-MS-Exchange-CrossTenant-Network-Message-Id", [None])[0],
            "x_ms_exchange_cross_tenant_auth_source": headers.get("X-MS-Exchange-CrossTenant-AuthSource", [None])[0],
            "x_ms_exchange_cross_tenant_auth_as": headers.get("X-MS-Exchange-CrossTenant-AuthAs", [None])[0],
            "x_ms_exchange_cross_tenant_original_arrival_time":
                headers.get("X-MS-Exchange-CrossTenant-OriginalArrivalTime", [None])[0],
            "x_ms_exchange_cross_tenant_from_entity_header":
                headers.get("X-MS-Exchange-CrossTenant-FromEntityHeader", [None])[0],
            "x_ms_exchange_cross_tenant_id": headers.get("X-MS-Exchange-CrossTenant-Id", [None])[0],
            "x_ms_exchange_cross_tenant_rms_persisted_consumer_org":
                headers.get("X-MS-Exchange-CrossTenant-RMS-Persisted-Consumer-Org", [None])[0],
            "x_ms_exchange_transport_cross_tenant_headers_stamped":
                headers.get("X-MS-Exchange-Transport-CrossTenant-Headers-Stamped", [None])[0]
        }
        return cls(**email_data)

    @classmethod
    def from_dict(cls, data: dict):
        filtered_data = {key: value for key, value in data.items() if key in cls.__annotations__}
        return cls(**filtered_data)
