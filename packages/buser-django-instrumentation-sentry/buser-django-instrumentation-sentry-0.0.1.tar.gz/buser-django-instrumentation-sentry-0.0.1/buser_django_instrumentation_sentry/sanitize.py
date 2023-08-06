import re
from raven.processors import Processor, SanitizeKeysProcessor

DEFAULT_RULES = [
    {
        "keys": [
            "social_name",
        ]
    },
    {
        "keys": [
            "email",
            "e-mail",
        ],
        "values": [
            r"\b[a-zA-Z0-9.!#$%&'*+/?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+\b",
        ],
    },
    {
        "keys": [
            "cpf",
            "document_number",
            "rg_number",
            "tax_id",
            "taxid",
        ],
        "values": [
            r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
            r"\b\d{2}\.\d{3}\.\d{3}-\d\b",
        ],
    },
    {
        "keys": [
            "phone",
            "telefone",
            "celular",
        ],
        "values": [
            r"\b55\d{11}\b",
            r"\b\d{11}\b",
            r"\b\d{10}\b",
        ],
    },
    {
        "keys": [
            "zip",
            "cep",
            "street",
            "logradouro",
        ],
        "values": [
            r"\b\d{5}-\d{3}\b",
            r'^[\'"]?rua .*$',
        ],
    },
    {
        "keys": [
            "cpf",
            "document_number",
            "rg_number",
            "tax_id",
            "taxid",
        ],
        "values": [
            r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
            r"\b\d{2}\.\d{3}\.\d{3}-\d\b",
        ],
    },
]


def create_event_sanitizer(rules=None):
    if rules is None:
        rules = DEFAULT_RULES

    processors = []

    for rule in rules:
        keys = rule.get("keys", [])
        values = rule.get("values", [])
        processors.append(SanitizeKeysAndValuesProcessor(FakeRavenClient, keys, values))

    def strip_sensitive_data(event, hint):
        for processor in processors:
            event = processor.process(event)
        return event

    return strip_sensitive_data


class FakeRavenClient:
    sanitize_keys = [
        "card",
        "card_number",
        "cvv",
        "card_cvv",
        "antt_password",
        "validade",
        "card_expiration_date",
        "token",
        "sessionid",
        "message",
        "redis.key",
    ]


class SanitizeKeysAndValuesProcessor(SanitizeKeysProcessor):
    MASK = "[Filtered]"
    KEYS = []

    def __init__(self, client, keys, values_re):
        super().__init__(client)
        self.keys = keys
        self.values_re = values_re

        # pattern for JSON key-value pairs (escaped or not)
        self.json_keyval_re = re.compile(
            rf"""
            # matches: \"key\": \"
            (?P<before>
                (?P<quote>\\?['"])
                ({'|'.join(self.KEYS)})
                (?P=quote)
                \s*:\s*
                (?P=quote)
            )
            # matches: value (non-greedy)
            .*?
            # matches: \"
            (?P<after>
                (?P=quote)
            )
        """,
            re.VERBOSE | re.IGNORECASE,
        )

    @property
    def sanitize_keys(self):
        return self.keys

    def process(self, data, **kwargs):
        # process normal fields
        data = super().process(data, **kwargs)

        # also process exception titles
        for value in data.get("exception", {}).get("values", []):
            if "value" in value:
                value["value"] = self.sanitize("value", value["value"])

        return data

    def sanitize(self, item, value):
        # sanitize keys
        value = super().sanitize(item, value)

        # sanitize keys in serialized JSON
        if isinstance(value, str):
            value = self.json_keyval_re.sub(rf"\g<before>{self.MASK}\g<after>", value)

        # sanitize values
        if isinstance(value, str):
            for pattern in self.values_re:
                if isinstance(pattern, str):
                    pattern = re.compile(pattern)

                value = pattern.sub(self.MASK, value)

        return value
