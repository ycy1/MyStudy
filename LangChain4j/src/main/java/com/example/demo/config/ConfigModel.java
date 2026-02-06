package com.example.demo.config;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.image.ImageModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.model.ollama.OllamaStreamingChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.openai.OpenAiStreamingChatModel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

import java.time.Duration;

import static dev.langchain4j.model.chat.request.ResponseFormat.JSON;

@Component
@Slf4j
public class ConfigModel {

    public static String modelname_modelscope = "Qwen/Qwen2.5-Coder-32B-Instruct";
    public static String apiKey = "ms-4d36edb8-****-4145-ae70-af8c40a34f10";
    public static String baseUrl = "https://api-inference.modelscope.cn/v1/";
    // deepseek-r1 、deepseek-r1:1.5b 、qwen3:4b 、qwen3:1.7b,  qwen2.5vl:3b qwen3-vl:4b
    public static String modelName_ollama = "qwen3-vl:4b";
    public static String baseUrl_ollama = "http://localhost:11434";

    static ChatLanguageModel ollamaModel = null;
    static OpenAiChatModel modelscopeModel = null;
    static OllamaStreamingChatModel modelStream = null;
    static OpenAiStreamingChatModel modelscopeStream = null;
    @Bean("ollamaChatMode")
    public static ChatLanguageModel getOllamaChatModel(){
        log.info("get ollamaModel");
        if (ollamaModel == null)
            ollamaModel = OllamaChatModel.builder()
//                    .responseFormat(JSON)
                    .baseUrl(baseUrl_ollama)
                    .modelName(modelName_ollama)
                    .temperature(0.8)
                    .numPredict(1000)  // 最大生成 tokens
                    .timeout(Duration.ofSeconds(2000))
                    .logRequests(true)
                    .logResponses(true)
                    .build();
        return ollamaModel;
    }


    @Bean("modelscopeModel")
    public static ChatLanguageModel getModelscopeModel(){
        log.info("get modelscopeModel");
        if (modelscopeModel == null)
            modelscopeModel = OpenAiChatModel.builder()
//                    .responseFormat("JSON")
                    .baseUrl(baseUrl)
                    .apiKey(apiKey)
                    .modelName(modelname_modelscope)
                    .maxTokens(1000)
                    .timeout(Duration.ofSeconds(2000))
                    .build();

        return modelscopeModel;
    }

    @Bean("openAiStreamingChatModel")
    public static OpenAiStreamingChatModel getOpenAiStreamingChatModel(){
        log.info("get OpenAiStreamingChatModel");
        modelscopeStream = OpenAiStreamingChatModel.builder()
                .baseUrl(baseUrl)
                .apiKey(apiKey)
                .modelName(modelname_modelscope)
                .maxTokens(1000)
                .timeout(Duration.ofSeconds(2000))
                .build();

        return modelscopeStream;
    }


    @Bean("streamOllamaChatModel")
    public static OllamaStreamingChatModel getStreamOllamaChatModel(){
        log.info("get getStreamOllamaChatModel");
        modelStream = OllamaStreamingChatModel.builder()
                .baseUrl(baseUrl_ollama)
                .modelName(modelName_ollama)
                .temperature(0.8)
                .numPredict(1000)  // 最大生成 tokens
                .timeout(Duration.ofSeconds(2000))
                .build();

        return modelStream;
    }




}
