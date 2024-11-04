package com.ssafy.member.model.service;

import java.sql.SQLException;
import java.util.Map;

import com.ssafy.member.model.MemberDto;

public interface MemberService {
	
	//회원 가입
	int regist(MemberDto member) throws SQLException;
	
	//아이디 중복체크
	Boolean idCheck(String userId) throws SQLException;
	
	//로그인
	MemberDto login(Map<String, String> map) throws SQLException;
	
	//회원 정보 수정
	int modify(MemberDto member) throws SQLException;
	
	int modifyPassword(MemberDto member) throws SQLException;
	
	//회원 탈퇴
	int delete(String userId) throws SQLException;

}
