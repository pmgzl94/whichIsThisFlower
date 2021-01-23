import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './menu.dart';

//  mutation login(\$username: String!, \$password: String!) {
final String login = """
  mutation Login(\$username: String!, \$password: String!) {
      auth(username: \$username, password: \$password) {
        accessToken
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
                Navigator.of(context).maybePop();
            },
        ),
     ],
  );
}

class CreateLogin extends StatefulWidget
{
    final CameraDescription camera;

    const CreateLogin({
        Key key,
        @required this.camera,
    }) : super(key: key);

    @override
    CreateLoginState createState() => CreateLoginState();
}

class CreateLoginState extends State<CreateLogin>
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
    void dispose()
    {
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
                Padding(
                    padding: EdgeInsets.only(
                        left: 25.0, right: 25.0, top: 50.0),
                    child: new Row(
                      mainAxisSize: MainAxisSize.max,
                      children: <Widget>[
                        new Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            new Text(
                              'Username',
                              style: TextStyle(
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ],
                    )
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 25.0, right: 25.0),
                    child: TextFormField(
                      decoration: const InputDecoration(
                          hintText: 'Enter your username',
                      ),
                      validator: (value) {
                          if (value.isEmpty) {
                            return 'Please enter your username';
                          }
                          return null;
                      },
                      controller: mc1,
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(
                        left: 25.0, right: 25.0, top: 25.0),
                    child: new Row(
                      mainAxisSize: MainAxisSize.max,
                      children: <Widget>[
                        new Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            new Text(
                              'Password',
                              style: TextStyle(
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ],
                    )
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 25.0, right: 25.0, bottom: 20.0),
                    child: TextFormField(
                      decoration: const InputDecoration(
                          hintText: 'Enter your password',
                      ),
                      validator: (value) {
                          if (value.isEmpty) {
                            return 'Please enter your password';
                          }
                          return null;
                      },
                      controller: mc2,
                      obscureText: true,
                    ),
                  ),
                Mutation(
                  options: MutationOptions(
                    documentNode: gql(login),
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
                      if (resultData != null && resultData.data["auth"] != null && resultData.data["auth"]["accessToken"] != null) {
                        print(resultData.data["auth"]["accessToken"]);
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => Menu(token: resultData.data["auth"]["accessToken"],
                                                     camera: widget.camera
                          )),
                        );
                        print("RESETING");
                        _id.currentState?.reset();
                      } else {
                        print("User doesn't exist");
                        showDialog<AlertDialog>(
                          context: context,
                          builder: (BuildContext context) {
                            return dialog(context, "User doesn't exist");
                        });
                      }
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 25),
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                               shape: RoundedRectangleBorder(
                                 borderRadius: BorderRadius.circular(20),
                                 // borderRadius: BorderRadius.circular(10),
                               ),
                               minimumSize: Size(350, 40),
                          //      primary: Color.fromRGBO(0, 102, 0, 0.6),
                          ),
                          onPressed: () {
                            runMutation({"username": mc1.text, "password": mc2.text});
                          },
                          child: Text('Login'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}

class ButtonCreateLogin extends StatelessWidget
{
  @override
  Widget build(BuildContext context) {
      return ElevatedButton(
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => CreateLogin()),
                );
              },
              child: Text('Login'),
            );
  }
}