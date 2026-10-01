{% snapshot snp_claim_status %}

{{
    config(
        unique_key='claim_id',
        strategy='check',
        check_cols=['current_status', 'closed_at', 'reopened_at'],
        invalidate_hard_deletes=True
    )
}}

select
    claim_id,
    current_status,
    closed_at,
    reopened_at,
    loaded_at
from {{ ref('stg_claims') }}

{% endsnapshot %}
