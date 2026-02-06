package com.example.demo;

import com.example.demo.service.Assistant;
import com.example.demo.service.impl.StreamingChatResponseHandlerImpl;
import dev.langchain4j.data.message.*;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.model.chat.response.StreamingChatResponseHandler;
import dev.langchain4j.model.ollama.OllamaStreamingChatModel;
import dev.langchain4j.model.openai.OpenAiStreamingChatModel;
import dev.langchain4j.service.AiServices;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Base64;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

import static dev.langchain4j.model.LambdaStreamingResponseHandler.onPartialResponse;
import static dev.langchain4j.model.LambdaStreamingResponseHandler.onPartialResponseAndError;

@SpringBootTest
class ChatModelTest {

    @Autowired
    @Qualifier("ollamaChatMode")
    public ChatLanguageModel ollamaModel;


    @Autowired
    @Qualifier("modelscopeModel")
    public ChatLanguageModel modelscopeModel;

    @Autowired
    @Qualifier("streamOllamaChatModel")
    public OllamaStreamingChatModel streamingChatModel;

    @Autowired
    @Qualifier("openAiStreamingChatModel")
    public OpenAiStreamingChatModel openAiStreamingChatModel;

    @Autowired
    @Qualifier("myAssistant")
    public Assistant myAssistant;

//    @Autowired
//    @Qualifier("streamingChatResponseHandler")
//    public StreamingChatResponseHandler streamingChatResponseHandler;

	@Test
	void contextLoads() throws IOException, InterruptedException {
//        String answer = ollamaModel.chat("介绍一下你自己");
//        System.out.println(answer);

//        System.out.println("-------------------------------------------------------------------------------");
//        String answer2 = modelscopeModel.chat("介绍一下你自己");
//        System.out.println(answer2);

        SystemMessage systemMessage = SystemMessage.from("你是一个智能问答助手");
        URL url = new URL("http://182.92.85.80/group1/M00/00/05/tlxVUGjMD12ARrLnAAEMpONpIN806.webp");
        InputStream inputStream = url.openStream();
        byte[] imageBytes = inputStream.readAllBytes();
        String base64Image = Base64.getEncoder().encodeToString(imageBytes);
        UserMessage firstUserMessage = UserMessage.from(
//                ImageContent.from(base64Image, "image/webp"),
//                ImageContent.from("http://182.92.85.80/group1/M00/00/05/tlxVUGjMD12ARrLnAAEMpONpIN806.webp"),
                TextContent.from("你好，简短的介绍一下你自己")

        );
//        ChatResponse response = ollamaModel.chat(firstUserMessage);
//        AiMessage aiMessage = response.aiMessage();
//        System.out.println(response);

//        Assistant assistant = AiServices.builder(Assistant.class)
//                .chatLanguageModel(ollamaModel)
//                .build();
//
//        String chat = assistant.chat("你好，简短的介绍一下你自己");
//        System.out.println(chat);
//        myAssistant.buildModel(ollamaModel);
//        ChatResponse chat1 = myAssistant.chat(firstUserMessage);
//        System.out.println(chat1);



//        流式响应是异步的，主线程可能在响应完成前就结束了
//        当前线程可能会在 onCompleteResponse 被调用前退出
        StreamingChatResponseHandlerImpl streamingChatResponseHandler = new StreamingChatResponseHandlerImpl();
        streamingChatModel.chat(List.of(firstUserMessage), streamingChatResponseHandler);
        streamingChatResponseHandler.latch.await(60,TimeUnit.SECONDS);


        streamingChatModel.chat("langchain是什么", streamingChatResponseHandler);
        streamingChatResponseHandler.latch.await(60,TimeUnit.SECONDS);


        streamingChatModel.chat("java是什么", streamingChatResponseHandler);
        streamingChatResponseHandler.latch.await(60,TimeUnit.SECONDS);

        // 所有响应处理完成后，调用 countDown() 方法来释放线程
        streamingChatResponseHandler.latch.countDown();

//        CountDownLatch latch = new CountDownLatch(1);
//        streamingChatModel.chat("你好", onPartialResponseAndError(System.out::println,Throwable::getMessage));
//        latch.await(60, TimeUnit.SECONDS);


    }

}
