# 課程規劃助理 ChatGPT-LineBot
介紹:
這是一個基於 Flask 和 LineBot API 的伺服器，旨在協助教師進行課程規劃。
透過與 GPT 的交互，它提供了友善且有助於指導的課程建議。
此外，這是一個流程機器人，專為遵循特定流程而設計，以確保每一步都按照預期進行。

主要功能:
1. LineBot 對話：解析從 LineBot 發送的消息，並回覆適當的答案。
2. 對話紀錄管理：儲存和管理用戶的對話紀錄。系統會檢查對話紀錄的總字數，確保其不超過 5000，以避免 Tokens 過多導致報錯。
3. 重新規劃功能：用戶可以隨時選擇重新規劃課程，系統會詢問用戶是否確定此操作，並根據用戶的回覆進行相應的操作。
4. 與 OpenAI 交互：組裝提示並詢問 GPT，以獲得課程建議。

如何使用:
1. 啟動伺服器。
2. 透過 LineBot 發送消息，例如 "我想教授數學給高中生"。
3. 跟隨課程規劃助理的指引進行對話，以完成課程規劃。
4. 若想重新規劃課程，只需在 LineBot 中發送消息 "重新規劃"。系統會詢問您是否確定要重新開始，回覆 "Y" 表示確定，回覆 "N" 則繼續當前的規劃。

技術細節:
1. 使用 Flask 框架建立伺服器。
2. 利用 LineBot API 處理消息。
3. 使用 Azure OpenAI 的 GPT-35-turbo-16k 進行課程建議。
4. 使用日誌工具來記錄和追踪伺服器的活動。

待完善之項目:
1. 將對話紀錄儲存在資料庫中，而不是程式內暫時的字典。
2. 增加更多的錯誤處理和異常管理。
3. 優化與 GPT 的交互，以提供更精確的課程建議及更嚴謹的流程遵守。

參考資料:
1. https://openai.com/blog/teaching-with-ai
2. https://steam.oxxostudio.tw/category/python/example/line-bot-openai-1.html

Demo 畫面:

![下載](https://github.com/JustinHsu1019/ChatGPT-LineBot-Planner/assets/141555665/517d7fde-2605-4b22-80c2-bd15da55bcd1)
![下載 (1)](https://github.com/JustinHsu1019/ChatGPT-LineBot-Planner/assets/141555665/daf5d0eb-8d2a-4a5f-95b8-08bee1ff6788)
