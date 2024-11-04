package com.ssafy.trip.dto.request;

import java.util.List;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RecommandPathRequest {
	@NotBlank
	private String startId;
	@NotBlank 
	private String endId;
	@NotNull
	private List<String> waypointIds;
}
