from your-index
| where event.action == "user_lockout"
| eval bucket_date = bucket("@timestamp", "1d")
| stats count(*) as daily_lockouts by user.name, bucket_date
| stats avg(daily_lockouts) as avg_lockouts,
        median_absolute_deviation(daily_lockouts) as mad_lockouts,
        values(bucket_date) as dates,
        values(daily_lockouts) as daily_counts
  by user.name
| mv_expand dates, daily_counts
| eval threshold = avg_lockouts + mad_lockouts
| where daily_counts > threshold
| sort daily_counts desc