with claims as (
    select * from {{ ref('stg_claims') }}
),

financials as (
    select * from {{ ref('int_claim_financials') }}
)

select
    md5(claims.claim_id) as claim_key,
    md5(claims.policy_id) as policy_key,
    claims.claim_id,
    claims.loss_date,
    claims.reported_at,
    claims.current_status,
    claims.coverage_type,
    claims.loss_state,
    coalesce(financials.case_reserve_amount, 0) as case_reserve_amount,
    coalesce(financials.paid_amount, 0) as paid_amount,
    coalesce(financials.outstanding_amount, 0) as outstanding_amount,
    datediff(
        'day',
        claims.reported_at::date,
        coalesce(claims.closed_at::date, current_date)
    ) as lifecycle_days
from claims
left join financials using (claim_id)
