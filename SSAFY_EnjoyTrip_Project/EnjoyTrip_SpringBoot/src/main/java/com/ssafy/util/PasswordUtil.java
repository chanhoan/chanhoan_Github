package com.ssafy.util;

import org.mindrot.jbcrypt.BCrypt;

public class PasswordUtil {

    // 비밀번호를 bcrypt 해시로 변환하는 함수
    public static String hashPassword(String plainPassword) {
        // 해시 생성 (12는 강도값으로, 값이 클수록 계산이 느려짐)
        return BCrypt.hashpw(plainPassword, BCrypt.gensalt());
    }

    // 사용자가 입력한 비밀번호와 저장된 해시값을 비교하는 함수
    public static boolean checkPassword(String plainPassword, String hashedPassword) {
        // 입력된 비밀번호와 저장된 해시된 비밀번호가 일치하는지 확인
        return BCrypt.checkpw(plainPassword, hashedPassword);
    }
}
