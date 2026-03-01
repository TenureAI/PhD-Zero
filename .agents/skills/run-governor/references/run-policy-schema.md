# run_policy.yaml (reference)

```yaml
run_id: "20260301_190000-reproduce-ppo"
mode: "moderate" # full-auto|moderate|detailed
high_resource:
  low: "<2 gpu-hours and <20 usd equivalent"
  medium: "2-10 gpu-hours or 20-100 usd equivalent"
  high: ">10 gpu-hours or >100 usd equivalent or long multi-node"
safety:
  major_risk_examples:
    - mass file deletion
    - secret exposure
    - destructive remote mutations
  full_auto_interrupt_only_on_major_risk: true
allowances:
  # action_type -> policy
  rm_workspace_cache: "allow-once" # allow-once|allow-run|disallow|custom
  custom_notes: ""
```
