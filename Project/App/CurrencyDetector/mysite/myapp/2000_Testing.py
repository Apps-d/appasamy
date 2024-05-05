{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Testing of Rs. 2000 currency notes"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This notebook carries out the complete evaluation of an input Rs. 2000 currency note"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Importing all necessary libraries\n",
    "\n",
    "import cv2                            # Importing Opencv library for image processing and computer vision\n",
    "import numpy as np                    # Importing numpy library \n",
    "import matplotlib.pyplot as plt       # Importing matplotlib library to plot the images directly in notebook\n",
    "from skimage.metrics import structural_similarity as ssim   # Importing ssim calculating modules from skimage library\n",
    "\n",
    "# Importing tkinter library to build GUI\n",
    "from tkinter import *\n",
    "from tkinter.ttk import Progressbar\n",
    "\n",
    "import time\n",
    "\n",
    "#Resizing the Plots\n",
    "plt.rcParams[\"figure.figsize\"] = (12, 12)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Declaring variable for progress bar to store the total progress\n",
    "myProgress =0.0"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# This Ipython magic will retrieve the path of the input image which is stored when the gui_1.ipynb is executed.\n",
    "\n",
    "%store -r path\n",
    "\n",
    "# A sample path:\n",
    "# path = r'Dataset\\2000_dataset\\2000_s1.jpg'\n",
    "\n",
    "print('Path of input image: ', path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reading the image\n",
    "test_img = cv2.imread(path)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Pre- processing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Pre- processing\n",
    "\n",
    "# Resizing the image\n",
    "test_img = cv2.resize(test_img, (1165,455))\n",
    "\n",
    "# Guassian Blur\n",
    "blur_test_img = cv2.GaussianBlur(test_img, (5,5), 0)\n",
    "\n",
    "# Grayscale conversion\n",
    "gray_test_image = cv2.cvtColor(blur_test_img, cv2.COLOR_BGR2GRAY)\n",
    "\n",
    "def preprocessing():\n",
    "    # Showing original currency note\n",
    "    plt.imshow(gray_test_image, 'gray')\n",
    "    plt.title('Input image after pre- processing')\n",
    "    plt.show()\n",
    "    \n",
    "    # Updating the progress\n",
    "    progress['value']=5\n",
    "    ProgressWin.update_idletasks()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#  Calculating SSIM of the two images sent as parameters\n",
    "\n",
    "def calculateSSIM(template_img, query_img):\n",
    "    \n",
    "    min_w = min(template_img.shape[1], query_img.shape[1])\n",
    "    min_h = min(template_img.shape[0], query_img.shape[0])\n",
    "    \n",
    "    # Resizing the two images so that both have same dimensions\n",
    "    img1 = cv2.resize(template_img, (min_w, min_h))\n",
    "    img2 = cv2.resize(query_img, (min_w, min_h))\n",
    "    \n",
    "    # Conversion to gray- scale\n",
    "    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)\n",
    "    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)\n",
    "    \n",
    "    # Plotting the images\n",
    "    plt.subplot(1, 2, 1)\n",
    "    plt.imshow(img1, 'gray')\n",
    "    \n",
    "    plt.subplot(1, 2, 2)\n",
    "    plt.imshow(img2, 'gray')\n",
    "    \n",
    "    plt.show()\n",
    "    \n",
    "    # Find the SSIM score and return\n",
    "    score = ssim(img1, img2)\n",
    "    return score"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Feature detection using ORB\n",
    "\n",
    "def computeORB(template_img, query_img):\n",
    "    # ===================== Creating orb object ==============================\n",
    "\n",
    "    nfeatures=700;\n",
    "    scaleFactor=1.2;\n",
    "    nlevels=8;\n",
    "    edgeThreshold=15; # Changed default (31);\n",
    "\n",
    "    # Initialize the ORB detector algorithm \n",
    "    orb = cv2.ORB_create(\n",
    "        nfeatures,\n",
    "        scaleFactor,\n",
    "        nlevels,\n",
    "        edgeThreshold)\n",
    "    # =========================================================================\n",
    "    \n",
    "    # Find the keypoints and descriptors with ORB\n",
    "    # This will find the keypoints of each of the image and then find the descriptors corresponding to each keypoint.\n",
    "    \n",
    "    kpts1, descs1 = orb.detectAndCompute(template_img,None)\n",
    "    kpts2, descs2 = orb.detectAndCompute(query_img,None)\n",
    "    \n",
    "    # ====================================== Brute Force Matching ==============================\n",
    "    # Starting a brute force matcher object\n",
    "    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)\n",
    "\n",
    "    # Finding matches between the 2 descrptor sets\n",
    "    matches = bf.match(descs1, descs2)\n",
    "\n",
    "    # sort the matches in the order of their distance\n",
    "    # Lower the distance, better the matching\n",
    "    dmatches = sorted(matches, key = lambda x:x.distance)\n",
    "\n",
    "    # ===========================================================================================\n",
    "    \n",
    "    # ======================================= Image homography ================================\n",
    "    ## extract the matched keypoints\n",
    "    src_pts  = np.float32([kpts1[m.queryIdx].pt for m in dmatches]).reshape(-1,1,2)\n",
    "    dst_pts  = np.float32([kpts2[m.trainIdx].pt for m in dmatches]).reshape(-1,1,2)\n",
    "        \n",
    "    ## find homography matrix and do perspective transform\n",
    "    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)\n",
    "    h,w = template_img.shape[:2]\n",
    "    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)\n",
    "    \n",
    "    if M is not None:\n",
    "        dst = cv2.perspectiveTransform(pts,M)\n",
    "    else:\n",
    "        dst = None\n",
    "\n",
    "    # This finds the template region in the test currency note\n",
    "    # ====================================================================================\n",
    "    \n",
    "    # Returning necessary data\n",
    "    return dst, dst_pts, kpts1, kpts2, dmatches"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Features 1- 7: Using ORB and SSIM"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Values for specifying search area of features 1 to 7\n",
    "search_area_list = [[200,270,160,330],\n",
    "                    [1050,1500,250,400],\n",
    "                    [50,400,0,100],\n",
    "                    [750,1050,0,100],\n",
    "                    [850,1050,280,380],\n",
    "                    [700,820,290,370],\n",
    "                    [400,650,0,100]]\n",
    "\n",
    "# Values of max_area and min_area for each feature for features 1 to 7\n",
    "feature_area_limits_list = [[10000,14000],\n",
    "                            [9000,15000],\n",
    "                            [17000,21500],\n",
    "                            [19000,28000],\n",
    "                            [17500,23000],\n",
    "                            [6500,9000],\n",
    "                            [10000,16000]]\n",
    "\n",
    "score_set_list = []               # Stores the ssim score set of each feature\n",
    "best_extracted_img_list = []      # Stores the extracted image with highest SSIM score for each feature\n",
    "avg_ssim_list = []                # Stores the avg ssim value for each feature\n",
    "NUM_OF_FEATURES = 7               # Number of features"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Algo- 1: Verification of features 1 to 7\n",
    "\n",
    "def testFeature_1_2_7():\n",
    "    i = 0\n",
    "    j = 0\n",
    "    NUMBER_OF_TEMPLATES = 6\n",
    "    global score_set_list                # Stores the ssim score set of each feature\n",
    "    global best_extracted_img_list       # Stores the extracted image with highest SSIM score for each feature\n",
    "    global avg_ssim_list                 # Stores the avg ssim value for each feature\n",
    "\n",
    "    \n",
    "    #Progress bar\n",
    "    global myProgress\n",
    "    myProgress =progress['value']\n",
    "    \n",
    "    # Iterating for each feature\n",
    "    for j in range(NUM_OF_FEATURES):\n",
    "        print('ANALYSIS OF FEATURE ' + str(j+1))\n",
    "\n",
    "        score_set = []           # SSIM scores for each teamplate of current feature will be stored here\n",
    "        max_score = -1           # Stores max SSIM score\n",
    "        max_score_img = None     # Stores extraced image with max SSIM score for the current feature\n",
    "        \n",
    "        # Performing feature detection, extraction and comparison for each template stored in dataset \n",
    "        for i in range(NUMBER_OF_TEMPLATES):\n",
    "            print('---> Template ' + str(i+1) + ' :')\n",
    "            \n",
    "            # Current template \n",
    "            template_path = r'Dataset\\2000_Features Dataset\\Feature ' + str(j+1) + '\\\\' + str(i+1) + '.jpg'\n",
    "            template_img = cv2.imread(template_path)\n",
    "\n",
    "            template_img_blur = cv2.GaussianBlur(template_img, (5,5), 0)\n",
    "            template_img_gray = cv2.cvtColor(template_img_blur, cv2.COLOR_BGR2GRAY)\n",
    "            test_img_mask = gray_test_image.copy()\n",
    "            \n",
    "            # Creating a mask to search the current template.\n",
    "            search_area = search_area_list[j]\n",
    "\n",
    "            test_img_mask[:, :search_area[0]] = 0\n",
    "            test_img_mask[:, search_area[1]:] = 0\n",
    "            test_img_mask[:search_area[2], :] = 0\n",
    "            test_img_mask[search_area[3]:, :] = 0\n",
    "            \n",
    "            # Feature detection using ORB \n",
    "            dst, dst_pts, kpts1, kpts2, dmatches = computeORB(template_img_gray, test_img_mask)\n",
    "            \n",
    "            # Error handling\n",
    "            if dst is None:\n",
    "                print('An Error occurred - Homography matrix is of NoneType')\n",
    "                continue\n",
    "            \n",
    "            query_img = test_img.copy()\n",
    "            \n",
    "            # drawing polygon around the region where the current template has been detected on the test currency note -- the blue polygon\n",
    "            res_img1 = cv2.polylines(query_img, [np.int32(dst)], True, (0,0,255), 1, cv2.LINE_AA)\n",
    "\n",
    "            # draw match lines between the matched descriptors\n",
    "            res_img2 = cv2.drawMatches(template_img, kpts1, res_img1, kpts2, dmatches[:20],None,flags=2)\n",
    "\n",
    "            # Find the details of a bounding rectangle that bounds the above polygon --- green rectangle\n",
    "            (x, y, w, h) = cv2.boundingRect(dst) # This gives us details about the rectangle that bounds this contour  \n",
    "            \n",
    "            # Checking if the area of the detected region is within the min and max area allowed for current feature \n",
    "            min_area = feature_area_limits_list[j][0]\n",
    "            max_area = feature_area_limits_list[j][1]\n",
    "\n",
    "            feature_area = w*h\n",
    "\n",
    "            if feature_area < min_area or feature_area > max_area:\n",
    "                (x, y, w, h) = cv2.boundingRect(dst_pts) \n",
    "\n",
    "                feature_area = w*h\n",
    "                if feature_area < min_area or feature_area > max_area: \n",
    "                    # If even area of 2nd rect is outside limits, then Discard current template\n",
    "                    print('Template Discarded- Area of extracted feature is outside permitted range!')\n",
    "                    continue\n",
    "\n",
    "            # Draw the rectangle\n",
    "            cv2.rectangle(res_img1, (x,y), (x+w, y+h), (0,255,0), 3)\n",
    "            \n",
    "            # Plotting images\n",
    "            plt.rcParams[\"figure.figsize\"] = (16, 16)\n",
    "            plt.subplot(1, 2, 1)\n",
    "            plt.imshow(res_img2)\n",
    "\n",
    "            plt.subplot(1, 2, 2)\n",
    "            plt.imshow(res_img1)\n",
    "            plt.show()\n",
    "            \n",
    "\n",
    "            # SSIM calculation\n",
    "            # Crop out the region inside the green rectangle (matched region)\n",
    "            crop_img = blur_test_img[y:y+h, x:x+w]\n",
    "\n",
    "            plt.rcParams[\"figure.figsize\"] = (5, 5)\n",
    "            score = calculateSSIM(template_img_blur, crop_img)\n",
    "\n",
    "            score_set.append(score)\n",
    "            print('SSIM score: ', score, '\\n')\n",
    "            \n",
    "            # Keeping details about extracted region with highest SSIM score\n",
    "            if score > max_score:\n",
    "                max_score = score\n",
    "                max_score_img = crop_img\n",
    "                \n",
    "            #Progress bar- Updating the progess\n",
    "            myProgress = myProgress + (75.0/(NUM_OF_FEATURES*NUMBER_OF_TEMPLATES))\n",
    "            progress['value'] = myProgress \n",
    "            ProgressWin.update_idletasks()\n",
    "            \n",
    "        # Storing necessary data\n",
    "        score_set_list.append(score_set)\n",
    "        print('SSIM score set of Feature ' + str(j+1) + ': ', score_set, '\\n')\n",
    "        \n",
    "        if len(score_set) != 0:\n",
    "            avg_ssim_list.append(sum(score_set)/len(score_set))\n",
    "            print('Average SSIM of Feature ' + str(j+1) + ': ',sum(score_set)/len(score_set),'\\n')\n",
    "        else:\n",
    "            print('No SSIM scores were found for this feature!')\n",
    "            avg_ssim_list.append(0.0)\n",
    "            print('Average SSIM of Feature ' + str(j+1) + ': 0','\\n')\n",
    "        \n",
    "        best_extracted_img_list.append([max_score_img, max_score])\n",
    "\n",
    "    # Printing all details for features 1- 7\n",
    "    print('Final Score- set list:','\\n')\n",
    "\n",
    "    for x in range(len(score_set_list)):\n",
    "        print('Feature',x+1,':',score_set_list[x])\n",
    "    print('\\n')\n",
    "\n",
    "    print('Final Average SSIM list for each feature:','\\n')\n",
    "\n",
    "    for x in range(len(avg_ssim_list)):\n",
    "        print('Feature',x+1,':',avg_ssim_list[x])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "left_BL_result = []\n",
    "right_BL_result = []\n",
    "result_list = []\n",
    "number_panel_result = []"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Feature 8: Left Bleed Lines"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to count number of bleed lines in left side- Feature 8\n",
    "# Algo 2\n",
    "\n",
    "def testFeature_8():\n",
    "    plt.rcParams[\"figure.figsize\"] = (5, 5)\n",
    "\n",
    "    # Check Feature 8- Left bleed lines\n",
    "    print('\\nANALYSIS OF FEATURE 8 : LEFT BLEED LINES\\n')\n",
    "    \n",
    "    # Cropping the region in which left bleed lines are present- Feature extraction\n",
    "    crop = test_img[80:230, 10:30]\n",
    "\n",
    "    img = crop.copy()\n",
    "    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n",
    "    \n",
    "    # Thresholding the image\n",
    "    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)\n",
    "\n",
    "    plt.imshow(thresh, 'gray')\n",
    "    plt.show()\n",
    "    \n",
    "    whitePixelValue = 255      # White pixel   \n",
    "    blackPixelValue = 0        # Black pixel\n",
    "\n",
    "    width = thresh.shape[1]    # width of thresholded image\n",
    "\n",
    "    # Result will be stored here\n",
    "    result = []                # will contain the number of black regions in each column (if the colums is non- erroneos)\n",
    "    num_of_cols = 0            # will contain the number of non- erroneos columns\n",
    "\n",
    "    # Non erroneous columns are those columns which contains less noise.\n",
    "\n",
    "    print('Number of black regions found in each column: ')\n",
    "    \n",
    "    # iteration over each column in the cropped image\n",
    "    for j in range(width):\n",
    "        col =thresh[:, j:j+1]     # Extracting each column of thresholded image\n",
    "        count = 0                 # Counter to count number of black regions in each extracted column\n",
    "        \n",
    "        # Iterating over each row (or pixel) in the current columm\n",
    "        for i in range(len(col)-1):\n",
    "\n",
    "            # Taking two consecutive pixels and storing their intensity value\n",
    "            pixel1_value = col[i][0]\n",
    "            pixel2_value = col[i+1][0]\n",
    "\n",
    "            #----------------------------------------------\n",
    "            # This part modifies any error pixels, if present.\n",
    "            # Actually in a binary threshold, all pixels should be either white or black.\n",
    "            # If due to some error pixels other than white or black are present, then the pixel is taken as white pixel\n",
    "\n",
    "            if pixel1_value != 0 and pixel1_value != 255:\n",
    "                pixel1_value = 255\n",
    "            if pixel2_value != 0 and pixel2_value != 255:\n",
    "                pixel2_value = 255\n",
    "\n",
    "            #-------------------------------------------------\n",
    "\n",
    "\n",
    "            # If current pixel is white and next pixel is black, then increment the counter.\n",
    "            # This shows that a new black region has been discovered.\n",
    "            if pixel1_value == whitePixelValue and pixel2_value == blackPixelValue:\n",
    "                count += 1\n",
    "\n",
    "        # If the counter is less than 10, it is a valid column. (less noise is present)\n",
    "        if count > 0 and count < 10:\n",
    "            print(count)\n",
    "            result.append(count)\n",
    "            num_of_cols += 1\n",
    "        else:\n",
    "            # discard the count if it is too great e.g. count> 10 (Erroneous Column)\n",
    "            # This removes/ drops those columns which contain too much noise\n",
    "            print(count, 'Erroneous -> discarded') \n",
    "    \n",
    "    # Printing necessary details\n",
    "    print('\\nNumber of columns examined: ', width)\n",
    "    print('Number of non- erroneous columns found: ', num_of_cols)\n",
    "    \n",
    "    if num_of_cols != 0:\n",
    "        average_count = sum(result)/num_of_cols\n",
    "    else:\n",
    "        average_count = -1\n",
    "        print('Error occured- Division by 0')\n",
    "\n",
    "    print('\\nAverage number of black regions is: ', average_count)\n",
    "    \n",
    "    # Storing the thresholded image and average number of bleed lines detected \n",
    "    global left_BL_result\n",
    "    left_BL_result = [thresh, average_count]\n",
    "    \n",
    "    # Updating progess in progress bar\n",
    "    global myProgress\n",
    "    progress['value']=80\n",
    "    ProgressWin.update_idletasks()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Feature 9: Right Bleed Lines"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Function to count number of bleed lines in right side- Feature 9\n",
    "\n",
    "def testFeature_9():\n",
    "    plt.rcParams[\"figure.figsize\"] = (5, 5)\n",
    "\n",
    "    # Check Feature 9- Right bleed lines\n",
    "    print('\\nANALYSIS OF FEATURE 9 : RIGHT BLEED LINES\\n')\n",
    "    \n",
    "    # Cropping the region in which left bleed lines are present- Feature extraction\n",
    "    crop = test_img[90:230, 1140:1160]\n",
    "\n",
    "    img = crop.copy()\n",
    "    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n",
    "    \n",
    "    # Thresholding the image\n",
    "    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)\n",
    "\n",
    "    plt.imshow(thresh, 'gray')\n",
    "    plt.show()\n",
    "\n",
    "    whitePixelValue = 255      # White pixel   \n",
    "    blackPixelValue = 0        # Black pixel\n",
    "\n",
    "    width = thresh.shape[1]    # width of thresholded image\n",
    "\n",
    "    # Result will be stored here\n",
    "    result = []                # will contain the number of black regions in each column (if the colums is non- erroneos)\n",
    "    num_of_cols = 0            # will contain the number of non- erroneos columns\n",
    "\n",
    "    # Non erroneous columns are those columns which contains less noise.\n",
    "\n",
    "    print('Number of black regions found in each column: ')\n",
    "    \n",
    "    # Iteration over each column in the cropped image\n",
    "    for j in range(width):\n",
    "        col =thresh[:, j:j+1]     # Extracting each column of thresholded image\n",
    "        count = 0                 # Counter to count number of black regions in each extracted column\n",
    "        \n",
    "        # Iterating over each row (or pixel) in the current columm\n",
    "        for i in range(len(col)-1):\n",
    "\n",
    "            # Taking two consecurive pixels and storing their intensity value\n",
    "            pixel1_value = col[i][0]\n",
    "            pixel2_value = col[i+1][0]\n",
    "\n",
    "            #----------------------------------------------\n",
    "            # This part modifies any error pixels, if present.\n",
    "            # Actually in a binary threshold, all pixels should be either white or black.\n",
    "            # If due to some error pixels other than white or black are present, then the pixel is taken as white pixel\n",
    "\n",
    "            if pixel1_value != 0 and pixel1_value != 255:\n",
    "                pixel1_value = 255\n",
    "            if pixel2_value != 0 and pixel2_value != 255:\n",
    "                pixel2_value = 255\n",
    "\n",
    "            #-------------------------------------------------\n",
    "\n",
    "            # If current pixel is white and next pixel is black, then increment the counter.\n",
    "            # This shows that a new black region has been discovered.\n",
    "            if pixel1_value == whitePixelValue and pixel2_value == blackPixelValue:\n",
    "                count += 1\n",
    "\n",
    "        # If the counter is less than 10, it is a valid column. (less noise is present)\n",
    "        if count > 0 and count < 10:\n",
    "            print(count)\n",
    "            result.append(count)\n",
    "            num_of_cols += 1\n",
    "        else:\n",
    "            # discard the count if it is too great e.g. count> 10 (Erroneous Column)\n",
    "            # This removes/ drops those columns which contain too much noise\n",
    "            print(count, 'Erroneous -> discarded')\n",
    "\n",
    "    # Printing necessary details\n",
    "    print('\\nNumber of columns examined: ', width)\n",
    "    print('Number of non- erroneous columns found: ', num_of_cols)\n",
    "\n",
    "    if num_of_cols != 0:\n",
    "        average_count = sum(result)/num_of_cols\n",
    "    else:\n",
    "        average_count = -1\n",
    "        print('Error occured- Division by 0')\n",
    "\n",
    "\n",
    "    print('\\nAverage number of black regions is: ', average_count)\n",
    "\n",
    "    # Storing the thresholded image and average number of bleed lines detected \n",
    "    global right_BL_result\n",
    "    right_BL_result = [thresh, average_count]\n",
    "    \n",
    "    # Updating progess in progress bar\n",
    "    global myProgress\n",
    "    progress['value']=85\n",
    "    ProgressWin.update_idletasks()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Feature 10: Currency Number Panel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.rcParams[\"figure.figsize\"] = (7, 7)\n",
    "\n",
    "# Cropping out the number panel. - FEATURE EXTRACTION\n",
    "\n",
    "crop = gray_test_image[360:440, 760:1080]    # This is the cropped gray image\n",
    "crop_bgr = test_img[360:440, 760:1080]       # This is the cropped BGR image\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Algo 3\n",
    "\n",
    "def testFeature_10():\n",
    "    plt.imshow(crop_bgr)\n",
    "    plt.show()\n",
    "\n",
    "    plt.rcParams[\"figure.figsize\"] = (7, 7)\n",
    "\n",
    "    print('\\n\\nANALYSIS OF FEATURE 10 : NUMBER PANEL \\n')\n",
    "\n",
    "    test_passed = False        # If true, then the test is successful\n",
    "    res_img_list = []          # List of images of successful cases\n",
    "    count = 0                  # Stores number of cases whihc are successful\n",
    "    num = 1\n",
    "    \n",
    "    # THRESHOLDING at multiple values\n",
    "    # Start from 90 as threshold value, increase the threshold value by 5 every time and check if 9 characters are detected in the thresholded image of number panel\n",
    "    # If 9 characters are detected in at least one of the cases, the currency number panel is verified.\n",
    "    # If more than 1 cases pass, the best image will be choosen from the successful cases.\n",
    "    for thresh_value in range(90, 155, 5):\n",
    "        # Thresholding at current value\n",
    "        _, thresh = cv2.threshold(crop, thresh_value, 255, cv2.THRESH_BINARY)\n",
    "\n",
    "        print('---> Threshold ' + str(num) + ' with Threshold value ' + str(thresh_value) + ' :')\n",
    "        num += 1\n",
    "\n",
    "        copy = crop_bgr.copy()\n",
    "\n",
    "        # Finding all the contours in the image of the number panel- CONTOUR DETECTION \n",
    "        img = cv2.bitwise_and(crop, crop, mask=thresh)\n",
    "        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)\n",
    "\n",
    "        h_img, w_img = img.shape[:2]\n",
    "\n",
    "        # cv2.drawContours(copy, contours, -1, (0, 0, 255), 1)\n",
    "\n",
    "        # Storing the details of all the BOUNDING RECTANGLES for each contour\n",
    "        bounding_rect_list = []    \n",
    "\n",
    "        for contour in contours:\n",
    "            [x, y, w, h] = cv2.boundingRect(contour)\n",
    "\n",
    "            if x != 0:\n",
    "                bounding_rect_list.append([x,y,w,h])\n",
    "\n",
    "        # Sorting the list of rectangles\n",
    "        # Rectangles will get sorted according to the x coordinate of the top left corner\n",
    "        bounding_rect_list.sort()\n",
    "\n",
    "        # ELIMINATION OF ERRONEOUS RECTANGLES\n",
    "        # Min area is taken as 150\n",
    "        min_area = 150\n",
    "        res_list = []\n",
    "\n",
    "        # Storing all rectangles having area greater than the min_area in a separate list\n",
    "        for i in range(0, len(bounding_rect_list)):\n",
    "            if i>= len(bounding_rect_list):\n",
    "                break\n",
    "            if bounding_rect_list[i][2]*bounding_rect_list[i][3] > min_area:\n",
    "                res_list.append(bounding_rect_list[i])\n",
    "\n",
    "        # Eliminating the rectangles that are present within a bigger rectangle\n",
    "        i = 0\n",
    "        while i<len(res_list):\n",
    "            [x,y,w,h] = res_list[i]\n",
    "            j = i+1\n",
    "            while j<len(res_list):\n",
    "                [x0,y0,w0,h0] = res_list[j]\n",
    "\n",
    "                if (x+w) >= x0+w0:\n",
    "                    res_list.pop(j)\n",
    "                else:\n",
    "                    break\n",
    "            i+= 1\n",
    "\n",
    "        # Eliminating unnecessary rectangles\n",
    "        i = 0\n",
    "        while i<len(res_list):\n",
    "            [x,y,w,h] = res_list[i]\n",
    "\n",
    "            if (h_img-(y+h)) > 40:     #  Eliminating the rectangles whose lower edge is further away from lower edge of the image \n",
    "                res_list.pop(i)\n",
    "            elif h<17:\n",
    "                res_list.pop(i)        # Eliminating the rectangles whose height is less than 17 pixels    \n",
    "            else:\n",
    "                i += 1\n",
    "        \n",
    "        for rect in res_list:          # Drawing the remaining rectangles\n",
    "            [x,y,w,h] = rect\n",
    "            cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 0, 255), 1)        \n",
    "\n",
    "        # COUNTING REMAINING RECTANGLES\n",
    "        # result of each image\n",
    "        if len(res_list) == 9:         # If number of rectangles detected is equal to 9, test passed\n",
    "            test_passed = True\n",
    "            res_img_list.append(copy)\n",
    "            count += 1\n",
    "            print('Test Successful: 9 letters found!')\n",
    "        else:\n",
    "            print('Unsuccessful!')\n",
    "\n",
    "        # If three consecutive cases pass the test, then break \n",
    "        if count == 3:\n",
    "            break\n",
    "\n",
    "    # Choosing the BEST IMAGE to be displayed   \n",
    "    # Even if a single case passes the test, then the currency number panel is verified.\n",
    "    # Selecting the best image to display\n",
    "    if count == 0:                    # If none of the cases passes the test\n",
    "        best_img = crop_bgr\n",
    "    elif count == 1:                  # If 1 case passes the test, then the image used in 1st case is selected as the best image\n",
    "        best_img = res_img_list[0]\n",
    "    elif count == 2:                  # If 2 cases pass the test, then the image used in 2nd case is selected as best image\n",
    "        best_img = res_img_list[1]\n",
    "    else:                             # If >= 3 cases pass the test, then the image used in 3rd case is selected as best image\n",
    "        best_img = res_img_list[2]\n",
    "       \n",
    "    \n",
    "    # Displaying final result\n",
    "\n",
    "    if(test_passed):\n",
    "        print('Test Passed!- 9 characters were detected in the serial number panel.')\n",
    "        plt.imshow(best_img)\n",
    "        plt.show()\n",
    "    else:\n",
    "        print('Test Failed!- 9 characters were NOT detected in the serial number panel.')\n",
    "    \n",
    "    # Storing the thresholded image and the result\n",
    "    global number_panel_result\n",
    "    number_panel_result = [best_img, test_passed]\n",
    "    \n",
    "    # Updating progress in progress bar\n",
    "    global myProgress\n",
    "    progress['value']=90\n",
    "    ProgressWin.update_idletasks()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Result analysis\n",
    "\n",
    "def testResult():\n",
    "    plt.rcParams[\"figure.figsize\"] = (3, 3)\n",
    "    \n",
    "    print('\\n\\nRESULT ANALYSIS\\n')\n",
    "    \n",
    "    # Stores the min allowed SSIM score for each feature\n",
    "    min_ssim_score_list = [0.45, 0.4, 0.45, 0.45, 0.5, 0.4, 0.5]\n",
    "\n",
    "    global result_list\n",
    "    result_list = []               # To store details of each feature\n",
    "    successful_features_count = 0  # To store number of features which passed the test\n",
    "\n",
    "    # Feature 1 to 7: Results\n",
    "    for i in range(NUM_OF_FEATURES):\n",
    "        avg_score = avg_ssim_list[i]\n",
    "        img, max_score = best_extracted_img_list[i]\n",
    "        status = False\n",
    "        min_allowed_score = min_ssim_score_list[i]\n",
    "        \n",
    "        # A feature passes the test if its avg SSIM score is greater than a min. decided value \n",
    "        # or if its max SSIM score is greater than 0.8\n",
    "        if avg_score >= min_allowed_score or max_score >= 0.79:\n",
    "            status = True\n",
    "            successful_features_count += 1\n",
    "            print('Feature ' + str(i+1) + ': Successful')\n",
    "        else:\n",
    "            status = False\n",
    "            print('Feature ' + str(i+1) + ': Unsuccessful')\n",
    "        \n",
    "        if img is None:\n",
    "            img = cv2.imread('Image_not_found.jpg')\n",
    "        result_list.append([img, avg_score, max_score, status])\n",
    "\n",
    "        \n",
    "    # Feature 8: Left Bleed lines\n",
    "\n",
    "    img, line_count = left_BL_result[:]\n",
    "    \n",
    "    # The feature passes the test if number of bleed lines is close to 7 (6.7 - 7.6)\n",
    "    if line_count >= 6.7 and line_count <= 7.6:\n",
    "        status = True\n",
    "        successful_features_count += 1\n",
    "        print('Feature 8: Successful- 7 bleed lines found in left part of currency note')\n",
    "    else:\n",
    "        status = False\n",
    "        print('Feature 8: Unsuccessful!')\n",
    "\n",
    "    if img is None:\n",
    "        img = cv2.imread('Image_not_found.jpg')\n",
    "    result_list.append([img, line_count, status])\n",
    "\n",
    "    \n",
    "    # Feature 9: Right Bleed lines\n",
    "\n",
    "    img, line_count = right_BL_result[:]\n",
    "    \n",
    "    # The feature passes the test if number of bleed lines is close to 7 (6.7 - 7.6)\n",
    "    if line_count >= 6.7 and line_count <= 7.6:\n",
    "        status = True\n",
    "        successful_features_count += 1\n",
    "        print('Feature 9: Successful- 7 bleed lines found in right part of currency note')\n",
    "    else:\n",
    "        status = False\n",
    "        print('Feature 9: Unsuccessful!')\n",
    "\n",
    "    if img is None:\n",
    "        img = cv2.imread('Image_not_found.jpg')\n",
    "    result_list.append([img, line_count, status])\n",
    "\n",
    "    \n",
    "    # Feature 10: Currency Number Panel\n",
    "    \n",
    "    img, status = number_panel_result[:]\n",
    "    \n",
    "    # The feature passes the test if 9 characters are detected in the number panel\n",
    "    if status:\n",
    "        successful_features_count += 1\n",
    "        print('Feature 10: Successful- 9 characters found in number panel of currency note')\n",
    "    else:\n",
    "        print('Feature 10: Unsuccessful!')\n",
    "    \n",
    "    if img is None:\n",
    "        img = cv2.imread('Image_not_found.jpg')\n",
    "    result_list.append([img, status])\n",
    "\n",
    "    \n",
    "    # printing FINAL RESULT\n",
    "\n",
    "    print('\\nResult Summary:')\n",
    "    print(str(successful_features_count) + ' out of 10 features are VERIFIED!')\n",
    "    \n",
    "    # Updating progress bar\n",
    "    global myProgress\n",
    "    progress['value']=97\n",
    "    ProgressWin.update_idletasks()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Driver cell"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Driver cell- contains GUI elements\n",
    "\n",
    "# Call all testing functions\n",
    "def Testing():  \n",
    "    button.config(state = DISABLED)\n",
    "    result_list.clear()\n",
    "    preprocessing()\n",
    "    testFeature_1_2_7()\n",
    "    testFeature_8()\n",
    "    testFeature_9()\n",
    "    testFeature_10()\n",
    "    testResult()\n",
    "    progress['value']=100\n",
    "    ProgressWin.update_idletasks()\n",
    "    time.sleep(0.8)\n",
    "    ProgressWin.destroy()\n",
    "\n",
    "def exitGUI():\n",
    "    ProgressWin.destroy()\n",
    "\n",
    "\n",
    "# creating tkinter window \n",
    "ProgressWin = Tk() \n",
    "ProgressWin.title(\"Processing Image\")\n",
    "ProgressWin.title('Fake Currency Detection - Processing')\n",
    "\n",
    "# Defining attributes of root window\n",
    "ProgressWin.resizable(False, False)  # This code helps to disable windows from resizing\n",
    "\n",
    "window_height = 200\n",
    "window_width = 500\n",
    "\n",
    "screen_width = ProgressWin.winfo_screenwidth()\n",
    "screen_height = ProgressWin.winfo_screenheight()\n",
    "\n",
    "x_cordinate = int((screen_width/2) - (window_width/2))\n",
    "y_cordinate = int((screen_height/2) - (window_height/2))\n",
    "\n",
    "ProgressWin.geometry(\"{}x{}+{}+{}\".format(window_width, window_height, x_cordinate, y_cordinate))\n",
    "\n",
    "# Creating a main frame inside the root window\n",
    "main_frame=Frame(ProgressWin,relief=GROOVE)\n",
    "main_frame.place(x=10,y=10) # Placing the frame at (10, 10)\n",
    "\n",
    "# Creating sub- frames\n",
    "frame1 = Frame(main_frame, padx=3, pady=3)\n",
    "frame2 = Frame(main_frame, bg='dark blue', pady=5, padx = 5)\n",
    "frame3 = Frame(main_frame, pady=5, padx = 5)\n",
    "\n",
    "frame1.grid(row = 1, column = 1, padx = 5, pady = 5)\n",
    "frame2.grid(row = 2, column = 1, padx = 5, pady = 5)\n",
    "frame3.grid(row = 3, column = 1, padx = 5, pady = 30)\n",
    "\n",
    "\n",
    "# Title label in sub_frame1\n",
    "label = Label(master=frame1, text=\"Processing! Please wait...\", fg = 'green', font = \"Verdana 13 bold\")\n",
    "label.pack() # Put the label into the window\n",
    "\n",
    "# Progress bar widget \n",
    "progress = Progressbar(frame2, orient = HORIZONTAL, length = 450, mode = 'determinate') \n",
    "progress.pack()\n",
    "\n",
    "# Button widget\n",
    "button = Button(frame3, text = 'Click to continue', command = Testing, font = \"Verdana 12 bold\", pady = 5)\n",
    "button.pack()\n",
    "\n",
    "# Run the GUI  \n",
    "ProgressWin.mainloop()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Store the list containing the final result of each feature\n",
    "\n",
    "%store result_list"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
