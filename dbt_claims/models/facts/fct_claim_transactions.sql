{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='transaction_id',
        on_schema_change='sync_all_columns'
    )
}}

with transactions as (
    select *
    from {{ ref('stg_claim_transactions') }}
    {% if is_incremental() %}
        -- Reprocess a lookback window so delayed source records are merged safely.
        where recorded_at >= (
            select dateadd('day', -14, coalesce(max(recorded_at), '1900-01-01'))
            from {{ this }}
        )
    {% endif %}
)

select
    transaction_id,
    md5(claim_id) as claim_key,
    claim_id,
    transaction_type,
    transaction_date,
    reserve_change_amount,
    payment_amount,
    transaction_detail,
    recorded_at
from transactions
