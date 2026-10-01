select
    md5(policy_id) as policy_key,
    policy_id,
    policy_number,
    customer_id,
    line_of_business,
    risk_state,
    effective_date,
    expiration_date,
    annual_premium,
    coverage_limit
from {{ ref('stg_policies') }}
