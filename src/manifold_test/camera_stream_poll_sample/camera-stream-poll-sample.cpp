/*! @file camera_stream_poll_sample.cpp
 *  @version 4.0.0
 *  @date Feb 1st 2018
 *
 *  @brief
 *  AdvancedSensing, Camera Stream API usage in a Linux environment.
 *  This sample shows how to poll new images from FPV camera or/and
 *  main camera from the main thread.
 *  (Optional) With OpenCV installed, user can visualize the images
 *
 *  @Copyright (c) 2017 DJI
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * */


#include "dji_vehicle.hpp"
#include <iostream>
#include "dji_linux_helpers.hpp"

#ifdef OPEN_CV_INSTALLED
  #include "opencv2/opencv.hpp"
  #include "opencv2/highgui/highgui.hpp"
using namespace cv;
#endif

using namespace DJI::OSDK;
using namespace std;

void show_rgb(CameraRGBImage img, char* name)
{
  cout << "#### Got image from:\t" << string(name) << endl;
#ifdef OPEN_CV_INSTALLED
  Mat mat(img.height, img.width, CV_8UC3, img.rawData.data(), img.width*3);
  cvtColor(mat, mat, COLOR_RGB2BGR);
  imshow(name,mat);
  cv::waitKey(1);
#endif
}

void emit_stream(CameraRGBBImage img)
{
  string str = "ffmpeg -re -i " + img + " -c:v copy -f rtsp -rtsp_transport tcp rtsp://localhost:8888";
  const char *command = str.c_str();
  system(command)
  return 0;
}

int main(int argc, char** argv)
{
  bool f = false;
  bool m = false;
  char c = 0;
  cout << "Please enter the type of camera stream you want to view\n"
       << "m: Main Camera\n"
       << "f: FPV  Camera\n" 
       << "b: both Cameras" << endl;
  cin >> c;

  switch(c)
  {
  case 'm':
    m=true; break;
  case 'f':
    f=true; break;
  case 'b':
    f=true; m=true; break;
  default:
    cout << "No camera selected";
    return 1;
  }

  // Setup OSDK.
  bool enableAdvancedSensing = true;
  LinuxSetup linuxEnvironment(argc, argv, enableAdvancedSensing);
  Vehicle*   vehicle = linuxEnvironment.getVehicle();
  const char *acm_dev = linuxEnvironment.getEnvironment()->getDeviceAcm().c_str();
  vehicle->advancedSensing->setAcmDevicePath(acm_dev);
  if (vehicle == NULL)
  {
    std::cout << "Vehicle not initialized, exiting.\n";
    return -1;
  }

  bool fpvCamResult = false;
  bool mainCamResult = false;

  if(f)
  {
    fpvCamResult = vehicle->advancedSensing->startFPVCameraStream();
    if(!fpvCamResult)
    {
      cout << "Failed to open FPV Camera" << endl;
    }
  }
  
  if(m)
  {
    mainCamResult = vehicle->advancedSensing->startMainCameraStream();
    if(!mainCamResult)
    {
      cout << "Failed to open Main Camera" << endl;
    }
  }  

  if((!fpvCamResult) && (!mainCamResult))
  {
    cout << "Failed to Open Either Cameras, exiting" << endl;
    return 1;
  }
  
  CameraRGBImage fpvImg;
  CameraRGBImage mainImg;
  char fpvName[] = "FPV_CAM";
  char mainName[] = "MAIN_CAM";
  for(int i=0; i<1000; i++)
  {
    if(f && fpvCamResult && vehicle->advancedSensing->newFPVCameraImageIsReady())
    {
      if(vehicle->advancedSensing->getFPVCameraImage(fpvImg))
      {
        show_rgb(fpvImg, fpvName);
      }
      else
      {
        cout << "Time out" << endl;
      }
    }

    if(m && mainCamResult && vehicle->advancedSensing->newMainCameraImageReady())
    {
      if(vehicle->advancedSensing->getMainCameraImage(mainImg))
      {
        show_rgb(mainImg, mainName);
      }
      else
      {
        cout << "Time out" << endl;
      }
    }
    usleep(2e4); 
  }

  if(f)
  {
    vehicle->advancedSensing->stopFPVCameraStream();
  }
  else if(m)
  {
    vehicle->advancedSensing->stopMainCameraStream();
  }

  return 0;
}
