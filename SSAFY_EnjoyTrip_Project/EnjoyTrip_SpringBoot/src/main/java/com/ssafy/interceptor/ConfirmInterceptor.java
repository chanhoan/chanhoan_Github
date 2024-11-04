package com.ssafy.interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;


import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

//@SuppressWarnings("deprecation")
//public class ConfirmInterceptor extends HandlerInterceptorAdapter {
//spring 5.3 부터는 HandlerInterceptor implements
@Component
public class ConfirmInterceptor implements HandlerInterceptor { 

//	@Override
//	public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
//			throws Exception {
//		System.out.println("asdf");
//		HttpSession session = request.getSession();
//		UserDto memberDto = (UserDto) session.getAttribute("userinfo");
//		System.out.println("dto : "+memberDto);
//		
//		if(memberDto == null || !memberDto.getRole().equals("ADMIN")) {
//			request.setAttribute("msg", "권한이 없습니다.");
//			response.sendRedirect("/errors");
//			return false;
//		}
//		return true;
//	}
	
}