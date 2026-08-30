# Project Decisions

## Game start

### Decision
Players start with one already-floated company.
Starter companies are active from game setup and are exempt from the normal 50% flotation threshold. Their initial capital comes only from shares actually purchased during setup. The exact size of the founder's starting stake remains an open balance decision.

### Reason
Game will not force a delay in operations of comapnies.

### Consequences
Game will be fully playable from the begining and will be generating data.

## New companies activation

### Decision
Companies will activate after selling at least 50% of shares with money earned by that.

### Reason
More realistic source of money and no need to wait for company to sell all or almost all shares.

### Consequences
Company will start with real money from real investors, not with cash granted by bank for some reason. Company ovned even 50% of their shares will not decided by themself, its just shares to sell in future, but ownership will be move to new president.


## Domain invariants

### Share transactions
- Quantity must be greater than zero.
- Buyer must have enough money.
- Company must have enough shares available.
- Failed transaction must not change state.
- Successful transaction must update both player and company consistently.