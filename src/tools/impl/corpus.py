from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    source_type: str
    text: str
    date: str = "2026-01-01"


DOCUMENTS = [
    Document("acme-overview", "Acme Support product overview", "vendor", "Acme Support provides AI chat, email automation, Salesforce integration, and a human handoff for mid-market teams."),
    Document("acme-pricing", "Acme Support pricing", "pricing", "Acme Support publishes a Starter plan at $49 per seat per month. Enterprise pricing is not published."),
    Document("beacon-overview", "BeaconDesk product overview", "vendor", "BeaconDesk offers AI chat and knowledge-base search for small businesses. It supports Zendesk integration."),
    Document("beacon-pricing", "BeaconDesk pricing", "pricing", "BeaconDesk publishes a $29 per seat per month Team plan and a $79 Business plan."),
    Document("market-brief", "Customer support software market brief", "press", "The category is crowded. Public pricing is common for self-serve plans, while enterprise pricing is often negotiated."),
    Document("market-brief-conflict", "Alternative market estimate", "press", "A separate estimate describes enterprise pricing as usually starting at $99 per seat per month; the figure conflicts with other estimates."),
]


def search(query: str, source_type: str = "all", max_results: int = 10) -> list[dict]:
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    hits = []
    for doc in DOCUMENTS:
        if source_type not in ("all", doc.source_type):
            continue
        score = len(words & set(re.findall(r"[a-z0-9]+", (doc.title + " " + doc.text).lower())))
        if score:
            hits.append({"id": doc.id, "title": doc.title, "source_type": doc.source_type, "date": doc.date, "snippet": doc.text[:240], "score": score})
    return sorted(hits, key=lambda hit: hit["score"], reverse=True)[:max_results]


def retrieve(document_id: str, section: str | None = None) -> dict:
    for doc in DOCUMENTS:
        if doc.id == document_id:
            return {"document_id": doc.id, "title": doc.title, "source_type": doc.source_type, "date": doc.date, "text": doc.text, "section": section}
    raise KeyError(f"document_id not found: {document_id}")