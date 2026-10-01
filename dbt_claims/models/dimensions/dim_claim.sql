select
    md5(claim_id) as claim_key,
    md5(policy_id) as policy_key,
    claim_id,
    claim_number,
    loss_date,
    reported_at,
    fnol_channel,
    cause_of_loss,
    coverage_type,
    loss_state,
    current_status,
    closed_at,
    reopened_at
from {{ ref('stg_claims') }}
