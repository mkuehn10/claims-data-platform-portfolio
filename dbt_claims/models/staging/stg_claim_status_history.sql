select
    status_event_id::varchar as status_event_id,
    claim_id::varchar as claim_id,
    upper(trim(status))::varchar as status,
    status_effective_at::timestamp_tz as status_effective_at,
    recorded_at::timestamp_tz as recorded_at,
    datediff('day', status_effective_at, recorded_at) as arrival_lag_days
from {{ source('claims_raw', 'claim_status_history') }}
