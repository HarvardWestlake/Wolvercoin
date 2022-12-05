IN PROGRESS
Side Quests Pseudo
Workers: Simon W + Matthew Ko


**Beat Mr. Theiss at Super Hexagon**

Variables: 
- TheissHighScore: Mr Theiss' High Score as an int
- NewScore: Your High Score as an int
- UserAddress: YourAddress as an adress

Methods:
CompareHighScores
- If TheissHighScore<NewScore, send user 2.14x their current WC balance
- Else, nothing
In real life, you must show Mr. Theiss your score, and he will have to print an NFT of his most recent instagram post


**Dance for Mr. Theiss** 
NOT POSSIBLE ON THE BLOCKCHAIN
Solution: Mr Theiss independently pays people for doing a dance
Mr Theiss would have to check whether or not he has already sent you 5 WC for a dance, can verify because the transaction would exist on the blockchain

RULES FOR THE DANCE:
- If you impress Mr. Theiss with a little dance, you get 5 WolverCoin. Can only be used once
- 3 extra Wolvercoin if it's to a Taylor Swift song
- 3 extra Wolvercoin per person if you get over 3 people in your dance
- 1 extra Wolvercoin if you can remain stonefaced
- 5 extra Wolvercoin if you are in costume

**Technical Specifications for Haiku SideQuest**
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

Alternative Method by Jake
Variables:
- haiku: boolean (three lines, 5/7/5 syllables, rhyme for all three lines or end with a couplet)
- 3haiku3topic: boolean (checks if there are 3 haikus and they are based on; The feeling of leaving campus at school at the end of the day, Making more money than your brother, Hanging the phone on your parents)
- plCheck: boolean (checks if Haiku is plaigarized)
- romanceLanguage: boolean (if written in a romance language)
- recorded: boolean (if they recorded and sent themselves doing it to whole class)
- firstTime: boolean (checks if the user has done this before)
Method:
    if haiku=true and plCheck=true and firstTime=true
        +5 wolvercoin to user's wallet 
        if 3haiku3topic=true 
            +5 more Wolvercoin to user's wallet 
            if recorded=true
                +15 wolercoin to user's wallet 
        if romanceLanguage=true
            +3 wolvercoin to user's wallet