package com.ssafy.trip.model.service;

import java.util.List;
import java.util.Map;

import com.ssafy.trip.dto.request.TripListRequest;
import com.ssafy.trip.model.TripDto;
import com.ssafy.util.PageNavigation;

public interface TripService {
	// 지역 정보 조회
		List<TripDto> searchListAreaInfo();
		
		// 관광지 검색
		List<TripDto> searchTripList(TripListRequest tripListRequest);
		
	    // 관광지 정보 조회
	    List<TripDto> searchListContentType();
	    
	    // 관광지 상세보기
	    TripDto viewTrip(int no);

	    // 페이징
		PageNavigation makePageNavigation(Map<String, String> map) throws Exception;
		
		//검색어 자동완성 trie
		List<String> getTrieList(Map<String, Object> map);
		
		// 근처 관광지 추천 알고리즘
		List<TripDto> getNearTrip(String latitude, String longitude);
		
		// 외판원 순회 알고리즘 (출발지, 경유지, 도착지 입력 후 최적 경로 제공)  
		List<TripDto> findOptimalPath(int startNo, List<Integer> waypointNos, int endNo) throws Exception;


}
