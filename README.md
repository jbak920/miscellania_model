# miscellania_model
A model of the Kingdom of Miscellania in Old School Runescape. It exists to answer the following questions:

"If I infuse my Miscellania kingdom with some cash, max out my approval, and then walk away until my coffers are empty, how
much profits will I have made once coffers are empty? And what's the optimal value for starting cash, for maximizing profits?"

# Usage
In `__main__`, edit the `assumed_base_revenue` to be whatever value you think is correct. The default value is 125k. This
value represents the ideal *revenue* generated in 1 day with a sufficiently large coffer and maximum approval rating. You'll
need to research the revenue generated for your chosen worker distribution, then enter it here.

Then simply run `python miscellania_model.py` and a plot will be generated, showing the optimal starting cash for your 
assumed_base_revenue.

# Example output

![Example output for default value of assumed_base_revenue](/images/example_output.png)