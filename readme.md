
# Anonymous Source Tracker

Python rewrite of the Anonymous Source Tracker.

## How it will work

The tracker will leverage RSS feeds from Google News alerts to track anonymous sources used by major news sources in the United States.

Unlike the original tracker, it will not attempt to track sources from all news sites.

The following news sources will be tracked (more may be added later):

* The New York Times
* The Washington Post
* The Associated Press
* Politico

The previous tracker leveraged Google Reader feeds, which have been deprecated. This version will leverage Google News alerts.

You can limit your search to specific news outlets on Google News by using the "source:" search operator.

For example, to find a mention of the phrase "anonymous sources" in The New York Times, your news query would be:

    "anonymous sources" source:new_york_times

[Here's what that looks like on Google News](https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q=%22anonymous+sources%22+source%3Anew_york_times&oq=%22anonymous+sources%22+source%3Anew_york_times).

These search results can then be turned into RSS feed alerts by clicking the "Create alert" button at the bottom of the page.

