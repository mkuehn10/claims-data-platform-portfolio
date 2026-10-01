select claim.claim_id
from {{ ref('stg_claims') }} as claim
inner join {{ ref('stg_policies') }} as policy using (policy_id)
where claim.loss_date < policy.effective_date
   or claim.loss_date >= policy.expiration_date
