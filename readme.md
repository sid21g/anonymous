	
# Anonymous Source Tracker

This is the code for the [Anonymous Source Tracker](http://schaver.com/anonymous).

The Anonymous Source Tracker leverages [Google Custom Search](https://cse.google.com/) to find examples of anonymous sources used by major media organizations in the United States.

These were the top 50 online news entities in 2015 [as identified by the Pew Research Center](http://www.journalism.org/media-indicators/digital-top-50-online-news-entities-2015/).

Once a day the tracker searches the websites of these entities for [phrases commonly used to identify anonymous sources](https://github.com/markschaver/anonymous/blob/master/anonymous-phrases.txt).

Examples are stored in a SQLite database that is [available for download](https://github.com/markschaver/anonymous/blob/master/anon.db). Only the 250 most recent examples for each entity are viewable on the website, but all examples since this iteration of the tracker are included in the database. You can also download the data as [a csv file](https://github.com/markschaver/anonymous/blob/master/anon.csv)

If you have questions or suggestions, you can [email me](mailto:mark.schaver@gmail.com).
