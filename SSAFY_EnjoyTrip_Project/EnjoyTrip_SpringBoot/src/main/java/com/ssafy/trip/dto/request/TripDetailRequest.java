package com.ssafy.trip.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TripDetailRequest {
	@NotBlank
	private String code;
}
