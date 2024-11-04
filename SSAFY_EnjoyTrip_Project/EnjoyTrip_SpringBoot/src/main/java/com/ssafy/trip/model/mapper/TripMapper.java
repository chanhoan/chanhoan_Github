package com.ssafy.trip.model.mapper;

import java.util.List;
import java.util.Map;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import com.ssafy.trip.dto.request.TripListRequest;
import com.ssafy.trip.model.TripDto;

@Mapper
public interface TripMapper {

    // 지역 정보 리스트 조회
    List<TripDto> selectListAreaInfo();

    // 여행지 리스트 검색 조회
	List<TripDto> selectTripList(TripListRequest tripListRequest);

    // 콘텐츠 타입 리스트 조회
    List<TripDto> selectListContentType();

    // 여행지 번호로 여행지 조회
    TripDto selectTrip(int no);

    // 여행지 총 개수 조회
	int getTotalTripCount(Map<String, Object> map);

    // 여행지 키워드 리스트 조회
	List<String> selectListTripKeyword(Map<String, Object> map);

    // 근처 여행지 조회
    List<TripDto> selectNearTrip(@Param("latitude") String latitude, @Param("longitude") String longitude);

}
