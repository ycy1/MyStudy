package com.example.demo;

import com.example.demo.service.Assistant;
import com.example.demo.tools.MovieTools;
import com.example.demo.tools.WeatherTools;
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.agent.tool.ToolExecutionRequest;
import dev.langchain4j.agent.tool.ToolSpecification;
import dev.langchain4j.agent.tool.ToolSpecifications;
import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.ToolExecutionResultMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.request.ChatRequest;
import dev.langchain4j.model.chat.request.json.JsonObjectSchema;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.Result;
import dev.langchain4j.service.TokenStream;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@SpringBootTest
public class ToolsTest {

    @Autowired
    @Qualifier("ollamaChatMode")
    public ChatLanguageModel ollamaModel;

    @Autowired
    @Qualifier("modelscopeModel")
    public ChatLanguageModel modelscopeModel;

    @Autowired
    @Qualifier("myAssistant")
    public Assistant myAssistant;

    @Test
    void test() {
//        ToolSpecification toolSpecification = ToolSpecification.builder()
//                .name("getWeather")
//                .description("返回给定城市的天气预报")
//                .parameters(JsonObjectSchema.builder()
//                        .addStringProperty("city", "应返回天气预报的城市")
//                        .addEnumProperty("temperatureUnit", List.of("CELSIUS", "FAHRENHEIT"))
//                        .required("city") // 必须明确指定必需的属性
//                        .build())
//                .build();
//
//
//        List<ToolSpecification> toolSpecifications = ToolSpecifications.toolSpecificationsFrom(WeatherTools.class);
//        System.out.println(toolSpecifications);
//        List<ToolSpecification> tools = (List) Arrays.stream(WeatherTools.class.getDeclaredMethods())
//                .filter((method) -> method.isAnnotationPresent(Tool.class))
//                .map(ToolSpecifications::toolSpecificationFrom)
//                .collect(Collectors.toList());
//        System.out.println(tools);

//
//
//
//        ChatRequest request = ChatRequest.builder()
//                .messages(UserMessage.from("明天伦敦的天气会怎样？"))
//                .toolSpecifications(toolSpecifications)
//                .build();
//        ChatResponse response = ollamaModel.chat(request);
//        List<ToolExecutionRequest> toolExecutionRequests = response.aiMessage().toolExecutionRequests();
//
//        String result = "预计明天伦敦会下雨。";
//        ToolExecutionResultMessage toolExecutionResultMessage = ToolExecutionResultMessage.from(toolExecutionRequests.get(0), result);
//        System.out.println(response);
//
//        ChatRequest request2 = ChatRequest.builder()
//                .messages(List.of(UserMessage.from("明天伦敦的天气会怎样？"), response.aiMessage(), toolExecutionResultMessage))
//                .toolSpecifications(toolSpecifications)
//                .build();
//        ChatResponse response2 = ollamaModel.chat(request2);
//        System.out.println(response2);

//
//        Assistant assistant = AiServices.builder(Assistant.class)
////                .tools(new WeatherTools(), new MovieTools())
//                .chatLanguageModel(ollamaModel)
////                .chatMemory(chatMemory)
//                .build();
//        Result<String> result = assistant.chat("查询美人鱼的电影信息");
//        System.out.println(result.content());
//        System.out.println(result.tokenUsage());
//        System.out.println(result.sources());
//        查询上海到北京的机票，并查询北京的天气怎么样
        myAssistant.buildModel(ollamaModel).buildTools(WeatherTools.class, MovieTools.class);
        ChatResponse chat1 = myAssistant.chat(UserMessage.from("查询上海到北京的机票，并查询北京的天气怎么样，最后查询美人鱼的电影信息"));
        System.out.println(chat1);


    }
}
