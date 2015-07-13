package com.dictionary.search;

import java.sql.SQLException;
import java.util.ArrayList;

public class Main {
	public static void main(String[] args) {
		Searcher srearcher = new Searcher();
		String src = "d;stanc,e";
		ArrayList<Word> strings = new ArrayList<Word>();
		try {
			strings = srearcher.searchWords(src);
			for (Word w : strings) {
				System.out.println(w.from_word + ":" + w.to_word);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}
}
