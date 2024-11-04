let serviceKey = "n6pLAD%2Be8bzvU2y2jUSk7zyhIKPSG5BPkQrIRDiTTLdJHQRtcIF0ycAtpUgS%2FtIwu%2BjpGVdf%2BT3qz2IT8kjKeg%3D%3D";
let areaUrl = "https://apis.data.go.kr/B551011/KorService1/areaCode1?serviceKey=" + serviceKey + "&numOfRows=20&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json";
let sigunguUrlBase = "https://apis.data.go.kr/B551011/KorService1/areaCode1?serviceKey=" + serviceKey + "&MobileOS=ETC&MobileApp=AppTest&_type=json";

// 전국 시도 정보를 로드하여 search-area 드롭다운에 추가
fetch(areaUrl, { method: "GET" })
    .then((response) => response.json())
    .then((data) => makeOption(data, "search-area"));

function makeOption(data, elementId) {
    let items = data.response.body.items.item;
    let sel = document.getElementById(elementId);
    items.forEach((item) => {
        let opt = document.createElement("option");
        opt.setAttribute("value", item.code);
        opt.appendChild(document.createTextNode(item.name));
        sel.appendChild(opt);
    });
}

// 시도를 선택하면 해당 시도의 시군구를 로드하여 search-sigungu 드롭다운에 추가
document.getElementById("search-area").addEventListener("change", function() {
    let areaCode = this.value;
    let sigunguUrl = sigunguUrlBase + "&areaCode=" + areaCode;

    // 시군구 선택 초기화
    let sigunguSelect = document.getElementById("search-sigungu");
    sigunguSelect.innerHTML = '<option value="">시군구 선택</option>';

    // 시군구 데이터를 가져와서 드롭다운 업데이트
    fetch(sigunguUrl, { method: "GET" })
        .then((response) => response.json())
        .then((data) => makeOption(data, "search-sigungu"));
});

// 검색 버튼 클릭 시 URL 생성 및 데이터 가져오기
document.getElementById("btn-search").addEventListener("click", () => {
    let baseUrl = `https://apis.data.go.kr/B551011/KorService1/`;
    let queryString = `serviceKey=${serviceKey}&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=A`;

    let areaCode = document.getElementById("search-area").value;
    let sigunguCode = document.getElementById("search-sigungu").value;
    let contentTypeId = document.getElementById("search-content-id").value;

    if (parseInt(areaCode)) queryString += `&areaCode=${areaCode}`;
    if (parseInt(sigunguCode)) queryString += `&sigunguCode=${sigunguCode}`;
    if (parseInt(contentTypeId)) queryString += `&contentTypeId=${contentTypeId}`;

    service = `areaBasedList1`;

    let searchUrl = baseUrl + service + "?" + queryString;

    console.log(searchUrl);

    fetch(searchUrl)
        .then((response) => response.json())
        .then((data) => makeList(data));
});

var positions; // marker 배열
function makeList(data) {
    console.log(data);
    const resultsTable = document.getElementById("trip-list");
    const tripListContainer = resultsTable.getElementsByTagName('tbody')[0];

    // 이전 검색 결과 초기화
    tripListContainer.innerHTML = '';

    const trips = data.response.body.items.item;

    // 검색 결과가 없는 경우
    if (!trips || trips.length === 0) {
        alert("No results found for your search.");
        resultsTable.style.display = "none"; // 결과가 없을 때는 테이블 숨기기
        return;
    }

    resultsTable.style.display = ""; // 결과가 있을 때는 테이블 표시
    positions = [];

    trips.forEach((area) => {
        let tripList = `
            <tr onclick="moveCenter(${area.mapy}, ${area.mapx});">
                <td><img src="${area.firstimage}" width="100px"></td>
                <td>${area.title}</td>
                <td>${area.addr1} ${area.addr2}</td>
                <td>${area.mapy}</td>
                <td>${area.mapx}</td>
            </tr>
        `;
        
        tripListContainer.innerHTML += tripList;
        
            // 마커 정보를 저장 (카카오맵 예시를 따름)
            // let markerInfo = {
            //     title: area.title,
            //     latlng: new kakao.maps.LatLng(area.mapy, area.mapx),
            // };
            // positions.push(markerInfo);
        });

        // displayMarker(); // 마커를 표시하는 함수 (생략된 부분)
}