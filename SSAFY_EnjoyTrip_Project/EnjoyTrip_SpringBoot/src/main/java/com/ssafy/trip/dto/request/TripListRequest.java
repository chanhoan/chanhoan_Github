package com.ssafy.trip.dto.request;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TripListRequest {
	private int pgno = 1;
	private String code;
	private String type;
	private String name;
}
