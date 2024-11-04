package com.ssafy.board.controller;

import java.util.List;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.ssafy.board.model.dto.BoardDto;
import com.ssafy.board.model.service.BoardService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/board")
@Tag(name = "BoardController", description = "게시판 관리 기능 제공")
public class BoardController {
	private BoardService boardService;

	@Autowired
	public BoardController(BoardService boardService) {
		this.boardService = boardService;
	}

	@Operation(summary = "게시글 등록", description = "새로운 게시글을 등록합니다.")
	@PostMapping("/insert")
	public ResponseEntity<?> insert(BoardDto boardDto) {
		try {
			int cnt = boardService.insert(boardDto);
			if (cnt == 1) {
				return ResponseEntity.ok().build();
			} else {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}

	@Operation(summary = "게시글 삭제", description = "게시글 ID를 사용하여 게시글을 삭제합니다.")
	@PostMapping("/delete")
	public ResponseEntity<?> delete(@RequestParam("boardId") int boardId) {
		try {
			int cnt = boardService.delete(boardId);
			if (cnt == 1) {
				return ResponseEntity.ok().build();
			} else {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}

	@Operation(summary = "게시글 수정", description = "기존 게시글의 내용을 수정합니다.")
	@PostMapping("/update")
	public ResponseEntity<?> update(BoardDto boardDto) {
		try {
			int cnt = boardService.update(boardDto);
			if (cnt == 1) {
				return ResponseEntity.ok().build();
			} else {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}

	@Operation(summary = "전체 게시글 목록 조회", description = "모든 게시글 목록을 조회합니다.")
	@PostMapping("/list/all")
	public ResponseEntity<?> listALL() {
		try {
			List<BoardDto> list = boardService.listAll();
			if (Objects.isNull(list)) {
				return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
			} else {
				return ResponseEntity.ok(list);
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}

	@Operation(summary = "카테고리별 게시글 조회", description = "특정 카테고리에 속하는 게시글 목록을 조회합니다.")
	@PostMapping("/list/category")
	public ResponseEntity<?> listCategory(@RequestParam(value = "categoryId") String categoryId) {
		try {
			List<BoardDto> list = boardService.listByCategory(categoryId);
			if (Objects.isNull(list)) {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			} else {
				return ResponseEntity.ok(list);
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}

	@Operation(summary = "게시글 상세 조회", description = "게시글 ID를 사용하여 게시글의 상세 정보를 조회합니다.")
	@PostMapping("/detail")
	public ResponseEntity<?> detail(@RequestParam(value = "boardId") int boardId) {
		try {
			BoardDto boardDto = boardService.detail(boardId);
			if (Objects.isNull(boardDto)) {
				return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
			} else {
				return ResponseEntity.ok(boardDto);
			}
		} catch (Exception e) {
			e.printStackTrace();
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
		}
	}
}
