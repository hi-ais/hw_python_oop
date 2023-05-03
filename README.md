# Calculator for money and calories
Money and calories calculator - tools to control expenses and income

## Conditions of the problem

Create two calculators: for counting money and calories. All you need is logic - a separate class for each of the calculators.

__Money calculator can:__

* Save new expense record with add_record() method
* Calculate how much money was spent today using the get_today_stats() method
* Determine how much more money you can spend today in rubles, dollars or euros - get_today_cash_remained(currency) method
* Calculate how much money was spent in the last 7 days - get_week_stats() method

__Calorie calculator can:__

* Save a new meal record - add_record() method
* Calculate how many calories have already been eaten today - get_today_stats() method
* Determine how many more calories you can / need to get today - get_calories_remained() method
* Calculate how many calories you got in the last 7 days - get_week_stats() method

__General functionality of calculators ***(Calculator class)***:__

* storage of records
* knowledge of the daily limit
* summation of records for specific dates
