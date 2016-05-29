
# Anonymous Source Tracker

Code for the [Anonymous Source Tracker](http://schaver.com/anonymous).

The Anonymous Source Tracker leverages [Google Custom Search](https://cse.google.com/) to find examples of anonymous sources used by major media organizations in the United States.

Once a day it searches the websites of those organizations for [phrases commonly used to identify anonymous sources](https://github.com/markschaver/anonymous/blob/master/anonymous-phrases.txt).

Examples are stored in a SQLite database that is [available for download](https://github.com/markschaver/anonymous/blob/master/anon.db).
Only the 500 most recent examples are viewable on the website, but all examples since this iteration of the tracker are included in the database.

If you have questions or suggestions, you can [email me](mailto:mark.schaver@gmail.com).
