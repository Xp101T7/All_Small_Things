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
    combined_mitre=mvappend(mitre, mitre_T1, mitre_TA)
| eval 
    combined_mitre=split(mvjoin(combined_mitre, ","), ",")
| eval 
    combined_mitre=mvfilter(match(combined_mitre, "^(?i)(T\d{1,4}(\.\d{1,3})?|TA\d{4}(\.\d{1,3})?)$")),
    combined_mitre=mvmap(combined_mitre, upper(trim(combined_mitre)))
| stats values(combined_mitre) as unique_mitre
| eval 
    annotations=if(
        isnotnull(unique_mitre) AND mvcount(unique_mitre) > 0, 
        "(\"mitre_attack\":[\"" + mvjoin(unique_mitre, "\", \"") + "\"])", 
        null()
    )

---

| eval mitre=coalesce(mitre, "")
| eval mitre_T1=coalesce(mitre_T1, "")
| eval mitre_TA=coalesce(mitre_TA, "")
| eval combined_mitre = mvappend(
    split(mitre, ","),
    split(mitre_T1, ","),
    split(mitre_TA, ",")
)
| eval combined_mitre = mvmap(combined_mitre, trim(upper(combined_mitre)))
| eval combined_mitre = mvfilter(match(combined_mitre, "^(T\d{1,4}(\.\d{1,3})?|TA\d{4}(\.\d{1,3})?)$"))
| eval combined_mitre = mvdedup(combined_mitre)
| eval unique_count = mvcount(combined_mitre)
| eval unique_combined_mitre = mvjoin(combined_mitre, "\",\"")
| eval annotations = if(
    isnotnull(unique_combined_mitre) AND unique_count > 0, 
    "(\"mitre_attack\":[\"" + unique_combined_mitre + "\"])", 
    null()
)

