package com.example.demo;

import dev.langchain4j.data.embedding.Embedding;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.request.ChatRequest;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;

import java.time.Duration;

public class Test {

    public static void main(String[] args) {
        OpenAiChatModel customUrlModel = OpenAiChatModel.builder()
                .baseUrl("https://api-inference.modelscope.cn/v1/")
                .apiKey("ms-4d36edb8-d883-4145-ae70-af8c40a34f10")
                .modelName("Qwen/Qwen2.5-Coder-32B-Instruct")
                .maxTokens(1024)
                .timeout(Duration.ofSeconds(2000))
                .logRequests(true)
                .logResponses(true)
                .build();
        String chat = customUrlModel.chat("介绍一下LangChain4j");
        System.out.println(chat);


//        ChatLanguageModel model = OllamaChatModel.builder()
//                .baseUrl("http://localhost:11434")
//                .modelName("deepseek-r1:1.5b")
//                .temperature(0.8)
//                .numPredict(512)  // 最大生成 tokens
//                .timeout(Duration.ofSeconds(2000))
//                .build();
//
//        String answer = model.chat("介绍一下LangChain4j");
//        System.out.println(answer);

    }

}
