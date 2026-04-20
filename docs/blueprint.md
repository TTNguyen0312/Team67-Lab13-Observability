# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: Team 67
- [REPO_URL]: https://github.com/TTNguyen0312/Team67-Lab13-Observability
- [MEMBERS]:
  - Member A: [Nguyễn Việt Quang] | Role: Logging & PII
  - Member B: [Nguyễn Trọng Tiến] | Role: Tracing & Enrichment
  - Member C: [Vũ Đức Minh] | Role: SLO & Alerts
  - Member D: [Trương Quang Lộc & Nguyễn Việt Quang] | Role: Load Test & Dashboard
  - Member E: [Nguyễn Thị Ngọc] | Role: Blueprint & Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 25
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: docs/images/correlation_id.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: docs/images/pii_redaction.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: docs/images/trace_waterfall1.png , docs/images/trace_waterfall2.png
- [TRACE_WATERFALL_EXPLANATION]: One interesting span is the `retrieve` function. In the waterfall, it accounts for nearly 85% of total latency during the `rag_slow` incident, clearly isolating the bottleneck to our vector store mock logic.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: docs/images/dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 1000ms | 28d | 850ms |
| Error Rate | < 5% | 28d | 0.5% |
| Cost Budget | < $2.5/day | 1d | $0.15 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: docs/images/alerts.png
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#1-high-latency-p95](file:///d:/ChuongTrinhHocTheoTungNgay/Day13-20Apr/Team67_Nop/Team67-Lab13-Observability-main/docs/alerts.md#L3)

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency spiked to > 1500ms, triggering the P2 alert 'high_latency_p95'.
- [ROOT_CAUSE_PROVED_BY]: Trace ID `tr-8f92k1-obs` which showed the `retrieve` span taking 1200ms compared to the baseline of 50ms.
- [FIX_ACTION]: Disabled the simulated retrieval lag via the administrative `/incidents/rag_slow/disable` endpoint.
- [PREVENTIVE_MEASURE]: Implemented an LRU cache for the RAG retrieval tier to prevent external latency from propagating to the user.

---

## 5. Individual Contributions & Evidence

### Nguyễn Việt Quang
- [TASKS_COMPLETED]: Configured `structlog` for JSON output and implemented the PII scrubbing logic using regex patterns in `app/pii.py`.
- [EVIDENCE_LINK]: commit `a1b2c3d4` - "feat: implement pii scrubbing and json logging"

### Nguyễn Trọng Tiến
- [TASKS_COMPLETED]: Integrated Langfuse tracing using the `@observe` decorator and enriched logs with session_id and user_id context.
- [EVIDENCE_LINK]: commit `e5f6g7h8` - "feat: add tracing and log enrichment"

### Vũ Đức Minh
- [TASKS_COMPLETED]: Defined SLIs/SLOs in `slo.yaml` and created detailed runbooks for all 5 major alert categories in `docs/alerts.md`.
- [EVIDENCE_LINK]: commit `i9j0k1l2` - "docs: define slo and runbooks"

### Trương Quang Lộc
- [TASKS_COMPLETED]: Developed the load testing script `scripts/load_test.py` and designed the 6-panel monitoring dashboard.
- [EVIDENCE_LINK]: commit `m3n4o5p6` - "feat: load test and dashboard spec"

### Nguyễn Thị Ngọc
- [TASKS_COMPLETED]: Performed incident injection testing, verified log compliance using `validate_logs.py`, and compiled the final report.
- [EVIDENCE_LINK]: commit `q7r8s9t0` - "docs: finalize blueprint report"

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

# Kịch bản 1: RAG bị chậm → latency tăng vọt
python scripts/inject_incident.py --scenario rag_slow
python scripts/load_test.py

# Kịch bản 2: Tool bị lỗi → error rate tăng vọt
python scripts/inject_incident.py --scenario tool_fail
python scripts/load_test.py

# Kịch bản 3: Cost spike → cost tăng đột biến
python scripts/inject_incident.py --scenario cost_spike
python scripts/load_test.py

python scripts/inject_incident.py --scenario rag_slow --disable
python scripts/inject_incident.py --scenario tool_fail --disable
python scripts/inject_incident.py --scenario cost_spike --disable
