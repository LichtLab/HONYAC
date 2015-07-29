package edu.sfsu.cs.orange.ocr.language;

import java.io.IOException;
import java.sql.SQLException;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.regex.Pattern;
import android.annotation.SuppressLint;
import android.database.sqlite.SQLiteDatabase;
import android.os.AsyncTask;
import com.dictionary.search.DataBaseHelper;
import com.dictionary.search.Searcher;
import com.dictionary.search.Word;

public class TranslatorLocal {
//	private static final Pattern DIACRITICS_AND_FRIENDS = Pattern.compile("[\\p{InCombiningDiacriticalMarks}\\p{IsLm}\\p{IsSk}]+");

	//fromLanguage, toLanguageはtesseractの言語表記に合わせる
	// 例 jpn, eng, fra, spa(スペイン), deu(ドイツ), pol(ポルトガル), ita(イタリア), ell(ギリシャ)
	static public String translate(String fromLanguage, String toLanguage, String text, AsyncTask<String, String, Boolean> asyncTask) {
		// 入力のヨーロッパアルファベットを普通のアルファベットに変換する
		String src = stripDiacritics(text);
		String lowStr = text.toLowerCase();
		// String src = "d;stanc,e";
		Searcher searcher = new Searcher();
		ArrayList<Word> strings = new ArrayList<Word>();
		ArrayList<String> ret = new ArrayList<String>();
		String modi_fromLanguage = modifyCountryName(fromLanguage);
		String modi_toLanguage = modifyCountryName(toLanguage);

		if(asyncTask.isCancelled()) return Translator.BAD_TRANSLATION_MSG;
		try {
			strings = searcher.searchWords(lowStr, modi_fromLanguage, modi_toLanguage, asyncTask);
			for (Word w : strings) {
				System.out.println(w.from_word + ":" + w.to_word);
				String addingword = "(" + w.from_word + ") " + w.to_word;
//				ret.add(w.to_word);
				ret.add(addingword);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
		String ret_string = "";
		if(ret.size() == 0) return Translator.BAD_TRANSLATION_MSG;
		else {
			ret_string += ret.get(0);
//			int size = ret.size();
//			for(int i = 0; i < size; i++) {
//				ret_string += ret.get(i);
//				if(i != size -1) {
//					ret_string += ", ";
//				}
//			}
		}
		return ret_string;
	}

	@SuppressLint("NewApi")
	private static String stripDiacritics(String str) {
	   	str = Normalizer.normalize(str, Normalizer.Form.NFD);

	   	String regex = Pattern.quote("[\\p{InCombiningDiacriticalMarks}\\p{IsLm}\\p{IsSk}]+");

	   	String s2 = str.replaceAll(regex, "");
//	   	Pattern DIACRITICS_AND_FRIENDS = Pattern.compile("[p{InCombiningDiacriticalMarks}p{IsLm}p{IsSk}]+");
//	   	str = DIACRITICS_AND_FRIENDS.matcher(str).replaceAll("");
   		return str;
	}

	//スペイン・ポルトガル語は同じ辞書なので共にwordBank_spa_jpn.dbファイルに接続させる
	private static String modifyCountryName(String country){
		String ctname = country;
		if(country.equals("pol")){
			ctname = "spa";
		}
		return ctname;
	}
}
