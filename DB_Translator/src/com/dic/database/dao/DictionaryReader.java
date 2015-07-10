package com.dic.database.dao;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

public class DictionaryReader {
	private Connection conn = null;

	public DictionaryReader() {
		super();
	}
	
//	public static void main(String[] args) {
//		Connection conn = new DictionaryConnector().getConnection();
////		if(conn == null) {
////			System.out.println("Error");
////		} else {
////			System.out.println("OK");
////		}
//		try {
//			Statement st = conn.createStatement();
//			ResultSet rs = st.executeQuery("select * from dictionary;");
//			ResultSetMetaData rsmd = rs.getMetaData();
//			while(rs.next()) {
//				System.out.println(rs.getString(1));
//				System.out.println(rs.getString(2));
//			}
//		} catch (SQLException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		
//	}
//	
	public String search(String from) {
		String result = "";
		if(conn == null) {
			conn = new DictionaryConnector().getConnection();
		}
		try {
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery("select jpn from dictionary where eng='" + from + "';");
			if(rs.next()) {
				result = rs.getString(1);
			} else {
				
				result = "NOTFOUND";
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				conn.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return result;
	}
}
