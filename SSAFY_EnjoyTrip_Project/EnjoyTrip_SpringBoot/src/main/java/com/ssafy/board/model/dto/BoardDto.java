package com.ssafy.board.model.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BoardDto {

	int boardId;
	String boardCategory;
	String title;
	String userId;
	String registDate;
	String content;
	String boardRecommendCount;
	String boardNotRecommendCount;
	
}
