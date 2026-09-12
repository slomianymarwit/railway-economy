# Project Decisions


## Game start

### Decision
Each player starts the game with one already-floated and operational company.
Starter companies are active from the beginning of the game and are exempt from the normal flotation requirement that applies to newly introduced companies.
Their initial treasury is funded only by shares actually purchased during setup. The exact size of the founder's initial ownership stake remains an open balance decision.

### Reason
The game should allow railway operations to begin immediately instead of forcing players to spend the opening turns waiting for enough shares to be sold.
Starting with an operational company also ensures that the simulation begins generating transport, financial, and economic data from the first turns.
Using real share purchases as the source of starting capital keeps company financing consistent with the rest of the economic model.

### Alternatives considered
Requiring starter companies to reach the normal flotation threshold before becoming operational.
Giving starter companies a fixed amount of starting cash from the bank.
Requiring all shares, or almost all shares, to be sold before operations can begin.

### Consequences
Players can begin making operational decisions from the start of the game.
Starter companies may begin with different amounts of capital depending on the amount of equity purchased during setup.
The starter company is a special exception to normal flotation rules, while later companies continue to follow the standard market-based activation process.
The founder's initial ownership percentage remains a balance parameter and can be adjusted later without changing the underlying financing model.


## New company activation

### Decision
Companies introduced after the start of the game remain dormant until at least 50% of their shares have been sold.
Money paid for newly issued shares goes directly into the company's treasury.
Unsold shares remain available for future issuance and are not treated as being owned by the company itself.
Reaching the flotation threshold activates the company, but company ownership and company control remain determined by shareholder positions and presidency rules.

### Reason
A new company should begin operations only after attracting meaningful investor support.
Funding the company through actual share purchases provides a more realistic and internally consistent source of capital than granting money automatically from the bank.
A 50% flotation threshold allows companies to become operational without requiring almost the entire share supply to be sold first.

### Alternatives considered
Activating companies immediately when created.
Requiring 100% of shares to be sold before flotation.
Giving newly floated companies a fixed bank-funded starting treasury.
Treating unsold shares as if they were owned by the company.

### Consequences
New companies enter the game with capital that reflects real investor demand.
A company may begin operations while a substantial portion of its shares remains available for later sale.
Unsold shares do not influence control of the company.
Flotation, ownership, and presidency remain separate concepts: reaching 50% activates the company, while control depends on the distribution of shares among investors.
Future share issuance can continue to provide additional capital after flotation.


## Company presidency and tied shareholdings

### Decision
The president of a floated company is determined by share ownership.
If one shareholder owns more shares than every other shareholder, that player becomes the president.
If multiple shareholders are tied for the largest number of shares and the current president is one of them, the current president keeps control of the company. Therefore, another shareholder must own strictly more shares than the current president to take control.
If exactly 50% of the company's shares have been sold and the largest shareholders are tied, the company becomes floated but remains without a president.
If more than 50% of the company's shares have been sold, the company still has no president, and multiple shareholders are tied for the largest position, the shareholder who became a shareholder of the company first becomes the president.

### Reason
A tie should not automatically remove an existing president from control. Requiring another shareholder to exceed the president's position makes company takeovers deliberate rather than accidental.
Flotation and presidency are separate concepts. Reaching the flotation threshold activates the company, but does not require a president to be selected if ownership is evenly tied at exactly 50%.
If the company later moves beyond the flotation threshold while the leading shareholders remain tied and no president has yet been established, using the earliest shareholder provides a deterministic way to establish control.

### Alternatives considered
Leaving the company without a president until one shareholder obtains a larger position.
Assigning the presidency immediately at exactly 50% even when the largest shareholders are tied.
Giving the presidency to the shareholder who first reached the current highest number of shares.

### Consequences
A company can be floated and operational while temporarily having no president.
The current president remains protected during a tie but can lose control as soon as another shareholder owns more shares.
The order in which players first become shareholders can matter when a company receives its first president after passing the 50% flotation threshold.
Share ownership remains the source of company control; presidency does not represent ownership of the company itself.


## Domain invariants

### Share transactions
- Quantity must be greater than zero.
- Buyer must have enough money.
- Company must have enough shares available.
- Failed transaction must not change state.
- Successful transaction must update both player and company consistently.


## Cargo units and train cargo representation

### Decision
Goods transported by trains are measured in carloads.
A Good is identified by its name, so two objects with the same name represent the same type of good, the name of the Good is immutable.
One train car can carry exactly one carload of one type of good. A carload is an abstract transport unit and does not represent a fixed weight or volume across different goods.
Train cargo is represented as a dictionary where the key identifies the good and the value represents the number of carloads currently transported.
Example:
{
    "steel": 3,
    "grain": 2
}
A train carrying this cargo uses five cars.

