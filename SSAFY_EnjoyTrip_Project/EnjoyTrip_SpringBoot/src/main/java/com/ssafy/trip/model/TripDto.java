package com.ssafy.trip.model;

import lombok.Getter;
import lombok.Setter;

/**
 * 관광지 도메인 클래스
 * - DTO(Data Transfer Object) Pattern
 * - Encapsulation 적용 설계
 * - 직렬화 객체 적용 설계
 * - Lombok 기반 적용 설계
 * - 관광지 테이블 스키마 매핑
 */
@Getter
@Setter
public class TripDto {
    private int no;
    private String contentId;
    private String title;
    private String contentTypeId;
    private String contentTypeName;
    private String areaCode;
    private String sidoName;
    private String siGunGuCode;
    private String gugunName;
    private String firstImage1;
    private String firstImage2;
    private String latitude;
    private String longitude;
    private String tel;
    private String addr1;
    private String addr2;
    private String homepage;
    private String overview;

}