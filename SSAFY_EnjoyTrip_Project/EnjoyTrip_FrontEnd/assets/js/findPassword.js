const findPwdBtn = document.getElementById("findPwd");
findPwdBtn.addEventListener("click", () => {
	const id = document.getElementById("id").value;
	const name = document.getElementById("name").value;
	const email = document.getElementById("email").value;

	// 로컬 스토리지에 아이디로 회원 정보를 찾고, 같은 아이디가 존재한다면
	// 이름과 이메일도 동일한지 검증 후
	// 성공 여부에 따라 다르게 처리
  // 검증 성공시 : 알림창으로 비번 띄워주기 (이메일 보내는 법을 모름)
	// 검증 실패시 : 알림창으로 회원 정보가 틀려서 찾을 수 없다 띄워주기
    
	// 로컬 스토리지에서 사용자 정보 모두 가져오기
	let users = JSON.parse(localStorage.getItem("users")) || [];

	let findIdSuccess = false;
	let userPassword = "";

	// 기존의 것들과 일치하는 값 있는지 조회하기
	for (let i = 0; i < users.length; i++) {
		let user = users[i];
		if (user.id === id) {
			if (user.name === name && user.email === email) {
				findIdSuccess = true;
				userPassword = user.password;
			} else {
				alert("비밀번호 찾기 실패..\n\n이름 또는 이메일이 다릅니다!\n\n" +
					"다른 이름 또는 이메일로 다시 비밀번호 찾기 시도해주세요.");
				return;
			}
		}
	}

	if (findIdSuccess) {
		alert("비밀번호 찾기 성공!\n\n비밀번호는 " + userPassword + " 입니다.\n\n" +
			"이메일로 보내기 지원은 앞으로 제공될 예정입니다.\n" +
			"너그러운 양해 부탁드립니다!");
  } else {
    alert("비밀번호 찾기 실패..\n\n존재하지 않는 아이디입니다!\n\n" +
			"아이디 찾기부터 하시거나\n회원이 아니시라면\n회원가입 해주시기 바랍니다!");
  }
});