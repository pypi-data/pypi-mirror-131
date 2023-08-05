Intelligent Pigeon is a program made form IOT, by which you can detect Object from a Image and send to a server.

## Command for extracting images from a video:

```
python pigeon.py extract video_path output_path
```
After running the code output_path will created with 4 subfolder on your current folder, and image extracted on those folders.

## Command for detect object and send it to server is: 

```
python pigeon.py send <server_name> <path> weights classes.txt labeled
```

`server_name` is where you want to send object detected image.

`path` is the path from where you want detect and send images.

`weights` is darknet trained file for yolov4 object detection which you have to download.

`classes.txt` is a text file where list of all object present.

`labeled` is optional. If you want to send The image to the server with label then write it.