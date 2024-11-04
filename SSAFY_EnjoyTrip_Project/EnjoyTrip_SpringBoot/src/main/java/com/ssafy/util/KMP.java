package com.ssafy.util;
public class KMP {

    // 패턴에 대한 LPS 배열 생성 (접두사 접미사 테이블)
    public static int[] buildLPS(String pattern) {
        int[] lps = new int[pattern.length()];
        int j = 0;  // 접두사 길이
        for (int i = 1; i < pattern.length(); ) {
            if (pattern.charAt(i) == pattern.charAt(j)) {
                j++;
                lps[i] = j;
                i++;
            } else {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    // KMP 알고리즘을 사용하여 텍스트에서 패턴을 검색
    public static boolean kmpSearch(String text, String pattern) {
        int[] lps = buildLPS(pattern);
        int i = 0, j = 0;  // i는 텍스트 인덱스, j는 패턴 인덱스

        while (i < text.length()) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            if (j == pattern.length()) {
                return true;  // 패턴이 텍스트 내에 존재
            } else if (i < text.length() && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return false;  // 패턴이 텍스트 내에 존재하지 않음
    }
}
