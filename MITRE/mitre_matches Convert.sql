| eval urgency=case(
    match(urgency, "Critical"), "Critical",
    match(urgency, "high"), "high",
    match(urgency, "medium"), "medium",
    match(urgency, "low"), "low",
    1=1, "informational"
)
| eval mitre_matches=mvappend(
    mvfilter(match(mitre, "(?i)\\b(T\\d{4}(\\.\\d{3})?|TA\\d{4})\\b")),
    mvfilter(match(mitre_T1, "(?i)\\b(T\\d{4}(\\.\\d{3})?|TA\\d{4})\\b"))
)
| eval mitre_matches=mvdedup(mitre_matches)
| eval annotations=if(
    isnotnull(mitre_matches),
    "(\"mitre_attack\":[\"" + mvjoin(mitre_matches, "\", \"") + "\"])",
    null()
)
| eval duplicate_count=if(
    isnotnull(mitre_matches),
    mvcount(mitre_matches) - mvcount(mvdedup(mitre_matches)),
    null()
)