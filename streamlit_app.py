import json
import os
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from src.main import run


st.set_page_config(
    page_title="MarketMind AI",
    page_icon=":material/query_stats:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.session_state.setdefault("active_report", None)
st.session_state.setdefault("active_request", "")
st.session_state.setdefault("last_decision", None)
st.session_state.setdefault("api_key", "")
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("auth_error", "")


with st.sidebar:
    st.markdown("## :material/query_stats: MarketMind")
    st.caption("Evidence-first business research")
    st.markdown("### Workspace")
    st.badge("Local corpus", icon=":material/database:", color="blue")
    st.badge("Approval required", icon=":material/verified_user:", color="orange")
    st.markdown("### Run controls")
    st.caption("The current demo uses the deterministic corpus. It does not invent search results.")
    if st.session_state.authenticated:
        st.badge("Signed in", icon=":material/lock_open:", color="green")
        if st.button("Log out", icon=":material/logout:", width="stretch"):
            st.session_state.api_key = ""
            st.session_state.authenticated = False
            st.session_state.auth_error = ""
            os.environ.pop("OPENAI_API_KEY", None)
            st.rerun()
    if st.button("Clear active draft", icon=":material/refresh:", width="stretch"):
        st.session_state.active_report = None
        st.session_state.active_request = ""
        st.session_state.last_decision = None
        st.rerun()
    st.space("small")
    st.caption("MarketMind AI · AAI-412 / PRAC-05")


def persist_report(report: dict) -> None:
    run_id = report["report_id"]
    path = Path("runs") / run_id / "report.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def finding_rows(report: dict) -> list[dict]:
    rows = []
    for section in ("market_overview", "key_trends", "opportunities", "risks", "recommendations"):
        for finding in report.get(section, []):
            rows.append({
                "section": section.replace("_", " ").title(),
                "claim type": finding.get("claim_type", "unknown"),
                "confidence": finding.get("confidence", "unknown"),
                "statement": finding.get("statement", ""),
                "evidence": ", ".join(finding.get("evidence_ids", [])) or "none",
            })
    return rows


def render_report(report: dict) -> None:
    evidence = report.get("evidence_appendix", [])
    defects_path = Path("runs") / report["report_id"] / "qc.json"
    defects = json.loads(defects_path.read_text(encoding="utf-8")) if defects_path.exists() else []
    decision = report.get("approval") or {}

    left, middle, right = st.columns(3)
    left.metric("Evidence records", len(evidence))
    middle.metric("QC defects", len(defects))
    right.metric("Overall confidence", report.get("confidence_level", "unknown").title())

    if decision.get("decision") == "approve":
        st.success("Approved for publication", icon=":material/check_circle:")
    elif decision.get("decision") == "reject":
        st.error("Rejected. Nothing was published.", icon=":material/block:")
    else:
        st.warning("Draft only. Explicit approval is still required.", icon=":material/pending:")

    overview, evidence_tab, controls = st.tabs([
        ":material/description: Report",
        ":material/library_books: Evidence",
        ":material/security: QC and approval",
    ])
    with overview:
        st.markdown("### Executive summary")
        st.write(report.get("executive_summary", ""))
        st.markdown("### Findings")
        rows = finding_rows(report)
        if rows:
            st.dataframe(rows, width="stretch", hide_index=True, column_config={
                "claim type": st.column_config.TextColumn("Claim type", width="small"),
                "confidence": st.column_config.TextColumn("Confidence", width="small"),
                "statement": st.column_config.TextColumn("Statement", width="large"),
                "evidence": st.column_config.TextColumn("Evidence IDs", width="medium"),
            })
        else:
            st.caption("No supported findings were produced.")
        st.markdown("### Limitations and gaps")
        for gap in report.get("limitations_and_gaps", []):
            st.markdown(f"- {gap}")
    with evidence_tab:
        if evidence:
            st.dataframe(evidence, width="stretch", hide_index=True, column_config={
                "claim": st.column_config.TextColumn("Claim", width="large"),
                "source_ref": st.column_config.TextColumn("Source result", width="small"),
                "claim_type": st.column_config.TextColumn("Type", width="small"),
            })
        else:
            st.caption("No evidence records.")
    with controls:
        st.markdown("### Quality control")
        if defects:
            st.dataframe(defects, width="stretch", hide_index=True)
        else:
            st.success("No QC defects recorded.", icon=":material/check:")
        st.markdown("### Human approval")
        st.caption("Review the report, evidence, limitations, and QC defects before deciding.")
        note = st.text_input("Reviewer note", key="review_note")
        with st.container(horizontal=True):
            if st.button("Approve", type="primary", icon=":material/check_circle:"):
                report["approval"] = {"decision": "approve", "approver": "Streamlit reviewer", "timestamp": datetime.now(timezone.utc).isoformat(), "notes": note}
                persist_report(report)
                st.session_state.last_decision = "approve"
                st.rerun()
            if st.button("Reject", icon=":material/block:"):
                report["approval"] = {"decision": "reject", "approver": "Streamlit reviewer", "timestamp": datetime.now(timezone.utc).isoformat(), "notes": note}
                persist_report(report)
                st.session_state.last_decision = "reject"
                st.rerun()


st.markdown("# Research workspace")
st.caption("Turn a rough business question into a traceable, reviewable brief.")

if not st.session_state.authenticated:
    with st.container(border=True):
        st.markdown("### Sign in to MarketMind")
        st.caption("Use an OpenAI API key to sign in. The key is kept in this browser session only and is never saved to disk.")
        with st.form("api_login"):
            api_key = st.text_input(
                "OpenAI API key",
                type="password",
                placeholder="sk-...",
                help="Use a project-scoped key with an appropriate spend limit.",
            )
            login = st.form_submit_button("Sign in", type="primary", icon=":material/login:", width="stretch")
        if login:
            api_key = api_key.strip()
            if not api_key:
                st.session_state.auth_error = "Enter an API key to continue."
            else:
                with st.spinner("Verifying API key"):
                    try:
                        from openai import OpenAI
                        OpenAI(api_key=api_key, timeout=10).models.list()
                    except Exception:
                        st.session_state.auth_error = "The API key could not be verified. Check the key and try again."
                    else:
                        st.session_state.api_key = api_key
                        st.session_state.authenticated = True
                        st.session_state.auth_error = ""
                        os.environ["OPENAI_API_KEY"] = api_key
                        st.rerun()
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error, icon=":material/error:")
else:
    with st.container(border=True):
        st.success("Signed in. Research workspace unlocked.", icon=":material/lock_open:")

