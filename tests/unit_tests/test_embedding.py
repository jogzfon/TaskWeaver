import os

import pytest
from injector import Injector

from taskweaver.config.config_mgt import AppConfigSource
from taskweaver.llm import QWenService, ZhipuAIService
from taskweaver.llm.ollama import OllamaService
from taskweaver.llm.openai import OpenAIService
from taskweaver.llm.sentence_transformer import SentenceTransformerService
from taskweaver.llm.google_genai import GoogleGenAIService

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_sentence_transformer_embedding():
    app_injector = Injector([])
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "sentence_transformer",
            "llm.embedding_model": "all-mpnet-base-v2",
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    sentence_transformer_service = app_injector.create_object(
        SentenceTransformerService,
    )

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embedding1 = sentence_transformer_service.get_embeddings(text_list)

    assert len(embedding1) == 2
    assert len(embedding1[0]) == 768
    assert len(embedding1[1]) == 768


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_openai_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "openai",
            "llm.embedding_model": "text-embedding-ada-002",
            "llm.api_key": "",
            # need to configure llm.api_key in the config to run this test
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    openai_service = app_injector.create_object(OpenAIService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embedding1 = openai_service.get_embeddings(text_list)

    assert len(embedding1) == 2
    assert len(embedding1[0]) == 1536
    assert len(embedding1[1]) == 1536


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_ollama_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "ollama",
            "llm.embedding_model": "llama2",
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    ollama_service = app_injector.create_object(OllamaService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embedding1 = ollama_service.get_embeddings(text_list)

    assert len(embedding1) == 2
    assert len(embedding1[0]) == 4096
    assert len(embedding1[1]) == 4096


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_qwen_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "qwen",
            "llm.embedding_model": "text-embedding-v1",
            "llm.api_key": "",
            # need to configure llm.api_key in the config to run this test
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    qwen_service = app_injector.create_object(QWenService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embeddings = qwen_service.get_embeddings(text_list)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1536
    assert len(embeddings[1]) == 1536


@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_zhipuai_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "zhipuai",
            "llm.embedding_model": "embedding-2",
            "llm.api_key": "",
            # need to configure llm.api_key in the config to run this test
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    zhipuai_service = app_injector.create_object(ZhipuAIService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embedding1 = zhipuai_service.get_embeddings(text_list)

    assert len(embedding1) == 2
    assert len(embedding1[0]) == 1024
    assert len(embedding1[1]) == 1024

@pytest.mark.skipif(True, reason="Test doesn't work in Github Actions.")
def test_google_genai_embedding():
    app_injector = Injector()
    app_config = AppConfigSource(
        config={
            "llm.embedding_api_type": "google_genai",
            "llm.embedding_model": "genai-v1",
            "llm.api_key": "AIzaSyA0fCGtlAyxF_s_dBObsnL70xocI3GJlTE",
            # need to configure llm.api_key in the config to run this test
        },
    )
    app_injector.binder.bind(AppConfigSource, to=app_config)
    google_genai_service = app_injector.create_object(GoogleGenAIService)

    text_list = ["This is a test sentence.", "This is another test sentence."]
    embeddings = google_genai_service.get_embeddings(text_list)

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1536  # assuming the embedding size for Google GenAI is 1536
    assert len(embeddings[1]) == 1536