package com.dictionary.search;

import java.util.ArrayList;

import android.os.AsyncTask;

import com.dictionary.search.Ngramworker;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Dicworker {
	static Connection conn;
	static Statement stmt;
	String dbname;
	AsyncTask<String, String, Boolean> asyncTask;
	/**
	 * 読み込むDBの名前で初期化
	 * 
	 * @param dbname
	 *            ("wordBank")
	 */
	public Dicworker(String dbname, AsyncTask<String, String, Boolean> asyncTask) {
		this.dbname = dbname;
		this.asyncTask = asyncTask;
	}

	public Dicworker() {
		this.dbname = "wordBank";
	}

	public ArrayList<Word> getWords(String src) throws SQLException {
		try {
			Class.forName("org.sqldroid.SQLDroidDriver").newInstance();
		} catch (InstantiationException e) {
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
		this.conn = DriverManager
				.getConnection("jdbc:sqldroid:/data/data/edu.sfsu.cs.orange.ocr/databases/" + dbname + ".db");
		this.stmt = conn.createStatement();
		// 入力されたstringで検索
		ArrayList<Word> searchedwords = sqlWorker(src);
		if(asyncTask.isCancelled()) return searchedwords;
		// 1つもヒットしなかったらngramに分割して部分一致の検索
		if (searchedwords == null || searchedwords.size() < 1) {
			searchedwords = getRelativeWords(src);
		}
		return searchedwords;
	}

	private ArrayList<Word> getRelativeWords(String src) throws SQLException {
		ArrayList<Word> relativeWords = new ArrayList<Word>();
		ArrayList<String> ngramlist = new ArrayList<String>();
		Ngramworker ngwkr = new Ngramworker();
		ngramlist = ngwkr.getNgramlist(src);
		relativeWords = sqlWorker(ngramlist);
		return relativeWords;
	}

	// (引数が複数ある)引数のstringリストの中で部分一致する文字列群をlistとしてリターン
	private ArrayList<Word> sqlWorker(ArrayList<String> srclist)
			throws SQLException {
		ArrayList<Word> querieddwords = new ArrayList<Word>();

		for (String str : srclist) {

			if(asyncTask.isCancelled()) return querieddwords;
			ResultSet rs = stmt
					.executeQuery("select from_word, to_word from wordTable where from_word like '%"
							+ str + "%' limit 1000");

			while (rs.next()) {
				if(asyncTask.isCancelled()) return querieddwords;
				String from_word = rs.getString(1);
				String to_word = rs.getString(2);
				// from_wordで重複チェックしながら登録
				Word newword = new Word(from_word, to_word);
				if (!isDuplicated(querieddwords, newword)) {
					querieddwords.add(newword);
				}
			}
		}
		return querieddwords;
	}

	// （引数が一つしかない）引数のstringで完全一致する文字列群をlistとしてリターン
	private ArrayList<Word> sqlWorker(String src) throws SQLException {
		ArrayList<Word> querieddwords = new ArrayList<Word>();
		// テーブル名はＤＢが何であれすべてwordBankで固定
		ResultSet rs = this.stmt
				.executeQuery("select from_word, to_word from wordTable where from_word='"
						+ src + "'");
		
		while (rs.next()) {
			String from_word = rs.getString(1);
			String to_word = rs.getString(2);
			Word newword = new Word(from_word, to_word);
			querieddwords.add(newword);
		}
		return querieddwords;
	}

	private boolean isDuplicated(ArrayList<Word> wordlist, Word target) {
		for (Word w : wordlist) {
			if (w.from_word == target.from_word) {
				return true;
			}
		}
		return false;
	}
}
