/*
 * Copyright 2009 ZXing authors
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
package edu.sfsu.cs.orange.ocr;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;

import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.graphics.BitmapFactory;
import android.graphics.ImageFormat;
import android.graphics.Matrix;
import android.graphics.Rect;
import android.graphics.YuvImage;
import android.util.Log;

/**
 * This object extends LuminanceSource around an array of YUV data returned from the camera driver,
 * with the option to crop to a rectangle within the full data. This can be used to exclude
 * superfluous pixels around the perimeter and speed up decoding.
 *
 * It works for any pixel format where the Y channel is planar and appears first, including
 * YCbCr_420_SP and YCbCr_422_SP.
 *
 * The code for this class was adapted from the ZXing project: http://code.google.com/p/zxing
 */
public final class PlanarYUVLuminanceSource extends LuminanceSource {

  private final byte[] yuvData;
  private final int dataWidth;
  private final int dataHeight;
  private final int left;
  private final int top;

  public PlanarYUVLuminanceSource(byte[] yuvData,
                                  int dataWidth,
                                  int dataHeight,
                                  int left,
                                  int top,
                                  int width,
                                  int height,
                                  boolean reverseHorizontal) {
    super(width, height);

//    if (left + width > dataWidth || top + height > dataHeight) {
//      throw new IllegalArgumentException("Crop rectangle does not fit within image data.");
//    }

    this.yuvData = yuvData;
    this.dataWidth = dataWidth;
    this.dataHeight = dataHeight;
    Log.d("rotate", "this.dataWidth:"+this.dataWidth+" this.dataHeight:"+this.dataHeight);
//    this.left = left;
//    this.top = top;
    this.left = (dataWidth- height)/2;
    this.top = (dataHeight - width)/2;
    Log.d("rotate", "bmp this.top:"+this.top+" dataWidth:"+this.dataWidth+" this.left:"+this.left);
    if (reverseHorizontal) {
      reverseHorizontal(width, height);
    }
  }

  @Override
  public byte[] getRow(int y, byte[] row) {
    if (y < 0 || y >= getHeight()) {
      throw new IllegalArgumentException("Requested row is outside the image: " + y);
    }
    int width = getWidth();
    if (row == null || row.length < width) {
      row = new byte[width];
    }
    int offset = (y + top) * dataWidth + left;
    System.arraycopy(yuvData, offset, row, 0, width);
    return row;
  }

  @Override
  public byte[] getMatrix() {
    int width = getWidth();
    int height = getHeight();

    // If the caller asks for the entire underlying image, save the copy and give them the
    // original data. The docs specifically warn that result.length must be ignored.
    if (width == dataWidth && height == dataHeight) {
      return yuvData;
    }

    int area = width * height;
    byte[] matrix = new byte[area];
    int inputOffset = top * dataWidth + left;

    // If the width matches the full width of the underlying data, perform a single copy.
    if (width == dataWidth) {
      System.arraycopy(yuvData, inputOffset, matrix, 0, area);
      return matrix;
    }

    // Otherwise copy one cropped row at a time.
    byte[] yuv = yuvData;
    for (int y = 0; y < height; y++) {
      int outputOffset = y * width;
      System.arraycopy(yuv, inputOffset, matrix, outputOffset, width);
      inputOffset += dataWidth;
    }
    return matrix;
  }

  @Override
  public boolean isCropSupported() {
    return true;
  }

  @Override
  public LuminanceSource crop(int left, int top, int width, int height) {
    return new PlanarYUVLuminanceSource(yuvData,
                                        dataWidth,
                                        dataHeight,
                                        this.left + left,
                                        this.top + top,
                                        width,
                                        height,
                                        false);
  }
  