### Reason
Different goods have very different physical properties, so using a universal unit such as tons or cubic meters would require additional modeling of weight, volume, wagon types, and capacities.
These details would add complexity without significantly improving the economic decisions that are central to the game.
Using carloads keeps transport capacity simple while still allowing meaningful decisions about which goods should be transported and where.
A dictionary is used instead of representing every individual car in a list because the game primarily needs aggregate information about how many carloads of each good are being transported.

### Alternatives considered
Measuring all goods by weight, such as tons.
Measuring goods by volume.
Giving different goods different wagon capacities.
Representing every train car individually in a list.
Creating separate wagon classes with different capacities.

### Consequences
Train capacity can be calculated directly from the number of cars.
One car always provides one cargo slot regardless of the transported good.
Different goods can still have different prices, production rates, consumption rates, and economic value per carload.
Wagon capacity upgrades are not currently planned. Improvements to train capacity should primarily come from locomotives capable of pulling more cars.
Physical differences between goods are intentionally abstracted away in favor of economic gameplay and simpler data analysis.


## Cargo ownership and transfers

### Decision
Trains and cities manage their own cargo-related state independently.
A train stores the goods it currently transports in its cargo dictionary.
A city stores locally available goods in its inventory dictionary.
Methods belonging to Train modify train cargo only, while methods belonging to City modify city inventory only.
Transfers between a city and a train will be coordinated by a higher-level game action or engine rather than by either entity directly.

### Reason
Train movement and cargo capacity are responsibilities of the train, while production, consumption, and local inventory belong to the city economy.
Keeping these responsibilities separate prevents Train and City from becoming tightly coupled and makes their behavior easier to test independently.
A higher-level transaction can later ensure that both sides of a cargo transfer are updated consistently.

### Consequences
Loading cargo from a city will eventually consist of two coordinated state changes:
goods are removed from the city's inventory;
the same number of carloads is added to the train's cargo.

Unloading performs the opposite transfer.
Failed transfers should leave both entities unchanged.
This structure also leaves room for future rules such as prices, payments, loading costs, availability checks, and transaction logging without placing those responsibilities inside Train or City.


## Goods as domain objects

### Decision
Goods are represented by dedicated Good objects rather than plain strings.
Inventories and train cargo use Good objects as identifiers for transported and stored goods.

### Reason
Strings are sufficient for early cargo prototypes, but goods will later need their own economic properties such as prices, production relationships, consumption behavior, and categories.
Representing goods as domain objects gives those properties a natural place to live and avoids spreading good-specific logic across unrelated parts of the codebase.

### Consequences
City inventories and train cargo will use Good objects as dictionary keys.
Cargo transfer logic will operate on goods as domain objects.
The initial Good model should remain minimal and only gain additional attributes when new economic mechanics require them.


## Base value of goods

### Decision
Each Good has a positive base_price representing the reference value of one carload of that good.
The base price is not the actual market price in a city. Local market prices will later be derived from the base price and city-specific economic conditions such as inventory, production, and consumption.

### Reason
Different goods need different baseline economic values before local supply and demand can influence their prices.
Separating a stable base price from a dynamic local market price keeps the Good model simple while allowing cities to price the same good differently.

### Consequences
The value of one carload can differ between goods.
A Good cannot be created with a zero or negative base price.
Future city pricing logic should treat base_price as a reference value rather than storing the changing market price directly on the Good object.


## Local price pressure and market memory

### Decision
Local prices are influenced by both the current supply situation and the recent history of supply availability in a city.
The current market state is determined using Days of Supply, calculated from available inventory and expected daily consumption.
Days of Supply is mapped to qualitative supply states such as shortage, normal supply, or surplus. Each state is also assigned a numeric score.
The city keeps a short history of these supply-state scores, initially planned as a rolling window of approximately seven days.
The average historical score is converted into a secondary price multiplier representing local business confidence and bargaining pressure.
Cities store only active production/consumption values, and the absence of an entry implies zero.

Economic interpretation
A city that experiences persistent shortages becomes less confident that future supply will be reliable. Local businesses are therefore willing to pay more to secure goods.
When supply consistently exceeds demand, buyers have stronger bargaining power and suppliers face greater pressure to accept lower prices.

Price model
The local price is conceptually calculated as:

local_price =
    base_price
    × current_supply_multiplier
    × historical_pressure_multiplier

The current supply multiplier is the primary driver of price.
The historical pressure multiplier should have a smaller effect and provide market memory rather than duplicate the full impact of the current supply state.

### Reason
Using only the current inventory situation would cause many cities with similar Days of Supply to produce identical prices.
Adding a short history of supply conditions gives markets distinct behavior while keeping price changes tied to understandable economic causes rather than arbitrary randomness.

### Consequences
Cities with identical current inventory conditions may still have different prices because their recent supply histories differ.
Persistent shortages can keep prices elevated even after conditions begin to improve.
Persistent surpluses can continue to suppress prices for a short period after supply tightens.
Random price noise is not required as the main source of variation. Future random events should preferably affect production, consumption, or supply conditions, allowing prices to respond through the economic model.


## Days of Supply as a derived value

