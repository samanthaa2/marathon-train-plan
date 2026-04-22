# A file where the behind the scenes calculations for the plan are conducted
# version 1 rules
# 1. Put long run on preferred day.
# 2. Keep required off days as rest.
# 3. If running_days >= 5, include one workout day.
# 4. Do not place workout next to long run if possible.
# 5. Fill remaining running days with easy runs.
# 6. Long run starts at longest_recent_run + 1, capped reasonably.
# 7. Easy pace = average pace + 0.5 to 1.5
# 8. Long run pace = average pace + 0.75 to 1.75
