package com.dic.database.dao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;

public class DictionaryWriter {
	
	public DictionaryWriter() {
		
	}
	
	public void write() {
		File dic = new File("dic_data/ejdic-YinSV.txt");
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(dic));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		String str = "";
		Connection conn = null;
		try {
			conn = new DictionaryConnector().getConnection();
			Statement st = conn.createStatement();
			while((str = reader.readLine()) != null) {
				String[] split = str.split("%YINSV%");
		//		System.out.println(split[1]);
				st.executeUpdate("insert into dictionary values('"+ split[0] + "', '" +split[1] + "');");
//				System.out.println(split[0]);
//				System.out.println(split[1]);
				
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException sqlex) {
			sqlex.printStackTrace();
		} finally {
			try {
				conn.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	public static void main(String[] args) {
		Date start = new Date();
		System.out.println(start.toString());
		new DictionaryWriter().write();
		Date stop = new Date();
		System.out.println(stop.toString());
	}
}
