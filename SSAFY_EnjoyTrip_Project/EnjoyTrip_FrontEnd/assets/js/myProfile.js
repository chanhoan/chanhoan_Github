document.addEventListener("DOMContentLoaded", () => {
  // 로컬 스토리지에서 현재 로그인한 사용자 정보를 가져옴
  let loginUser = JSON.parse(localStorage.getItem("loginUser"));

  // 비밀번호 필드에 현재 사용자의 비밀번호를 설정
  if (loginUser && loginUser.id) {
    let id = document.getElementById("id");
    let name = document.getElementById("name");
    let email = document.getElementById("email");
    let birthDate = document.getElementById("birthDate");

    id.setAttribute("value", loginUser.id);
    name.setAttribute("value", loginUser.name);
    email.setAttribute("value", loginUser.email);
    birthDate.setAttribute("value", loginUser.birthDate);
  }
});

const updateBtn = document.getElementById("updateBtn");
updateBtn.addEventListener("click", () => {
  // 새로 입력받았거나 그대로인 필드들 전체 가져오기
  const id = document.getElementById("id").value;
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const birthDate = document.getElementById("birthDate").value;

  // 오늘 날짜 "YYYY-MM-DD" 형식으로 가져오기
  const today = new Date();
  const formattedToday = today.toISOString().split("T")[0];
  console.log("formattedToday : " + formattedToday);

  // 유효성 검사하기
  if (birthDate === "" || birthDate > formattedToday) {
    alert("유효하지 않은 생일 날짜입니다.\n오늘 날짜 이전의 날짜를 선택해주세요.");
    return;
  } 

  // 로컬 스토리지에서 사용자 정보 모두 가져오기
  let users = JSON.parse(localStorage.getItem("users")) || [];

  // 로컬 스토리지에서 현재 로그인한 사용자 아이디 가져오기
  const loginUser = JSON.parse(localStorage.getItem("loginUser"));

  // 기존의 것들과 중복 검사하기 (나 제외)
  for (let i = 0; i < users.length; i++) {
    let user = users[i];

    if (user.id !== loginUser.id && user.email === email) {
      alert("이미 존재하는 이메일입니다.\n\n" +
        "해당 이메일로 로그인하시거나, 다른 이메일로 회원가입 시도해주세요.");
      return;
    }
    // 유효성 검사 중복 검사 다 통과했다면
    if (user.id === loginUser.id) {
      // 해당 사용자 정보 수정 후
      // 로컬스토리지에서 받은 users에 수정된 loginUser로 교체해주기
      // loginUser = user;
      loginUser.name = name;
      loginUser.email = email;
      loginUser.birthDate = birthDate;
      users[i] = loginUser;
      break;
    }
  }

  // 로컬 스토리지에 다시 반영해주기
  localStorage.setItem("users", JSON.stringify(users));
  localStorage.setItem("loginUser", JSON.stringify(loginUser));

  // 회원 정보 수정 성공 알림창 띄우기
  alert("회원 정보가 성공적으로 수정되었습니다.");
});


const deleteBtn = document.getElementById("deleteBtn");
deleteBtn.addEventListener("click", () => {
  // 정말 탈퇴하시겠습니까? confirm 창 띄우기
  const confirmDelete = confirm("정말 탈퇴하시겠습니까?");

  // 확인 누르면 아래 실행
  if (confirmDelete) {
    let loginUser = JSON.parse(localStorage.getItem("loginUser"));

    let users = JSON.parse(localStorage.getItem("users")) || [];
    let newUsers = [];

    for (let i = 0; i < users.length; i++) {
      let user = users[i];
      if (user.id === loginUser.id) {
        // 배열이라 삭제 반영하기 어렵다고 판단
        users[i] = null;
        break;
      }
      // 새로운 배열에 삭제할 거 제외하고 새로 담기
      newUsers.push(user);
    }
    localStorage.setItem("users", JSON.stringify(newUsers)); // 새로운 배열로 교체
    localStorage.removeItem("loginUser");

    alert("회원 탈퇴가 완료되었습니다.");

    window.location.href = "index.html";
  }
});