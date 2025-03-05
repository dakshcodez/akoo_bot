# 🤖 akoo_bot
A Discord bot that uses Gemini API to generate responses

## 📌 Features:
- Welcomes new members who join the server.
- Generate AI responses
- Schedule reminders in sec, mins, hours
- Can create polls
- Plays music

## 🛠️ TODO:
- [x] Link the Discord API
- [x] Welcome new members to the server
- [x] Enable bot to use slash commands 
- [ ] Be able to create polls
- [x] Link the Gemini API to the Discord API to generate responses in the server
- [ ] Add features like music and reminders

## 🎯 CHALLENGES FACED:
- Setting reminders in sec, mins, hours
- Handling AI responses larger than 2000 characters and sending it to the discord API
- Figuring out discord API's timeout and fixing that 

## 🚀 IMPROVEMENTS THAT CAN BE MADE:
- [ ] Store the reminders in a database so that they are not delayed in case the bot goes offline or restarts
- [ ] Set reminders according date and time
- [ ] Can make use of embed method to generate embeded messages
- [ ] Better Error Handling
- [ ] Better handling of requests generated to the Gemini API in order to prevent exceeding rate limit