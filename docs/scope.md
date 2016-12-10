# Project Description and Scope

Project Goal:

To develop a tool that can be utilized by a variety of user types to analyze, and project, the impact of injuries on MLB player performance.

What Made It Interesting:

Building a comprehensive understanding of the effect of injuries required pulling in data from a number of disparate sources to form a complete, central repository.  While more information on the data used can be found in the (datasources.md) file, we'll say here that they spanned from the text injury announcements that appear on MLB.com, to the detailed pitch metrics (spin, location, etc) from PitchF/X.  Because of this, the most challenging aspect of this project was building a pipeline that would pull, ingest, and store this diverse data on a regular basis into a series of databases that formed a cohesive central repository. Second to this was building out a set of functions that accessed multiple data types in parallel to derive user-facing outputs.

Current Scope:

InjuryF/X currently focusses on analyzing the effect of injuries on specific pitchers or batters.  The tool allows users to select a specific instance of an injury that a player endured, and see how the injury affected their performance through heat maps, time series graphs, and easy to consume aggregate stats.

For example, a user could select Steven Strasburg's Tommy John surgery in 2010, and be able to see side-by-side heat maps of his pitch placement before and after the injury.  Similarly, a user could select Yoenis Cespedes' hamstring injury, and see side-by-side charts of pitches he swung at before and after the injury.

Future Development:

There are a number of areas where we would like to progress the tool, namely integrating more data (i.e. historical and more metrics), and building out the site's functions.

* OLDER DATA: Currently our data only goes back as far as 2009.  We'd like to incorporate transaction data and play-by-play data prior to this. The challenge here is that the older data have difficult formats to parse.  Further, PitchF/X data, one of our richest and most heavily relied upon sources, only began in 2008.

* BETER LEVERAGE PITCHF/X: Right now, we mostly use the pitch coordinate information from PitchF/X. In the future we'd like to use statistics like spine rate, ball movement, pitcher arm slot, and others in the context of injury for both pitchers and batters.

* FURTHER ANALYSIS: We'd like to provide users with a broader and more robust selection of statistical analysis. At the top of the list would be comparing changes in performance across groups of players who all experienced the same injury, paired with the statistical significance of differences.

*  IMPROVE UI: There are a variety of areas where we could remove barriers related to the interface that decrease the usability of the site.  This would included improved search functions that don't require as much manual filter and user text input, as well as having dynamic player pages.




[Return to Documentation Index](index.md)
