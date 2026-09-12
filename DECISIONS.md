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


## Company presidency and tied shareholdings

### Decision
The president of a floated company is determined by share ownership.
If one shareholder owns more shares than every other shareholder, that player becomes the president.
If multiple shareholders are tied for the largest number of shares and the current president is one of them, the current president keeps control of the company. Therefore, another shareholder must own strictly more shares than the current president to take control.
If the company does not yet have a president and multiple shareholders are tied for the largest number of shares, the shareholder who became a shareholder of the company first becomes the president.

### Reason
A tie should not automatically remove an existing president from control. Requiring another shareholder to exceed the president's position makes company takeovers deliberate rather than accidental.
When a newly floated company has no president and its largest shareholders are tied, using the earliest shareholder provides a deterministic way to establish control without requiring an additional arbitrary decision.

### Alternatives considered
Leaving the company without a president until one shareholder obtains a larger position.
Giving the presidency to the shareholder who first reached the current highest number of shares.

### Consequences
The current president remains protected during a tie but can lose control as soon as another shareholder owns more shares.
The order in which players first become shareholders can matter when a company receives its first president.
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