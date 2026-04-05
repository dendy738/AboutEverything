"AboutEverything" post platform.

This isn't just a platform with posts collected in various categories. Each post has its own category, selectable at the publishing stage. There are approximately 50 different categories available. The platform also involves category filtering and a post searching. If no category is selected, the five most recently published posts will be displayed. Users can decide whether a post is useful or not instead of just liking it. Each post and comment is also checked for obscene language, and the system will not allow posting or commenting if it contains obscenities. Of course, each user has the ability to manage their posts (edit, delete) and comments (at this stage of development, only deletion is possible).


Custom data validation is used, including following:
- checking the first and last name for valid entered data;
- checking the username and password for prohibited characters;
- checking the phone number for valid entered data;


A custom decorator was also created to check user authorization and the current session.
The project was implemented with an emphasis on maximum security, so much of the business logic is related to interaction with the database.


Tech stack:
Django, PostgreSQL, asyncio, aiohttp, 
