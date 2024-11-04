package com.ssafy.openai.controller;

import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ssafy.openai.util.PromptTemplateLoader;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
//@CrossOrigin("*")
@RequestMapping("/ai")
@Tag(name = "AIController", description = "여행 추천 기능 처리")
public class AIController {

	private final ChatModel chatModel;
	private final PromptTemplateLoader promptLoader;

	public AIController(ChatModel chatModel, PromptTemplateLoader promptLoader) {
		super();
		this.chatModel = chatModel;
		this.promptLoader = promptLoader;
	}

	
	@GetMapping("/plans/{city}")
	@Operation(summary = "여행 추천", description = "지역과 날에 맞는 여행 추천")
    public ResponseEntity<String> getAttractions(@PathVariable("city") String city) {
        try {
            // 유저 프롬프트 템플릿 로드 및 변수 설정
            String userPromptTemplate = promptLoader.loadUserPrompt();
            PromptTemplate userTemplate = new PromptTemplate(userPromptTemplate);
            userTemplate.add("city", city);
            String userCommand = userTemplate.render();

            // 시스템 프롬프트 로드
            String systemPromptTemplate = promptLoader.loadSystemPrompt();
            PromptTemplate systemTemplate = new PromptTemplate(systemPromptTemplate);
            String systemCommand = systemTemplate.render();
            
            // 메시지 생성
            Message userMessage = new UserMessage(userCommand);
            Message systemMessage = new SystemMessage(systemCommand);
            
            // API 호출
            String response = chatModel.call(userMessage, systemMessage);
            System.out.println(response);
//            log.info("Generated response for city: {}, day: {}", city, day);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
//            log.error("Error processing attraction request for city: " + city, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error processing request: " + e.getMessage());
        }
    }
	
}
