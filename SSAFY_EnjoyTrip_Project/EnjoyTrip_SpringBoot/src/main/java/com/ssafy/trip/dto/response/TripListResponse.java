package com.ssafy.trip.dto.response;

import java.util.List;

import com.ssafy.trip.model.TripDto;
import com.ssafy.util.PageNavigation;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class TripListResponse {
	private List<TripDto> tripList;
	private List<TripDto> sidoList;
	private List<TripDto> contentTypeList;
	private PageNavigation pageNavigation;
}
