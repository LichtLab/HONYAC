package edu.sfsu.cs.orange.ocr.language;

import java.sql.SQLException;
import java.util.ArrayList;

import com.dictionary.search.Searcher;
import com.dictionary.search.Word;

public class TranslatorLocal {

	static public String translate(String fromLanguage, String toLanguage, String text) {
		
		Searcher srearcher = new Searcher();
		String src = "d;stanc,e";
		ArrayList<Word> strings = new ArrayList<Word>();
		
		ArrayList<String> ret = new ArrayList<String>();
		try {
			strings = srearcher.searchWords(src);
			for (Word w : strings) {
				System.out.println(w.from_word + ":" + w.to_word);
				ret.add(w.to_word);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		if(ret.size() == 0) return null;
		else
		return ret.get(0);
	}
}
