# 🤖 akoo_bot
A Discord bot that uses Gemini API to generate responses

## 📌 Features:
- Welcomes new members who join the server.
- Generate AI responses
- Summarize long paragraphs
- Plays music
- Schedule reminders in sec, mins, hours

## 🛠️ TODO:
- [x] Link the Discord API
- [x] Welcome new members to the server
- [x] Enable bot to use slash commands 
- [x] Link the Gemini API to the Discord API to generate responses in the server
- [x] Add features like music and reminders
- [ ] Be able to create polls

## 🎯 CHALLENGES FACED:
- Setting reminders in sec, mins, hours
- Handling AI responses larger than 2000 characters and sending it to the discord API
- Figuring out discord API's timeout and fixing that 
- Playing music using ffmpeg was really hard

## 🚀 IMPROVEMENTS THAT CAN BE MADE:
- [ ] Store the reminders in a database so that they are not delayed in case the bot goes offline or restarts
- [ ] Set reminders according date and time
- [ ] Can make use of embed method to generate embeded messages
- [ ] Better Error Handling
- [ ] Better handling of requests generated to the Gemini API in order to prevent exceeding rate limit
- [ ] Queue and dequeue system for the music
- [ ] Be able to pause and resume music using a good UI