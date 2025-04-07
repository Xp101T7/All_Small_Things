from your-index
| where event.action == "user_lockout"
| eval lockout_date = date_trunc('1d', '@timestamp')
| stats daily_lockouts = count() by user.name, lockout_date
| stats avg_daily_lockouts = avg(daily_lockouts), mad_daily_lockouts = MEDIAN_ABSOLUTE_DEVIATION(daily_lockouts) by user.name
| eval threshold = avg_daily_lockouts + mad_daily_lockouts
| where daily_lockouts > threshold
| sort daily_lockouts desc