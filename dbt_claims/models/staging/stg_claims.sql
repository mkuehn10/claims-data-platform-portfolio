with source as (
    select * from {{ source('claims_raw', 'claims') }}
)

select
    trim(claim_id)::varchar as claim_id,
    trim(claim_number)::varchar as claim_number,
    trim(policy_id)::varchar as policy_id,
    loss_date::date as loss_date,
    reported_at::timestamp_tz as reported_at,
    upper(trim(fnol_channel))::varchar as fnol_channel,
    lower(trim(cause_of_loss))::varchar as cause_of_loss,
    upper(trim(coverage_type))::varchar as coverage_type,
    upper(trim(loss_state))::varchar as loss_state,
    upper(trim(current_status))::varchar as current_status,
    nullif(closed_at, '')::timestamp_tz as closed_at,
    nullif(reopened_at, '')::timestamp_tz as reopened_at,
    loaded_at::timestamp_tz as loaded_at
from source
