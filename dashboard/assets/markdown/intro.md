This dashboard shows how punctual flights are at the ten **Swedavia airports** in Sweden
(Stockholm Arlanda, Göteborg Landvetter, Malmö, Bromma and more).

The data comes from the **Swedavia FlightInfo API** and covers arrivals and departures for the
**last three days**. It is loaded into Snowflake every day, modelled with dbt and shown here.

**How we measure punctuality**

- A flight is **delayed** when it lands or departs **more than 15 minutes** after the scheduled time.
- A flight is **on time** when it lands or departs at most 15 minutes late (early flights count as on time).
- **Share delayed** = delayed flights / flights that have landed or departed.
  Cancelled flights and flights that haven't happened yet are not counted, because their punctuality isn't known.

**Pages**

- **Dashboard**: filter by direction, airport, airline and date, and see the KPIs, punctuality per airline and the most delayed flights.
- **Charts**: delayed flights per date, airport, airline and hour of the day, using the same filters.
