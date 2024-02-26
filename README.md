OVERVIEW
The Volatility Trading Case gives participants the opportunity to generate profits by implementing
options strategies to trade volatility. The underlying asset of the options is a non-dividend-paying
Exchange Traded Fund (ETF) called RTM that tracks a major stock index. Participants will be able
to trade shares of the ETF as well as 1-month and 2-month call/put options at 10 different strike
prices. Information including the ETF price, options prices, and news releases will be provided.
Participants are encouraged to use the provided information to identify mispricing opportunities
and construct options trading strategies accordingly.


DESCRIPTION
There will be 5 independent heats with two team members participating in each heat. Please note
that only two team members shall trade to represent the team for all heats. Each heat will be 10
minutes long and represent two months of calendar time.
Parameter Value
Number of trading heats 5
Trading time per heat 600 seconds (10 minutes)
Calendar time per heat 2 months (40 trading days)
News will be released during each heat. Order submissions using the RIT API will be enabled. Data
retrieval via Real-time Data (RTD) Links and the RIT API will also be enabled.


MARKET DYNAMICS
Participants will be able to trade RTM and 40 separate options contracts on RTM at the beginning
of the case. All options are European, so early exercise is not allowed. After the first period ends,
the one-month expiration options will no longer be tradable as they expire.

Starting Option Prices for One-month Expiration
Call Price Call Ticker Strike Price Put Ticker Put Price
$5.04 RTM1C45 45 RTM1P45 $0.04
$4.09 RTM1C46 46 RTM1P46 $0.09
$3.20 RTM1C47 47 RTM1P47 $0.20
$2.40 RTM1C48 48 RTM1P48 $0.40
$1.71 RTM1C49 49 RTM1P49 $0.71
$1.15 RTM1C50 50 RTM1P50 1.15
$0.73 RTM1C51 51 RTM1P51 $1.73
$0.44 RTM1C52 52 RTM1P52 $2.44
$0.24 RTM1C53 53 RTM1P53 $3.24
$0.13 RTM1C54 54 RTM1P54 $4.13

Starting Option Prices for Two-month Expiration
Call Price Call Ticker Strike Price Put Ticker Put Price
$5.18 RTM2C45 45 RTM2P45 $0.18
$4.31 RTM2C46 46 RTM2P46 $0.31
$3.51 RTM2C47 47 RTM2P47 $0.51
$2.79 RTM2C48 48 RTM2P48 $0.79
$2.16 RTM2C49 49 RTM2P49 $1.16
$1.63 RTM2C50 50 RTM2P50 1.63
$1.19 RTM2C51 51 RTM2P51 $2.19
$0.85 RTM2C52 52 RTM2P52 $2.85
$0.59 RTM2C53 53 RTM2P53 $3.59
$0.39 RTM2C54 54 RTM2P54 $4.39

All securities are priced by market-makers who will always quote a bid-ask spread of 2 cents (i.e.
$49.99*$50.01 for the RTM, or $4.08*$4.10 for the RTM1C46). The bids and asks are for very large
quantities (there are no liquidity constraints in this case).

The price of RTM follows a random-walk and the path is generated using the following process:
𝑃𝑅𝑇𝑀,𝑡 = 𝑃𝑅𝑇𝑀,𝑡−1 ∗ (1 + 𝑟𝑡
) 𝑤ℎ𝑒𝑟𝑒 𝑟𝑡~𝑁(0, 𝜎𝑡)

The price of the stock is based on the previous price multiplied by a return that is drawn from a
normal distribution with a mean of zero and standard deviation (volatility) of 𝜎𝑡 = 20% (on an
annualized basis).

The trading period is divided into 8 weeks, with 𝑡 = 1 … 75 being week one, 𝑡 = 76 … 150 being
week two, and so on. At the beginning of each week, the volatility value (𝜎𝑡) will shift and the new
value will be provided to participants. In addition, at the middle of each week (e.g. 𝑡 = 38) an
analyst estimate of next week’s volatility value will be announced.

Sample News Release Schedule
Time Week Release
1 Week 1 The realized volatility of RTM for this week will be 20%
1 Week 1 The delta limit for this sub-heat is 10,000
38 Week 1 The realized volatility of RTM for next week will be between 27-30%
76 Week 2 The realized volatility of RTM for this week will be 29%
… … …
526 Week 8 The realized volatility of RTM for this week will be 26%

