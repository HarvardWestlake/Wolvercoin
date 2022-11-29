#Technical Specifications for Haiku SideQuest
> If you send Mr. Theiss a unique haiku, get 5 WolverCoin (one time use)

> Variables: 
- allHaikus: String of three different haikus spaced with 1 line between the three
- romanceLanguage: bool, True if written in romance, False else
- video: bool, True if filmed a video, False else
- videoLink: String of link to public video on internet (either google drive link or youtube)
- allSuccesses: DynArray[String,20]

> Functions: 
- submitHaiku(address, String: haikus, bool: romance, bool: isVid, String: link)
  - check if address has already succeded by going through allSuccesses, proceed if not in list
  - assigns allHaikus to haikus
  - assign romanceLanguage to romance
  - if isVid is True: set video to true and videoLink to link
  - else: set video to False
  
> Events: 
- Successful Haikus
  - Log: Whenever someone submits 3 haikus
  - Log: When someone succeeds (is checked) and completes side quest
