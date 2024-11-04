package com.ssafy.member.model.mapper;

import java.sql.SQLException;
import java.util.Map;

import org.apache.ibatis.annotations.Mapper;

import com.ssafy.member.model.MemberDto;


@Mapper
public interface MemberMapper {
	// 회원 가입
	int regist(MemberDto member) throws SQLException;

	// 아이디 중복체크 중복 있으면 0 없으면 1
	int idCheck(String userId) throws SQLException;

	// 로그인
	MemberDto login(Map<String, String> map) throws SQLException;

	// 회원 정보 수정
	int modify(MemberDto member) throws SQLException;
	
	//신규비밀번호 발급으로 정보 수정
	int modifyPassword(MemberDto member) throws SQLException;

	// 회원 탈퇴
	int delete(String userId) throws SQLException;

	MemberDto getMemberById(String userId) throws SQLException;
}
