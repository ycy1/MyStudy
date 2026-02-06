package com.example.demo;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.DocumentSplitter;
import dev.langchain4j.data.document.loader.FileSystemDocumentLoader;
import dev.langchain4j.data.document.splitter.*;
import dev.langchain4j.data.embedding.Embedding;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.ollama.OllamaEmbeddingModel;
import dev.langchain4j.model.openai.OpenAiEmbeddingModel;
import dev.langchain4j.model.output.Response;
import dev.langchain4j.rag.DefaultRetrievalAugmentor;
import dev.langchain4j.rag.RetrievalAugmentor;
import dev.langchain4j.rag.content.Content;
import dev.langchain4j.rag.content.injector.DefaultContentInjector;
import dev.langchain4j.rag.content.retriever.EmbeddingStoreContentRetriever;
import dev.langchain4j.rag.query.Query;
import dev.langchain4j.rag.query.transformer.ExpandingQueryTransformer;
import dev.langchain4j.service.Result;
import dev.langchain4j.store.embedding.EmbeddingSearchRequest;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.store.embedding.IngestionResult;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;

import java.nio.file.FileSystems;
import java.nio.file.PathMatcher;
import java.time.Duration;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@SpringBootTest
public class RagTest {

    @Autowired
    @Qualifier("ollamaChatMode")
    public ChatLanguageModel ollamaModel;

    @Test
    void test() {
//        List<Document> documents = FileSystemDocumentLoader.loadDocuments("C:\\Users\\lids\\Desktop\\test");
//        System.out.println(documents);

        PathMatcher pathMatcher = FileSystems.getDefault().getPathMatcher("glob:*.pdf");
        List<Document> documents = FileSystemDocumentLoader.loadDocuments("C:\\Users\\lids\\Desktop\\test", pathMatcher);
//        System.out.println(documents);
//        System.out.println(documents.get(0).metadata().getString(Document.FILE_NAME));
//        var splitter = new ParagraphSplitter();
//        DocumentSplitters.
//        DocumentByParagraphSplitter splitter = DocumentSplitters.byParagraph();
//        DocumentByParagraphSplitter splitter = DocumentSplitters.byParagraph();

//        DocumentSplitter splitter = DocumentSplitters.recursive(1000, 100);
//        DocumentSplitter splitter = new DocumentByParagraphSplitter(1000, 100);
//        DocumentSplitter splitter = new DocumentByParagraphSplitter(1000, 100);
//        List<TextSegment> textSegments = splitter.splitAll(documents);
//        System.out.println(textSegments.size());
//        for (int i = 0; i < textSegments.size(); i++){
//            System.out.println(i+ "-----------------------------------------");
//            TextSegment textSegment = textSegments.get(i);
//            TextSegment from = TextSegment.from(textSegment.text(), textSegment.metadata());
//            System.out.println(textSegment);
//        }

        EmbeddingModel embeddingModel = OllamaEmbeddingModel.builder()
                .baseUrl("http://localhost:11434")  // Ollama 服务地址
                .modelName("qwen3-embedding:4b")      // 嵌入模型名称
                .timeout(Duration.ofSeconds(200))    // 超时设置
                .maxRetries(3)                      // 最大重试次数
                .build();

        var text = """
            人工智能是计算机科学的一个重要分支.
            它致力于让机器模拟人类的智能行为.

            近年来，大语言模型取得了突破性进展。
            这些模型能够理解并生成自然语言。

            然而，AI 仍面临可解释性和伦理挑战。
            """;

        // 1. 创建文档
        Document document2 = Document.from(
                "LangChain4j is a Java framework for building LLM-powered applications. " +
                        "It simplifies integration with various LLM providers."
        );

        Document document = Document.from(text);
//        var splitter = new DocumentByCharacterSplitter(20, 0); // 创建字符分割器
        var splitter = new DocumentByLineSplitter(30, 0); // 创建行分割器
//        var splitter = new DocumentByParagraphSplitter(50, 0); // 创建段落分割器
//        var splitter = new DocumentBySentenceSplitter(50, 0); // 创建句子分割器
//        var splitter = new DocumentByWordSplitter(10,0);// 创建单词分割器
//        List<TextSegment> paragraphs = splitter.split(document);
//        Response<List<Embedding>> listResponse = embeddingModel.embedAll(paragraphs);
//        System.out.println(listResponse.content().size());
//        System.out.println(listResponse);
//        System.out.println(embeddingModel.dimension());
//        System.out.println(paragraphs.size());
//        for (TextSegment paragraph : paragraphs) {
//            embeddingModel.embed(paragraph);
//            System.out.println(embeddingModel.dimension());
//        }

        ExpandingQueryTransformer queryTransformer = new ExpandingQueryTransformer(ollamaModel);
        // 创建查询转换器 扩展为多个Query
//        Collection<Query> transform = queryTransformer.transform(Query.from("人工智能是什么?"));
//        System.out.println(transform);
        // 验证所有文档
//        int expectedDim = embeddingModel.embed("test").content().dimension();
//        for (Document doc : List.of(document,document2)) {
//            Embedding emb = embeddingModel.embed(doc.text()).content();
//            if (emb.dimension() != expectedDim) {
//                throw new IllegalStateException("维度不一致！");
//            }
//        }

//        int dimension = embeddingModel.embed(document.toTextSegment()).content().dimension();
//        System.out.println(dimension);
//        int dimension1 = embeddingModel.embed(Query.from("LangChain4j是什么?").text()).content().dimension();
//        System.out.println(dimension1);

        InMemoryEmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();
//        IngestionResult ingest = EmbeddingStoreIngestor.ingest(document, embeddingStore);

        var ingestor = EmbeddingStoreIngestor.builder()
                .embeddingStore(embeddingStore)
                .embeddingModel(embeddingModel) // <-- 使用一致的模型
                .documentSplitter(splitter)
//                .documentTransformer()
//                .textSegmentTransformer()
                .build();

        ingestor.ingest(List.of(document,document2)); // 将文档段落及其嵌入向量存入 store



        EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
                .embeddingStore(embeddingStore)
                .embeddingModel(embeddingModel)
                .build();
//        List<Content> retrieve = retriever.retrieve(Query.from("LangChain4j?"));
//        System.out.println(retrieve);



        String templateString = """
            请根据以下信息回答问题：
            上下文：{{context}}
            问题：{{question}}
            答案：
            """;
        PromptTemplate promptTemplate = PromptTemplate.from(templateString);
        Map<String, Object> variables = new HashMap<>();
        variables.put("context", "LangChain4j 是一个用于简化在 Java 应用程序中集成大型语言模型（LLM）的框架。");
        variables.put("question", "LangChain4j 是什么？");
        String renderedPrompt = promptTemplate.apply(variables).text();
        System.out.println(renderedPrompt);




    }
}
