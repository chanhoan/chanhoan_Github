package com.ssafy.board.model.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ssafy.board.model.dto.BoardDto;
import com.ssafy.board.model.mapper.BoardMapper;

@Service
public class BoardServiceImpl implements BoardService{
	
	private BoardMapper boardMapper;
	
	@Autowired
	public BoardServiceImpl(BoardMapper boardMapper) {
		this.boardMapper = boardMapper;
	}

	@Override
	public int insert(BoardDto boardDto) throws Exception {
		return boardMapper.insert(boardDto);
	}

	@Override
	public int delete(int boardId) throws Exception {
		return boardMapper.delete(boardId);
	}

	@Override
	public int update(BoardDto boardDto) throws Exception {
		return boardMapper.update(boardDto);
	}

	@Override
	public List<BoardDto> listAll() throws Exception {
		return boardMapper.listAll();
	}

	@Override
	public List<BoardDto> listByCategory(String category) throws Exception {
		return boardMapper.listByCategory(category);
	}

	@Override
	public BoardDto detail(int boardId) throws Exception {
		return boardMapper.detail(boardId);
	}

}
