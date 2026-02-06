package com.example.demo.service;

import dev.langchain4j.agent.tool.ToolSpecification;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.request.ChatRequest;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.service.Result;
import dev.langchain4j.service.TokenStream;

import java.util.List;

public interface Assistant {

    Assistant buildModel(ChatLanguageModel  model);

    Assistant buildMemory(ChatMemory  memory);

    Assistant buildTools(Class... clazzs);

    Result<String> chat(String question);

    ChatResponse chat(ChatMessage... messages);



    ChatResponse chatCarryMemory(ChatMessage... messages);
}
