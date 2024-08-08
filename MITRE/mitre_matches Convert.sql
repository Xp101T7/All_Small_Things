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

| eval urgency=case(
    match(urgency, "Critical"), "Critical",
    match(urgency, "high"), "high",
    match(urgency, "medium"), "medium",
    match(urgency, "low"), "low",
    1=1, "informational"
)
| eval mitre_matches=mvfilter(match(mitre, "(?i)^(T\\d{4}(\\.\\d{3})?|TA\\d{4})$"))
| eval mitre_T1_matches=mvfilter(match(mitre_T1, "(?i)^(T\\d{4}(\\.\\d{3})?|TA\\d{4})$"))
| eval all_matches=coalesce(mitre_matches, "") + if(isnotnull(mitre_T1_matches), if(isnotnull(mitre_matches), ",", "") + mitre_T1_matches, "")
| eval all_matches=split(all_matches, ",")
| eval all_matches=mvdedup(all_matches)
| eval all_matches=mvmap(all_matches, upper(_))
| eval annotations=if(
    isnotnull(all_matches) AND mvcount(all_matches) > 0,
    "(\"mitre_attack\":[\"" + mvjoin(all_matches, "\", \"") + "\"])",
    null()
)
| eval duplicate_count=if(
    isnotnull(all_matches),
    mvcount(split(coalesce(mitre_matches, "") + if(isnotnull(mitre_T1_matches), "," + mitre_T1_matches, ""), ",")) - mvcount(all_matches),
    null()
)
| fields urgency, annotations, duplicate_count, all_matches

