# -*- coding: utf-8 -*

import cv2

try:
    img = cv2.imread('fin0101.jpg')

    if img is None:
        print ('ファイルを読み込めません。')
        import sys
        sys.exit()

    cascade = cv2.CascadeClassifier('cascade/cascade.xml')
    facerect = cascade.detectMultiScale(img)

    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)
    else:
        print('no finger')

    cv2.imwrite('./cascade.jpg', img)
    cv2.imshow('img', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
except:
    import sys
    print("Error:", sys.exc_info()[0])
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))
