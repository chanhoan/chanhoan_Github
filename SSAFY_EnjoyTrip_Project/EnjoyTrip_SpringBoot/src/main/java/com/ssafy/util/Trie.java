package com.ssafy.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEndOfWord = false;
}

public class Trie {
    private final TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    // Trie에 단어 삽입
    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
        }
        node.isEndOfWord = true;
    }

    // 주어진 prefix로 시작하는 모든 단어 반환
    public List<String> searchByPrefix(String prefix) {
        List<String> results = new ArrayList<>();
        TrieNode node = root;
        
        for (char c : prefix.toCharArray()) {
            if (!node.children.containsKey(c)) {
                return results; // prefix가 없는 경우 빈 리스트 반환
            }
            node = node.children.get(c);
        }
        
        // prefix로 시작하는 모든 단어 찾기
        searchPrefix(node, new StringBuilder(prefix), results);
        return results;
    }

    // 재귀적으로 주어진 노드에서 모든 접미사 찾기
    private void searchPrefix(TrieNode node, StringBuilder prefix, List<String> results) {
        if (node.isEndOfWord) {
            results.add(prefix.toString());
        }
        for (char c : node.children.keySet()) {
            searchPrefix(node.children.get(c), prefix.append(c), results);
            prefix.deleteCharAt(prefix.length() - 1); // 문자열 롤백
        }
    }
}
