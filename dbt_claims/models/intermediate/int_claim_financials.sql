with transactions as (
    select * from {{ ref('stg_claim_transactions') }}
),

aggregated as (
    select
        claim_id,
        sum(reserve_change_amount) as case_reserve_amount,
        sum(payment_amount) as paid_amount,
        min(transaction_date) as first_transaction_date,
        max(transaction_date) as latest_transaction_date,
        max(recorded_at) as latest_recorded_at
    from transactions
    group by claim_id
)

select
    claim_id,
    case_reserve_amount,
    paid_amount,
    case_reserve_amount - paid_amount as outstanding_amount,
    first_transaction_date,
    latest_transaction_date,
    latest_recorded_at
from aggregated
