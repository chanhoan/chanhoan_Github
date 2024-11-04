// key.js에서 변수 가져오기
import { serviceKey } from "./key";

// index page 로딩 후 전국의 시도 설정.
let areaUrl =
"https://apis.data.go.kr/B551011/KorService1/areaCode1?serviceKey=" +
serviceKey +
"&numOfRows=20&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json";
let sigunguUrlBase =
"https://apis.data.go.kr/B551011/KorService1/areaCode1?serviceKey=" +
serviceKey +
"&MobileOS=ETC&MobileApp=AppTest&_type=json";

fetch(areaUrl, { method: "GET" })
.then((response) => response.json())
.then((data) => makeOption(data, "search-area"));

function makeOption(data, selectId) {
let areas = data.response.body.items.item;
let sel = document.getElementById(selectId); // 시도 or 구군
console.log("areas :" + areas);
console.log("sel :" + sel);

areas.forEach((area) => {
  let opt = document.createElement("option");
  opt.setAttribute("value", area.code);
  opt.appendChild(document.createTextNode(area.name));
  sel.appendChild(opt);
});
}

// 시도 변경 시 구군 정보를 불러옵니다.
document.getElementById("search-area").addEventListener("change", function () {
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

// 검색 버튼을 누르면..
// 지역, 유형, 검색어 얻기.
// 위 데이터를 가지고 공공데이터에 요청.
// 받은 데이터를 이용하여 화면 구성.

document.getElementById("btn-search").addEventListener("click", () => {
let baseUrl = `https://apis.data.go.kr/B551011/KorService1/`;
let queryString = `serviceKey=${serviceKey}&numOfRows=50&pageNo=1&MobileOS=ETC&MobileApp=AppTest&_type=json&listYN=Y&arrange=A`;

let areaCode = document.getElementById("search-area").value;
let sigunguCode = document.getElementById("search-sigungu").value;
let contentTypeId = document.getElementById("search-content-id").value;

if (parseInt(areaCode)) queryString += `&areaCode=${areaCode}`;
if (parseInt(sigunguCode)) queryString += `&sigunguCode=${sigunguCode}`;
if (parseInt(contentTypeId)) queryString += `&contentTypeId=${contentTypeId}`;

service = `areaBasedList1`;

let searchUrl = baseUrl + service + "?" + queryString;

fetch(searchUrl)
  .then((response) => response.json())
  .then((data) => makeList(data));
});

const itemsPerPage = 5;
let totalItems = 0;
let currentPage = 1;
let totalPages = 0;
let allTrips = [];

// Total items count and pagination logic
function updatePagination(paginationId) {
const totalCountElement = document.getElementById("total-count");
const paginationElement = document.getElementById(paginationId);

// Clear pagination
paginationElement.innerHTML = "";

// Create pagination buttons
const createPageButton = (pageNum, text) => {
  const li = document.createElement("li");
  li.classList.add("page-item");
  if (pageNum === currentPage) li.classList.add("active");
  const a = document.createElement("a");
  a.classList.add("page-link");
  a.href = "#";

  if (paginationId === "pagination-top") {
    totalCountElement.textContent = `총 ${totalItems}개`;
    a.textContent = text;
  }

  a.addEventListener("click", (e) => {
    e.preventDefault();
    currentPage = pageNum;
    renderTable();
    updatePagination("pagination-top");
    updatePagination("pagination-bottom");
  });
  li.appendChild(a);
  return li;
};

if (totalPages > 1) {
  // Previous button
  if (currentPage > 1) {
    paginationElement.appendChild(createPageButton(currentPage - 1, "«"));
  }

  // Page buttons
  if (paginationId === "pagination-top") {
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
      paginationElement.appendChild(createPageButton(i, i));
    }
  } else {
    for (let i = 1; i <= totalPages; i++) {
      paginationElement.appendChild(createPageButton(i, i));
    }
  }

  // Next button
  if (currentPage < totalPages) {
    paginationElement.appendChild(createPageButton(currentPage + 1, "»"));
  }
}
}

function renderTable() {
const tripListElement = document.getElementById("trip-list");
tripListElement.innerHTML = "";

const startIndex = (currentPage - 1) * itemsPerPage;
const endIndex = Math.min(startIndex + itemsPerPage, allTrips.length);

for (let i = startIndex; i < endIndex; i++) {
  const trip = allTrips[i];
  tripListElement.innerHTML += `
    <tr onclick="moveCenter(${trip.mapy}, ${trip.mapx});">
      <td><img src="${trip.firstimage}" width="100px"></td>
      <td>${trip.title}</td>
      <td>${trip.addr1} ${trip.addr2}</td>
    </tr>
  `;
}
}
var positions; // marker 배열.
function makeList(data) {
console.log(data);
document.querySelector("table").setAttribute("style", "display: ;");

allTrips = data.response.body.items.item;
totalItems = allTrips.length;
totalPages = Math.ceil(totalItems / itemsPerPage);

document.querySelector("table").style.display = "table";
renderTable();
updatePagination("pagination-top");
updatePagination("pagination-bottom");

// let trips = data.response.body.items.item;
// let tripList = ``;
// positions = [];

// trips.forEach((area) => {
//   tripList += `
//     <tr onclick="moveCenter(${area.mapy}, ${area.mapx});">
//       <td><img src="${area.firstimage}" width="100px"></td>
//       <td>${area.title}</td>
//       <td>${area.addr1} ${area.addr2}</td>
//     </tr>
//   `;

//   let markerInfo = {
//     title: area.title,
//     latlng: new kakao.maps.LatLng(area.mapy, area.mapx),
//   };
//   positions.push(markerInfo);
// });

// document.getElementById("trip-list").innerHTML = tripList;
// displayMarker();
}