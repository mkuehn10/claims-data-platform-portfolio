select claim_id
from {{ ref('fct_claim') }}
where current_status = 'CLOSED'
  and abs(outstanding_amount) > 0.02
