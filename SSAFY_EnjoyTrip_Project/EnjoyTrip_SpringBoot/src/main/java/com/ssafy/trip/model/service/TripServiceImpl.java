package com.ssafy.trip.model.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ssafy.trip.dto.request.TripListRequest;
import com.ssafy.trip.model.TripDto;
import com.ssafy.trip.model.mapper.TripMapper;
import com.ssafy.util.BoardSize;
import com.ssafy.util.PageNavigation;
import com.ssafy.util.Trie;

@Service
public class TripServiceImpl implements TripService {

    private TripMapper tripMapper;
    
    @Autowired
    public TripServiceImpl(TripMapper tripMapper) {
    	this.tripMapper = tripMapper;
    }

    @Override
    public List<TripDto> searchListAreaInfo() {
        return tripMapper.selectListAreaInfo();
    }

    @Override
    public List<TripDto> searchTripList(TripListRequest tripListRequest){
    	return tripMapper.selectTripList(tripListRequest);
    }

    @Override
    public List<TripDto> searchListContentType() {
        return tripMapper.selectListContentType();
    }

    @Override
    public TripDto viewTrip(int no) {
        return tripMapper.selectTrip(no);
    }

    @Override
	public PageNavigation makePageNavigation(Map<String, String> map) throws Exception {
		PageNavigation pageNavigation = new PageNavigation();

		int listSize = BoardSize.LIST.getBoardSize();
		int navigationSize = BoardSize.NAVIGATION.getBoardSize();
		int currentPage = Integer.parseInt(map.get("pgno"));

		pageNavigation.setCurrentPage(currentPage);
		pageNavigation.setNaviSize(navigationSize);

		// Prepare parameters for querying
		Map<String, Object> param = new HashMap<>();
		String code = map.get("code");
		String type = map.get("type");
		String name = map.get("name");

		param.put("code", code);
		param.put("type", type);
		param.put("name", name);

		int totalCount = tripMapper.getTotalTripCount(param);
		pageNavigation.setTotalCount(totalCount);

		int totalPageCount = (totalCount - 1) / listSize + 1;
		pageNavigation.setTotalPageCount(totalPageCount);

		boolean startRange = currentPage <= navigationSize;
		pageNavigation.setStartRange(startRange);

		boolean endRange = (totalPageCount - 1) / navigationSize * navigationSize < currentPage;
		pageNavigation.setEndRange(endRange);

		pageNavigation.makeNavigator();

		return pageNavigation;

	}

	private Trie trie;

	@Override
	public List<String> getTrieList(Map<String, Object> map) {
		trie = new Trie();

		// map에서 keyword와
		String keyword = (String) map.get("name");

		// DB에서 해당하는 관광지 리스트를 가져옴
		List<String> attractions = tripMapper.selectListTripKeyword(map);

		// Trie에 모든 관광지 추가
		for (String attraction : attractions) {
			trie.insert(attraction.toLowerCase());
		}

		List<String> results = new ArrayList<>();
		List<String> tempResults = trie.searchByPrefix(keyword.toLowerCase());
		System.out.println("검색 결과 : " + tempResults.size());
		Collections.shuffle(tempResults);
		if (tempResults.size() > 10)
			results = tempResults.subList(0, 10);
		else
			results = tempResults;
		for(int i=0; i<results.size(); i++) {
			System.out.println(results.get(i));
		}
		return results;
	}

	@Override
	public List<TripDto> getNearTrip(String latitude, String longitude) {
	    List<TripDto> list = tripMapper.selectNearTrip(latitude, longitude);
	    System.out.println(list.size());

	    
	    Double curLatitude = Double.parseDouble(latitude);
	    Double curLongitude = Double.parseDouble(longitude);
	    System.out.println("curLat : " + curLatitude + ", curLng : "+ curLongitude);
	    

	    // 4개 미만이면 그대로 반환
	    if (list.size() < 4) {
	        return list;
	    }

	    // 거리 계산하여 정렬하기 위한 리스트 생성
	    List<TripDistance> attractionDistances = new ArrayList<>();
	    for (TripDto tripDto : list) {
	    	if(tripDto.getLatitude().equals(latitude) && tripDto.getLongitude().equals(longitude)){
	    		continue;
	    	}
	    	
	    	System.out.println(Double.parseDouble(tripDto.getLatitude()));
	    	System.out.println(Double.parseDouble(tripDto.getLongitude()));
	        double distance = calculateDistance(curLatitude, curLongitude, 
	            Double.parseDouble(tripDto.getLatitude()), 
	            Double.parseDouble(tripDto.getLongitude()));
	        attractionDistances.add(new TripDistance(tripDto, distance));
	    }

	    // 거리 기준으로 정렬
	    attractionDistances.sort(Comparator.comparingDouble(TripDistance::getDistance));

	    // 상위 4개 Attraction 추출
	    List<TripDto> result = new ArrayList<>();
	    for (int i = 0; i < 4; i++) {
	        result.add(attractionDistances.get(i).getTrip());
	    }

	    return result;
	}

