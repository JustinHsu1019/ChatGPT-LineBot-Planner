### LLM ###
from langchain.chat_models import AzureChatOpenAI
from openai.error import RateLimitError
from langchain.schema import HumanMessage

### Logger ###
import logging.config
logging.config.fileConfig('logging_config_line.ini')
logger = logging.getLogger('CsLogger')

### Config ###
import configparser
config = configparser.ConfigParser()
config.read('CSconfig_line.ini')

### Call OpenAI LLM Model ###
def do_openai(messages, retry_count=0, max_retries=3):
    AzureOpenAIconfig = config['Open AI Default']['open_ai_section_name']
    openAI = AzureChatOpenAI(
        openai_api_base=config[AzureOpenAIconfig]['OPENAI_API_BASE'],
        openai_api_version=config[AzureOpenAIconfig]['OPENAI_API_VERSION'],
        deployment_name=config[AzureOpenAIconfig]['COMPLETIONS_MODEL'],
        openai_api_key=config[AzureOpenAIconfig]['OPENAI_AZURE_API_KEY'],
        openai_api_type=config[AzureOpenAIconfig]['OPENAI_API_TYPE'],
        temperature=0,
        max_tokens=4096
    )
    try:
        res = openAI(messages)
        return res.content
    except RateLimitError:
        if retry_count < max_retries:
            print("get rate limit, run again")
            logger.error("get rate limit", exc_info=True)
            return do_openai(messages, retry_count=retry_count+1)
        else:
            logger.error("系統忙碌，請稍後再試", exc_info=True)
            return "系統忙碌，請稍後再試"
    except Exception as e:
        print(f"get error: {e}")
        logger.error("系統發生錯誤，請通知系統管理員!", exc_info=True)
        return "系統發生錯誤，請通知系統管理員!"

### 整理對話紀錄格式 ###
def format_conversation(conversation_history):
    formatted_history = ""
    for item in conversation_history:
        formatted_history += item + "\n"
    return formatted_history

### 處理 重新規劃-階段二 ###
def handle_delete_response(response, user_id, conversation_history):
    if response.lower() == 'y':
        conversation_history[user_id]['messages'] = []
        conversation_history[user_id]['pending_deletion'] = False
        conversation_history[user_id]['messages'].append("教師: 你好")
        conversation_history[user_id]['messages'].append("課程規劃師: 我是一個友善且有助於指導的課程規劃師，擅長協助教師計劃課程。請告訴我您想要教授的主題和學生的年級是什麼")
        return "我是一個友善且有助於指導的課程規劃師，擅長協助教師計劃課程。請告訴我您想要教授的主題和學生的年級是什麼"
    else:
        conversation_history[user_id]['pending_deletion'] = False
        return "繼續規劃課程"

### 組裝 Prompt 以詢問 GPT ###
def chat(quest, conversation_history):
    system_prompt = f"""你是一個友善且有助於指導的課程規劃師，擅長協助[教師]計劃課程。
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
    response = do_openai([HumanMessage(content=system_prompt)])
    return response
