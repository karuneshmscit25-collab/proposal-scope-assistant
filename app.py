import streamlit as st
from datetime import date

st.set_page_config(
    page_title="ScopeCraft | Proposal Studio",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual system ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root { --ink:#172b4d; --muted:#66758b; --line:#e3e9f2; --blue:#315fce; --paper:#f6f8fc; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f6f8fc; }
.block-container { max-width: 1380px; padding-top: 2rem; padding-bottom: 3rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif; color:var(--ink); letter-spacing:-.035em; }
h1 { font-size:2.1rem !important; font-weight:800 !important; }
h2 { font-size:1.35rem !important; font-weight:750 !important; }
h3 { font-size:1.02rem !important; font-weight:700 !important; letter-spacing:-.01em; }
p, label, .stMarkdown { color:#334155; }
[data-testid="stSidebar"] { background:#14243b; border-right:1px solid #203650; }
[data-testid="stSidebar"] * { color:#eef4ff !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#c0cde0 !important; }
[data-testid="stSidebar"] hr { border-color:#344761; }
[data-testid="stSidebar"] div[role="radiogroup"] label { background:transparent; border-radius:9px; padding:8px 10px; margin:2px 0; }
[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background:#233955; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color:#cbd7e8 !important; }
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea { color:#172b4d !important; }
div[data-testid="stVerticalBlockBorderWrapper"] { background:white; border:1px solid var(--line); border-radius:15px; padding:1rem 1.15rem; }
div[data-testid="stMetric"] { background:white; border:1px solid var(--line); padding:14px 16px; border-radius:13px; box-shadow:0 2px 7px rgba(20,36,59,.025); }
div[data-testid="stMetricLabel"] { color:#64748b; }
div[data-testid="stMetricValue"] { color:var(--ink); font-family:'Manrope',sans-serif; font-weight:800; }
.stButton > button, .stDownloadButton > button { border-radius:9px; min-height:2.7rem; font-weight:700; border:1px solid #d5deeb; }
.stButton > button[kind="primary"] { background:#315fce; border-color:#315fce; color:white; }
.stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] { border-radius:9px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"] { padding:10px 14px; }
.hero { background:linear-gradient(115deg,#172b4d 0%,#244777 100%); padding:25px 28px; border-radius:18px; color:white; margin-bottom:20px; box-shadow:0 12px 28px rgba(23,43,77,.12); }
.hero h2 { color:white !important; margin:0 0 7px 0; font-size:1.45rem !important; }
.hero p { color:#d8e4f7 !important; margin:0; max-width:780px; }
.eyebrow { color:#9eb9f4; font-size:.75rem; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin-bottom:9px; }
.step-pill { display:inline-block; background:#edf3ff; color:#315fce; border:1px solid #dce7ff; padding:5px 10px; border-radius:100px; font-size:.78rem; font-weight:700; }
.small-note { color:#718096; font-size:.86rem; }
.sidebar-brand { font-family:'Manrope',sans-serif; font-size:1.35rem; font-weight:800; color:white; letter-spacing:-.04em; }
.sidebar-sub { color:#b7c7dc; font-size:.78rem; margin-top:2px; }
.sidebar-card { background:#1d324d; border:1px solid #304965; padding:13px; border-radius:12px; margin:10px 0; }
.sidebar-label { font-size:.7rem; color:#9eb1c9; text-transform:uppercase; letter-spacing:.1em; font-weight:700; }
.sidebar-value { font-size:.95rem; color:white; font-weight:700; margin-top:4px; }
div[data-testid="stProgressBar"] > div > div { background:#80a7ff; }
</style>
""", unsafe_allow_html=True)

# ---------- State helpers ----------
def init(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

defaults = {
    "company_name": "", "client_name": "", "proposal_title": "Project Proposal",
    "proposal_date": date.today(), "currency_note": "",
    "discovery_notes": "", "client_goals": "", "client_questions": "",
    "package_name": "", "package_description": "", "deliverables_input": "",
    "exclusions_input": "", "assumptions_input": "", "template_text": "",
    "milestones_input": "", "timeline_notes": "", "extra_assumptions": "",
    "extra_exclusions": "", "proposal_output": "",
}
for k, v in defaults.items():
    init(k, v)

# Streamlit removes widget state when a widget is not rendered on the current
# page. Keep durable application data under stable keys and use separate
# widget keys (ui_<field>) so navigation cannot erase saved values.
def sync_field(field):
    widget_key = f"ui_{field}"
    if widget_key in st.session_state:
        st.session_state[field] = st.session_state[widget_key]

def field_value(field):
    return st.session_state.get(field, defaults.get(field, ""))

def lines(value):
    return [line.strip(" •-\t") for line in value.splitlines() if line.strip(" •-\t")]

def section(title, body):
    return f"\n\n## {title}\n{body.strip() if body.strip() else '[Needs client/company confirmation]'}"

def make_proposal():
    company = st.session_state.company_name.strip() or "[Company name]"
    client = st.session_state.client_name.strip() or "[Client name]"
    package = st.session_state.package_name.strip() or "[Selected service package]"
    proposal_title = st.session_state.proposal_title.strip() or "Project Proposal"
    proposal_date = st.session_state.proposal_date
    intro = (
        f"# {proposal_title}\n\n**Prepared by:** {company}\n\n"
        f"**Prepared for:** {client}\n\n**Date:** {proposal_date.strftime('%d %B %Y')}\n\n"
        f"**Service package:** {package}\n\n"
        "> **Draft for review:** Generated only from information supplied. Resolve confirmation items before sharing."
    )
    template = st.session_state.template_text.strip()
    template_section = section("Approved company template / standard wording", template) if template else (
        "\n\n## Company template\n[No approved company template supplied. Replace this note with your approved template before sending.]"
    )
    discovery = st.session_state.discovery_notes.strip() or "[Discovery notes not provided — confirm client requirements.]"
    goals = st.session_state.client_goals.strip() or "[Success criteria need client confirmation.]"
    package_desc = st.session_state.package_description.strip() or "[Package description needs confirmation.]"
    deliverables = "\n".join(f"- {x}" for x in lines(st.session_state.deliverables_input)) or "- [Confirm deliverables from the approved package]"
    assumptions = lines(st.session_state.assumptions_input) + lines(st.session_state.extra_assumptions)
    exclusions = lines(st.session_state.exclusions_input) + lines(st.session_state.extra_exclusions)
    milestones = "\n".join(f"- {x}" for x in lines(st.session_state.milestones_input)) or "- [Milestones and dates need confirmation]"
    questions = lines(st.session_state.client_questions)
    checks = [
        ("company_name", "What company name should appear on the proposal?"),
        ("client_name", "Who is the authorized client / organization?"),
        ("package_name", "Which approved service package is being proposed?"),
        ("package_description", "Can the package description and scope be confirmed?"),
    ]
    for key, question in checks:
        if not st.session_state[key].strip():
            questions.append(question)
    if not lines(st.session_state.deliverables_input):
        questions.append("What exact deliverables are included in the selected package?")
    if not lines(st.session_state.milestones_input):
        questions.append("What milestones and target dates have been agreed?")
    if not st.session_state.currency_note.strip():
        questions.append("Is pricing applicable, and who will provide approved pricing?")
    questions = list(dict.fromkeys(questions))
    assumption_text = "\n".join(f"- {x}" for x in assumptions) or "- [Confirm assumptions; do not treat unapproved assumptions as commitments.]"
    exclusion_text = "\n".join(f"- {x}" for x in exclusions) or "- [Confirm what is explicitly out of scope.]"
    question_text = "\n".join(f"- {x}" for x in questions) or "- Confirm the final scope, draft, and approval process."
    pricing = st.session_state.currency_note.strip() or "[Pricing not supplied — do not send a price until approved.]"
    timeline_notes = st.session_state.timeline_notes.strip()
    return (
        intro + template_section
        + section("1. Background and discovery summary", discovery)
        + section("2. Client goals and success criteria", goals)
        + section("3. Selected package and scope", package_desc)
        + section("4. Deliverables", deliverables)
        + section("5. Assumptions", assumption_text)
        + section("6. Exclusions / out of scope", exclusion_text)
        + section("7. Milestones and timeline", milestones + (f"\n\n**Timing notes:** {timeline_notes}" if timeline_notes else ""))
        + section("8. Pricing and commercial details", pricing)
        + section("9. Questions requiring client confirmation", question_text)
        + "\n\n## 10. Approval and next steps\n"
          "- Client to review and confirm requirements, deliverables, assumptions, exclusions, and milestones.\n"
          "- Company representative to verify pricing and insert approved commercial terms.\n"
          "- Do not treat this draft as an approved contract or final commitment until authorized reviewers approve it.\n"
    )

# ---------- Sidebar ----------
def reset_draft():
    # Reset both durable application data and widget keys. This callback runs
    # before widgets are instantiated, so changing the navigation key is safe.
    for key, value in defaults.items():
        st.session_state[key] = value
        ui_key = f"ui_{key}"
        if ui_key in st.session_state:
            st.session_state[ui_key] = value
    st.session_state["page_navigation"] = "Overview"

with st.sidebar:
    st.markdown('<div class="sidebar-brand">ScopeCraft<span style="color:#8fb0ff">.</span></div><div class="sidebar-sub">Proposal Studio · Workspace</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-label">Workspace navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "Workspace navigation",
        ["Overview", "Client & Discovery", "Scope & Deliverables", "Timeline & Pricing", "Template & Review", "Generated Proposal"],
        label_visibility="collapsed",
        key="page_navigation",
    )
    st.divider()
    st.markdown('<div class="sidebar-label">Current draft</div>', unsafe_allow_html=True)
    status = "Generated" if st.session_state.proposal_output else "In progress"
    st.markdown(f'<div class="sidebar-card"><div class="sidebar-label">Status</div><div class="sidebar-value">{status}</div></div>', unsafe_allow_html=True)
    required = ["company_name", "client_name", "discovery_notes", "package_name", "package_description", "deliverables_input", "milestones_input"]
    completed = sum(bool(str(st.session_state[k]).strip()) for k in required)
    progress = completed / len(required)
    st.progress(progress, text=f"{completed} of {len(required)} key fields")
    st.caption("Drafting support only. Confirm scope, dates and approved pricing before sending.")
    st.divider()
    st.button("Start a new draft", use_container_width=True, on_click=reset_draft)

# ---------- Main content ----------
st.markdown('<div class="hero"><div class="eyebrow">Client delivery workspace</div><h2>Build clear proposals. Align expectations.</h2><p>Turn discovery conversations into a structured scope of work with clear deliverables, assumptions, exclusions, milestones, and client questions — without inventing pricing.</p></div>', unsafe_allow_html=True)

def page_heading(kicker, title, desc):
    st.markdown(f'<div class="step-pill">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.write(desc)
    st.write("")

if page == "Overview":
    page_heading("WORKSPACE OVERVIEW", "Welcome to your proposal workspace", "Complete each section from the sidebar, then generate a draft for review.")
    a, b, c = st.columns(3)
    with a:
        st.metric("Workflow", "6 sections")
    with b:
        st.metric("Pricing", "Never invented")
    with c:
        st.metric("Output", "Editable draft")
    st.write("")
    st.subheader("Your workflow")
    workflow = [
        ("01", "Client & Discovery", "Capture client context, goals, and discovery notes."),
        ("02", "Scope & Deliverables", "Select the approved package and define what is included."),
        ("03", "Timeline & Pricing", "Add milestones and approved pricing notes, if available."),
        ("04", "Template & Review", "Reuse company-approved wording and identify open questions."),
        ("05", "Generated Proposal", "Generate, edit, and download the proposal draft."),
    ]
    for n, title, desc in workflow:
        with st.container(border=True):
            x, y = st.columns([1, 8])
            with x:
                st.markdown(f'<div style="font-size:1.3rem;font-weight:800;color:#315fce;padding-top:5px">{n}</div>', unsafe_allow_html=True)
            with y:
                st.markdown(f"**{title}**")
                st.markdown(f'<span class="small-note">{desc}</span>', unsafe_allow_html=True)
    st.info("Start with Client & Discovery in the sidebar. Your entries are kept in this app session as you move between sections.")

elif page == "Client & Discovery":
    page_heading("STEP 01", "Client & discovery", "Capture the people, context, and outcomes behind this proposal.")
    with st.container(border=True):
        st.subheader("Proposal identity")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Company name", key="ui_company_name", value=field_value("company_name"), on_change=sync_field, args=("company_name",), placeholder="e.g., Northstar Digital")
            st.text_input("Client / organization", key="ui_client_name", value=field_value("client_name"), on_change=sync_field, args=("client_name",), placeholder="e.g., Acme Group")
        with c2:
            st.text_input("Proposal title", key="ui_proposal_title", value=field_value("proposal_title"), on_change=sync_field, args=("proposal_title",))
            st.date_input("Proposal date", key="ui_proposal_date", value=field_value("proposal_date"), on_change=sync_field, args=("proposal_date",))
    with st.container(border=True):
        st.subheader("Discovery notes")
        st.text_area("Meeting notes, needs, constraints, and background", key="ui_discovery_notes", value=field_value("discovery_notes"), on_change=sync_field, args=("discovery_notes",), height=200,
                     placeholder="Summarize what the client said. Keep unconfirmed details clearly identified.")
        st.text_area("Client goals and success criteria", key="ui_client_goals", value=field_value("client_goals"), on_change=sync_field, args=("client_goals",), height=110,
                     placeholder="What should improve? How will success be measured?")
        st.text_area("Known open questions (optional)", key="ui_client_questions", value=field_value("client_questions"), on_change=sync_field, args=("client_questions",), height=100,
                     placeholder="Questions already identified during discovery")

elif page == "Scope & Deliverables":
    page_heading("STEP 02", "Scope & deliverables", "Use the selected, approved package as the source of truth for the work included.")
    with st.container(border=True):
        st.subheader("Selected service package")
        st.text_input("Package name", key="ui_package_name", value=field_value("package_name"), on_change=sync_field, args=("package_name",), placeholder="e.g., Website Essentials")
        st.text_area("Package description / approved scope", key="ui_package_description", value=field_value("package_description"), on_change=sync_field, args=("package_description",), height=140,
                     placeholder="Paste approved package details. Avoid adding unapproved commitments.")
    with st.container(border=True):
        st.subheader("What is included")
        st.text_area("Approved deliverables — one per line", key="ui_deliverables_input", value=field_value("deliverables_input"), on_change=sync_field, args=("deliverables_input",), height=150,
                     placeholder="Responsive landing page\nContact form\nBasic analytics setup")
        st.text_area("Assumptions — one per line", key="ui_assumptions_input", value=field_value("assumptions_input"), on_change=sync_field, args=("assumptions_input",), height=110,
                     placeholder="Client supplies final copy\nClient provides brand assets")
        st.text_area("Exclusions — one per line", key="ui_exclusions_input", value=field_value("exclusions_input"), on_change=sync_field, args=("exclusions_input",), height=110,
                     placeholder="Paid advertising\nOngoing maintenance")
        st.text_area("Additional assumptions to confirm (optional)", key="ui_extra_assumptions", value=field_value("extra_assumptions"), on_change=sync_field, args=("extra_assumptions",), height=80)
        st.text_area("Additional exclusions to confirm (optional)", key="ui_extra_exclusions", value=field_value("extra_exclusions"), on_change=sync_field, args=("extra_exclusions",), height=80)

elif page == "Timeline & Pricing":
    page_heading("STEP 03", "Timeline & commercial details", "Enter confirmed milestones and approved pricing information. Leave uncertain details open for confirmation.")
    with st.container(border=True):
        st.subheader("Milestones")
        st.text_area("Milestones — one per line; use confirmed dates only", key="ui_milestones_input", value=field_value("milestones_input"), on_change=sync_field, args=("milestones_input",), height=190,
                     placeholder="Discovery sign-off — date to be confirmed\nDesign review — date to be confirmed\nDelivery and handover — date to be confirmed")
        st.text_input("Timing constraints / deadline notes (optional)", key="ui_timeline_notes", value=field_value("timeline_notes"), on_change=sync_field, args=("timeline_notes",),
                      placeholder="e.g., Client launch target; exact date not confirmed")
    with st.container(border=True):
        st.subheader("Pricing safeguard")
        st.text_input("Approved pricing or commercial note (optional)", key="ui_currency_note", value=field_value("currency_note"), on_change=sync_field, args=("currency_note",),
                      placeholder="e.g., Pricing to be confirmed by account manager")
        st.warning("Do not enter estimates as approved pricing. If no approved price is available, leave this blank and the draft will flag it for confirmation.")

elif page == "Template & Review":
    page_heading("STEP 04", "Company template & review", "Reuse approved wording and check the draft for missing information before sharing.")
    with st.container(border=True):
        st.subheader("Approved company template")
        st.text_area("Paste your approved proposal template or standard wording", key="ui_template_text", value=field_value("template_text"), on_change=sync_field, args=("template_text",), height=260,
                     placeholder="Paste approved company wording here. If blank, the draft will clearly flag that no approved template was supplied.")
        st.caption("This tool does not know your company's internal policies, legal terms, or standard clauses unless you provide them.")
    with st.container(border=True):
        st.subheader("Readiness check")
        checks = [
            ("Company name", "company_name"), ("Client name", "client_name"),
            ("Discovery notes", "discovery_notes"), ("Selected package", "package_name"),
            ("Package description", "package_description"), ("Approved deliverables", "deliverables_input"),
            ("Milestones", "milestones_input"), ("Approved template (recommended)", "template_text"),
            ("Pricing note (if applicable)", "currency_note"),
        ]
        for label, key in checks:
            value = bool(str(st.session_state[key]).strip())
            st.write(("✅ " if value else "○ ") + label + (" — provided" if value else " — still needed"))
        st.caption("Missing fields are allowed, but the generated draft will flag them for confirmation.")

elif page == "Generated Proposal":
    page_heading("STEP 05", "Generated proposal", "Generate the draft, review it carefully, edit as needed, then download the final draft.")
    if st.button("Generate / refresh proposal draft", type="primary", use_container_width=True):
        st.session_state.proposal_output = make_proposal()
    if not st.session_state.proposal_output:
        st.info("No draft generated yet. Fill in the sections in the sidebar, then select Generate / refresh proposal draft.")
    else:
        st.success("Draft generated. Review all placeholder notes and client-confirmation questions before sending.")
        def sync_proposal_editor():
            st.session_state.proposal_output = st.session_state.get(
                "proposal_editor", st.session_state.proposal_output
            )

        st.text_area(
            "Edit your proposal draft",
            value=st.session_state.proposal_output,
            height=620,
            key="proposal_editor",
            on_change=sync_proposal_editor,
        )
        d1, d2 = st.columns(2)
        with d1:
            st.download_button("Download Markdown (.md)", data=st.session_state.proposal_output.encode("utf-8"),
                               file_name="proposal_draft.md", mime="text/markdown", use_container_width=True)
        with d2:
            st.download_button("Download plain text (.txt)", data=st.session_state.proposal_output.encode("utf-8"),
                               file_name="proposal_draft.txt", mime="text/plain", use_container_width=True)
        with st.expander("Final quality checklist"):
            st.markdown("""
            - [ ] Deliverables match the approved service package.
            - [ ] Assumptions and exclusions are clear.
            - [ ] Milestones and dates are confirmed or marked as pending.
            - [ ] Pricing is approved or clearly marked as pending.
            - [ ] Approved company template and terms are included.
            - [ ] All client questions are resolved before sending.
            """)

st.markdown("---")
st.markdown('<div class="small-note">ScopeCraft Proposal Studio · Internal drafting aid · Review all details before sharing externally.</div>', unsafe_allow_html=True)
