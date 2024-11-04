package com.ssafy.trip.dto.response;

import java.util.List;

import com.ssafy.trip.model.TripDto;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class TripDetailResponse {
	private TripDto trip;
	private List<TripDto> nearTripList;

}
