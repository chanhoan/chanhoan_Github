package com.ssafy.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfiguration {

    @Bean
    public OpenAPI openAPI() {
        Info info = new Info()
                .title("Reservation 명세서")
                .description("<h3>SSAFY12_광주5_관통_Framework_10팀_ 정찬환_김의현 TripAPI Reference for Developers</h3>Swagger를 이용한 Trip API<br><img src=\"/assets/img/images.png\" width=\"150\"><br>")
                .version("v1")
                .contact(new Contact()
                        .name("정찬환/김의현")
                        .email("keh0885@gmail.com")
                        .url("http://edu.ssafy.com"));

        return new OpenAPI()
                .components(new Components())
                .info(info);
    }

    @Bean
    public GroupedOpenApi userApi() {
        return GroupedOpenApi.builder()
                .group("member")
                .pathsToMatch("/member/**")
                .build();
    }

    @Bean
    public GroupedOpenApi tripApi() {
        return GroupedOpenApi.builder()
                .group("trip")
                .pathsToMatch("/trip/**")
                .build();
    }
    
    @Bean
    public GroupedOpenApi aiApi() {
        return GroupedOpenApi.builder()
                .group("ai")
                .pathsToMatch("/ai/**")
                .build();
    }
    
    @Bean
    public GroupedOpenApi boardApi() {
        return GroupedOpenApi.builder()
                .group("board")
                .pathsToMatch("/board/**")
                .build();
    }
}
