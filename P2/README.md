# Project 2: A Database Schema for Complex Real-World Data
﻿Process:
The initial discussion we had was about how we wanted the user interface of our activity groups database to work. The chief difficulty in this project was balancing our aims of creating a useful interface design and having a model that is not overcomplicated by too many disparate entity sets, which would result in a clunky and developer-unfriendly back-end that would make edits to the existing structure time-inefficient and prone to error. The discussion below primarily reflects the roadblocks we encountered as a result of our dilemma, along with the solutions we settled on. Entity set names are italicized and bolded, while attributes are only italicized. Relationship sets are bolded and underlined.

We had some issues with the ER diagram, where we discussed whether or not to include a separate Membership entity set. It would be difficult to include membership information pertaining to a specific activity group in the User entity set, since users may belong to more than one activity group. Therefore, we settled on having a separate Membership entity set. However, after considering the nature of entity sets vs. relationship sets, we realized that membership is ultimately a relation between users and activity groups, rather than an entity of its own. So we created a Member relationship set.

Another issue we encountered was whether it would be necessary to have a CollegeID as the primary key for the College entity set. We settled on just identifying colleges by Name instead of a separate CollegeID, since we take it for granted that no two colleges will have the exact same name. We then realized that having a separate entity set for colleges was unnecessary, as College could simply be an attribute in the User entity set.

We also discussed whether activity groups could belong to more than one category, which would necessitate another entity set for categories, but we settled on simplifying the model to include only one category per activity group, which would allow us to make CategoryID an attribute of Activity Group. 

We discussed whether to have a separate UserInterest entity set, because users may have many interests, which would make it impossible to have Interest as an attribute of User. While we considered having a separate entity set UserInterest that would express the interests of the users, which would be linked to Category, we ultimately decided to express Interests as a relationship set, which would join User to Category.

## Functional Dependencies:
### For User:
- ID <—> Email
- ID —> Name 
- ID —> Affiliation 
- ID —> College
- Email —> Name 
- Email —> Affiliation 
- Email —> College

### For ActivityGroup:
- ID <—> Website
- ID —> Name
- ID —> Description
- ID —> Email
- ID —> Address
- ID —> CategoryID
- ID —> AffiliatedWithCollege
- ID —> College
- ID —> RequiresDues
- College —> AffiliatedWithCollege
- Website —> Name
- Website —> Description
- Website —> Email
- Website —> Address
- Website —> CategoryID
- Website —> AffiliatedWithCollege
- Website —> College
- Website —> RequiresDues
- Email —> ContactName

### For Event:
- EventID —> GroupID
- EventID —> Name
- EventID —> Location
- EventID —> Description
- EventID —> Date
- EventID —> StartTime
- EventID —> EndTime
- EventID —> Frequency

### For Category:
- ID —> Name
- ID —> Description

## Team member Contributions:
- Jacob took notes for the purpose of this narrative, mapped the functional dependencies of the ER model, and worked to develop the database schema.   

- Robbie helped map relationships between entity sets in the ER diagram. Particularly with constraints on cardinality. He refined existing entities and defined new attributes. He also helped to convert the diagram into a schema notation as outlined by Silberschatz. Robbie moved the narrative to the README four days late when he realize this was never done.

- Grant created the ER diagram, which others contributed to as well. He helped define many tables and relationship sets. 

- Max contributed to the ER diagram, helping to define attributes and how the data connects between tables. I also created the schema.sql file, which others contributed to as well.

- Charlie assisted in the creation of the ER diagram in addition to polishing parts of the schema.sql file. Also, he helped write some of the README/narrative.
