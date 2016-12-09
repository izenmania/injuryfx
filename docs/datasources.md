# Datasources

### InjuryFX
InjuryFX data can be found here: JOE ADD AN APPROPRIATE URL  
It contains injury data including who was injured, when they were injured, what disabled list they were put on, when they returned from the disabled list, and the location of the injury. We've ingested this data from 2009 to 2016.

### MLB Gameday
Gameday data can be found here: http://gd2.mlb.com/components/game/mlb/  
It contains data about games, players, individual atbats, and individual pitches. There are many years of data but it's not all consistent as you go back in time. Because injury science improves over time and older gameday data doesn't contain the in depth pitch data we need to perform our analysis and (InjuryFX data), we are less interested in the older data from gameday. Therefore, we have only imported data since 2009. 

### Retrosheet
Retrosheet data can be found here: http://www.retrosheet.org/game.htm  
Retrosheet has some similar data to but is not as complete as Gameday. However it goes further back in time so we imported it as well so that we can do our analysis on older data.

[Return to Documentation Index](index.md)
