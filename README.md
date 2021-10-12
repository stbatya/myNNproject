# myNNproject
little self-teaching project to develop my skills in machine learning and flask

The idea was to create a convolutional neural network for handwritten digits(mnist) recognition and to create a flask-based webapp implementing this cnn. The app is practically single(may be a couple more, to practice in creating links) web page with canvas html element. Drawing on canvas is sent through ajax to the flask-server and feeded to the pretrained network. Then the prediction is sent back to the user as a response.

After a while, I tried to do facial emotion recognition. This is represented by a page with videofeed. The video is loaded frame by frame on the server side, each frame is then inspected to determine a face by CV module, and then the rectangle with detected face is passed to pretrained neural network. The result of face detection (rectangle) and emotion prediction (name of emotion from list) are printed on frame before it is sent to webpage.
