with reserves as (
    select
        reserve_event_id::varchar as transaction_id,
        claim_id::varchar as claim_id,
        transaction_date::date as transaction_date,
        reserve_change_amount::number(18, 2) as reserve_change_amount,
        0::number(18, 2) as payment_amount,
        reserve_reason::varchar as transaction_detail,
        recorded_at::timestamp_tz as recorded_at
    from {{ source('claims_raw', 'reserve_transactions') }}
),

payments as (
    select
        payment_id::varchar as transaction_id,
        claim_id::varchar as claim_id,
        payment_date::date as transaction_date,
        0::number(18, 2) as reserve_change_amount,
        payment_amount::number(18, 2) as payment_amount,
        payment_type::varchar as transaction_detail,
        recorded_at::timestamp_tz as recorded_at
    from {{ source('claims_raw', 'payments') }}
)

select 'RESERVE'::varchar as transaction_type, * from reserves
union all
select 'PAYMENT'::varchar as transaction_type, * from payments
