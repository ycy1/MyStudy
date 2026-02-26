package com.example.demo;

import com.example.demo.service.AsyncTaskService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeoutException;

@SpringBootTest
public class AsyncTaskTest {
    @Autowired
    private AsyncTaskService asyncTaskService;
    @Test
    public void testAsyncTask() throws ExecutionException, InterruptedException, TimeoutException {
        // 测试异步任务
        asyncTaskService.submitTasks("test", 10);
    }
}