  public Bitmap getBitmapImageFromYUV(byte[] data, int width, int height) {
      YuvImage yuvimage = new YuvImage(data, ImageFormat.NV21, width, height, null);
      ByteArrayOutputStream baos = new ByteArrayOutputStream();
      yuvimage.compressToJpeg(new Rect(0, 0, width, height), 80, baos);
      byte[] jdata = baos.toByteArray();
      BitmapFactory.Options bitmapFatoryOptions = new BitmapFactory.Options();
      bitmapFatoryOptions.inPreferredConfig = Bitmap.Config.ARGB_8888;
      Bitmap bmp = BitmapFactory.decodeByteArray(jdata, 0, jdata.length, bitmapFatoryOptions);
      return bmp;
  }

  public Bitmap renderCroppedGreyscaleBitmap() {
    int width = getWidth();
    int height = getHeight();
    Log.d("rotate", "width:"+width+" height:"+height);
    int[] pixels = new int[width * height];
    byte[] yuv = yuvData;
//    int inputOffset = top * dataWidth + left;
    Log.d("rotate", "bmp top:"+top+" dataWidth:"+dataWidth+" left:"+left);

//    for (int y = 0; y < height; y++) {
//      int outputOffset = y * width;
//      for (int x = 0; x < width; x++) {
//        int grey = yuv[inputOffset + x] & 0xff;
//        pixels[outputOffset + x] = 0xFF000000 | (grey * 0x00010101);
//      }
//      inputOffset += dataWidth;
//    }
    

    // プレビューデータから Bitmap を生成 
    Bitmap bmp = getBitmapImageFromYUV(yuv, dataWidth, dataHeight);
//    // あとはBitmapを好きに使う。
//    try {
//        // 保存処理開始
//        FileOutputStream fos = null;
//        fos = new FileOutputStream(new File( "/sdcard/preview.jpg"));
//
//        // jpegで保存
//        bmp.compress(CompressFormat.JPEG, 100, fos);
//
//        // 保存処理終了
//        fos.close();
//        } catch (Exception e) {
//        Log.e("Error", "" + e.toString());
//        }
    Bitmap crop_bitmap = Bitmap.createBitmap(bmp, left, top, height, width);
//    Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
//    bitmap.setPixels(pixels, 0, width, 0, 0, width, height);
//    bitmap.setPixels(pixels, 0, height, 0, 0, height, width);
//    try {
//    // 保存処理開始
//    FileOutputStream fos = null;
//    fos = new FileOutputStream(new File( "/sdcard/crop.jpg"));
//
//    // jpegで保存
//    crop_bitmap.compress(CompressFormat.JPEG, 100, fos);
//
//    // 保存処理終了
//    fos.close();
//    } catch (Exception e) {
//    Log.e("Error", "" + e.toString());
//    }
    Log.d("rotate", "bmp bitmap.getWidth():"+crop_bitmap.getWidth()+" bitmap.getHeight():"+crop_bitmap.getHeight());

    //回転
    Matrix m = new Matrix();
    m.setRotate(90);

    //保存用 bitmap生成
    Bitmap rotated_bmp = Bitmap.createBitmap(crop_bitmap,0,0,crop_bitmap.getWidth(),crop_bitmap.getHeight(),m,true);
    Log.d("rotate", "rotated_bmp rotated_bmp.getWidth():"+rotated_bmp.getWidth()+" rotated_bmp.getHeight():"+rotated_bmp.getHeight());
//    try {
//    // 保存処理開始
//    FileOutputStream fos = null;
//    fos = new FileOutputStream(new File( "/sdcard/rotate.jpg"));
//
//    // jpegで保存
//    rotated_bmp.compress(CompressFormat.JPEG, 100, fos);
//
//    // 保存処理終了
//    fos.close();
//    } catch (Exception e) {
//    Log.e("Error", "" + e.toString());
//    }
    return rotated_bmp;
  }

  private void reverseHorizontal(int width, int height) {
    byte[] yuvData = this.yuvData;
    for (int y = 0, rowStart = top * dataWidth + left; y < height; y++, rowStart += dataWidth) {
      int middle = rowStart + width / 2;
      for (int x1 = rowStart, x2 = rowStart + width - 1; x1 < middle; x1++, x2--) {
        byte temp = yuvData[x1];
        yuvData[x1] = yuvData[x2];
        yuvData[x2] = temp;
      }
    }
  }

}
