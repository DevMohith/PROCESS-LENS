from typing import List, Dict

def fetch_process_data(query: str) -> Dict:
    return {
        "period": "Last 7 days",
        "process": "Procure-to-Pay",
        "kpis": {
            "avg_cycle_time_days": 12.4,
            "rework_rate": 0.18,
            "stuck_in_approval_pct": 0.27,
            "late_payment_pct": 0.11,
        },
        "bottleneck_examples": [
            {"step": "Approve PO", "median_wait_hours": 54, "owner":"Procurement", "cases_affected": 143},
            {"step": "3-way Match", "median_wait_hours": 37, "owner":"Shared Services", "cases_affected": 88},
            {"step": "Vendor Onboarding", "median_wait_hours": 29, "owner":"Vendor Mgmt", "cases_affected": 22},
        ],
        "top_variants": [
            {"variant": "Start→Create PO→Approve PO→3-way Match→Post Invoice→Pay", "share": 0.41},
            {"variant": "Start→Create PO→Approve PO→Rework→Approve PO→3-way Match→Pay", "share": 0.17}
        ],
    }

def send_to_llm_context(data: Dict) -> str:
    lines = [
        f"Process: {data.get('process')}",
        f"Period: {data.get('period')}",
        "KPIs:",
        f" - Avg cycle time (days): {data['kpis']['avg_cycle_time_days']}",
        f" - Rework rate: {data['kpis']['rework_rate']}",
        f" - Stuck in approval %: {data['kpis']['stuck_in_approval_pct']}",
        f" - Late payment %: {data['kpis']['late_payment_pct']}",
        "",
        "Bottlenecks:",
    ]
    for b in data["bottleneck_examples"]:
        lines.append(f" - Step: {b['step']} | Median wait (hrs): {b['median_wait_hours']} | Owner: {b['owner']} | Cases: {b['cases_affected']}")
    lines.append("")
    lines.append("Top Variants:")
    for v in data["top_variants"]:
        lines.append(f" - {v['variant']} (share: {v['share']})")
    return "\n".join(lines)
    