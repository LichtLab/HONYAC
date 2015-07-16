package dic_search;

import java.util.ArrayList;

public class Ngramworker {
	//6文字以上の単語は3文字ずつの畳み込み分割、5字以下は2文字ずつ畳み込み
	public ArrayList<String> getNgramlist(String src) {
		ArrayList<String> ngramlist = new ArrayList<String>();
		if (src.length() > 5) {
			ngramlist = twogram(src);
		} else {
			ngramlist = threegram(src);
		}
		return ngramlist;
	}
	
	//2文字ずつで畳み込み分割
	private ArrayList<String> twogram(String src) {
		ArrayList<String> twogramlist = new ArrayList<String>();
		for (int i = 0; i < src.length() - 2; i++) {
			String string = src.substring(i, i + 2);
			twogramlist.add(string);
		}
		return twogramlist;
	}

	//3文字ずつで畳み込み分割
	private ArrayList<String> threegram(String src) {
		ArrayList<String> threegramlist = new ArrayList<String>();
		for (int i = 0; i < src.length() - 3; i++) {
			String string = src.substring(i, i + 3);
			threegramlist.add(string);
		}
		return threegramlist;
	}
}
