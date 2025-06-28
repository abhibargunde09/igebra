try:
    from melo.api import TTS
    MELO_AVAILABLE = True
except ImportError:
    TTS = None
    MELO_AVAILABLE = False
    import warnings
    warnings.warn("melo.api.TTS is not available. Voice features will be disabled.")

from langchain_openai import ChatOpenAI
from app.model import Topic
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import json
import logging
import os

llm = None
agent = None
VOICE_ENGINE = None
device = 'cpu'
config_data = None

def init_engine():
    global llm
    global VOICE_ENGINE
    if llm is None:
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)
    if MELO_AVAILABLE and VOICE_ENGINE is None:
        VOICE_ENGINE = TTS(language='EN', device=device)

def config_agent():
    global agent
    global config_data
    config_path = '/app/app/config.json'
    template_path = '/app/app/agent_template.json'
    if not os.path.exists(config_path) or not os.path.exists(template_path):
        raise FileNotFoundError("Config or agent template file not found.")
    config_data = json.load(open(config_path, 'r'))
    template_data = json.load(open(template_path, 'r'))
    agent = list(filter(lambda x: x["name"] == config_data.get("agentName"), template_data))
    if not agent:
        raise ValueError("Agent with the specified name not found in template.")

def create_content_suggestions(query: str):
    if agent is None or llm is None:
        raise RuntimeError("Agent or LLM not initialized. Call init_engine() and config_agent() first.")
    parser = JsonOutputParser(pydantic_object=Topic)
    template = f"""
        Name: {agent[0]['name']}\n
        Role: {agent[0]['role']}\n
        Personality: {agent[0]['personality']}\n
        Task: List 5 learning topics based on query.\n{{format_instructions}}\n {{query}}\n
    """
    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    print(prompt)
    try:
        chain = prompt | llm | parser
        result = chain.invoke({"query": query})
        return result
    except Exception as e:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred while creating content suggestions: {e}")
        raise

def create_podcast_script(input: str):
    if agent is None or llm is None:
        raise RuntimeError("Agent or LLM not initialized. Call init_engine() and config_agent() first.")
    try:
        template = f"""
            Name: {agent[0]['name']}\n
            Role: {agent[0]['role']}\n
            Personality: {agent[0]['personality']}\n
            Areas: {agent[0]['areas']}\n
            Style: {agent[0]['style']}\n

            Question: {input}\n
            Objective: Describe a question like a human talk max ~500 words. Don't need to introduction or introduce youself.
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["input"],
        )
        print(prompt)
        chain = prompt | llm
        result = chain.invoke({"input": input})
        return result.content
    except Exception as e:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred: {e}")
        raise

def text_to_voice(text: str):
    if not MELO_AVAILABLE or VOICE_ENGINE is None:
        raise RuntimeError("melo.api.TTS is not available. Voice features are disabled.")
    if config_data is None:
        raise RuntimeError("Config data not loaded. Call config_agent() first.")
    try:
        file_name = config_data.get("podcastName", "output")
        speaker = config_data.get("voiceName")
        file_path = f"/tmp/voice/{file_name}.wav"
        speed = config_data.get("podcastSpeed", 1.0)
        speaker_ids = VOICE_ENGINE.hps.data.spk2id
        if speaker not in speaker_ids:
            raise ValueError(f"Speaker '{speaker}' not found in speaker IDs.")
        VOICE_ENGINE.tts_to_file(text, speaker_ids[speaker], file_path, speed=speed)
        print("Voice Generated")
        return file_path
    except Exception as e:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred: {e}")
        raise

def create_article(input: str):
    if agent is None or llm is None:
        raise RuntimeError("Agent or LLM not initialized. Call init_engine() and config_agent() first.")
    try:
        template = f"""
            Name: {agent[0]['name']}\n
            Role: {agent[0]['role']}\n
            Personality: {agent[0]['personality']}\n
            Areas: {agent[0]['areas']}\n
            Style: {agent[0]['style']}\n

            Objective: Create an article based on the following topic.\n {input}\n
            Don't need to introduce youself only create an article.\n
            Output should be in markdown format.
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["input"],
        )
        print(prompt)
        chain = prompt | llm
        result = chain.invoke({"input": input})
        return result.content
    except Exception as e:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"An error occurred: {e}")
        raise