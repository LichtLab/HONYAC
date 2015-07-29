/*
 * Copyright 2011 Robert Theis
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package edu.sfsu.cs.orange.ocr.language;

import java.io.IOException;

import com.dictionary.search.DataBaseHelper;

import android.app.Activity;
import android.content.Context;
import android.content.SharedPreferences;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.preference.PreferenceManager;

import edu.sfsu.cs.orange.ocr.CaptureActivity;
import edu.sfsu.cs.orange.ocr.PreferencesActivity;

/**
 * Delegates translation requests to the appropriate translation service.
 */
public class Translator {

	public static final String BAD_TRANSLATION_MSG = "[Translation unavailable]";

	private Translator(Activity activity) {  
		// Private constructor to enforce noninstantiability
	}

	static String translate(Activity activity, String sourceLanguageCode, String targetLanguageCode, String sourceText, AsyncTask<String, String, Boolean> asyncTask) {   

		// Check preferences to determine which translation API to use--Google, or Bing.
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(activity);
		String api = prefs.getString(PreferencesActivity.KEY_TRANSLATOR, CaptureActivity.DEFAULT_TRANSLATOR);

		String modi_fromLanguage = modifyCountryName(sourceLanguageCode);
		String modi_toLanguage = modifyCountryName(targetLanguageCode);
		String wordBankname = "wordBank_" + modi_fromLanguage + "_" + modi_toLanguage; 
		DataBaseHelper mDbHelper;  
		SQLiteDatabase db;  
		mDbHelper = new DataBaseHelper(activity, wordBankname);  
		try {  
			mDbHelper.createEmptyDataBase();  
			db = mDbHelper.openDataBase();  
		} catch (IOException ioe) {  
			throw new Error("Unable to create database");  
		} catch(SQLException sqle){  
			throw sqle;  
		}  

		if(asyncTask.isCancelled()) return BAD_TRANSLATION_MSG;
//		if(netWorkCheck(activity)) {
			return TranslatorLocal.translate(sourceLanguageCode, targetLanguageCode, sourceText, asyncTask);
//		} else {
//			// Delegate the translation based on the user's preference.
//			if (api.equals(PreferencesActivity.TRANSLATOR_BING)) {
//
//				// Get the correct code for the source language for this translation service.
//				sourceLanguageCode = TranslatorBing.toLanguage(
//						LanguageCodeHelper.getTranslationLanguageName(activity.getBaseContext(), sourceLanguageCode));
//
//				return TranslatorBing.translate(sourceLanguageCode, targetLanguageCode, sourceText);
//			} else if (api.equals(PreferencesActivity.TRANSLATOR_GOOGLE)) {
//
//				// Get the correct code for the source language for this translation service.
//				sourceLanguageCode = TranslatorGoogle.toLanguage(
//						LanguageCodeHelper.getTranslationLanguageName(activity.getBaseContext(), sourceLanguageCode));      
//
//				return TranslatorGoogle.translate(sourceLanguageCode, targetLanguageCode, sourceText);
//			}
//		}
//		return BAD_TRANSLATION_MSG;
	}

	//ネットワーク接続確認
	public static boolean netWorkCheck(Context context){
		ConnectivityManager cm =  (ConnectivityManager)context.getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo info = cm.getActiveNetworkInfo();
		if( info != null ){
			return info.isConnected();
		} else {
			return false;
		}
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