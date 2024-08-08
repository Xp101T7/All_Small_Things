| eval urgency=case(
    match(urgency, "Critical"), "Critical",
    match(urgency, "high"), "high",
    match(urgency, "medium"), "medium",
    match(urgency, "low"), "low",
    1=1, "informational"
)
| eval mitre_matches=mvappend(
    mvfilter(match(mitre, "(?i)^(T\\d{4}(\\.\\d{3})?|TA\\d{4})$")),
    mvfilter(match(mitre_T1, "(?i)^(T\\d{4}(\\.\\d{3})?|TA\\d{4})$"))
)
| eval mitre_matches=mvdedup(mitre_matches)
| eval mitre_matches=mvmap(mitre_matches, upper(_))
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


----

| eval 
    urgency=case(
        match(urgency, "Critical"), "Critical", 
        match(urgency, "high"), "high", 
        match(urgency, "medium"), "medium", 
        match(urgency, "low"), "low", 
        1=1, "informational"
    ),
    mitre_matches=mvappend(
        mvfilter(match(mitre, "(?i)\\b(TA\\d{4}(\\.\\d{3})?|T1\\d{3}(\\.\\d{3})?)\\b")),
        mvfilter(match(mitre_T1, "(?i)\\b(TA\\d{4}(\\.\\d{3})?|T1\\d{3}(\\.\\d{3})?)\\b"))
    ),
    annotations=if(
        isnotnull(mitre_matches), 
        "(\"mitre_attack\":[\"" + mvjoin(mitre_matches, "\", \"") + "\"])", 
        null()
    )

---

| eval 
    combined_mitre=mvappend(mitre, mitre_T1),
    combined_mitre=mvmap(combined_mitre, split(combined_mitre, ",\s*"))
| eval 
    mitre_matches=mvfilter(match(combined_mitre, "(?-i)^(TA\d{4}(\.\d{3})?|T1\d{3}(\.\d{3})?)$")),
    mitre_matches=mvmap(mitre_matches, upper(mitre_matches))
| eval
    annotations=if(
        isnotnull(mitre_matches), 
        "(\"mitre_attack\":[\"" + mvjoin(mitre_matches, "\", \"") + "\"])", 
        null()
    )