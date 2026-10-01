with source as (
    select * from {{ source('claims_raw', 'policies') }}
)

select
    trim(policy_id)::varchar as policy_id,
    trim(policy_number)::varchar as policy_number,
    trim(customer_id)::varchar as customer_id,
    upper(trim(line_of_business))::varchar as line_of_business,
    upper(trim(risk_state))::varchar as risk_state,
    effective_date::date as effective_date,
    expiration_date::date as expiration_date,
    annual_premium::number(18, 2) as annual_premium,
    coverage_limit::number(18, 2) as coverage_limit,
    loaded_at::timestamp_tz as loaded_at
from source
