package com.dic.database.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

import org.sqlite.*;
public class DictionaryConnector {

	public DictionaryConnector() {
		
	}
	public Connection getConnection() {

			Connection conn = null;
			try {
				conn = DriverManager.getConnection("jdbc:sqlite:/Users/rainbow/Downloads/honyac.dic");
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
				return conn;
	}
}