The observed and tradable prices of the options will be based on a computerized market-maker
posting bids and offers for all options. The market maker will price the options using the Black
Scholes model. It is important to note that the case assumes a risk-free rate of 0%. The volatility
forecasts made by the market maker are uninformed and therefore will not always accurately
reflect the future volatility of RTM. Mispricing will occur, creating trading opportunities for market
participants. These opportunities could be between specific options with respect to other options,
specific options with respect to the underlying, or all options with respect to the underlying.
The focus of this case is on trading volatility without being exposed to price changes of the
underlying security, RTM. Participants are therefore required to manage their portfolio’s delta
exposure. Recognizing the transaction costs and impracticality of perfect delta hedging (i.e.
keeping the portfolio’s delta at zero at all times), the RITC scoring committee will allow the
portfolio’s delta to be different from zero but it is required to stay between – 𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡 and
𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡. Please note that 𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡 is an integer number greater than 1,000 that will be
announced at the beginning of the case via a news release in RIT. For example, the following news
could be released: “The delta limit for this heat is 5,000 and the penalty percentage is 0.5%”.
According to that news, any participant that has a portfolio delta greater than 5,000 will be
penalized at the penalty percentage of 0.5% according to the penalties explained below.
For every second that a participant exceeds the limit (+/−𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡), s/he will be charged a penalty
according to the following formula:
𝑃𝑒𝑛𝑎𝑙𝑡𝑦 𝑎𝑡 𝑠𝑒𝑐𝑜𝑛𝑑 𝑡 = {
(|𝛥𝑝,𝑡
| − 𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡) × 𝑝 𝑖𝑓 |𝛥𝑝,𝑡
| > 𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡
0 𝑖𝑓 |𝛥𝑝,𝑡
| ≤ 𝑑𝑒𝑙𝑡𝑎 𝑙𝑖𝑚𝑖𝑡
Where, 𝛥𝑝,𝑡
is the portfolio’s delta at time 𝑡 and 𝑝 is the penalty percentage.
Penalties will be applied at the end of each heat but will not be included in the P&L calculation in
RIT. Participants will be provided with an Excel tool1
, the “Penalties Computation Tool”, that will
allow them to calculate the penalties using their results from the practice server.
TRADING LIMITS AND TRANSACTIONS COSTS
Each participant will be subject to gross and net trading limits specific to the security type as
specified below. The gross trading limit reflects the sum of the absolute values of the long and
short positions across all securities in each security type; the net trading limit reflects the sum of
long and short positions such that short positions negate any long positions. Trading limits will be
enforced and participants will not be able to exceed them.
Security Type Gross Limit Net Limit
RTM ETF 50,000 Shares 50,000 Shares
RTM Options 2,500 Contracts 1,000 Contracts
The maximum trade size will be 10,000 shares for RTM and 100 contracts for RTM options,
restricting the volume of shares and contracts transacted per trade to 10,000 and 100,respectively.
Transaction fees will be set at $0.02 per share traded for RTM and $2.00 per contract traded for
RTM options. As with standard options markets, each contract represents 100 shares (purchasing
1 option contract for $0.35/option will actually cost $35 plus a $2 commission, and will settle based
on the exercise value of 100 shares).


POSITION CLOSE-OUT
Any outstanding position in RTM will be closed at the end of trading based on the last-traded price.
There are no liquidity constraints for the options nor RTM. All options will be cash-settled based
on the following upon expiration:
𝐶𝑎𝑙𝑙 𝑂𝑝𝑡𝑖𝑜𝑛 𝑃𝑎𝑦𝑜𝑢𝑡 = 𝑚𝑎𝑥{0, 𝑆 − 𝐾}
𝑃𝑢𝑡 𝑂𝑝𝑡𝑖𝑜𝑛 𝑃𝑎𝑦𝑜𝑢𝑡 = 𝑚𝑎𝑥{0,𝐾 − 𝑆}
Where,
𝑆 is the last price of RTM;
𝐾 is the strike price of the option.


KEY OBJECTIVES

Objective 1
Build a model to forecast the future volatility of the underlying ETF based on known information
and given forecast ranges. Participants should use this model with an options pricing model to
determine whether the market prices for options are overvalued or undervalued. They should then
trade the specific options accordingly.

Objective 2
Use Greeks to calculate the portfolio exposure and hedge the position to reduce the risk of the
portfolio while profiting from volatility differentials across options.

Objective 3
Seek arbitrage opportunities across different options and different expiries using calendar spreads. 

