import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './seePictures.dart';
import './takePicture.dart';
import './createUser.dart';

final String logout = """
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

class CreateMenu extends StatelessWidget {
    final String token;
    final CameraDescription camera;

    CreateMenu({Key key,
                  @required this.token,
                  @required this.camera,
             }) : super(key: key);

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
            title: Text('Menu'),
              actions: <Widget>[
                IconButton(
                  icon: Icon(
                    Icons.photo_camera,
                    // color: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => CreateTakePicture(token: token,
                                                     camera: camera
                          )),
                    );
                  },
                ),
                IconButton(
                  icon: Icon(
                    Icons.logout,
                    // color: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.pop(context);
                  },
                ),
                IconButton(
                  icon: Icon(
                    Icons.photo_camera,
                    // color: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => CreateTakePicture(token: token,
                                                     camera: camera
                          )),
                    );
                  },
                ),
              ],
            ),
        body: Column(
          children: [
            Align (
              alignment: Alignment(0.0, -0.75),
              child: CreateMenuButton(token: token),
            ),
          ]
        ),
        backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        // body: Center(child: RawWords()),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
  }
}

class CreateMenuButton extends StatefulWidget
{
    final String token;
    CreateMenuButton({Key key, @required this.token}) : super(key: key);

    @override
    CreateMenuButtonState createState() => CreateMenuButtonState();
}

class CreateMenuButtonState extends State<CreateMenuButton>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked()
    {
      this.state = true;
    }

    final mc1 = TextEditingController();
    final mc2 = TextEditingController();

    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
      mc1.dispose();
      mc2.dispose();
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Form(
            key: _id,
            child: Column(
              children: <Widget> [
               Mutation(
                  options: MutationOptions(
                    documentNode: gql(logout),
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
                      print("LOGOUT");
                      Navigator.pop(context);
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: ElevatedButton(
                          onPressed: () async {
                            print("GET TOKENNNNNNN");
                            print(widget.token);
                            print("GET ENDED");
                            runMutation({"token": widget.token});
                          },
                          child: Text('Logout'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}
