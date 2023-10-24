# Course Planning Assistant ChatGPT-LineBot
## Introduction:
This is a server based on Flask and the LineBot API, aimed at assisting educators in course planning. Through interactions with GPT, it offers friendly and guiding course suggestions. Moreover, it's a workflow bot, specifically designed to follow a particular process, ensuring each step is carried out as anticipated.

## Key Features:
1. LineBot Conversation: Parse messages sent from LineBot and reply with appropriate responses.
2. Conversation Record Management: Store and manage user conversation logs. The system checks the total word count of the conversation logs, ensuring it doesn't exceed 5000 to prevent excessive tokens causing errors.
3. Re-planning Feature: Users can choose to re-plan the course at any time. The system will ask the user to confirm this action and will proceed based on the user's response.
4. Interaction with OpenAI: Assemble prompts and query GPT for course suggestions.

## How to Use:
1. Start the server.
2. Send a message through LineBot, e.g., "I want to teach math to high school students."
3. Follow the guidance of the Course Planning Assistant in the conversation to complete the course planning.
4. If you wish to re-plan the course, simply send the message "re-plan" in LineBot. The system will ask if you're sure about restarting; reply with "Y" to confirm, or "N" to continue the current planning.

## Technical Details:
1. Server established using the Flask framework.
2. Message handling through the LineBot API.
3. Course suggestions using Azure OpenAI's GPT-35-turbo-16k.
4. Logging tools used to record and track server activities.

## Prompt:
```python
prompt = f"""你是一個友善且有助於指導的課程規劃師，擅長協助[教師]計劃課程。
請依據下列步驟來推進對話，請確實確定前面步驟已經完成了，再進入下一步驟。
步驟 1. 自我介紹，並問[教師]他們想要教授的主題和學生的年級是什麼。等待[教師]回答。在[教師]回答之前不要繼續。
步驟 2. 問[教師]學生是否已經知道這個主題，或者這是一個全新的主題。如果學生已經知道這個主題，請[教師]簡單地解釋他們認為學生對它了解多少。等待[教師]的回答。不要替[教師]回答。
步驟 3. 然後問[教師]他們的學習目標是什麼；也就是說，他們希望學生在課後能理解或做什麼。等待回答。
步驟 4. 根據所有這些資訊，創建一個定制的課程計劃，其中包括各種教學技巧和模式，包括直接指導、檢查理解度（包括從大量學生中收集理解的證據）、討論、引人入勝的課堂活動和作業。解釋您特別選擇每一個的原因。
步驟 5. 問[教師]他們是否想要改變什麼，或者他們是否知道學生可能會遇到的關於這個主題的任何誤解。等待回答。
步驟 6. 如果[教師]想要改變任何東西，或者如果他們列出任何誤解，與[教師]合作更改課程並解決誤解。
步驟 7. 然後問[教師]是否需要任何建議，以確保達到學習目標。等待回答。
步驟 8. 如果[教師]對課程感到滿意，告訴[教師]他們可以返回此提示，再次與你聯繫，並讓你知道課程進行得如何。

過去的對話紀錄請參考 [Previous conversation history]

[Previous conversation history]:{format_conversation(conversation_history)}

[教師]: {quest}

輸出請直接輸出答案就好，不需要有其他的標籤
"""
```

## Areas for Improvement:
1. Store conversation logs in a database instead of a temporary dictionary within the program.
2. Incorporate more error handling and exception management.
3. Optimize interactions with GPT to provide more accurate course suggestions and stricter adherence to the process.

## References:
1. https://openai.com/blog/teaching-with-ai
2. https://steam.oxxostudio.tw/category/python/example/line-bot-openai-1.html

## Demo Screenshots:

![Download](https://github.com/JustinHsu1019/ChatGPT-LineBot-Planner/assets/141555665/517d7fde-2605-4b22-80c2-bd15da55bcd1)
![Download (1)](https://github.com/JustinHsu1019/ChatGPT-LineBot-Planner/assets/141555665/daf5d0eb-8d2a-4a5f-95b8-08bee1ff6788)
