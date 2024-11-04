package com.ssafy.board.model.service;

import org.springframework.stereotype.Service;

import com.ssafy.board.model.dto.BoardDto;

import java.util.List;

@Service
public interface BoardService {

	// 글 등록
	int insert(BoardDto boardDto) throws Exception;

	// 글 삭제
	int delete(int boardId) throws Exception;

	// 글 수정
	int update(BoardDto boardDto) throws Exception;

	// 글 전체 조회
	List<BoardDto> listAll() throws Exception;

	// 카테고리별 글 목록 조회
	List<BoardDto> listByCategory(String category) throws Exception;

	// 글 상세 조회
	BoardDto detail(int boardId) throws Exception;
}
