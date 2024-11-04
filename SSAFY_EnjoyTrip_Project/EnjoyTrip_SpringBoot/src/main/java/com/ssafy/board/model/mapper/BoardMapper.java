package com.ssafy.board.model.mapper;

import java.sql.SQLException;
import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.ssafy.board.model.dto.BoardDto;

@Mapper
public interface BoardMapper {

	// 글 등록
	int insert(BoardDto boardDto) throws SQLException;

	// 글 삭제
	int delete(int boardId) throws SQLException;

	// 글 수정
	int update(BoardDto boardDto) throws SQLException;

	// 글 전체 조회
	List<BoardDto> listAll() throws SQLException;

	// 카테고리별 글 목록 조회
	List<BoardDto> listByCategory(String category) throws SQLException;

	// 글 상세 조회
	BoardDto detail(int boardId) throws SQLException;
}
