package com.example.demo.app;

import com.example.demo.service.AsyncTaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
@RestController
@RequestMapping("/test")
public class TestController {
    @Autowired
    private AsyncTaskService asyncTaskService;

    @GetMapping("/async")
    public String testAsync() {
        try {
            asyncTaskService.submitTasksByLatch("test-002", 100);
            return "处理完成";
        } catch (Exception e) {
            e.printStackTrace();
            return "处理失败: " + e.getMessage();
        }
    }
}
