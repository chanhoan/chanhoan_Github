package com.ssafy.openai.util;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;
import org.springframework.util.FileCopyUtils;

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class PromptTemplateLoader {

	@Value("classpath:prompts/prompt-attraction-system.st")
    private Resource systemPromptResource;
    
    @Value("classpath:prompts/prompt-attraction-user.st")
    private Resource userPromptResource;
    
    public String loadSystemPrompt() {
        try {
            return new String(FileCopyUtils.copyToByteArray(systemPromptResource.getInputStream()), StandardCharsets.UTF_8);
        } catch (IOException e) {
            log.error("Error loading system prompt template", e);
            throw new RuntimeException("Failed to load system prompt template", e);
        }
    }
    
    public String loadUserPrompt() {
        try {
            return new String(FileCopyUtils.copyToByteArray(userPromptResource.getInputStream()), StandardCharsets.UTF_8);
        } catch (IOException e) {
            log.error("Error loading user prompt template", e);
            throw new RuntimeException("Failed to load user prompt template", e);
        }
    }
    
}
