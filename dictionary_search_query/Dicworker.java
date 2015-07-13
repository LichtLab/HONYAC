package dic_search;

import java.util.ArrayList;
import dic_search.Ngramworker;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class Dicworker {
	static Connection conn;
	static Statement stmt;
	String dbname;

	/**
	 * 読み込むDBの名前で初期化
	 * 
	 * @param dbname
	 *            ("wordBank")
	 */
	public Dicworker(String dbname) {
		this.dbname = dbname;
	}

	public Dicworker() {
		this.dbname = "wordBank";
	}

	public ArrayList<Word> getWords(String src) throws SQLException {
		this.conn = DriverManager
				.getConnection("jdbc:sqlite:" + dbname + ".db");
		this.stmt = conn.createStatement();
		ArrayList<Word> searchedwords = new ArrayList<Word>();
		// 入力されたstringで検索
		searchedwords = sqlWorker(src);
		// 1つもヒットしなかったらngramに分割して部分一致の検索
		if (searchedwords.size() < 1) {
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
			ResultSet rs = stmt
					.executeQuery("select from_word, to_word from wordTable where from_word like '%"
							+ str + "%' limit 1000");
			while (rs.next()) {
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
