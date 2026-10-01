select
    policy.line_of_business,
    date_trunc('month', claim.reported_at)::date as reported_month,
    count(*) as reported_claim_count,
    count_if(claim.current_status in ('OPEN', 'REOPENED')) as open_claim_count,
    sum(claim.paid_amount) as paid_amount,
    sum(claim.outstanding_amount) as outstanding_amount,
    avg(claim.lifecycle_days) as average_lifecycle_days,
    sum(claim.paid_amount + claim.outstanding_amount)
        / nullif(sum(policy.annual_premium), 0) as incurred_to_premium_ratio
from {{ ref('fct_claim') }} as claim
inner join {{ ref('dim_policy') }} as policy using (policy_key)
group by 1, 2
