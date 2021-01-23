import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'dart:async';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:path/path.dart' show join;
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart';
import 'package:http_parser/http_parser.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';

final String takePicture = """
  mutation takePicture(\$token: String!, \$imageName: String!, \$image: Upload!) {
      takePicture(token: \$token, imageName: \$imageName, image: \$image) {
          ok {
            ... on IsOk {
                ok
              }
          },
          flowerName {
            ... on GetFlowerName {
                flowerName
              }
          }
      }
  }
""";

AlertDialog dialog(context, mssg)
{
  return AlertDialog(
    title: Text('Error occured'),
    content: SingleChildScrollView(
        child: ListBody(
            children: <Widget>[
                Text(mssg),
            ],
        ),
    ),
    actions: <Widget>[
        TextButton(
            child: Text("Close"),
            onPressed: () {
                Navigator.of(context).pop();
            },
        ),
     ],
  );
}

class CreateTakePicture extends StatefulWidget
{
    final String token;
    final CameraDescription camera;

    CreateTakePicture({Key key,
                               @required this.token,
                               @required this.camera,
                          }) : super(key: key);

    @override
    CreateTakePictureState createState() => CreateTakePictureState();
}

class CreateTakePictureState extends State<CreateTakePicture>
{
    final _id = GlobalKey<FormState>();
    bool state = false;
    String path = "";
    CameraController _controller;
    Future<void> _initializeControllerFuture;

    @override
    void initState() {
        super.initState();
        _controller = CameraController(
                            widget.camera,
                            ResolutionPreset.medium,
        );
        _initializeControllerFuture = _controller.initialize();
    }

    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
        _controller.dispose();
        super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
            title: Text('Camera'),
            centerTitle: true,
            //   actions: <Widget>[
            //     IconButton(
            //       icon: Icon(
            //         Icons.photo_camera,
            //         // color: Colors.white,
            //       ),
            //       onPressed: () {
            //         Navigator.push(
            //           context,
            //           MaterialPageRoute(builder: (context) => CreateTakePicture()),
            //         );
            //       },
            //     ),
            //   ],
            ),
          body: Mutation(
            options: MutationOptions(
                documentNode: gql(takePicture),
                update: (Cache cache, QueryResult result) {
                    return cache;
                },
                onError: (result) {
                    print("error");
                    print(result);
                },
                onCompleted: (dynamic resultData) {
                    print("on completed");
                    print(resultData.data);
                    String res = "It is not a flower";
                    if (resultData != null && resultData.data["takePicture"] != null && resultData.data["takePicture"]["flowerName"] != null) {
                        print(resultData.data["takePicture"]["flowerName"]["flowerName"]);
                        res = resultData.data["takePicture"]["flowerName"]["flowerName"];
                        print(res);
                        print("takePICTURE");
                    } else {
                      print("coudn't find picture");
                      dialog(context, "image not received");
                      showDialog<AlertDialog>(
                        context: context,
                        builder: (BuildContext context) {
                          return dialog(context, "image not received");
                      });
                    }


                    // to change, add return to picture
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => DisplayPictureScreen(imagePath: path, imageName: res),
                        ),
                    );
                    // Navigator.pop(context);
                  }
            ),
            builder: (RunMutation runMutation, QueryResult result) {
                return Scaffold(
                    body: FutureBuilder<void>(
                        future: _initializeControllerFuture,
                        builder: (context, snapshot) {
                            if (snapshot.connectionState == ConnectionState.done) {
                                return CameraPreview(_controller);
                            } else {
                                return Center(child: CircularProgressIndicator());
                            }
                        },
                    ),
                    floatingActionButton: FloatingActionButton(
                        child: Icon(Icons.camera_alt, color: Colors.black),
			backgroundColor: Colors.white,
                          // Provide an onPressed callback.
                        onPressed: () async {
                            try {
                                await _initializeControllerFuture;

                                final name = '${DateTime.now()}.jpg';
                                path = join(
                                        (await getTemporaryDirectory()).path,
                                        name
                                );
                                // path = join("./assets/tmp/", name);

                                print("PATH : ");
                                print(path);
                                // await _controller.takePicture();
                                await _controller.takePicture(path);

                                print("GET TOKENNNNNNN");
                                print(widget.token);
                                print("GET ENDED");
                                File pic = new File(path);
                                var byteData = pic.readAsBytesSync();


				print("SAVED :");
				print(File(path).existsSync());


				// Directory directory = await getTemporaryDirectory();
				// if (!await directory.exists()) {
        			//     await directory.create(recursive: true);
				// }
				///////saving file
				final result = await ImageGallerySaver.saveFile(path, isReturnPathOfIOS: true); // check why it's failing
				print("RESULT HERE :");
				print(result);
				/////////

                                var multipartFile = MultipartFile.fromBytes(
                                    'photo',
                                    byteData,
                                    filename: name,
                                    contentType: MediaType("image", "jpg"),
                                );

                                runMutation({"token": widget.token, "image": multipartFile, "imageName": name});
				print("path EXIST?????? :");
				print(File(path).existsSync());
                            } catch (e) {
                                print(e);
                            }
                        },
                    ),
		    floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,

                );
              }
          ),
            backgroundColor: Theme.of(context).primaryColor,
            // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
      );
    }
}


class DisplayPictureScreen extends StatelessWidget {
    final String imagePath;
    final String imageName;

    const DisplayPictureScreen({Key key, this.imagePath, this.imageName}) : super(key: key);

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: Text(imageName)),
            // The image is stored as a file on the device. Use the `Image.file`
            // constructor with the given path to display the image.
            body: Image.file(File(imagePath)),
        );
    }
}
