<instruction>
{city}의 관광지를 기반으로 여행 코스를 작성해줘.
0. 한번에 10개의 데이터를 가져와줘. 무조건 10개야. 적게 가져오지마
1. 관광지 : name,
2. 관광타입 : contentTypeId로 하고 값의 경우 (12:관광지, 14:문화시설, 15:축제공연행사, 25:여행코스, 28:레포츠, 32:숙박, 38:쇼핑, 39:음식점) 예시의 숫자로 해줘
3. 관련 이미지를 검색하여 대표 이미지의 실제 url도 넣어 주면 좋을거 같아 : imageUrl.
4. 주소 : address
5. 관광지 위치의 위도 : latitude, 경도 : longitude
6. 관광지의 중심좌표의 위도 : centerLatitude, 경도 : centerLongitude
7. 정확한 json 파일 형식만 답변 부탁해(```json 제외).


</instruction>
<example>
\{
    "plans": [
        \{
            "centerLatitude" : 35.2587,
            "centerLongitude": 129.1614,
            "attractions": [
                \{
                    "name": "해운대 해수욕장",
                    "contentTypeId": 12,
                    "imageUrl": "https://example.com/image_haeundae.jpg",
                    "address": "부산광역시 해운대구 해운대해변로 264",
                    "latitude": 35.1587,
                    "longitude": 129.1604
                \},
                \{
                    "name": "해운대 미포철길",
                    "contentTypeId": 25,
                    "imageUrl": "https://example.com/image_mipo.jpg",
                    "address": "부산광역시 해운대구 중동 804",
                    "latitude": 35.1614,
                    "longitude": 129.1707
                \},
                \{
                    "name": "동백섬 누리마루 APEC 하우스",
                    "contentTypeId": 12,
                    "imageUrl": "https://example.com/image_apec.jpg",
                    "address": "부산광역시 해운대구 동백로 116",
                    "latitude": 35.1532,
                    "longitude": 129.1451
                \},
                \{
                    "name": "해운대 암소갈비",
                    "contentTypeId": 39,
                    "imageUrl": "https://example.com/image_amsogalbi.jpg",
                    "address": "부산광역시 해운대구 구남로 32",
                    "latitude": 35.1636,
                    "longitude": 129.1628
                \},
                \{
                    "name": "파라다이스 호텔 부산",
                    "contentTypeId": 32,
                    "imageUrl": "https://example.com/image_paradise.jpg",
                    "address": "부산광역시 해운대구 해운대해변로 296",
                    "latitude": 35.1595,
                    "longitude": 129.1631
                \}
            ]
        \}
    ]
\}
</example>