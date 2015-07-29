package com.dictionary.search;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import android.content.Context;
import android.content.res.AssetManager;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;

public class DataBaseHelper extends SQLiteOpenHelper {  

	private String mDBName = "";
	private static final int DATABASE_VERSION = 1;  

	private SQLiteDatabase mDatabase;  
	private final Context mContext;  
	private final File mDatabasePath;  

	public DataBaseHelper(Context context, String db_name) {  
		super(context, db_name+".db", null, DATABASE_VERSION);  
		mDBName = db_name;
		mContext = context;  
		mDatabasePath = mContext.getDatabasePath(mDBName+".db");  
	}  

	/** 
	 * asset に格納したデータベースをコピーするための空のデータベースを作成する 
	 */  
	public void createEmptyDataBase() throws IOException {  
		boolean dbExist = checkDataBaseExists();  

		if (dbExist) {  
			// すでにデータベースは作成されている  
		} else {  
			// このメソッドを呼ぶことで、空のデータベースがアプリのデフォルトシステムパスに作られる  
			// 空のデータベースをデフォルトシステムパスに作成
			SQLiteDatabase db_Read = this.getReadableDatabase();
			db_Read.close();

			try {  
				// asset に格納したデータベースをコピーする  
				//                copyDataBaseFromAsset();
				unzipCopyDataBaseFromAsset();  

				String dbPath = mDatabasePath.getAbsolutePath();  
				SQLiteDatabase checkDb = null;  
				try {  
					checkDb = SQLiteDatabase.openDatabase(dbPath, null, SQLiteDatabase.OPEN_READWRITE);  
				} catch (SQLiteException e) {  
				}  

				if (checkDb != null) {  
					checkDb.setVersion(DATABASE_VERSION);  
					checkDb.close();  
				}  

			} catch (IOException e) {  
				throw new Error("Error copying database");  
			}  
		}  
	}



	/** 
	 * 再コピーを防止するために、すでにデータベースがあるかどうか判定する 
	 * 
	 * @return 存在している場合 {@code true} 
	 */  
	private boolean checkDataBaseExists() {  
		String dbPath = mDatabasePath.getAbsolutePath();  

		SQLiteDatabase checkDb = null;  
		try {  
			checkDb = SQLiteDatabase.openDatabase(dbPath, null, SQLiteDatabase.OPEN_READONLY);  
		} catch (SQLiteException e) {  
			// データベースはまだ存在していない  
		}  

		if (checkDb == null) {  
			// データベースはまだ存在していない  
			return false;  
		}  

		int oldVersion = checkDb.getVersion();  
		int newVersion = DATABASE_VERSION;  

		if (oldVersion == newVersion) {  
			// データベースは存在していて最新  
			checkDb.close();  
			return true;  
		}  

		// データベースが存在していて最新ではないので削除  
		File f = new File(dbPath);  
		f.delete();  
		return false;  
	}  

	/** 
	 * asset に格納したデーだベースをデフォルトのデータベースパスに作成したからのデータベースにコピーする 
	 */  
	private void copyDataBaseFromAsset() throws IOException{  

		// asset 内のデータベースファイルにアクセス  
		InputStream mInput = mContext.getAssets().open(mDBName);  

		// デフォルトのデータベースパスに作成した空のDB  
		OutputStream mOutput = new FileOutputStream(mDatabasePath);  

		// コピー  
		byte[] buffer = new byte[1024];  
		int size;  
		while ((size = mInput.read(buffer)) > 0) {  
			mOutput.write(buffer, 0, size);  
		}  

		// Close the streams  
		mOutput.flush();  
		mOutput.close();  
		mInput.close();  
	}  

	public SQLiteDatabase openDataBase() throws SQLException {  
		return getReadableDatabase();  
	}  

	private void unzipCopyDataBaseFromAsset() throws IOException{
		try {
			//ZIPから解答して結合;
			AssetManager am = mContext.getResources().getAssets();
			InputStream is = am.open(mDBName+".zip",AssetManager.ACCESS_STREAMING);
			ZipInputStream zis        = new ZipInputStream(is);
			ZipEntry ze        = zis.getNextEntry();
			if (ze != null) { 
				OutputStream mOutput = new FileOutputStream(mDatabasePath); 
				byte[] buffer = new byte[1024];
				int size;
				while ((size = zis.read(buffer,0,buffer.length)) > -1) {
					mOutput.write(buffer, 0, size);
				}
				mOutput.flush();
				mOutput.close();
				zis.closeEntry();
			}
			zis.close();
		} catch (Exception e) {
		}
	}

	@Override  
	public void onCreate(SQLiteDatabase db) {  
	}  

	@Override  
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {  
	}  

	@Override  
	public synchronized void close() {  
		if(mDatabase != null)  
			mDatabase.close();  

		super.close();  
	}  
}  