### Decision
days_of_supply is not stored as persistent state in City.
Instead, it is calculated on demand from the city's current inventory and daily consumption: days_of_supply = inventory / daily_consumption
Only goods with active daily consumption are included in the result.
If a good has positive daily consumption but no inventory, its Days of Supply is 0.
If a good is not present in daily_consumption, it is not included in Days of Supply at all.

### Reason
Days of Supply is fully derived from two existing sources of truth:
City.inventory
City.daily_consumption

Storing it separately would duplicate state and create a synchronization risk whenever inventory or consumption changes.
The calculation is computationally inexpensive, so recalculating it when needed is preferable to maintaining an additional mutable value.

### Alternatives considered
Storing and updating a days_of_supply dictionary whenever inventory or consumption changes.
Caching calculated Days of Supply values.

### Consequences
Inventory and daily consumption remain the source of truth for local supply conditions.
Any system that needs Days of Supply should request the current calculated value rather than rely on previously stored data.
Changes caused by production, consumption, loading, or unloading goods are automatically reflected the next time Days of Supply is calculated.
Caching may be introduced later only if performance measurements show that recalculating the value is meaningfully expensive.


## Initial supply state thresholds

### Decision
A city's current supply condition for a good is classified using Days of Supply.
The initial thresholds are:
0–1 days    → extreme shortage
>1–3 days   → shortage
>3–6 days   → tight
>6–10 days  → normal
>10–15 days → surplus
>15 days    → heavy surplus

### Reason
The ranges are intentionally broad enough to avoid excessive switching between market states while still allowing meaningful changes as inventory conditions improve or deteriorate.

### Consequences
Supply states can later be mapped to price multipliers and historical market-pressure scores.
These thresholds are balance parameters, not fixed simulation truths. They should be adjusted later using observed game behavior and generated economic data.


## Supply state price multipliers

### Decision
Each supply state is mapped to an initial price multiplier:
extreme shortage → 1.50
shortage         → 1.30
tight            → 1.15
normal           → 1.00
surplus          → 0.85
heavy surplus    → 0.70

The multiplier is applied to the good's base_price and represents the immediate effect of local supply conditions on price.

### Reason
The values are distributed around 1.00, with normal supply preserving the base price.
Shortages increase prices, while surpluses reduce them. Extreme states have a noticeable effect without making prices excessively volatile.
The multipliers are intentionally simple and easy to interpret during early simulation runs.

### Consequences
The same good can have different local prices in different cities depending on current supply conditions.
The current supply multiplier will be the primary short-term driver of price.
A separate historical pressure multiplier may later adjust the result slightly to represent recent market conditions and business confidence.
These values are initial balance parameters and should be calibrated later using observed simulation behavior and generated economic data.


## Inactive markets and zero-consumption goods

### Decision
Supply pressure is evaluated differently depending on whether a good is locally consumed and whether inventory exists.

The rules are:
If daily consumption is greater than zero, the supply state is determined from Days of Supply.
If daily consumption is zero but inventory is greater than zero, the good is treated as a heavy surplus with supply score 6.
If daily consumption is zero and inventory is also zero, the local market for that good is considered inactive and no supply state is recorded.

A city may still have a market price for every good available in the game, even if the local market is currently inactive.

### Reason
A good that is present in a city but has no local demand should face strong downward price pressure because suppliers have little bargaining power.
However, a good that is neither supplied nor demanded should not be treated as a surplus. Recording artificial surplus history for an inactive market would create misleading market memory.

### Consequences
Supply history contains only economically meaningful observations.
A newly activated market does not inherit artificial historical pressure from periods when neither supply nor demand existed.
Goods with inventory but no local consumption can still develop meaningful market history through persistent oversupply.
The distinction between an inactive market and a heavy surplus remains important for future local pricing logic.


## Historical supply pressure multiplier

### Decision
The rolling average supply score is converted into a secondary historical price multiplier.
The initial anchor values are:
average score 1 → 1.10
average score 2 → 1.05
average score 3 → 1.00
average score 4 → 1.00
average score 5 → 0.95
average score 6 → 0.90

Values between these anchor points are calculated using linear interpolation.
Scores between 3 and 4 remain neutral at 1.00.

### Reason
Persistent shortages should increase buyers' willingness to pay because businesses have experienced unreliable supply.
Persistent surpluses should strengthen buyers' bargaining position and reduce prices.
The historical multiplier is intentionally weaker than the current supply multiplier. Its purpose is to provide market memory and gradual pressure rather than dominate the current supply situation.
Keeping scores between 3 and 4 neutral prevents mildly tight but still functional markets from creating unnecessary long-term price pressure.
Linear interpolation allows fractional rolling-average scores to influence prices smoothly instead of introducing another set of hard thresholds.

### Consequences
Historical market conditions can modify prices by approximately ±10%.
Markets recovering from persistent shortages or surpluses retain some price pressure until their recent history improves.
Fractional average supply scores produce proportionally adjusted multipliers.
The historical multiplier remains a balance parameter and may be recalibrated using simulation data.