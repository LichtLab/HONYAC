package com.dic.database.util;

import com.dic.database.dao.DictionaryReader;
public class TranslatorLocal {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		DictionaryReader dic = new DictionaryReader();
		String to = dic.search("air");
		System.out.println(to);
	}

	public String translate(String fromLanguage, String toLanguage, String text) {
		DictionaryReader dic = new DictionaryReader();
		String to = dic.search("air");
		
		return to;
	}
}
