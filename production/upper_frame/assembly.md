# Upper-frame nuts and unresolved retaining spring

Three existing M4 nut occurrences live under `frame/upper_frame`.
They and the four frame nuts contribute once to the whole-profile seven-nut
line. Marcus Wu's [hardware BOM](https://docs.google.com/spreadsheets/d/16EJePozXW-uC6UFISzyT2eMk7c8wh6v-EP5L1U8fzfM/edit#gid=1182246287)
links those seven nuts to [Bolt Depot product 4784](https://www.boltdepot.com/Product-Details.aspx?product=4784),
whose indexed dimensional specification supports DIN 934 M4x0.7.
No manufacturer, grade or purchasable offer is inferred.

The retaining spring is deliberately unresolved. The author's printed
BOM lists one tens bell spring, while `simulation/retaining_spring.py`
represents that physical body by five mixed rigid/flexible patches:
mount, two arms and two hooks. Those five candidates remain unassigned;
this profile neither treats them as five author parts nor automatically
fuses them into a fabricated print. Evidence inspected 2026-10-04.