if not st.session_state.authenticated:
    st.info("Sign in with a verified OpenAI API key to access the research workspace.", icon=":material/lock:")
    st.stop()

with st.container(border=True):
    st.markdown("### Start a research run")
    with st.form("research_request", clear_on_submit=False):
        request = st.text_area(
            "Client request",
            value=st.session_state.active_request,
            height=110,
            placeholder="Research the market for AI-powered customer support software and prepare a business intelligence report.",
        )
        submitted = st.form_submit_button("Generate evidence-backed draft", type="primary", icon=":material/play_arrow:", width="stretch", disabled=not st.session_state.authenticated)
    if submitted:
        if not request.strip():
            st.error("Enter a client request first.", icon=":material/error:")
        else:
            with st.status("Running bounded research workflow", expanded=True) as status:
                st.write("Analysing scope and ambiguities")
                st.write("Building a validated research plan")
                st.write("Searching the approved local corpus")
                report = run(request, lambda _: {"decision": "pending", "notes": "Awaiting Streamlit reviewer"})
                status.update(label="Draft ready for review", state="complete", expanded=False)
            st.session_state.active_request = request
            st.session_state.active_report = report
            st.session_state.last_decision = None
            st.rerun()

report = st.session_state.active_report
if report:
    st.markdown("## Active draft")
    st.caption(f"Run {report['report_id']} · objective: {report['research_objective']}")
    render_report(report)
else:
    st.markdown("## No active draft")
    st.caption("Submit a research request above to populate the review workspace.")
    with st.container(horizontal=True):
        st.metric("Workflow", "Bounded")
        st.metric("Evidence source", "Local corpus")
        st.metric("Publication", "Human approval")
