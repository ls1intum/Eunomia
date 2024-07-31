import logging
import os
import re
from base64 import b64decode
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from quopri import decodestring as quopri_decode
from typing import List

from app.domain.data.email_dto import EmailDTO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailParser:
    def __init__(self):
        self.policy = policy.default

    def process_eml_file(self, file_path: str, sensitive) -> EmailDTO:
        logger.info(f"Processing file: {file_path}")
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=self.policy).parse(f)

        email_data = self._extract_headers(msg)
        body_plain, body_html = self._extract_body(msg)
        email_data['body_plain'] = self._extract_first_email(body_plain)
        email_data['body_html'] = body_html
        return EmailDTO(**email_data, sensitive=sensitive)

    def _extract_headers(self, msg) -> dict:
        headers = ['Message-ID', 'Date', 'Subject', 'From', 'To', 'Content-Type', 'In-Reply-To', 'References', 'MIME-Version', 'User-Agent', 'Content-Language']
        email_data = {header.lower().replace('-', '_'): msg.get(header, '') for header in headers}

        email_data['to'] = [addr for name, addr in getaddresses([email_data['to']])]
        email_data['references'] = email_data['references'].split()
        # Correcting the 'from' key
        email_data['from_'] = email_data.pop('from', '')

        return email_data

    def _extract_body(self, msg) -> (str, str):
        body_plain = ""
        body_html = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_transfer_encoding = part.get('Content-Transfer-Encoding')
                if content_type == 'text/plain':
                    body_plain = self._decode_payload(part.get_payload(), content_transfer_encoding,
                                                      part.get_content_charset())
                elif content_type == 'text/html':
                    body_html = self._decode_payload(part.get_payload(), content_transfer_encoding,
                                                     part.get_content_charset())
        else:
            body_plain = self._decode_payload(msg.get_payload(), msg.get('Content-Transfer-Encoding'),
                                              msg.get_content_charset())

        return body_plain, body_html

    def _decode_payload(self, payload: str, encoding: str, charset: str) -> str:
        if encoding == 'base64':
            payload = b64decode(payload).decode(charset, errors='ignore')
        elif encoding == 'quoted-printable':
            payload = quopri_decode(payload).decode(charset, errors='ignore')
        return payload

    def _extract_first_email(self, text: str) -> str:
        # Muster für Datum und Uhrzeit der eingebetteten E-Mail
        date_pattern = re.compile(r'Am \d{2}\.\d{2}\.\d{4} um \d{2}:\d{2} schrieb .*:')
        matches = list(date_pattern.finditer(text))
        if not matches:
            return text.strip()
        last_match = matches[-1]
        first_email = text[last_match.end():].strip()
        return first_email
    def process_eml_files_in_directory(self, directory_path: str, sensitive: bool) -> List[EmailDTO]:
        eml_files = [f for f in os.listdir(directory_path) if f.endswith('.eml')]
        email_data = []

        for eml_file in eml_files:
            file_path = os.path.join(directory_path, eml_file)
            email_data.append(self.process_eml_file(file_path, sensitive))

        logger.info(f"Processed {len(eml_files)} emails from directory: {directory_path}")
        return email_data