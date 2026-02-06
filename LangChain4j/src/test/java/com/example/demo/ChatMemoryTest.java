package com.example.demo;

import com.example.demo.service.Assistant;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.model.ollama.OllamaStreamingChatModel;
import dev.langchain4j.rag.content.Content;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.TokenStream;
import dev.langchain4j.service.tool.ToolExecution;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.concurrent.CountDownLatch;

@SpringBootTest
public class ChatMemoryTest {

    @Autowired
    @Qualifier("ollamaChatMode")
    public ChatLanguageModel ollamaModel;


    @Autowired
    @Qualifier("modelscopeModel")
    public ChatLanguageModel modelscopeModel;

    @Autowired
    @Qualifier("myAssistant")
    public Assistant myAssistant;

    @Autowired
    @Qualifier("streamOllamaChatModel")
    public OllamaStreamingChatModel streamingChatModel;


    @Test
    void Test() throws InterruptedException {
        ChatMemory chatMemory = MessageWindowChatMemory.builder()
                .id("12345")
                .maxMessages(10)
//                .chatMemoryStore(new PersistentChatMemoryStore())
                .build();

        Assistant assistant = AiServices.builder(Assistant.class)
                .streamingChatLanguageModel(streamingChatModel)
                .chatMemory(chatMemory)
                .build();
        CountDownLatch latch = new CountDownLatch(1);

        Assistant assistant1 = AiServices.create(Assistant.class, streamingChatModel);

//        TokenStream tokenStream = assistant.chat("你好，我叫张三");
//        CountDownLatch finalLatch = latch;
//        tokenStream.onPartialResponse((String partialResponse) -> System.out.println(partialResponse))
//                .onRetrieved((List<Content> contents) -> System.out.println(contents))
//                .onToolExecuted((ToolExecution toolExecution) -> System.out.println(toolExecution))
//                .onCompleteResponse((ChatResponse response) -> {
//                    System.out.println(response);
//                    finalLatch.countDown();
//                })
//                .onError((Throwable error) -> error.printStackTrace())
//                .start();
//        latch.await();
//
//        latch = new CountDownLatch(1);
//        tokenStream = assistant.chat("现在 你知道我叫什么吗?");
//        CountDownLatch finalLatch1 = latch;
//        tokenStream.onPartialResponse((String partialResponse) -> System.out.println(partialResponse))
//                .onRetrieved((List<Content> contents) -> System.out.println(contents))
//                .onToolExecuted((ToolExecution toolExecution) -> System.out.println(toolExecution))
//                .onCompleteResponse((ChatResponse response) -> {
//                    System.out.println(response);
//                    finalLatch1.countDown();
//                })
//                .onError((Throwable error) -> error.printStackTrace())
//                .start();
//        latch.await();

//        myAssistant.buildModel(ollamaModel).buildMemory(chatMemory);
//        ChatResponse chat1 = myAssistant.chatCarryMemory(UserMessage.from("你好，我叫张三"));
//        System.out.println(chat1);
//        ChatResponse chat2 = myAssistant.chatCarryMemory(UserMessage.from("现在你知道我叫什么吗"));
//        System.out.println(chat2);


    }


}
