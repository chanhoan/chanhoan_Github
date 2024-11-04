package com.ssafy.member.model.service;

import java.sql.SQLException;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ssafy.member.model.MemberDto;
import com.ssafy.member.model.mapper.MemberMapper;
import com.ssafy.util.PasswordUtil;

@Service
public class MemberServiceImpl implements MemberService {

	private MemberMapper memberMapper;
	
	@Autowired
	public MemberServiceImpl(MemberMapper memberMapper) {
		this.memberMapper = memberMapper;
	}

	@Override
	public int regist(MemberDto memberDto) throws SQLException {
		String hashedPassword = PasswordUtil.hashPassword(memberDto.getUserPassword());
		memberDto.setUserPassword(hashedPassword);
        return memberMapper.regist(memberDto);
	}

	@Override
	public Boolean idCheck(String userId) throws SQLException {
		if(memberMapper.idCheck(userId) == 0) { 
			return false;
		} else {
			return true;	
		}
		
	}

	@Override
	public MemberDto login(Map<String, String> map) throws SQLException {
		
		// DB에서 사용자의 해시된 비밀번호를 가져옴
        MemberDto storedMember = memberMapper.login(map);
        
        // 비밀번호가 맞는지 확인
        if (storedMember != null && PasswordUtil.checkPassword(map.get("userPassword"), storedMember.getUserPassword())) {
            return storedMember;                                                                  
        }
        return null;
	}

	@Override
	public int modify(MemberDto member) throws SQLException {
		String hashedPassword = PasswordUtil.hashPassword(member.getUserPassword());
        member.setUserPassword(hashedPassword);
		return memberMapper.modify(member);
	}

	@Override
	public int modifyPassword(MemberDto member) throws SQLException {
		String hashedPassword = PasswordUtil.hashPassword(member.getUserPassword());
        member.setUserPassword(hashedPassword);
        return memberMapper.modifyPassword(member);
	}

	@Override
	public int delete(String id) throws SQLException {
		return memberMapper.delete(id);
	}

}