	// 거리 계산 메서드
	private double calculateDistance(double lat1, double lon1, double lat2, double lon2) {
	    final int R = 6371; // 지구 반지름 (km)
	    double latDistance = Math.toRadians(lat2 - lat1);
	    double lonDistance = Math.toRadians(lon2 - lon1);
	    double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2) +
	               Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
	               Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
	    double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
	    return R * c; // 반환 단위: km
	}

	// Attraction과 거리 정보를 담는 클래스
	private static class TripDistance {
	    private TripDto tripDto;
	    private double distance;

	    public TripDistance(TripDto tripDto, double distance) {
	        this.tripDto = tripDto;
	        this.distance = distance;
	    }

	    public TripDto getTrip() {
	        return tripDto;
	    }

	    public double getDistance() {
	        return distance;
	    }
	}

	@Override
	public List<TripDto> findOptimalPath(int startNo, List<Integer> waypointNos, int endNo) throws Exception {
		// 출발지 + 경유지 + 도착지
        List<Integer> allPoints = new ArrayList<>();
        allPoints.add(startNo);
        if (waypointNos != null) {
            allPoints.addAll(waypointNos);
        }
        allPoints.add(endNo);

        int n = allPoints.size(); // 경유지를 포함한 전체 정점의 개수
        double[][] dist = new double[n][n]; // 모든 정점 간의 최단 거리 저장 배열

        // 모든 정점 간의 최단 거리 계산 (다익스트라 또는 플로이드-와샬)
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                dist[i][j] = dist[j][i] = haversine(
                        Double.parseDouble(tripMapper.selectTrip(allPoints.get(i)).getLatitude()),
                        Double.parseDouble(tripMapper.selectTrip(allPoints.get(i)).getLongitude()),
                        Double.parseDouble(tripMapper.selectTrip(allPoints.get(j)).getLatitude()),
                        Double.parseDouble(tripMapper.selectTrip(allPoints.get(j)).getLongitude()));
            }
        }

        // DP + 비트마스킹으로 외판원 문제 해결
        double[][] dp = new double[n][(1 << n)]; // DP 배열: [현재 위치][방문 상태]
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < (1 << n); j++) {
                dp[i][j] = Double.MAX_VALUE; // 초기화: 무한대로 설정
            }
        }
        
        // DP 초기화: 출발지에서 시작
        dp[0][1] = 0;

        // 외판원 문제 해결 (DP + 비트마스킹)
        for (int visited = 1; visited < (1 << n); visited++) {
            for (int current = 0; current < n; current++) {
                if ((visited & (1 << current)) == 0) continue; // 현재 지점이 방문된 경우만 처리
                for (int next = 0; next < n; next++) {
                    if ((visited & (1 << next)) != 0) continue; // 이미 방문한 지점은 제외
                    dp[next][visited | (1 << next)] = Math.min(dp[next][visited | (1 << next)], 
                            dp[current][visited] + dist[current][next]);
                }
            }
        }

        // 마지막 도착지로 돌아가는 경로 추적
        double minDist = Double.MAX_VALUE;
        int finalState = (1 << n) - 1; // 모든 지점을 방문한 상태
        for (int i = 0; i < n; i++) {
            minDist = Math.min(minDist, dp[i][finalState] + dist[i][n-1]);
        }

        // 최적 경로를 역추적하여 반환
        return reconstructPath(dp, dist, allPoints);
	}
	
	private List<TripDto> reconstructPath(double[][] dp, double[][] dist, List<Integer> allPoints) throws Exception {
        int n = allPoints.size();
        List<Integer> path = new ArrayList<>();

        int finalState = (1 << n) - 1; // 모든 지점을 방문한 상태
        int current = 0; // 시작 지점에서부터 시작 (allPoints의 0번째)

        // 출발지는 이미 추가된 상태로 시작
        path.add(allPoints.get(0));

        // 방문한 상태에서 최적 경로를 역추적
        while (finalState != 0) {
            int next = -1;
            for (int i = 0; i < n; i++) {
                if ((finalState & (1 << i)) == 0 || current == i) continue; // 방문하지 않은 지점만 처리
                if (next == -1 || dp[i][finalState] + dist[i][current] < dp[next][finalState] + dist[next][current]) {
                    next = i;
                }
            }

            // 방문한 상태 갱신
            finalState &= ~(1 << next); // 현재 지점을 방문 처리
            current = next; // 다음 지점으로 이동
            if (!path.contains(allPoints.get(current))) { // 경로에 중복 추가 방지
                path.add(allPoints.get(current)); // 경로에 추가
            }
        }

        // 경로의 마지막이 도착지점이 아닐 경우 도착지점을 추가
        if (path.get(path.size() - 1) != allPoints.get(n - 1)) {
            path.add(allPoints.get(n - 1));
        }

        // AttractionDTO로 경로를 변환하여 반환
        List<TripDto> attractionPath = new ArrayList<>();
        for (int contentId : path) {
        	TripDto attraction = tripMapper.selectTrip(contentId);
            if (attraction != null) {
                attractionPath.add(attraction);
            }
        }

        return attractionPath;
    }
	
    private double haversine(double lat1, double lon1, double lat2, double lon2) {
        final int R = 6371; // 지구 반지름 (킬로미터)
        double latDistance = Math.toRadians(lat2 - lat1);
        double lonDistance = Math.toRadians(lon2 - lon1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                        * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = R * c;
        return distance;
    }
}
