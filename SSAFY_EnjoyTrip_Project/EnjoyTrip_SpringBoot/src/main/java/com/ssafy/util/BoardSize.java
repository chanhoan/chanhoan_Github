package com.ssafy.util;

public enum BoardSize {

	LIST(8), NAVIGATION(10);

//	Size를 저장 할 필드
	private int boardSize;

//	싱글톤 (생성자)	
	private BoardSize(int boardSize) {
		this.boardSize = boardSize;
	}

//	Getter
	public int getBoardSize() {
		return boardSize;
	}

}
