#Technical Specifications for Haiku SideQuest
> If you send Mr. Theiss a unique haiku, get 5 WolverCoin (one time use)

> Variables: 
- allHaikus: String of three different haikus spaced with 1 line between the three
- romanceLanguage: bool, True if written in romance, False else
- video: bool, True if filmed a video, False else
- videoLink: String of link to public video on internet (either google drive link or youtube)

> Functions: 
- submitHaiku(String: haikus, bool: romance, bool: isVid, String: link)
  - assigns allHaikus to haikus
  - assign romanceLanguage to romance
  - if isVid is True: set video to true and videoLink to link
  - else: set video to False
  
- 
