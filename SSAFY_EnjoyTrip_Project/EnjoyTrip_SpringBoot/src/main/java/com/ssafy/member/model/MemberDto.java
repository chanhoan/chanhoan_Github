package com.ssafy.member.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class MemberDto {
	private String userId;
	private String userName;
	private String userPassword;
	private String email;
}
