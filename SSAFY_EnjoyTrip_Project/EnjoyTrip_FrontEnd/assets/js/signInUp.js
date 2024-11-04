
// 회원가입 or 로그인 중 어떤 걸 선택할지 고르기
const signInSelectBtn = document.getElementById("signIn");
const signUpSelectBtn = document.getElementById("signUp");
const container = document.querySelector(".container");

signInSelectBtn.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

signUpSelectBtn.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

// form1 : sign up (회원가입) 시도
const signUpBtn = document.getElementById("signUpBtn");
signUpBtn.addEventListener("click", () => {
  // 입력받은 필드들 가져오기
  const id = document.getElementById("id").value;
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const passwordCheck = document.getElementById("passwordCheck").value;
  const birthDate = document.getElementById("birthDate").value;

  // 오늘 날짜 "YYYY-MM-DD" 형식으로 가져오기
  const today = new Date();
  const formattedToday = today.toISOString().split("T")[0];
  console.log("formattedToday : " + formattedToday);

  // 유효성 검사하기
  if (password.length < 8 || password.length > 16) {
    alert("비밀번호는 8~16자를 입력해주세요");
    return;
  }
  if (passwordCheck !== password) {
    alert("비밀번호 확인 값과 실제 비밀번호가 일치하지 않습니다.\n\n" +
      "비밀번호를 제대로 기억하고 확인값도 동일하게 기입해주세요.");
    return;
  }
  if (birthDate === "" || birthDate > formattedToday) {
    alert("유효하지 않은 생일 날짜입니다.\n오늘 날짜 이전의 날짜를 선택해주세요.");
    return;
  }

  // 로컬 스토리지에서 사용자 정보 모두 가져오기
  let users = JSON.parse(localStorage.getItem("users")) || [];

  // 기존의 것들과 중복 검사하기
  for (let i = 0; i < users.length; i++) {
    let user = users[i];

    if (user.id === id) {
      alert("이미 존재하는 아이디입니다.\n\n" +
        "다른 아이디로 회원가입 시도해주세요.");
      return;
    }
    if (user.email === email) {
      alert("이미 존재하는 이메일입니다.\n\n" +
        "해당 이메일로 로그인하시거나, 다른 이메일로 회원가입 시도해주세요.");
      return;
    }
  }

  // 유효성 검증과 중복 검사를 모두 통과했다면
  // 사용자 객체 생성하기
  const user = {
    id: id,
    name: name,
    email: email,
    password: password,
    birthDate: birthDate
  };
  
  // 로컬 스토리지에 저장
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users)); // JSON 형식 문자열로 저장

  // 알림창으로 성공 여부 알려주기
  alert("회원가입을 완료하였습니다 축하드립니다 ㅎㅎㅎ");
});

// form2 : sign in (로그인) 시도
const signInBtn = document.getElementById("signInBtn");
signInBtn.addEventListener("click", () => {
  const id = document.getElementById("signInId").value;
  const password = document.getElementById("signInPwd").value;

  // 로컬 스토리지에서 사용자 정보 모두 가져오기
  let users = JSON.parse(localStorage.getItem("users")) || [];

  let loginSuccess = false;
  let loginUser = "";

  // 기존의 것들과 일치하는 값 있는지 조회하기
  for (let i = 0; i < users.length; i++) {
    let user = users[i];

    if (user.id === id) {
      if (user.password === password) {
        loginSuccess = true;
        loginUser = user;
        break;
      } else {        
        alert("로그인 실패..\n\n비밀번호가 틀렸습니다!\n\n" +
          "다시 로그인 시도해주시거나 비밀번호 변경바랍니다");
        return;
      }
    }
  }

  // 로그인 성공 여부에 따라 다르게 처리
  // 로그인 성공시 : 로컬 스토리지에 현재 로그인 유저 정보 저장 및 로그아웃 보이기
  // 로그인 실패시 : 알림창 띄우고 끝내기
  if (loginSuccess) {
    localStorage.setItem("loginUser", JSON.stringify(loginUser)); // 로그인 유저 정보 로컬 스토리지에 저장
    window.location.href = "index.html"; // index.html로 이동
    // updateHeader(); // 로그인 가리고 로그아웃 보이게 처리
  } else {
    alert("로그인 실패..\n\n존재하지 않는 아이디입니다!\n\n" +
      "아이디 찾기하시거나 회원이 아니시라면\n회원가입 해주시기 바랍니다!");
  }
});