package com.ssafy.trip.controller;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.ssafy.trip.dto.request.RecommandPathRequest;
import com.ssafy.trip.dto.request.TripDetailRequest;
import com.ssafy.trip.dto.request.TripListRequest;
import com.ssafy.trip.dto.request.TripTrieSearchRequest;
import com.ssafy.trip.dto.response.TripDetailResponse;
import com.ssafy.trip.dto.response.TripListResponse;
import com.ssafy.trip.dto.response.TripTrieSearchResponse;
import com.ssafy.trip.model.TripDto;
import com.ssafy.trip.model.service.TripService;
import com.ssafy.util.PageNavigation;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("/trip")
@Tag(name = "Trip", description = "여행 관련 API")
public class TripController {

    private final TripService tripService;

    @Operation(summary = "여행 목록 조회", description = "검색 조건에 따라 여행 목록을 조회합니다.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "성공", content = @Content(schema = @Schema(implementation = TripListResponse.class))),
            @ApiResponse(responseCode = "400", description = "잘못된 요청", content = @Content)
    })
    @PostMapping("/list")
    public ResponseEntity<?> tripList(@RequestBody TripListRequest tripListRequest) {
    	
    	if (tripListRequest.getPgno() <= 0) {
    		tripListRequest.setPgno(1);
    	}

        TripListResponse tripListResponse = new TripListResponse();
        // 검색 조건 출력(디버깅용)
        System.out.println("pgno: " + tripListRequest.getPgno());
        System.out.println("code: " + tripListRequest.getCode());
        System.out.println("type: " + tripListRequest.getType());
        System.out.println("name: " + tripListRequest.getName());

        Map<String, String> map = new HashMap<>();
        map.put("pgno", String.valueOf(tripListRequest.getPgno()));
        map.put("code", tripListRequest.getCode());
        map.put("type", tripListRequest.getType());
        map.put("name", tripListRequest.getName());

        // 시도 목록과 콘텐츠 타입 목록 설정
        tripListResponse.setSidoList(tripService.searchListAreaInfo());
        tripListResponse.setContentTypeList(tripService.searchListContentType());

        // 페이지 네비게이션 처리
        try {
            PageNavigation pageNavigation = tripService.makePageNavigation(map);
            tripListResponse.setPageNavigation(pageNavigation);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        try {
            tripListResponse.setTripList(tripService.searchTripList(tripListRequest));
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        return new ResponseEntity<>(tripListResponse, HttpStatus.OK);
    }

    @Operation(summary = "여행 상세 조회", description = "여행 상세 정보를 조회합니다.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "성공", content = @Content(schema = @Schema(implementation = TripDetailResponse.class))),
            @ApiResponse(responseCode = "400", description = "잘못된 요청", content = @Content)
    })
    @PostMapping("/detail")
    public ResponseEntity<?> tripDetail(@Valid @RequestBody TripDetailRequest tripDetailRequest) {

        TripDetailResponse tripDetailResponse = new TripDetailResponse();

        try {
            System.out.println(tripDetailRequest.getCode());
            TripDto tripDto = (TripDto) tripService.viewTrip(Integer.parseInt(tripDetailRequest.getCode()));
            List<TripDto> nearTripDto = new ArrayList<>();
            nearTripDto = tripService.getNearTrip(tripDto.getLatitude(), tripDto.getLongitude());
            tripDetailResponse.setTrip(tripDto);
            tripDetailResponse.setNearTripList(nearTripDto);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
        return ResponseEntity.ok().body(tripDetailResponse);
    }

    @Operation(summary = "여행 트라이 검색", description = "트라이 구조를 사용하여 여행 검색을 수행합니다.")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "성공", content = @Content(schema = @Schema(implementation = TripTrieSearchResponse.class))),
            @ApiResponse(responseCode = "400", description = "잘못된 요청", content = @Content)
    })
    @PostMapping("/trieSearch")
    public ResponseEntity<?> trieSearch(@Valid @RequestBody TripTrieSearchRequest tripTrieSearchRequest) {

        Map<String, Object> map = new HashMap<>();
        map.put("code", tripTrieSearchRequest.getCode());
        map.put("type", tripTrieSearchRequest.getType());
        map.put("name", tripTrieSearchRequest.getName());

        TripTrieSearchResponse tripTrieSearchResponse = new TripTrieSearchResponse();
        tripTrieSearchResponse.setTrieList(tripService.getTrieList(map));
        return ResponseEntity.ok().body(tripTrieSearchRequest);
    }
    
    @Operation(summary = "여행 경로 추천", description = "외판원 순회를 통해 출발지, 경유지, 도착지 사이의 최적 경로를 제공합니다.")
    @PostMapping("/getPath")
    private ResponseEntity<?> getPath(@Valid @RequestBody RecommandPathRequest recommandPathRequest) {
	    try {
	        int startId = Integer.parseInt(recommandPathRequest.getStartId());
	        int endId = Integer.parseInt(recommandPathRequest.getEndId());

	        List<Integer> waypointIds = new ArrayList<>();
	        for (String waypointIdStr : recommandPathRequest.getWaypointIds()) {
	            waypointIds.add(Integer.parseInt(waypointIdStr));
	        }

	        List<TripDto> optimalPath = tripService.findOptimalPath(startId, waypointIds, endId);
	        System.out.println(optimalPath);
	        
	        if (optimalPath.isEmpty()) {
	            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
	        }

	        // 최적 경로를 JSON으로 변환
	        HttpHeaders headers = new HttpHeaders();
	        headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
	        
	        return ResponseEntity.ok().headers(headers).body(optimalPath);
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
	    }
	}


    @Operation(summary = "여행 경로 선택", description = "출발지, 도착지, 경유지 순서대로 가고싶은 여행지를 선택합니다.")
    @PostMapping("/selectAttraction")
	private ResponseEntity<?> selectAttraction(@RequestParam(value = "contentId") int contentId) throws IOException {
	    
	    try {
	        TripDto attraction = tripService.viewTrip(contentId);
	        if (attraction == null) {
	        	return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
	        }

	        HttpHeaders headers = new HttpHeaders();
	        headers.setContentType(new MediaType("application", "json", StandardCharsets.UTF_8));
	        
	        return ResponseEntity.ok().headers(headers).body(attraction);
	    } catch (NumberFormatException e) {
	        // 유효하지 않은 contentId 형식
	        return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
	    } catch (Exception e) {
	        e.printStackTrace();
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
	    }
	}
    
}
