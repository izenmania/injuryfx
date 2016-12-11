# Datasources

### InjuryFX
InjuryFX data can be found here: JOE ADD AN APPROPRIATE URL  
It contains injury data including who was injured, when they were injured, what disabled list they were put on, when they returned from the disabled list, and the location of the injury. We've ingested this data from 2009 to 2016. For these years the data is provided in JSON. Prior to those years the format is HTML and requires more laborious scraping. Because the pitch data quality drops off the further back in time you go and because injury science has improved over the years this more recent data was of most interest to us.

### MLB Gameday
Gameday data can be found here: http://gd2.mlb.com/components/game/mlb/  
It contains data about games, players, individual atbats, and individual pitches. The pitching data come from the PitchF/X tracking system, comprised of two cameras mounted in every MLB stadium.  The data include release point, movement, velocity, spin, and location of every pitch.  The data at gd2.mlb.com includes the traditional baseball metrics as well, all in raw text files, indexed by individual games, and updated as the season progresses.  We use the open source library py-gameday (https://github.com/wellsoliver/py-gameday) to do the parsing of the raw files.  There are many years of data but it's less consistent further back in time. Because injury science improves over time and older gameday data doesn't contain the in depth pitch data we need to perform our analysis and (InjuryFX data), we are less interested in the older data from gameday. Therefore, we have only imported data since 2009. 

### Retrosheet
Retrosheet data can be found here: http://www.retrosheet.org/game.htm  
Retrosheet has some similar data to but is not as complete as Gameday, and it does not contain pitching data.  However it goes further back in time so we imported it as well so that we can do our analysis on older data.  The data is availbale in text files on the site, and we use the open source package py-retrosheet (https://github.com/wellsoliver/py-retrosheet) to parse and load the data into the MySQL database.

[Return to Documentation Index](index.md)
