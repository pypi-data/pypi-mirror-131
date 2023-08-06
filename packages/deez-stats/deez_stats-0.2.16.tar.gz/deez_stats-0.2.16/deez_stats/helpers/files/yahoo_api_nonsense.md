# Yahoo API
<https://developer.yahoo.com/fantasysports/guide/>

### spilchen: yahoo fantasy api
<https://pypi.org/project/yahoo-fantasy-api/>

<https://yahoo-fantasy-node-docs.vercel.app/>

### Base URI
<https://fantasysports.yahooapis.com/fantasy/v2/>

### Game Resource:
This is pretty high-level and only useful for game_id and game_weeks
- metadata (game_key)
- game_weeks (game_key)
- stat_categories (game_key)
- position_types (game_key)
- roster_positions (game_key)

### League Resource:
- metadata (league_key)
- settings (league_key)
- standings (league_key)
- scoreboard (league_key, week*)
- teams (league_key)
- players (league_key, player_key, week*)
- draftresults (league_key)
- transactions (league_key)

### Player Resource:
- metadata (player_key)
- stats (player_key, week*)
- ownership (player_key, league_key)
- percent_owned (player_key)
- draft_analysis (player_key)

### Roster Resource:
- players (team_key, week/date*)

### Team Resource
- metadata (team_key)
- stats (team_key, week/date*)
- standings (team_key)
- roster (team_key)
- draftresults (team_key)
- matchups (team_key, week*)

### Transaction Resource


TEAM Resource:
https://fantasysports.yahooapis.com/fantasy/v2/team/
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1/matchups;weeks=1,5
https://fantasysports.yahooapis.com/fantasy/v2/team/223.l.431.t.1/stats;type=season
https://fantasysports.yahooapis.com/fantasy/v2/team/253.l.102614.t.10/stats;type=date;date=2011-07-06


ROSTER Resource:
https://fantasysports.yahooapis.com/fantasy/v2/team//roster
https://fantasysports.yahooapis.com/fantasy/v2/team//roster;week=10
https://fantasysports.yahooapis.com/fantasy/v2/team/253.l.102614.t.10/roster/players

https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/players;player_keys=223.p.5479
https://fantasysports.yahooapis.com/fantasy/v2/league/223.l.431/players;player_keys=223.p.5479/stats

https://fantasysports.yahooapis.com/fantasy/v2/transaction/
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.tr.2 - Completed add/drop transaction
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.w.c.2_6390 - Waiver claim transaction
https://fantasysports.yahooapis.com/fantasy/v2/transaction/257.l.193.pt.1 - Pending trade transaction

type	add,drop,commish,trade	/transactions;type=add
types	Any valid types	/transactions;types=add,trade
team_key	A team_key within the league	/transactions;team_key=257.l.193.t.1
type with team_key	waiver,pending_trade	You can only use these options when also providing the team_key, ie /transactions;team_key=257.l.193.t.1;type=waiver
count	Any integer greater than 0	/transactions;count=5



```https://fantasysports.yahooapis.com/fantasy/v2/league/{}/scoreboard;week={}'.format(league_id, week))```
* raw_matchups_query.json
