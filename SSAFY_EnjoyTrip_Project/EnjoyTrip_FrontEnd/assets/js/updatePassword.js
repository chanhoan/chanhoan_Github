document.addEventListener("DOMContentLoaded", () => {
  // 로컬 스토리지에서 현재 로그인한 사용자 정보를 가져옴
  let loginUser = JSON.parse(localStorage.getItem("loginUser"));

  // 비밀번호 필드에 현재 사용자의 비밀번호를 설정
  if (loginUser && loginUser.password) {
    let curPassword = document.getElementById("curPassword");
    curPassword.setAttribute("value", loginUser.password);
  }
});

const updatePwd = document.getElementById("updatePwd");
updatePwd.addEventListener("click", () => {
  const curPassword = document.getElementById("curPassword").value;
  const toChangePassword = document.getElementById("toChangePassword").value;
  const toChangePasswordCheck = document.getElementById("toChangePasswordCheck").value;

  if (curPassword === toChangePassword) {
    alert("최근에 사용한 비밀번호와 동일한 값입니다.\n\n" +
      "다른 비밀번호를 입력해서 보안을 향상시켜보세요.");
  }
  if (toChangePassword.length < 8 || toChangePassword.length > 16) {
    alert("비밀번호는 8~16자를 입력해주세요");
    return;
  }
  if (toChangePasswordCheck !== toChangePassword) {
    alert("비밀번호 확인 값과 실제 비밀번호가 일치하지 않습니다.\n\n" +
      "비밀번호를 제대로 기억하고 확인값도 동일하게 기입해주세요.");
    return;
  }

  // 유효성 검사 다 통과했다면 변경해주기
  // 로컬 스토리지의 로그인 유저, users
  let loginUser = JSON.parse(localStorage.getItem("loginUser"));
  loginUser.password = toChangePassword;

  let users = JSON.parse(localStorage.getItem("users")) || [];

  for (let i = 0; i < users.length; i++) {
    let user = users[i];

    if (user.id === loginUser.id) {
      users[i] = loginUser;
      break;
    }
  }

  localStorage.setItem("loginUser", JSON.stringify(loginUser));
  localStorage.setItem("users", JSON.stringify(users));
  window.location.href = "my_profile.html";
});