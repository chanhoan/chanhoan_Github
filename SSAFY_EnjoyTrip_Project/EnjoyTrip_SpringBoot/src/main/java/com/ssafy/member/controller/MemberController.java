package com.ssafy.member.controller;

import java.nio.charset.StandardCharsets;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Random;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.ssafy.member.model.MemberDto;
import com.ssafy.member.model.service.MemberService;
import com.ssafy.util.PasswordUtil;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/member")
@Tag(name = "MemberController", description = "로그인, 로그아웃, 회원가입, 회원정보수정, 회원탈퇴 기능 처리")
public class MemberController {
	
	private MemberService memberService;

	@Autowired
	public MemberController(MemberService memberService) {
		this.memberService = memberService;
	}
	
	@PostMapping("/login")
	@Operation(summary = "로그인", description = "유저의 로그인 정보를 인증하고 성공 시 세션을 시작합니다.")
	public ResponseEntity<?> login(@RequestParam Map<String, String> map, HttpSession httpSession, HttpServletResponse response, HttpServletRequest request) {
		try {
			MemberDto loginUser = memberService.login(map);
			
			if (!Objects.isNull(loginUser)) { 
				httpSession.setAttribute("loginUser", loginUser);
				
				if ("on".equals(map.get("remember"))) {
					Cookie cookie = new Cookie("remeberId", loginUser.getUserId());
					cookie.setMaxAge(60*60*24*365*29);
					response.addCookie(cookie);
				} else {
					Cookie[] cookies = request.getCookies();
					for (Cookie cookie : cookies) {
						if (cookie.getName().equals("rememberId")) {
							cookie.setMaxAge(0);
							response.addCookie(cookie);
						}
					}
				}
				
				HttpHeaders headers = new HttpHeaders();
                headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8)); 
				
				// 로그인 성공
				return ResponseEntity.ok().build();
			} else {
				// 로그인 실패
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			// 서버 에러
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}	
	}
	
	@PostMapping("/logout")
	@Operation(summary = "로그아웃", description = "유저의 로그인 정보를 세션에서 제거합니다.")
	public ResponseEntity<?> logout(HttpSession httpSession) {
		MemberDto loginUser = (MemberDto) httpSession.getAttribute("loginUser");
		
		if (!Objects.isNull(loginUser)) {
			httpSession.invalidate();
			return ResponseEntity.ok().build();
		} else {
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();	
		}
	}
	
	@PostMapping("/regist")
	@Operation(summary = "회원가입", description = "새로운 유저를 등록하고 회원가입 절차를 완료합니다.")
	public ResponseEntity<?> regist(MemberDto memberDto) {
		try {
			int cnt = memberService.regist(memberDto);
			
			if (cnt == 1) {
				return ResponseEntity.ok().build();
			} else { 
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}
	
	@PostMapping("/modify")
	@Operation(summary = "회원 정보 수정", description = "바꾸고자하는 유저의 정보를 입력받아 수정합니다.")
	public ResponseEntity<?> modify(MemberDto memberDto) {
		try {
			int cnt = memberService.modify(memberDto);
			
			if (cnt == 1) {
				return ResponseEntity.ok().build();
			} else { 
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}
	
	@PostMapping("/delete")
	@Operation(summary = "회원탈퇴", description = "유저의 정보를 영구적으로 삭제합니다.")
	public ResponseEntity<?> delete(@RequestParam(value = "userId") String userId) {
		try {
			int cnt = memberService.delete(userId);
			
			if (cnt == 1) {
				return ResponseEntity.ok().build(); 
			} else {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();

		}
	}
	
	@GetMapping("/idCheck/{userId}")
	@Operation(summary = "중복 아이디 확인", description = "유저의 회원 가입 시 같은 아이디가 있는지 확인합니다.")
	public ResponseEntity<?> idCheck(@PathVariable(value = "userId") String userId) {
		try {			
			Map<String, Boolean> map = new HashMap<>();
			map.put("bool", memberService.idCheck(userId));
			
			HttpHeaders headers = new HttpHeaders();
			headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
			return ResponseEntity.ok().headers(headers).body(map);
		} catch (SQLException e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}
	
	@PostMapping("/passwordCheck")
	@Operation(summary = "비밀번호 확인", description = "유저의 개인 정보 확인 시 비밀번호를 확인합니다.")
	public ResponseEntity<?> passwordCheck(HttpSession httpSession, @RequestParam(value = "userPassword") String userPassword) {
		MemberDto loginUser = (MemberDto) httpSession.getAttribute("loginUser");
		
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
		return ResponseEntity.ok().headers(headers).body(PasswordUtil.checkPassword(userPassword, loginUser.getUserPassword()));
	}
	

	
	
	@PostMapping("/newPassword")
	@Operation(summary = "임시 비밀번호 발급", description = "알파벳 대/소문자, 숫자로 이루어진 8자리의 새로운 임시 비밀번호를 발급합니다.")
	public ResponseEntity<?> newPassword(@RequestParam Map<String, String> map) {
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        Random random = new Random();
        StringBuilder newPassword = new StringBuilder();
        for (int i = 0; i < 8; i++) {
            int index = random.nextInt(chars.length());
            newPassword.append(chars.charAt(index));
        }
        String password = newPassword.toString();
        
        MemberDto memberDto = new MemberDto();
        memberDto.setUserId(map.get("userId"));
        memberDto.setUserName(map.get("userName"));
        memberDto.setEmail(map.get("email"));
        memberDto.setUserPassword(password);
        
        try {
			if (memberService.modifyPassword(memberDto) == 1) {
				HttpHeaders headers = new HttpHeaders();
				headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
				return ResponseEntity.ok().headers(headers).body(memberDto.getUserPassword());
			} else {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (SQLException e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}
}
