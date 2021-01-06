import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';


import 'dart:async';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:path/path.dart' show join;
import 'package:path_provider/path_provider.dart';


final String takePicture = """
  mutation logout(\$token: String!) {
      logout(token: \$token) {
          ok {
            ... on IsOk {
                ok
              }
          }
      }
  }
""";

AlertDialog dialog(context, mssg) {
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
    CameraController _controller;
    Future<void> _initializeControllerFuture;

    @override
    void initState() {
        super.initState();
        _controller = CameraController(
                            widget.camera,
                            ResolutionPreset.medium,
        );

    // Next, initialize the controller. This returns a Future.
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
              actions: <Widget>[
                IconButton(
                  icon: Icon(
                    Icons.photo_camera,
                    // color: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => CreateTakePicture()),
                    );
                  },
                ),
              ],
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
                      print("takePICTURE");
                      // Navigator.pop(context);
                      // if (resultData != null) {
                      //   print(resultData.data["auth"]["accessToken"]);
                      //   Navigator.push(
                      //     context,
                      //     MaterialPageRoute(builder: (context) => CreateMenu(token: resultData.data["auth"]["accessToken"])),
                      //   );
                      // } else {
                      //   print("User doesn't exist");
                      //   showDialog<AlertDialog>(
                      //     context: context,
                      //     builder: (BuildContext context) {
                      //       return dialog(context, "User doesn't exist");
                      //   });
                      // }
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
                          child: Icon(Icons.camera_alt),
                            // Provide an onPressed callback.
                          onPressed: () async {
                              try {
                                  await _initializeControllerFuture;

                                  final path = join(
                                          (await getTemporaryDirectory()).path,
                                          '${DateTime.now()}.png',
                                  );

                                  await _controller.takePicture();
                                  // await _controller.takePicture(path); // NOT WORKING ???

                                  Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => DisplayPictureScreen(imagePath: path),
                                      ),
                                  );
                              } catch (e) {
                                  print(e);
                              }
                          },
                      ),
                  );
              }
          ),
          backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
      );
    }
}
class DisplayPictureScreen extends StatelessWidget {
    final String imagePath;

    const DisplayPictureScreen({Key key, this.imagePath}) : super(key: key);

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: Text('Display the Picture')),
            // The image is stored as a file on the device. Use the `Image.file`
            // constructor with the given path to display the image.
            body: Image.file(File(imagePath)),
        );
    }
}


class ButtonCreateTakePicture extends StatelessWidget {

    @override
    Widget build(BuildContext context) {
       return ElevatedButton(
              onPressed: () {
                Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => CreateTakePicture()),
                );
              },
              child: Text('TakePicture'),
            );
  }
}
