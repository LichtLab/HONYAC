package com.dictionary.search;

public class Word {
	public String from_word;
	public String to_word;
	double distance;
	int count;
	
	public Word(){
		this.from_word = "";
		this.to_word = "";
		this.distance = 0.0;
		this.count = 0;
	}
	public Word(String from_word){
		this.from_word = from_word;
		this.to_word = "";
		this.distance = 0.0;
		this.count = 0;
	}
	public Word(String fromword, String toword){
		this.from_word = fromword;
		this.to_word = toword;
		this.distance = 0.0;
		this.count = 0;
	}
	public Word(String fromword, String toword, double distance){
		this.from_word = fromword;
		this.to_word = toword;
		this.distance = distance;
		this.count = 0;
	}
}
