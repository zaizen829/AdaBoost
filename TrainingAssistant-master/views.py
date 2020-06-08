# -*- coding: utf-8 -*-

from flask import *
import os, sys
import json
import re
import sys

app = Flask(__name__)
app.secret_key = '佐久間さん可愛い'

#画像の準備
image_ptrn = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
image_dir = os.path.join( 'static', 'img' )
images = []
images = [ image for image in os.listdir( image_dir ) if re.match( image_ptrn, image ) ]
if not len( images ):
    sys.exit( 'Error: Could not find images')

logf = open('log.dat', 'w')

pos = 0

@app.route('/')
def index():
    
    global pos

    #正例と負例用のファイル
    global positive
    global negative
    
    positive = open('info.dat', 'a')
    negative = open('bg.txt', 'a')

    #最初の画像
    imgsrc = os.path.join( image_dir, images[pos] )
    imgnum = len(images)
    count = pos
    counter = ''.join( [ str(pos+1).zfill( len(str(imgnum)) ), ' of ', str(imgnum) ] )
    
    return render_template( 'index.html', imgsrc=imgsrc, imgnum=imgnum, count=count, counter=counter ) 

@app.route('/_next')
def _next():

    global pos

    #その画像をスキップするか
    skip = request.args.get('skip') 
    
    if skip == u'0':

        #囲まれた範囲の座標
        coords = request.args.get('coords')
        coords = json.loads(coords)

        #処理中の画像のパス
        image_path = os.path.join( image_dir, images[pos] )

        #正例か負例か
        if len(coords) == 0:
            negative.write( ''.join( [ image_path, '\n' ] ) )
            logf.write( ''.join( [ image_path, '\n' ] ) )
            logf.flush()

        else:
            s = ''
            for coord in coords:
                s = '  '.join( [ s, ' '.join( [ str(int(e)) for e in coord ] ) ] )
            
            positive.write('%s  %d%s\n' % (image_path, len(coords), s))
            logf.write( "%s %d%s\n" % (image_path, len(coords), s) )
            logf.flush()
    
    #まだ画像があるか
    if pos+1 >= len(images):
        imgsrc = ""
        finished = True
        pos = pos + 1
        logf.close()
        negative.close()
        positive.close()
    else:
        finished = False
        imgsrc = os.path.join( image_dir, images[pos+1] )
        pos = pos + 1

    return jsonify( imgsrc=imgsrc, finished=finished, count=pos ) 

if __name__ == '__main__':
    app.debug = True
    app.run()
