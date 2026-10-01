# Terraform local lifecycle mini-lab

This lab demonstrates configuration, dependency ordering, `plan`, `apply`, state, replacement, and `destroy` without provisioning paid cloud infrastructure. It creates a random environment suffix, renders one local file, and runs a local command through `terraform_data`.

## Run

Prerequisite: Terraform 1.5+.

```powershell
terraform init
terraform fmt -check
terraform validate
terraform plan -out=tfplan
terraform show tfplan
terraform apply tfplan
terraform state list
terraform state show local_file.lab_manifest
terraform output
terraform plan -var="message=changed input"
terraform destroy
```

Generated `.terraform/`, lock/state/plan files, and `generated/` are ignored. Never commit real state: it can contain sensitive values even when configuration does not.

## Concepts to observe

- `terraform plan` compares configuration, current state, provider behavior, and refreshed real resources.
- `terraform apply tfplan` executes the reviewed saved plan; a newly generated plan might differ.
- State maps Terraform addresses to resource identities and attributes. It is not merely a cache.
- Changing `message` updates the file and replaces `terraform_data.audit` because `triggers_replace` changes.
- `depends_on` makes the teaching dependency explicit; prefer inferred dependencies through references in normal code.
- `destroy` proposes deletion of managed resources; inspect its plan with the same care as creation.

Production teams generally use encrypted remote state, locking, restricted access, backups, separate environments, reviewed plans, and pinned provider versions. State commands such as `mv`, `rm`, and import-related workflows require care because they can change Terraform's ownership model without changing infrastructure.

## Honest boundaries

This lab does not test cloud APIs, IAM, networking, remote backends/locking, policy-as-code, drift under concurrent operators, modules, CI approvals, or secret handling. `local_file` and `terraform_data` teach lifecycle semantics but do not reproduce the failure modes of distributed cloud infrastructure.

## Interview talking points

- Walk through configuration → init → plan → reviewed apply → state → destroy.
- Explain why saved plans, provider lock files, remote state locking, and least-privilege CI identities matter.
- Distinguish a resource replacement from an in-place update and discuss blast radius.
- Be explicit that this lab proves Terraform workflow familiarity, not production cloud operations.
