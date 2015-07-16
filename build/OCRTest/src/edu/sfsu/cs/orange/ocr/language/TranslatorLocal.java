package edu.sfsu.cs.orange.ocr.language;

import java.sql.SQLException;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.regex.Pattern;

import com.dictionary.search.Searcher;
import com.dictionary.search.Word;

public class TranslatorLocal {
	//fromLanguage, toLanguageはtesseractの言語表記に合わせる
	// 例 jpn, eng, fra, spa(スペイン), deu(ドイツ), pol(ポルトガル), ita(イタリア), ell(ギリシャ)
	static public String translate(String fromLanguage, String toLanguage, String text) {
		// 入力のヨーロッパアルファベットを普通のアルファベットに変換する
		String src = stripDiacritics(text);
		// String src = "d;stanc,e";
		Searcher searcher = new Searcher();
		ArrayList<Word> strings = new ArrayList<Word>();
		ArrayList<String> ret = new ArrayList<String>();
		try {
			strings = searcher.searchWords(text, fromLanguage, toLanguage);
			for (Word w : strings) {
				System.out.println(w.from_word + ":" + w.to_word);
				ret.add(w.to_word);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		if(ret.size() == 0) return Translator.BAD_TRANSLATION_MSG;
		else
		return ret.get(0);
	}

	public static final Pattern DIACRITICS_AND_FRIENDS = Pattern.compile("[\\p{InCombiningDiacriticalMarks}\\p{IsLm}\\p{IsSk}]+");
	private static String stripDiacritics(String str) {
	   	str = Normalizer.normalize(str, Normalizer.Form.NFD);
	   	str = DIACRITICS_AND_FRIENDS.matcher(str).replaceAll("");
   		return str;
	}

	

}
