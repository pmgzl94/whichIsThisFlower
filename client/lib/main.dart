import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
// import 'package:image_picker/image_picker.dart';
import './createUser.dart';
import './client.dart';
import './login.dart';

import 'dart:async';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:path/path.dart' show join;
import 'package:path_provider/path_provider.dart';

// void main() {
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;

  runApp(MyApp(camera: firstCamera));
  print("hello");
}

//carefull alignment is between 1 and -1

class MyApp extends StatelessWidget {
  final CameraDescription camera;

  const MyApp({
    Key key,
    @required this.camera,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
      // client: clientFor(uri: "http://localhost:5000/graphql"),
      // client: clientFor(uri: "http://10.0.2.2:5000/graphql"),
      client: clientFor(uri: getUri()),
      child: MaterialApp(
            title: 'What is this Flower',
            theme: ThemeData(
              primarySwatch: Colors.green,
              // primarySwatch: Colors.white,
	      appBarTheme: AppBarTheme(
     	      		   color: Colors.white,
     	      		   // color: Color.fromRGBO(242, 242, 242, 0.6),
  	      ),
	      primaryTextTheme: TextTheme(
    	      			headline6: TextStyle(
      	      			color: Colors.black
    	          )
  	      ),
            ),
            home: Scaffold(
              appBar: AppBar(
	      	      title: Text('Login'),
	      	      centerTitle: true,
	      ),
              body: Column(
                children: [
                  Align (
                    alignment: Alignment(0.0, -0.75),
                    child: CreateLogin(camera: camera),
                  ),
                  Align (
                    alignment: Alignment(-1.0, 1),
                    child: ButtonCreateUser(),
                  )
                ]
              ),
              backgroundColor: Colors.white,
              // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
              // body: Center(child: RawWords()),
            ),
          )
    );
  }
}

//Stateless widgets are immutable, meaning that their properties can’t change, —all values are final.
